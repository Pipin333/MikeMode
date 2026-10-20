"""Tests de la especificacion del modulo team_guard."""
import dataclasses
import json
import re
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "skills" / "team-guardian" / "scripts"),
)

import pytest  # noqa: E402

from team_guard import (  # noqa: E402
    GateVerdict,
    SensitiveTestChange,
    ValidationResult,
    Violation,
    detect_sensitive_test_changes,
    evaluate_test_change_gate,
    fingerprint_sensitive_changes,
    install_commit_msg_hook,
    is_approved,
    main,
    validate_branch_name,
    validate_commit_message,
    write_approval,
)


def codes(result: ValidationResult) -> list[str]:
    """Devuelve los codigos de violacion de un resultado."""
    return [v.code for v in result.violations]


def make_diff(path: str, hunk_lines: list[str]) -> str:
    """Construye un diff unificado de un solo hunk."""
    return (
        f"diff --git a/{path} b/{path}\n"
        "index 111..222 100644\n"
        f"--- a/{path}\n"
        f"+++ b/{path}\n"
        "@@ -1,5 +1,5 @@\n" + "\n".join(hunk_lines) + "\n"
    )


def change(
    path: str = "tests/test_a.py",
    kind: str = "assertion_removed",
    before: str | None = "assert x == 1",
    after: str | None = None,
) -> SensitiveTestChange:
    """Crea un SensitiveTestChange."""
    return SensitiveTestChange(path, kind, before, after)


FULL_JUSTIFICATION = (
    "tests/test_a.py\nAntes: a\nAhora: b\nFuente: spec\nPrueba de que falla: x\n"
)


# ---------- tipos ----------


def test_types_are_frozen() -> None:
    """Las dataclasses son inmutables."""
    v = Violation("c", "m")
    with pytest.raises(dataclasses.FrozenInstanceError):
        v.code = "x"  # type: ignore[misc]
    c = change()
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.kind = "x"  # type: ignore[misc]


# ---------- branch ----------


@pytest.mark.parametrize(
    "name", ["main", "feat/login-form", "fix/bug-42", "chore/update-deps"]
)
def test_branch_valid(name: str) -> None:
    """Ramas validas."""
    result = validate_branch_name(name)
    assert result.ok is True
    assert result.violations == ()


@pytest.mark.parametrize(
    "name",
    [
        "",
        "develop",
        "feature/x",
        "feat/",
        "feat/Login",
        "feat/with space",
        "feat/under_score",
        "feat/-x",
        "feat/x-",
        "feat/a--b",
        "feat/a/b",
        "Feat/x",
    ],
)
def test_branch_invalid(name: str) -> None:
    """Ramas invalidas."""
    result = validate_branch_name(name)
    assert result.ok is False
    assert codes(result) == ["invalid_branch"]


# ---------- commit message ----------


@pytest.mark.parametrize(
    "message",
    [
        "feat: add login",
        "fix(auth): handle expired token",
        "feat(api)!: drop v1",
        "docs: update readme\n\nbody text",
        "# comment\nfix: x",
        "\n\nfix: x",
        'Merge branch "x" into main',
        "ci: x",
        "refactor: x",
        "test: x",
        "chore: x",
    ],
)
def test_commit_valid(message: str) -> None:
    """Mensajes validos."""
    result = validate_commit_message(message)
    assert result.ok is True
    assert result.violations == ()


@pytest.mark.parametrize(
    "message",
    [
        "",
        "add login",
        "feat add login",
        "feat:add",
        "Feat: x",
        "feat(Auth): x",
        "feat(): x",
        "   ",
        "# only comment",
    ],
)
def test_commit_invalid_format(message: str) -> None:
    """Formato invalido."""
    result = validate_commit_message(message)
    assert result.ok is False
    assert codes(result) == ["invalid_format"]


@pytest.mark.parametrize("message", ["feature: x", "wip: x"])
def test_commit_unknown_type(message: str) -> None:
    """Tipo desconocido."""
    result = validate_commit_message(message)
    assert result.ok is False
    assert codes(result) == ["unknown_type"]


