"""Tests de regresión para doc_guard.py (Doc-Guardian)."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS_DIR = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "doc-guardian"
    / "scripts"
)
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import doc_guard


class TestDocGuardMonorepoAndSubmodules(unittest.TestCase):
    """Verifica que doc_guard detecte módulos de primer nivel no documentados en el README raíz."""

    def setUp(self) -> None:
        """Crea un repositorio Git temporal simulando un monorepo de plugins."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_path = Path(self.temp_dir.name)
        subprocess.run(
            ["git", "init"],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )

        root_readme = self.repo_path / "README.md"
        root_readme.write_text(
            "# Plugins Suite\n\n| Plugin | Desc |\n|---|---|\n| `doc-guardian` | Docs |\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", "README.md"],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "initial commit"],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )

    def tearDown(self) -> None:
        """Limpia el directorio temporal."""
        self.temp_dir.cleanup()

    def test_untracked_new_plugin_with_own_readme_fails_if_missing_in_root_readme(self) -> None:
        """Reproduce el bug: crear un nuevo plugin con su propio README.md sin actualizar el README raíz debe fallar (exit code 1)."""
        plugin_dir = self.repo_path / "hermes-auto-learner"
        scripts_dir = plugin_dir / "skills" / "hermes-auto-learner" / "scripts"
        scripts_dir.mkdir(parents=True)

        (plugin_dir / "README.md").write_text("# Hermes Auto-Learner\n", encoding="utf-8")
        (plugin_dir / "plugin.json").write_text('{"name": "hermes-auto-learner"}\n', encoding="utf-8")
        (scripts_dir / "validate_skill.py").write_text("def validate() -> bool:\n    return True\n", encoding="utf-8")

        exit_code = doc_guard.check_docs(self.repo_path)
        self.assertEqual(
            exit_code,
            1,
            "check_docs debe retornar 1 cuando un nuevo plugin/módulo de primer nivel no está en el README.md raíz.",
        )

    def test_staged_new_plugin_with_own_readme_fails_if_missing_in_root_readme(self) -> None:
        """Reproduce el falso positivo con archivos en stage: un sub-README no reemplaza al README raíz."""
        plugin_dir = self.repo_path / "security-auditor"
        scripts_dir = plugin_dir / "skills" / "security-auditor" / "scripts"
        scripts_dir.mkdir(parents=True)

        (plugin_dir / "README.md").write_text("# Security Auditor\n", encoding="utf-8")
        (plugin_dir / "plugin.json").write_text('{"name": "security-auditor"}\n', encoding="utf-8")
        (scripts_dir / "run_audit.py").write_text("def audit() -> bool:\n    return True\n", encoding="utf-8")

        subprocess.run(
            ["git", "add", "security-auditor"],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )

        exit_code = doc_guard.check_docs(self.repo_path)
        self.assertEqual(
            exit_code,
            1,
            "check_docs debe retornar 1 cuando un plugin en stage tiene su propio README pero falta en el README raíz.",
        )

    def test_new_plugin_passes_once_documented_in_root_readme(self) -> None:
        """Verifica que al agregar el nuevo plugin al README.md raíz, check_docs retorna 0."""
        plugin_dir = self.repo_path / "hermes-auto-learner"
        scripts_dir = plugin_dir / "skills" / "hermes-auto-learner" / "scripts"
        scripts_dir.mkdir(parents=True)

        (plugin_dir / "README.md").write_text("# Hermes Auto-Learner\n", encoding="utf-8")
        (plugin_dir / "plugin.json").write_text('{"name": "hermes-auto-learner"}\n', encoding="utf-8")
        (scripts_dir / "validate_skill.py").write_text("def validate() -> bool:\n    return True\n", encoding="utf-8")

        root_readme = self.repo_path / "README.md"
        root_readme.write_text(
            "# Plugins Suite\n\n| Plugin | Desc |\n|---|---|\n| `doc-guardian` | Docs |\n| `hermes-auto-learner` | Auto learning |\n",
            encoding="utf-8",
        )

        exit_code = doc_guard.check_docs(self.repo_path)
        self.assertEqual(
            exit_code,
            0,
            "check_docs debe retornar 0 cuando el nuevo plugin fue documentado en el README.md raíz.",
        )

    def test_committed_plugin_missing_from_root_readme_index_is_detected(self) -> None:
        """Verifica que si el README raíz indexa plugins pero un plugin ya commiteado falta en él, check_docs lo detecta."""
        existing_plugin = self.repo_path / "doc-guardian"
        existing_plugin.mkdir()
        (existing_plugin / "plugin.json").write_text('{"name": "doc-guardian"}\n', encoding="utf-8")

        forgotten_plugin = self.repo_path / "graphify"
        forgotten_plugin.mkdir()
        (forgotten_plugin / "plugin.json").write_text('{"name": "graphify"}\n', encoding="utf-8")
        (forgotten_plugin / "README.md").write_text("# Graphify\n", encoding="utf-8")

        subprocess.run(
            ["git", "add", "."],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "add plugins without updating root README"],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )

        exit_code = doc_guard.check_docs(self.repo_path)
        self.assertEqual(
            exit_code,
            1,
            "check_docs debe detectar módulos/plugins de primer nivel ya commiteados que fueron omitidos del índice del README raíz.",
        )

    def test_gitignored_top_level_plugin_is_ignored(self) -> None:
        """Verifica que los directorios de primer nivel ignorados en .gitignore no exijan estar en el README raíz."""
        existing_plugin = self.repo_path / "doc-guardian"
        existing_plugin.mkdir()
        (existing_plugin / "plugin.json").write_text('{"name": "doc-guardian"}\n', encoding="utf-8")

        ignored_plugin = self.repo_path / "firebase"
        ignored_plugin.mkdir()
        (ignored_plugin / "plugin.json").write_text('{"name": "firebase"}\n', encoding="utf-8")

        gitignore = self.repo_path / ".gitignore"
        gitignore.write_text("firebase/\n", encoding="utf-8")

        subprocess.run(
            ["git", "add", "."],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "add doc-guardian and ignore firebase"],
            cwd=self.repo_path,
            capture_output=True,
            check=True,
        )

        exit_code = doc_guard.check_docs(self.repo_path)
        self.assertEqual(
            exit_code,
            0,
            "check_docs debe ignorar carpetas de primer nivel excluidas mediante .gitignore.",
        )


if __name__ == "__main__":
    unittest.main()
