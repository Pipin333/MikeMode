"""Regresion: el hook debe usar el interprete que lo instalo, no uno del PATH."""
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "skills" / "team-guardian" / "scripts"),
)

from team_guard import install_commit_msg_hook  # noqa: E402


def test_hook_pins_installing_interpreter(tmp_path: Path) -> None:
    """En Windows `python3` puede ser un alias de la Store que falla."""
    (tmp_path / ".git").mkdir()
    text = install_commit_msg_hook(tmp_path).read_text(encoding="utf-8")
    assert Path(sys.executable).as_posix() in text
    assert "command -v python" not in text