@pytest.mark.parametrize("message", ["feat: ", "feat:   "])
def test_commit_empty_description(message: str) -> None:
    """Descripcion vacia."""
    result = validate_commit_message(message)
    assert result.ok is False
    assert codes(result) == ["empty_description"]


def test_commit_header_length_boundary() -> None:
    """72 caracteres vale, 73 no."""
    ok_header = "feat: " + "a" * 66
    assert len(ok_header) == 72
    assert validate_commit_message(ok_header).ok is True
    long_header = "feat: " + "a" * 67
    result = validate_commit_message(long_header)
    assert result.ok is False
    assert "header_too_long" in codes(result)


def test_commit_only_header_evaluated() -> None:
    """El cuerpo es libre."""
    assert validate_commit_message("fix: x\n\nnot conventional at all\n!!").ok


# ---------- detect ----------


def test_detect_empty_diff() -> None:
    """Diff vacio."""
    assert detect_sensitive_test_changes("") == ()


def test_detect_assertion_modified() -> None:
    """Asercion modificada."""
    diff = make_diff(
        "tests/test_a.py",
        [" def test_x():", "-    assert f() == 1", "+    assert f() == 2"],
    )
    assert detect_sensitive_test_changes(diff) == (
        SensitiveTestChange(
            "tests/test_a.py",
            "assertion_modified",
            "assert f() == 1",
            "assert f() == 2",
        ),
    )


def test_detect_assertion_removed() -> None:
    """Asercion eliminada."""
    diff = make_diff(
        "pkg/test_a.py", [" def test_x():", "-    assert f() == 1", "     pass"]
    )
    assert detect_sensitive_test_changes(diff) == (
        SensitiveTestChange("pkg/test_a.py", "assertion_removed", "assert f() == 1", None),
    )


def test_detect_modified_pairs_by_order_and_extra_removed() -> None:
    """Se emparejan por orden; sobrante es removed."""
    diff = make_diff(
        "tests/test_a.py",
        [
            "-    assert a == 1",
            "-    assert b == 2",
            "+    assert a == 10",
        ],
    )
    assert detect_sensitive_test_changes(diff) == (
        SensitiveTestChange(
            "tests/test_a.py", "assertion_modified", "assert a == 1", "assert a == 10"
        ),
        SensitiveTestChange("tests/test_a.py", "assertion_removed", "assert b == 2", None),
    )


def test_detect_test_removed() -> None:
    """Test eliminado."""
    diff = make_diff("tests/test_a.py", ["-def test_gone():", "-    pass"])
    assert detect_sensitive_test_changes(diff) == (
        SensitiveTestChange("tests/test_a.py", "test_removed", "def test_gone():", None),
    )


def test_detect_test_moved_in_same_hunk_not_removed() -> None:
    """Misma definicion agregada en el hunk no es eliminacion."""
    diff = make_diff(
        "tests/test_a.py", ["-def test_same():", "+def  test_same():"]
    )
    assert detect_sensitive_test_changes(diff) == ()


@pytest.mark.parametrize(
    "line",
    [
        "@pytest.mark.skip",
        "pytest.skip('x')",
        "xit('x', () => {})",
        "xtest('x', () => {})",
        "it.skip('x', () => {})",
        "test.skip('x', () => {})",
        "describe.skip('x', () => {})",
        "t.Skip()",
        "@unittest.skip('x')",
    ],
)
def test_detect_skip_added(line: str) -> None:
    """Skip agregado."""
    diff = make_diff("tests/test_a.py", [f"+{line}"])
    assert detect_sensitive_test_changes(diff) == (
        SensitiveTestChange("tests/test_a.py", "skip_added", None, line),
    )


def test_detect_not_sensitive_additions() -> None:
    """Solo agregados no son sensibles."""
    diff = make_diff(
        "tests/test_a.py",
        [" ctx", "+def test_new():", "+    assert g() == 3", " assert ctx == 1"],
    )
    assert detect_sensitive_test_changes(diff) == ()


