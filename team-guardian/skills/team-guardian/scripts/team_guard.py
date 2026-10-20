#!/usr/bin/env python3
"""team_guard.py - Disciplina de equipo para agentes (Team-Guardian).

Valida ramas y mensajes de commit (Conventional Commits), detecta cambios
sensibles en tests dentro de un diff y bloquea el gate hasta que un humano
apruebe la justificacion del agente.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
BRANCH_PATTERN = re.compile(rf"(?:main|(?:feat|fix|chore)/{SLUG})")
COMMIT_TYPES = frozenset({"feat", "fix", "docs", "ci", "refactor", "test", "chore"})
COMMIT_HEADER_PATTERN = re.compile(
    rf"(?P<type>[a-z]+)(?:\((?P<scope>{SLUG})\))?!?: (?P<description>.*)"
)
MAX_HEADER_LENGTH = 72

TEST_FILE_PATTERN = re.compile(
    r"(?:test_.*\.py|.*_test\.py|.*_test\.go|.*\.(?:test|spec)\.(?:js|jsx|ts|tsx))"
)
TEST_DIRECTORIES = frozenset({"tests", "test", "__tests__"})
ASSERTION_PATTERN = re.compile(
    r"^assert|expect\(|self\.assert|t\.Error|t\.Fatal|require\."
)
TEST_DEFINITION_PATTERN = re.compile(
    r"^(?:def\s+test_|async\s+def\s+test_|it\(|test\(|it\.each|func\s+Test|#\[test\])"
)
SKIP_PATTERN = re.compile(
    r"@pytest\.mark\.skip|\bpytest\.skip\(|(?<![\w.])x(?:it|test)\("
    r"|\b(?:it|test|describe)\.skip\b|\bt\.Skip\(|@unittest\.skip"
)
DIFF_FILE_HEADER = re.compile(r"^diff --git a/.* b/(?P<path>.*)$")

PROFILES: dict[str, tuple[str, ...]] = {
    "prototype": ("tests", "secrets", "test_integrity"),
    "product": ("tests", "lint", "security", "secrets", "build", "test_integrity"),
}
PYTHON_PROJECT_MARKERS = ("pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini")
TOOLCHAIN_COMMANDS: dict[str, dict[str, tuple[str, ...]]] = {
    "cargo": {
        "tests": ("cargo", "test"),
        "lint": ("cargo", "clippy", "--", "-D", "warnings"),
    },
    "go": {
        "tests": ("go", "test", "./..."),
        "lint": ("go", "vet", "./..."),
    },
    "python": {
        "tests": (sys.executable, "-m", "pytest", "-q"),
        "lint": ("ruff", "check", "."),
    },
}
NPM_DEFAULT_TEST_PLACEHOLDER = "no test specified"
AUDIT_MODES = {"security": "audit", "secrets": "secrets"}
DEFAULT_JUSTIFICATION = Path(".scratch/justificacion-tests.md")
DEFAULT_APPROVAL = Path(".scratch/aprobacion-tests.json")
DEFAULT_EVIDENCE_DIR = Path(".scratch/gate-evidence")

JUSTIFICATION_LABELS = ("Antes:", "Ahora:", "Fuente:", "Prueba de que falla:")
HOOK_MARKER = "# team-guardian-managed"


@dataclass(frozen=True)
class Violation:
    """Incumplimiento de una regla, con codigo estable y mensaje legible."""

    code: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """Resultado de validar un nombre de rama o un mensaje de commit."""

    ok: bool
    violations: tuple[Violation, ...]


@dataclass(frozen=True)
class SensitiveTestChange:
    """Cambio en un test que podria debilitar la verificacion."""

    file_path: str
    kind: str
    before: str | None
    after: str | None


@dataclass(frozen=True)
class GateVerdict:
    """Veredicto del gate sobre los cambios sensibles de tests."""

    status: str
    changes: tuple[SensitiveTestChange, ...]
    fingerprint: str | None


def _result(*violations: Violation) -> ValidationResult:
    return ValidationResult(ok=not violations, violations=violations)


def validate_branch_name(name: str) -> ValidationResult:
    """Valida que la rama sea `main` o `feat|fix|chore/<slug-kebab-case>`."""
    if BRANCH_PATTERN.fullmatch(name):
        return _result()
    return _result(
        Violation(
            "invalid_branch",
            f"Rama '{name}' invalida: use 'main' o 'feat|fix|chore/<slug-kebab-case>'.",
        )
    )


def _commit_header(message: str) -> str | None:
    for line in message.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        return line
    return None


def validate_commit_message(message: str) -> ValidationResult:
    """Valida el encabezado del mensaje segun Conventional Commits."""
    header = _commit_header(message)
    if header is not None and header.startswith("Merge "):
        return _result()
    invalid_format = Violation(
        "invalid_format",
        "El encabezado debe ser '<tipo>(<alcance>)?: <descripcion>'.",
    )
    if header is None:
        return _result(invalid_format)
    match = COMMIT_HEADER_PATTERN.fullmatch(header)
    if match is None:
        return _result(invalid_format)
    violations: list[Violation] = []
    if match["type"] not in COMMIT_TYPES:
        violations.append(
            Violation(
                "unknown_type",
                f"Tipo '{match['type']}' desconocido; permitidos: "
                f"{', '.join(sorted(COMMIT_TYPES))}.",
            )
        )
    if not match["description"].strip():
        violations.append(Violation("empty_description", "La descripcion esta vacia."))
    if len(header) > MAX_HEADER_LENGTH:
        violations.append(
            Violation(
                "header_too_long",
                f"El encabezado supera {MAX_HEADER_LENGTH} caracteres.",
            )
        )
    return _result(*violations)


def _is_test_path(path: str) -> bool:
    parts = path.split("/")
    if any(part in TEST_DIRECTORIES for part in parts[:-1]):
        return True
    return TEST_FILE_PATTERN.fullmatch(parts[-1]) is not None


def _squash(line: str) -> str:
    return re.sub(r"\s+", "", line)


def _hunk_changes(
    path: str, removed: list[str], added: list[str]
) -> list[SensitiveTestChange]:
    removed_assertions = [s for s in removed if ASSERTION_PATTERN.search(s)]
    added_assertions = [s for s in added if ASSERTION_PATTERN.search(s)]
    changes: list[SensitiveTestChange] = []
    for index, before in enumerate(removed_assertions):
        if index >= len(added_assertions):
            changes.append(SensitiveTestChange(path, "assertion_removed", before, None))
            continue
        after = added_assertions[index]
        if _squash(before) != _squash(after):
            changes.append(
                SensitiveTestChange(path, "assertion_modified", before, after)
            )
    added_definitions = {
        _squash(s) for s in added if TEST_DEFINITION_PATTERN.search(s)
    }
    for line in removed:
        if (
            TEST_DEFINITION_PATTERN.search(line)
            and _squash(line) not in added_definitions
        ):
            changes.append(SensitiveTestChange(path, "test_removed", line, None))
    for line in added:
        if SKIP_PATTERN.search(line):
            changes.append(SensitiveTestChange(path, "skip_added", None, line))
    return changes


def detect_sensitive_test_changes(
    unified_diff: str,
) -> tuple[SensitiveTestChange, ...]:
    """Detecta aserciones, tests o skips alterados en archivos de test del diff."""
    changes: list[SensitiveTestChange] = []
    path: str | None = None
    removed: list[str] = []
    added: list[str] = []
    in_hunk = False

    def close_hunk() -> None:
        if path is not None and _is_test_path(path):
            changes.extend(_hunk_changes(path, removed, added))
        removed.clear()
        added.clear()

    for line in unified_diff.splitlines():
        header = DIFF_FILE_HEADER.match(line)
        if header:
            close_hunk()
            path, in_hunk = header["path"], False
        elif line.startswith("@@"):
            close_hunk()
            in_hunk = True
        elif in_hunk and line.startswith("-"):
            removed.append(line[1:].strip())
        elif in_hunk and line.startswith("+"):
            added.append(line[1:].strip())
    close_hunk()
    return tuple(changes)


def fingerprint_sensitive_changes(changes: tuple[SensitiveTestChange, ...]) -> str:
    """Calcula un SHA-256 estable e independiente del orden de los cambios."""
    serialized = sorted(
        json.dumps([c.file_path, c.kind, c.before, c.after], ensure_ascii=False)
        for c in changes
    )
    return hashlib.sha256("\n".join(serialized).encode("utf-8")).hexdigest()


def write_approval(path: Path, fingerprint: str, approver: str) -> None:
    """Registra la aprobacion humana de un fingerprint concreto."""
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "fingerprint": fingerprint,
        "approver": approver,
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def is_approved(path: Path, fingerprint: str) -> bool:
    """Indica si el archivo de aprobacion corresponde exactamente al fingerprint."""
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(record, dict) and record.get("fingerprint") == fingerprint


def _justification_is_complete(
    text: str, changes: tuple[SensitiveTestChange, ...]
) -> bool:
    if not text.strip():
        return False
    if any(c.file_path not in text for c in changes):
        return False
    return all(text.count(label) >= len(changes) for label in JUSTIFICATION_LABELS)


def evaluate_test_change_gate(
    changes: tuple[SensitiveTestChange, ...],
    justification_path: Path,
    approval_path: Path,
) -> GateVerdict:
    """Decide si los cambios sensibles de tests estan justificados y aprobados."""
    if not changes:
        return GateVerdict("pass", changes, None)
    fingerprint = fingerprint_sensitive_changes(changes)
    try:
        text = justification_path.read_text(encoding="utf-8")
    except OSError:
        text = ""
    if not _justification_is_complete(text, changes):
        return GateVerdict("blocked_missing_justification", changes, fingerprint)
    if is_approved(approval_path, fingerprint):
        return GateVerdict("approved", changes, fingerprint)
    return GateVerdict("blocked_pending_approval", changes, fingerprint)


def install_commit_msg_hook(repo_root: Path) -> Path:
    """Instala el hook `commit-msg` que valida Conventional Commits."""
    git_dir = repo_root / ".git"
    if not git_dir.is_dir():
        raise FileNotFoundError(f"No existe {git_dir}")
    hook_path = git_dir / "hooks" / "commit-msg"
    if hook_path.exists() and HOOK_MARKER not in hook_path.read_text(encoding="utf-8"):
        raise FileExistsError(f"Ya existe un hook ajeno en {hook_path}")
    script = Path(__file__).resolve().as_posix()
    interpreter = Path(sys.executable).as_posix()
    content = (
        "#!/bin/sh\n"
        f"{HOOK_MARKER}\n"
        f'exec "{interpreter}" "{script}" check-commit-msg "$1"\n'
    )
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    hook_path.write_bytes(content.encode("utf-8"))
    hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return hook_path


@dataclass(frozen=True)
class PlannedStep:
    """Paso del gate: comando a ejecutar o motivo por el que no esta disponible."""

    name: str
    argv: tuple[str, ...] | None
    unavailable_reason: str | None


@dataclass(frozen=True)
class CommandOutcome:
    """Codigo de salida y salida combinada de un comando ejecutado."""

    exit_code: int
    output: str


@dataclass(frozen=True)
class StepResult:
    """Resultado de un paso del gate con la ruta de su evidencia."""

    name: str
    status: str
    argv: tuple[str, ...] | None
    exit_code: int | None
    reason: str | None
    evidence_file: Path | None


@dataclass(frozen=True)
class GateReport:
    """Resultado agregado del gate para un perfil."""

    profile: str
    steps: tuple[StepResult, ...]
    passed: bool


def run_command(argv: tuple[str, ...], cwd: Path) -> CommandOutcome:
    """Ejecuta un comando en `cwd` y devuelve su salida combinada y su codigo."""
    completed = subprocess.run(
        argv,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return CommandOutcome(completed.returncode, completed.stdout)


def default_security_script() -> Path | None:
    """Ubica el script de `security-auditor` junto a este plugin, si existe."""
    plugins_dir = Path(__file__).resolve().parents[4]
    script = (
        plugins_dir / "security-auditor" / "skills" / "security-auditor"
        / "scripts" / "run_audit.py"
    )
    return script if script.is_file() else None


def _has_python_tests(root: Path) -> bool:
    patterns = ("test_*.py", "*_test.py")
    return any(
        next(directory.glob(pattern), None) is not None
        for directory in (root, root / "tests")
        for pattern in patterns
    )


def _detect_toolchain(root: Path) -> str | None:
    if (root / "package.json").is_file():
        return "npm"
    if (root / "Cargo.toml").is_file():
        return "cargo"
    if (root / "go.mod").is_file():
        return "go"
    if any((root / marker).is_file() for marker in PYTHON_PROJECT_MARKERS):
        return "python"
    return "python" if _has_python_tests(root) else None


def _npm_scripts(root: Path) -> dict[str, str]:
    try:
        manifest = json.loads((root / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    scripts = manifest.get("scripts") if isinstance(manifest, dict) else None
    return scripts if isinstance(scripts, dict) else {}


def _toolchain_step(root: Path, toolchain: str | None, name: str) -> PlannedStep:
    if toolchain is None:
        return PlannedStep(name, None, "No se detecto un runner para el proyecto.")
    if toolchain != "npm":
        return PlannedStep(name, TOOLCHAIN_COMMANDS[toolchain][name], None)
    script = "test" if name == "tests" else name
    command = _npm_scripts(root).get(script)
    if not isinstance(command, str) or NPM_DEFAULT_TEST_PLACEHOLDER in command:
        return PlannedStep(name, None, f"package.json no define el script '{script}'.")
    argv = ("npm", "test") if name == "tests" else ("npm", "run", name)
    return PlannedStep(name, argv, None)


def _audit_step(
    root: Path, name: str, security_script: Path | None
) -> PlannedStep:
    if security_script is None or not security_script.is_file():
        return PlannedStep(name, None, "No se encontro el script de security-auditor.")
    argv = (
        sys.executable, str(security_script),
        "--target", str(root), "--mode", AUDIT_MODES[name],
    )
    return PlannedStep(name, argv, None)


def _build_step(root: Path) -> PlannedStep:
    if not (root / "Dockerfile").is_file():
        return PlannedStep("build", None, "El proyecto no tiene Dockerfile.")
    return PlannedStep("build", ("docker", "build", "-q", "."), None)


def plan_command_steps(
    project_root: Path, profile: str, security_script: Path | None
) -> tuple[PlannedStep, ...]:
    """Planifica los pasos con comando del perfil, sin ejecutar nada."""
    if profile not in PROFILES:
        raise ValueError(f"Perfil desconocido: {profile}")
    toolchain = _detect_toolchain(project_root)
    steps: list[PlannedStep] = []
    for name in PROFILES[profile]:
        if name in ("tests", "lint"):
            steps.append(_toolchain_step(project_root, toolchain, name))
        elif name in AUDIT_MODES:
            steps.append(_audit_step(project_root, name, security_script))
        elif name == "build":
            steps.append(_build_step(project_root))
    return tuple(steps)


def _write_evidence(evidence_dir: Path, name: str, content: str) -> Path:
    path = evidence_dir / f"{name}.log"
    path.write_bytes(content.encode("utf-8"))
    return path


def _unavailable(
    name: str,
    argv: tuple[str, ...] | None,
    reason: str,
    evidence_dir: Path,
) -> StepResult:
    evidence = _write_evidence(evidence_dir, name, f"no verificado: {reason}\n")
    return StepResult(name, "unavailable", argv, None, reason, evidence)


def _command_step(
    planned: PlannedStep,
    runner: Callable[[tuple[str, ...], Path], CommandOutcome],
    project_root: Path,
    evidence_dir: Path,
) -> StepResult:
    argv = planned.argv
    if argv is None:
        return _unavailable(
            planned.name, None, planned.unavailable_reason or "", evidence_dir
        )
    try:
        outcome = runner(argv, project_root)
    except FileNotFoundError:
        return _unavailable(
            planned.name, argv, f"ejecutable no encontrado: {argv[0]}", evidence_dir
        )
    log = f"$ {' '.join(argv)}\nexit_code: {outcome.exit_code}\n\n{outcome.output}"
    evidence = _write_evidence(evidence_dir, planned.name, log)
    status = "passed" if outcome.exit_code == 0 else "failed"
    return StepResult(
        planned.name, status, argv, outcome.exit_code, None, evidence
    )


def _integrity_step(
    diff_text: str,
    justification_path: Path,
    approval_path: Path,
    evidence_dir: Path,
) -> StepResult:
    changes = detect_sensitive_test_changes(diff_text)
    verdict = evaluate_test_change_gate(changes, justification_path, approval_path)
    lines = [f"status: {verdict.status}"]
    lines += [f"{change.kind}: {change.file_path}" for change in changes]
    evidence = _write_evidence(evidence_dir, "test_integrity", "\n".join(lines) + "\n")
    if verdict.status in ("pass", "approved"):
        return StepResult("test_integrity", "passed", None, None, None, evidence)
    return StepResult(
        "test_integrity", "failed", None, None, verdict.status, evidence
    )


def run_gate(
    project_root: Path,
    profile: str,
    evidence_dir: Path,
    diff_text: str,
    justification_path: Path,
    approval_path: Path,
    security_script: Path | None = None,
    runner: Callable[[tuple[str, ...], Path], CommandOutcome] = run_command,
) -> GateReport:
    """Ejecuta los pasos del perfil y guarda la evidencia literal de cada uno."""
    planned = {
        step.name: step
        for step in plan_command_steps(project_root, profile, security_script)
    }
    evidence_dir.mkdir(parents=True, exist_ok=True)
    results: list[StepResult] = []
    for name in PROFILES[profile]:
        if name == "test_integrity":
            results.append(
                _integrity_step(
                    diff_text, justification_path, approval_path, evidence_dir
                )
            )
        else:
            results.append(
                _command_step(planned[name], runner, project_root, evidence_dir)
            )
    steps = tuple(results)
    return GateReport(profile, steps, all(s.status == "passed" for s in steps))


def _git_diff_against_head(root: Path) -> str:
    completed = subprocess.run(
        ("git", "diff", "HEAD"),
        cwd=root,
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return completed.stdout


def _report(result: ValidationResult) -> int:
    for violation in result.violations:
        print(violation.message, file=sys.stderr)
    return 0 if result.ok else 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="team_guard")
    commands = parser.add_subparsers(dest="command", required=True)
    commit = commands.add_parser("check-commit-msg")
    commit.add_argument("message_file", type=Path)
    branch = commands.add_parser("check-branch")
    branch.add_argument("name")
    hook = commands.add_parser("install-hook")
    hook.add_argument("--repo-root", type=Path, default=Path.cwd())
    for name in ("approve-test-changes", "gate-test-changes"):
        sub = commands.add_parser(name)
        sub.add_argument("--diff-file", type=Path, required=True)
        sub.add_argument("--justification", type=Path, required=True)
        sub.add_argument("--approval", type=Path, required=True)
        if name == "approve-test-changes":
            sub.add_argument("--approver", required=True)
    gate = commands.add_parser("gate")
    gate.add_argument("--profile", choices=tuple(PROFILES.keys()), required=True)
    gate.add_argument("--root", type=Path, default=Path.cwd())
    gate.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE_DIR)
    gate.add_argument("--justification", type=Path, default=DEFAULT_JUSTIFICATION)
    gate.add_argument("--approval", type=Path, default=DEFAULT_APPROVAL)
    gate.add_argument("--diff-file", type=Path, default=None)
    gate.add_argument(
        "--security-script",
        type=Path,
        default=default_security_script(),
    )
    return parser


def _verdict_for(args: argparse.Namespace) -> GateVerdict:
    diff = args.diff_file.read_text(encoding="utf-8")
    changes = detect_sensitive_test_changes(diff)
    return evaluate_test_change_gate(changes, args.justification, args.approval)


def main(argv: list[str]) -> int:
    """Punto de entrada de la CLI; devuelve el codigo de salida."""
    try:
        args = _build_parser().parse_args(argv)
    except SystemExit:
        return 2
    try:
        if args.command == "check-commit-msg":
            text = args.message_file.read_text(encoding="utf-8")
            return _report(validate_commit_message(text))
        if args.command == "check-branch":
            return _report(validate_branch_name(args.name))
        if args.command == "install-hook":
            print(install_commit_msg_hook(args.repo_root))
            return 0
        if args.command == "gate":
            if args.diff_file is not None:
                diff_text = args.diff_file.read_text(encoding="utf-8")
            else:
                diff_text = _git_diff_against_head(args.root)
            report = run_gate(
                project_root=args.root,
                profile=args.profile,
                evidence_dir=args.evidence_dir,
                diff_text=diff_text,
                justification_path=args.justification,
                approval_path=args.approval,
                security_script=args.security_script,
            )
            for step in report.steps:
                print(f"{step.name}: {step.status}")
            return 0 if report.passed else 1
        verdict = _verdict_for(args)
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    if args.command == "gate-test-changes":
        print(verdict.status)
        return 0 if verdict.status in ("pass", "approved") else 1
    if verdict.status == "pass":
        return 0
    if verdict.status == "blocked_missing_justification":
        print(verdict.status, file=sys.stderr)
        return 1
    write_approval(args.approval, verdict.fingerprint or "", args.approver)
    print(f"approved {verdict.fingerprint}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
