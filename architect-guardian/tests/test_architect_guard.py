"""Tests unitarios y de regresión para architect_guard.py (handover, pickup, babysit y report)."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS_DIR = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "architect-guardian"
    / "scripts"
)
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import architect_guard


class TestArchitectGuardWorkflows(unittest.TestCase):
    """Verifica los flujos deterministas de handover, pickup, babysit y report en architect_guard."""

    def setUp(self) -> None:
        """Crea un repositorio Git temporal para pruebas."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_path = Path(self.temp_dir.name)
        subprocess.run(
            ["git", "init", "-b", "main"],
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
        (self.repo_path / "README.md").write_text("# Proyecto Test\n", encoding="utf-8")
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

    def test_handover_and_pickup_lifecycle(self) -> None:
        """Verifica que generate_handover cree .scratch/HANDOVER.md y run_pickup lo valide."""
        exit_handover = architect_guard.generate_handover(
            self.repo_path,
            summary="Implementado módulo de autenticación JWT; falta endpoint de refresh.",
            next_step="Crear POST /auth/refresh con test en rojo.",
            dead_ends="No usar cookies sin SameSite=Strict por restricción CORS.",
        )
        self.assertEqual(exit_handover, 0)

        handover_file = self.repo_path / ".scratch" / "HANDOVER.md"
        self.assertTrue(handover_file.is_file(), "Debe existir .scratch/HANDOVER.md tras generate_handover.")
        content = handover_file.read_text(encoding="utf-8")
        self.assertIn("Implementado módulo de autenticación JWT", content)
        self.assertIn("Crear POST /auth/refresh", content)
        self.assertIn("No usar cookies sin SameSite=Strict", content)

        exit_pickup = architect_guard.run_pickup(self.repo_path)
        self.assertEqual(exit_pickup, 0)

    def test_babysit_detects_merge_conflict_markers(self) -> None:
        """Verifica que run_babysit_check detecte marcadores de conflicto de merge sin resolver."""
        broken_file = self.repo_path / "app.py"
        broken_file.write_text(
            "def main() -> None:\n<<<<<<< HEAD\n    return 1\n=======\n    return 2\n>>>>>>> feature\n",
            encoding="utf-8",
        )
        exit_code = architect_guard.run_babysit_check(self.repo_path)
        self.assertEqual(
            exit_code,
            1,
            "run_babysit_check debe retornar 1 cuando existen marcadores de conflicto en el árbol.",
        )

    def test_babysit_passes_on_clean_tree(self) -> None:
        """Verifica que run_babysit_check retorne 0 cuando el árbol de trabajo está limpio y sin conflictos."""
        exit_code = architect_guard.run_babysit_check(self.repo_path)
        self.assertEqual(exit_code, 0)

    def test_consolidated_report_executes_all_guardians(self) -> None:
        """Verifica que run_consolidated_report ejecute la suite de 5 guardianes sin errores de CLI."""
        exit_code = architect_guard.run_consolidated_report(self.repo_path)
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