def test_detect_whitespace_only_change_not_sensitive() -> None:
    """Cambio solo de espacios."""
    diff = make_diff(
        "tests/test_a.py", ["-    assert f()==1", "+        assert  f() == 1"]
    )
    assert detect_sensitive_test_changes(diff) == ()


def test_detect_ignores_non_test_files() -> None:
    """Archivos no test se ignoran."""
    diff = make_diff("src/app.py", ["-    assert f() == 1", "+    assert f() == 2"])
    assert detect_sensitive_test_changes(diff) == ()


def test_detect_ignores_context_lines() -> None:
    """Contexto no cuenta."""
    diff = make_diff("tests/test_a.py", [" assert a == 1", " def test_x():"])
    assert detect_sensitive_test_changes(diff) == ()


@pytest.mark.parametrize(
    "path",
    [
        "test_a.py",
        "a_test.py",
        "a_test.go",
        "a.test.js",
        "a.test.jsx",
        "a.test.ts",
        "a.test.tsx",
        "a.spec.js",
        "a.spec.tsx",
        "tests/helper.py",
        "test/helper.py",
        "src/__tests__/x.js",
        "deep/dir/tests/x.rs",
    ],
)
def test_detect_recognizes_test_paths(path: str) -> None:
    """Rutas de test reconocidas."""
    diff = make_diff(path, ["-    assert a == 1"])
    result = detect_sensitive_test_changes(diff)
    assert [c.file_path for c in result] == [path]


@pytest.mark.parametrize("path", ["src/testing.py", "a.test.py", "contest.py", "a.spec.py"])
def test_detect_rejects_non_test_paths(path: str) -> None:
    """Rutas que no son de test."""
    diff = make_diff(path, ["-    assert a == 1"])
    assert detect_sensitive_test_changes(diff) == ()


@pytest.mark.parametrize(
    "old,new",
    [
        ("expect(a).toBe(1)", "expect(a).toBe(2)"),
        ("self.assertEqual(a, 1)", "self.assertEqual(a, 2)"),
        ("assert.equal(a, 1)", "assert.equal(a, 2)"),
        ("t.Error(a)", "t.Error(b)"),
        ("require.Equal(t, a, 1)", "require.Equal(t, a, 2)"),
        ("assert_eq!(a, 1);", "assert_eq!(a, 2);"),
    ],
)
def test_detect_assertion_styles(old: str, new: str) -> None:
    """Estilos de asercion."""
    diff = make_diff("tests/x_test.go", [f"-  {old}", f"+  {new}"])
    assert detect_sensitive_test_changes(diff) == (
        SensitiveTestChange("tests/x_test.go", "assertion_modified", old, new),
    )


@pytest.mark.parametrize(
    "line",
    ["it('works', () => {", "test('works', () => {", "func TestX(t *testing.T) {", "#[test]"],
)
def test_detect_test_definition_styles(line: str) -> None:
    """Estilos de definicion de test."""
    diff = make_diff("tests/x.test.ts", [f"-{line}"])
    assert detect_sensitive_test_changes(diff) == (
        SensitiveTestChange("tests/x.test.ts", "test_removed", line, None),
    )


def test_detect_multiple_files_in_diff_order() -> None:
    """Orden del diff y archivos mezclados."""
    diff = (
        make_diff("tests/test_b.py", ["-    assert b == 1"])
        + make_diff("src/app.py", ["-    assert z == 1"])
        + make_diff("tests/test_a.py", ["-def test_a():"])
    )
    result = detect_sensitive_test_changes(diff)
    assert [(c.file_path, c.kind) for c in result] == [
        ("tests/test_b.py", "assertion_removed"),
        ("tests/test_a.py", "test_removed"),
    ]


def test_detect_per_hunk_pairing() -> None:
    """Las aserciones no se emparejan entre hunks distintos."""
    diff = (
        "diff --git a/tests/test_a.py b/tests/test_a.py\n"
        "--- a/tests/test_a.py\n+++ b/tests/test_a.py\n"
        "@@ -1,2 +1,2 @@\n-    assert a == 1\n"
        "@@ -10,2 +10,2 @@\n+    assert a == 2\n"
    )
    result = detect_sensitive_test_changes(diff)
    assert [c.kind for c in result] == ["assertion_removed"]


