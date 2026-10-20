"""Tests del gate de verificacion de team_guard (planificacion, ejecucion, CLI)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "skills" / "team-guardian" / "scripts"),
)

from team_guard import (  # noqa: E402
    PROFILES,
    CommandOutcome,
    GateReport,
    PlannedStep,
    StepResult,
    main,
    plan_command_steps,
    run_command,
    run_gate,
)

DELETED_ASSERTION_DIFF = (
    "diff --git a/tests/test_ok.py b/tests/test_ok.py\n"
    "index 1111111..2222222 100644\n"
    "--- a/tests/test_ok.py\n"
    "+++ b/tests/test_ok.py\n"
    "@@ -1,2 +1,1 @@\n"
    " def test_ok():\n"
    "-    assert True\n"
)


def steps_by_name(steps: tuple) -> dict:
    """Indexa pasos planificados o resultados por nombre."""
    return {step.name: step for step in steps}


def make_python_project(root: Path) -> None:
    """Crea un proyecto Python minimo con un test que pasa."""
    (root / "tests").mkdir(parents=True, exist_ok=True)
    (root / "tests" / "test_ok.py").write_text(
        "def test_ok():\n    assert True\n", encoding="utf-8"
    )


class RecordingRunner:
    """Runner falso que registra llamadas y devuelve salidas configuradas."""

    def __init__(self, outcomes: dict | None = None, default_exit: int = 0,
                 output: str = "salida\n") -> None:
        self.calls: list[tuple[tuple[str, ...], Path]] = []
        self.outcomes = outcomes or {}
        self.default_exit = default_exit
        self.output = output

    def __call__(self, argv: tuple[str, ...], cwd: Path) -> CommandOutcome:
        self.calls.append((argv, cwd))
        if argv in self.outcomes:
            return self.outcomes[argv]
        return CommandOutcome(self.default_exit, self.output)


def gate_kwargs(tmp_path: Path, root: Path, diff_text: str = "") -> dict:
    """Argumentos comunes de run_gate."""
    return {
        "project_root": root,
        "evidence_dir": tmp_path / "ev" / "nested",
        "diff_text": diff_text,
        "justification_path": tmp_path / "justificacion.md",
        "approval_path": tmp_path / "approval.json",
    }


def test_profiles_constant() -> None:
    assert PROFILES["prototype"] == ("tests", "secrets", "test_integrity")
    assert PROFILES["product"] == (
        "tests", "lint", "security", "secrets", "build", "test_integrity",
    )


def test_plan_invalid_profile(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        plan_command_steps(tmp_path, "nope", None)


def test_plan_excludes_test_integrity_and_keeps_order(tmp_path: Path) -> None:
    prototype = plan_command_steps(tmp_path, "prototype", None)
    assert [s.name for s in prototype] == ["tests", "secrets"]
    product = plan_command_steps(tmp_path, "product", None)
    assert [s.name for s in product] == [
        "tests", "lint", "security", "secrets", "build",
    ]
    assert all(isinstance(s, PlannedStep) for s in product)


def test_plan_no_runner(tmp_path: Path) -> None:
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["tests"].argv is None
    assert "runner" in steps["tests"].unavailable_reason
    assert steps["lint"].argv is None
    assert steps["lint"].unavailable_reason


def test_plan_npm_with_test_and_lint_scripts(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        json.dumps({"scripts": {"test": "vitest run", "lint": "eslint ."}}),
        encoding="utf-8",
    )
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["tests"].argv == ("npm", "test")
    assert steps["tests"].unavailable_reason is None
    assert steps["lint"].argv == ("npm", "run", "lint")


def test_plan_npm_default_placeholder_is_unavailable(tmp_path: Path) -> None:
    placeholder = 'echo "Error: no test specified" && exit 1'
    (tmp_path / "package.json").write_text(
        json.dumps({"scripts": {"test": placeholder}}), encoding="utf-8"
    )
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["tests"].argv is None
    assert steps["tests"].unavailable_reason
    assert steps["lint"].argv is None
    assert steps["lint"].unavailable_reason


def test_plan_npm_without_scripts(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["tests"].argv is None
    assert steps["tests"].unavailable_reason


def test_plan_cargo(tmp_path: Path) -> None:
    (tmp_path / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["tests"].argv == ("cargo", "test")
    assert steps["lint"].argv == ("cargo", "clippy", "--", "-D", "warnings")


def test_plan_go(tmp_path: Path) -> None:
    (tmp_path / "go.mod").write_text("module x\n", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["tests"].argv == ("go", "test", "./...")
    assert steps["lint"].argv == ("go", "vet", "./...")


def test_plan_python_by_config_file(tmp_path: Path) -> None:
    (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["tests"].argv == (sys.executable, "-m", "pytest", "-q")
    assert steps["lint"].argv == ("ruff", "check", ".")


@pytest.mark.parametrize(
    "relative", ["test_algo.py", "algo_test.py", "tests/test_algo.py",
                 "tests/algo_test.py"],
)
def test_plan_python_by_test_file(tmp_path: Path, relative: str) -> None:
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("def test_a():\n    pass\n", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "prototype", None))
    assert steps["tests"].argv == (sys.executable, "-m", "pytest", "-q")


def test_plan_priority_npm_over_cargo_go_python(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        json.dumps({"scripts": {"test": "jest"}}), encoding="utf-8"
    )
    (tmp_path / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    (tmp_path / "go.mod").write_text("module x\n", encoding="utf-8")
    (tmp_path / "pytest.ini").write_text("", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "prototype", None))
    assert steps["tests"].argv == ("npm", "test")


def test_plan_priority_cargo_over_go_python(tmp_path: Path) -> None:
    (tmp_path / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    (tmp_path / "go.mod").write_text("module x\n", encoding="utf-8")
    (tmp_path / "pytest.ini").write_text("", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "prototype", None))
    assert steps["tests"].argv == ("cargo", "test")


def test_plan_priority_go_over_python(tmp_path: Path) -> None:
    (tmp_path / "go.mod").write_text("module x\n", encoding="utf-8")
    (tmp_path / "pytest.ini").write_text("", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "prototype", None))
    assert steps["tests"].argv == ("go", "test", "./...")


def test_plan_security_and_secrets_with_script(tmp_path: Path) -> None:
    script = tmp_path / "audit.py"
    script.write_text("", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "product", script))
    assert steps["security"].argv == (
        sys.executable, str(script), "--target", str(tmp_path),
        "--mode", "audit",
    )
    assert steps["secrets"].argv == (
        sys.executable, str(script), "--target", str(tmp_path),
        "--mode", "secrets",
    )


def test_plan_security_script_none_or_missing(tmp_path: Path) -> None:
    for script in (None, tmp_path / "missing.py"):
        steps = steps_by_name(plan_command_steps(tmp_path, "product", script))
        for name in ("security", "secrets"):
            assert steps[name].argv is None
            assert steps[name].unavailable_reason


def test_plan_build_with_and_without_dockerfile(tmp_path: Path) -> None:
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["build"].argv is None
    assert "Dockerfile" in steps["build"].unavailable_reason
    (tmp_path / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
    steps = steps_by_name(plan_command_steps(tmp_path, "product", None))
    assert steps["build"].argv == ("docker", "build", "-q", ".")
    assert steps["build"].unavailable_reason is None


def test_plan_exactly_one_of_argv_or_reason(tmp_path: Path) -> None:
    make_python_project(tmp_path)
    for step in plan_command_steps(tmp_path, "product", None):
        assert (step.argv is None) != (step.unavailable_reason is None)


def test_run_gate_invalid_profile_runs_nothing(tmp_path: Path) -> None:
    runner = RecordingRunner()
    with pytest.raises(ValueError):
        run_gate(profile="nope", runner=runner, **gate_kwargs(tmp_path, tmp_path))
    assert runner.calls == []


def test_run_gate_all_passed(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    make_python_project(root)
    script = tmp_path / "audit.py"
    script.write_text("", encoding="utf-8")
    runner = RecordingRunner()
    report = run_gate(
        profile="prototype", security_script=script, runner=runner,
        **gate_kwargs(tmp_path, root),
    )
    assert isinstance(report, GateReport)
    assert report.profile == "prototype"
    assert [s.name for s in report.steps] == list(PROFILES["prototype"])
    assert all(isinstance(s, StepResult) for s in report.steps)
    assert [s.status for s in report.steps] == ["passed"] * 3
    assert report.passed is True
    assert [call[0] for call in runner.calls] == [
        (sys.executable, "-m", "pytest", "-q"),
        (sys.executable, str(script), "--target", str(root),
         "--mode", "secrets"),
    ]
    assert all(call[1] == root for call in runner.calls)


def test_run_gate_failed_exit_code_recorded(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    make_python_project(root)
    pytest_argv = (sys.executable, "-m", "pytest", "-q")
    runner = RecordingRunner({pytest_argv: CommandOutcome(5, "boom")})
    report = run_gate(
        profile="prototype", runner=runner, **gate_kwargs(tmp_path, root)
    )
    result = steps_by_name(report.steps)["tests"]
    assert result.status == "failed"
    assert result.exit_code == 5
    assert result.argv == pytest_argv
    assert report.passed is False


def test_run_gate_unavailable_never_passes_and_skips_runner(
    tmp_path: Path,
) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    make_python_project(root)
    runner = RecordingRunner()
    report = run_gate(
        profile="prototype", security_script=None, runner=runner,
        **gate_kwargs(tmp_path, root),
    )
    secrets = steps_by_name(report.steps)["secrets"]
    assert secrets.status == "unavailable"
    assert secrets.argv is None
    assert secrets.exit_code is None
    assert secrets.reason
    assert report.passed is False
    assert [call[0] for call in runner.calls] == [
        (sys.executable, "-m", "pytest", "-q")
    ]


def test_run_gate_file_not_found_is_unavailable(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "Cargo.toml").write_text("[package]\n", encoding="utf-8")

    def runner(argv: tuple[str, ...], cwd: Path) -> CommandOutcome:
        raise FileNotFoundError(argv[0])

    report = run_gate(
        profile="prototype", runner=runner, **gate_kwargs(tmp_path, root)
    )
    tests = steps_by_name(report.steps)["tests"]
    assert tests.status == "unavailable"
    assert "cargo" in tests.reason
    assert tests.exit_code is None
    assert report.passed is False


def test_run_gate_test_integrity_passes_on_empty_diff(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    report = run_gate(
        profile="prototype", runner=RecordingRunner(),
        **gate_kwargs(tmp_path, root),
    )
    integrity = steps_by_name(report.steps)["test_integrity"]
    assert report.steps[-1] is integrity
    assert integrity.status == "passed"
    assert integrity.argv is None
    assert integrity.exit_code is None


def test_run_gate_test_integrity_fails_on_deleted_assertion(
    tmp_path: Path,
) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    make_python_project(root)
    kwargs = gate_kwargs(tmp_path, root, DELETED_ASSERTION_DIFF)
    report = run_gate(profile="prototype", runner=RecordingRunner(), **kwargs)
    integrity = steps_by_name(report.steps)["test_integrity"]
    assert integrity.status == "failed"
    assert integrity.argv is None
    assert integrity.exit_code is None
    assert integrity.reason.startswith("blocked")
    assert report.passed is False
    log = (kwargs["evidence_dir"] / "test_integrity.log").read_text(
        encoding="utf-8"
    )
    assert integrity.reason in log
    assert "tests/test_ok.py" in log


def test_run_gate_evidence_files(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    make_python_project(root)
    pytest_argv = (sys.executable, "-m", "pytest", "-q")
    literal = "linea1\n  linea2 con espacios\r\nfin"
    runner = RecordingRunner({pytest_argv: CommandOutcome(0, literal)})
    kwargs = gate_kwargs(tmp_path, root)
    report = run_gate(
        profile="prototype", security_script=None, runner=runner, **kwargs
    )
    evidence_dir = kwargs["evidence_dir"]
    assert evidence_dir.is_dir()
    for step in report.steps:
        assert step.evidence_file == evidence_dir / f"{step.name}.log"
        assert step.evidence_file.is_file()
    tests_log = (evidence_dir / "tests.log").read_bytes().decode("utf-8")
    expected = "$ " + " ".join(pytest_argv) + "\nexit_code: 0\n\n" + literal
    assert tests_log == expected
    secrets = steps_by_name(report.steps)["secrets"]
    secrets_log = secrets.evidence_file.read_text(encoding="utf-8")
    assert "no verificado" in secrets_log
    assert secrets.reason in secrets_log


def test_run_gate_evidence_records_nonzero_exit(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    make_python_project(root)
    pytest_argv = (sys.executable, "-m", "pytest", "-q")
    runner = RecordingRunner({pytest_argv: CommandOutcome(7, "fallo")})
    kwargs = gate_kwargs(tmp_path, root)
    run_gate(profile="prototype", runner=runner, **kwargs)
    log = (kwargs["evidence_dir"] / "tests.log").read_text(encoding="utf-8")
    lines = log.split("\n")
    assert lines[0] == "$ " + " ".join(pytest_argv)
    assert lines[1] == "exit_code: 7"
    assert lines[2] == ""
    assert lines[3] == "fallo"


def test_run_gate_product_order_and_unavailable_build(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    make_python_project(root)
    runner = RecordingRunner()
    report = run_gate(
        profile="product", runner=runner, **gate_kwargs(tmp_path, root)
    )
    assert [s.name for s in report.steps] == list(PROFILES["product"])
    build = steps_by_name(report.steps)["build"]
    assert build.status == "unavailable"
    assert "Dockerfile" in build.reason
    assert report.passed is False


def test_run_command_success_output(tmp_path: Path) -> None:
    outcome = run_command((sys.executable, "-c", 'print("hola")'), tmp_path)
    assert isinstance(outcome, CommandOutcome)
    assert outcome.exit_code == 0
    assert "hola" in outcome.output


def test_run_command_exit_code(tmp_path: Path) -> None:
    outcome = run_command(
        (sys.executable, "-c", "import sys; sys.exit(3)"), tmp_path
    )
    assert outcome.exit_code == 3


def test_run_command_captures_stderr(tmp_path: Path) -> None:
    outcome = run_command(
        (sys.executable, "-c", 'import sys; sys.stderr.write("err")'), tmp_path
    )
    assert "err" in outcome.output


def test_run_command_respects_cwd(tmp_path: Path) -> None:
    outcome = run_command(
        (sys.executable, "-c", "import os; print(os.getcwd())"), tmp_path
    )
    printed = Path(outcome.output.strip()).resolve()
    assert printed == tmp_path.resolve()


def test_run_command_missing_executable(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        run_command(("definitivamente-no-existe-xyz",), tmp_path)


def cli_args(tmp_path: Path, profile: str, diff: str = "",
             script: Path | None = None) -> list[str]:
    """Construye los argumentos del subcomando gate."""
    root = tmp_path / "proj"
    root.mkdir(exist_ok=True)
    make_python_project(root)
    diff_file = tmp_path / "change.diff"
    diff_file.write_text(diff, encoding="utf-8")
    args = [
        "gate", "--profile", profile, "--root", str(root),
        "--evidence-dir", str(tmp_path / "evidence"),
        "--justification", str(tmp_path / "justificacion.md"),
        "--approval", str(tmp_path / "approval.json"),
        "--diff-file", str(diff_file),
    ]
    if script is not None:
        args += ["--security-script", str(script)]
    return args


def fake_audit(tmp_path: Path, code: int) -> Path:
    """Crea un script de auditoria falso con exit code fijo."""
    script = tmp_path / "fake_audit.py"
    script.write_text(f"import sys\nsys.exit({code})\n", encoding="utf-8")
    return script


def test_cli_prototype_all_pass(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = fake_audit(tmp_path, 0)
    code = main(cli_args(tmp_path, "prototype", script=script))
    lines = capsys.readouterr().out.splitlines()
    assert code == 0
    assert [ln for ln in lines if ln.split(":")[0] in PROFILES["prototype"]] == [
        "tests: passed", "secrets: passed", "test_integrity: passed",
    ]


def test_cli_prototype_secrets_failed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = fake_audit(tmp_path, 1)
    code = main(cli_args(tmp_path, "prototype", script=script))
    out = capsys.readouterr().out
    assert code == 1
    assert "secrets: failed" in out.splitlines()
    assert "tests: passed" in out.splitlines()


def test_cli_without_security_script_prints_secrets_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    main(cli_args(tmp_path, "prototype"))
    lines = capsys.readouterr().out.splitlines()
    assert any(ln.startswith("secrets: ") for ln in lines)
    assert "tests: passed" in lines
    assert "test_integrity: passed" in lines


def test_cli_deleted_assertion_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = fake_audit(tmp_path, 0)
    code = main(
        cli_args(tmp_path, "prototype", DELETED_ASSERTION_DIFF, script=script)
    )
    lines = capsys.readouterr().out.splitlines()
    assert code == 1
    assert "test_integrity: failed" in lines


def test_cli_invalid_profile_returns_2(tmp_path: Path) -> None:
    args = cli_args(tmp_path, "prototype")
    args[args.index("--profile") + 1] = "nope"
    assert main(args) == 2