# ---------- fingerprint ----------


def test_fingerprint_format_and_empty() -> None:
    """Formato SHA-256 hex y vacio estable."""
    fp = fingerprint_sensitive_changes(())
    assert re.fullmatch(r"[0-9a-f]{64}", fp)
    assert fp == fingerprint_sensitive_changes(())


def test_fingerprint_order_independent() -> None:
    """Independiente del orden."""
    a, b = change(before="assert a"), change(before="assert b")
    assert fingerprint_sensitive_changes((a, b)) == fingerprint_sensitive_changes((b, a))


def test_fingerprint_deterministic_and_nonempty_differs() -> None:
    """Determinista y distinto del vacio."""
    a = change()
    assert fingerprint_sensitive_changes((a,)) == fingerprint_sensitive_changes((a,))
    assert fingerprint_sensitive_changes((a,)) != fingerprint_sensitive_changes(())


@pytest.mark.parametrize(
    "variant",
    [
        change(path="tests/test_b.py"),
        change(kind="test_removed"),
        change(before="assert y"),
        change(after="assert z"),
        change(before=None),
    ],
)
def test_fingerprint_changes_with_any_field(variant: SensitiveTestChange) -> None:
    """Cualquier campo altera el hash."""
    assert fingerprint_sensitive_changes((variant,)) != fingerprint_sensitive_changes(
        (change(),)
    )


# ---------- approval ----------


def test_write_approval_creates_json_and_parents(tmp_path: Path) -> None:
    """Escribe JSON con claves esperadas."""
    path = tmp_path / "a" / "b" / "approval.json"
    write_approval(path, "abc", "felipe")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["fingerprint"] == "abc"
    assert data["approver"] == "felipe"
    assert isinstance(data["approved_at"], str)
    from datetime import datetime

    datetime.fromisoformat(data["approved_at"])


def test_is_approved_matrix(tmp_path: Path) -> None:
    """Casos de is_approved."""
    path = tmp_path / "ap.json"
    assert is_approved(path, "abc") is False
    write_approval(path, "abc", "me")
    assert is_approved(path, "abc") is True
    assert is_approved(path, "abd") is False
    assert is_approved(path, "ABC") is False
    path.write_text("{not json", encoding="utf-8")
    assert is_approved(path, "abc") is False
    path.write_text(json.dumps({"approver": "x"}), encoding="utf-8")
    assert is_approved(path, "abc") is False


# ---------- gate ----------


def test_gate_pass_without_changes(tmp_path: Path) -> None:
    """Sin cambios pasa."""
    verdict = evaluate_test_change_gate((), tmp_path / "j.md", tmp_path / "a.json")
    assert verdict.status == "pass"
    assert verdict.fingerprint is None
    assert verdict.changes == ()


def test_gate_missing_or_blank_justification(tmp_path: Path) -> None:
    """Justificacion ausente o vacia bloquea."""
    j = tmp_path / "j.md"
    changes = (change(),)
    v = evaluate_test_change_gate(changes, j, tmp_path / "a.json")
    assert v.status == "blocked_missing_justification"
    j.write_text("  \n\t\n", encoding="utf-8")
    v = evaluate_test_change_gate(changes, j, tmp_path / "a.json")
    assert v.status == "blocked_missing_justification"
    assert v.changes == changes


@pytest.mark.parametrize(
    "text",
    [
        "Antes: a\nAhora: b\nFuente: s\nPrueba de que falla: p\n",
        "tests/test_a.py\nAhora: b\nFuente: s\nPrueba de que falla: p\n",
        "tests/test_a.py\nAntes: a\nFuente: s\nPrueba de que falla: p\n",
        "tests/test_a.py\nAntes: a\nAhora: b\nPrueba de que falla: p\n",
        "tests/test_a.py\nAntes: a\nAhora: b\nFuente: s\n",
    ],
)
def test_gate_incomplete_justification(tmp_path: Path, text: str) -> None:
    """Falta ruta o etiqueta."""
    j = tmp_path / "j.md"
    j.write_text(text, encoding="utf-8")
    v = evaluate_test_change_gate((change(),), j, tmp_path / "a.json")
    assert v.status == "blocked_missing_justification"


def test_gate_label_counts_must_cover_all_changes(tmp_path: Path) -> None:
    """Etiquetas al menos tantas veces como cambios."""
    j = tmp_path / "j.md"
    changes = (change(before="assert a"), change(before="assert b"))
    j.write_text(FULL_JUSTIFICATION, encoding="utf-8")
    v = evaluate_test_change_gate(changes, j, tmp_path / "a.json")
    assert v.status == "blocked_missing_justification"
    j.write_text(FULL_JUSTIFICATION * 2, encoding="utf-8")
    v = evaluate_test_change_gate(changes, j, tmp_path / "a.json")
    assert v.status == "blocked_pending_approval"


def test_gate_requires_every_file_path(tmp_path: Path) -> None:
    """Debe citar todos los archivos."""
    j = tmp_path / "j.md"
    j.write_text(FULL_JUSTIFICATION * 2, encoding="utf-8")
    changes = (change(), change(path="tests/test_other.py"))
    v = evaluate_test_change_gate(changes, j, tmp_path / "a.json")
    assert v.status == "blocked_missing_justification"


def test_gate_pending_then_approved_then_reblocked(tmp_path: Path) -> None:
    """Flujo completo de aprobacion."""
    j, ap = tmp_path / "j.md", tmp_path / "a.json"
    j.write_text(FULL_JUSTIFICATION, encoding="utf-8")
    changes = (change(),)
    pending = evaluate_test_change_gate(changes, j, ap)
    assert pending.status == "blocked_pending_approval"
    assert pending.fingerprint == fingerprint_sensitive_changes(changes)
    write_approval(ap, pending.fingerprint or "", "me")
    approved = evaluate_test_change_gate(changes, j, ap)
    assert isinstance(approved, GateVerdict)
    assert approved.status == "approved"
    assert approved.fingerprint == pending.fingerprint
    assert approved.changes == changes
    other = (change(before="assert other"),)
    j.write_text(FULL_JUSTIFICATION, encoding="utf-8")
    again = evaluate_test_change_gate(other, j, ap)
    assert again.status == "blocked_pending_approval"
    assert again.fingerprint == fingerprint_sensitive_changes(other)


# ---------- hook ----------


def test_hook_missing_git_dir(tmp_path: Path) -> None:
    """Sin .git falla."""
    with pytest.raises(FileNotFoundError):
        install_commit_msg_hook(tmp_path)


def test_hook_install_content(tmp_path: Path) -> None:
    """Contenido y permisos del hook."""
    (tmp_path / ".git").mkdir()
    path = install_commit_msg_hook(tmp_path)
    assert path == tmp_path / ".git" / "hooks" / "commit-msg"
    raw = path.read_bytes()
    assert b"\r" not in raw
    text = raw.decode("utf-8")
    assert text.startswith("#!/bin/sh")
    assert "# team-guardian-managed" in text
    assert "team_guard" in text
    assert "check-commit-msg" in text
    assert '"$1"' in text or "$1" in text
    if sys.platform != "win32":
        assert path.stat().st_mode & 0o111


def test_hook_idempotent(tmp_path: Path) -> None:
    """Reinstalar da el mismo contenido."""
    (tmp_path / ".git").mkdir()
    first = install_commit_msg_hook(tmp_path)
    content = first.read_bytes()
    second = install_commit_msg_hook(tmp_path)
    assert second == first
    assert second.read_bytes() == content


def test_hook_refuses_foreign_hook(tmp_path: Path) -> None:
    """No pisa hooks ajenos."""
    hooks = tmp_path / ".git" / "hooks"
    hooks.mkdir(parents=True)
    foreign = hooks / "commit-msg"
    foreign.write_bytes(b"#!/bin/sh\necho mine\n")
    with pytest.raises(FileExistsError):
        install_commit_msg_hook(tmp_path)
    assert foreign.read_bytes() == b"#!/bin/sh\necho mine\n"


# ---------- CLI ----------


def test_cli_check_commit_msg(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """check-commit-msg."""
    good = tmp_path / "good.txt"
    good.write_text("feat: ok\n", encoding="utf-8")
    assert main(["check-commit-msg", str(good)]) == 0
    bad = tmp_path / "bad.txt"
    bad.write_text("nonsense", encoding="utf-8")
    capsys.readouterr()
    assert main(["check-commit-msg", str(bad)]) == 1
    expected = validate_commit_message("nonsense").violations[0].message
    assert expected in capsys.readouterr().err
    assert main(["check-commit-msg", str(tmp_path / "nope.txt")]) == 2


def test_cli_check_branch(capsys: pytest.CaptureFixture[str]) -> None:
    """check-branch."""
    assert main(["check-branch", "feat/ok"]) == 0
    capsys.readouterr()
    assert main(["check-branch", "bad"]) == 1
    expected = validate_branch_name("bad").violations[0].message
    assert expected in capsys.readouterr().err


def test_cli_unknown_and_empty() -> None:
    """Subcomando desconocido o vacio."""
    assert main([]) == 2
    assert main(["bogus"]) == 2


def _gate_args(tmp_path: Path, diff: str, justification: str | None) -> dict[str, Path]:
    """Prepara archivos para los subcomandos de gate."""
    diff_file = tmp_path / "d.diff"
    diff_file.write_text(diff, encoding="utf-8")
    j = tmp_path / "j.md"
    if justification is not None:
        j.write_text(justification, encoding="utf-8")
    return {"diff": diff_file, "j": j, "ap": tmp_path / "ap" / "a.json"}


SENSITIVE_DIFF = make_diff("tests/test_a.py", ["-    assert f() == 1"])


def _approve(p: dict[str, Path]) -> int:
    return main(
        [
            "approve-test-changes",
            "--diff-file", str(p["diff"]),
            "--justification", str(p["j"]),
            "--approval", str(p["ap"]),
            "--approver", "felipe",
        ]
    )


def _gate(p: dict[str, Path]) -> int:
    return main(
        [
            "gate-test-changes",
            "--diff-file", str(p["diff"]),
            "--justification", str(p["j"]),
            "--approval", str(p["ap"]),
        ]
    )


def test_cli_approve_no_sensitive_changes(tmp_path: Path) -> None:
    """Sin cambios sensibles no escribe aprobacion."""
    p = _gate_args(tmp_path, make_diff("src/a.py", ["-x"]), None)
    assert _approve(p) == 0
    assert not p["ap"].exists()


def test_cli_approve_incomplete_justification(tmp_path: Path) -> None:
    """Justificacion incompleta -> 1 sin aprobacion."""
    p = _gate_args(tmp_path, SENSITIVE_DIFF, "nada")
    assert _approve(p) == 1
    assert not p["ap"].exists()


def test_cli_approve_complete_and_gate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Aprobacion completa escribe fingerprint y el gate aprueba."""
    p = _gate_args(tmp_path, SENSITIVE_DIFF, FULL_JUSTIFICATION)
    capsys.readouterr()
    assert _gate(p) == 1
    assert "blocked_pending_approval" in capsys.readouterr().out
    assert _approve(p) == 0
    changes = detect_sensitive_test_changes(SENSITIVE_DIFF)
    data = json.loads(p["ap"].read_text(encoding="utf-8"))
    assert data["fingerprint"] == fingerprint_sensitive_changes(changes)
    assert data["approver"] == "felipe"
    capsys.readouterr()
    assert _gate(p) == 0
    assert "approved" in capsys.readouterr().out


def test_cli_gate_pass_and_missing_justification(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Gate pass sin cambios; bloqueado sin justificacion."""
    p = _gate_args(tmp_path, "", None)
    assert _gate(p) == 0
    assert "pass" in capsys.readouterr().out
    p = _gate_args(tmp_path, SENSITIVE_DIFF, None)
    assert _gate(p) == 1
    assert "blocked_missing_justification" in capsys.readouterr().out
