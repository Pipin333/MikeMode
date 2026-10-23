"""Tests unitarios y de regresión para opencode_bridge.py."""

from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import opencode_bridge
from opencode_bridge import (
    OpenCodeBridge,
    OpenCodeBridgeError,
    sanitize_prompt,
)


class TestOpenCodeBridgeSanitization(unittest.TestCase):
    """Verifica que el scrubber de secretos sanitice correctamente el prompt."""

    def test_sanitize_api_keys(self) -> None:
        """Comprueba que tokens y patrones de llaves API se reemplacen por [REDACTED_CREDENTIAL]."""
        raw = "Usa sk-abcdef1234567890abcdef123456 para autenticarte y password: secret123"
        sanitized = sanitize_prompt(raw)
        self.assertNotIn("sk-abcdef1234567890abcdef123456", sanitized)
        self.assertNotIn("secret123", sanitized)
        self.assertIn("[REDACTED_CREDENTIAL]", sanitized)

    def test_clean_prompt_untouched(self) -> None:
        """Verifica que prompts regulares sin secretos permanezcan intactos."""
        raw = "Por favor explica el algoritmo Quicksort en Python."
        sanitized = sanitize_prompt(raw)
        self.assertEqual(raw, sanitized)


class TestOpenCodeBridgeExecution(unittest.TestCase):
    """Verifica la lógica de orquestación de sesiones y llamadas a la API de OpenCode."""

    @patch("opencode_bridge.os.path.exists", return_value=True)
    def test_ask_flow_with_cleanup(self, mock_exists: MagicMock) -> None:
        """Prueba el ciclo de vida de una consulta: create -> prompt -> wait -> messages -> delete."""
        bridge = OpenCodeBridge(cli_path="C:\\dummy\\opencode-cli.exe")

        def fake_api(method: str, path: str, body: dict = None) -> dict:
            if method == "POST" and path == "/api/session":
                return {"data": {"id": "session-123"}}
            if method == "POST" and path == "/api/session/session-123/prompt":
                return {"status": "ok"}
            if method == "POST" and path == "/api/experimental/session/session-123/wait":
                return {"status": "completed"}
            if method == "GET" and path == "/api/session/session-123/message":
                return {
                    "data": [
                        {
                            "type": "assistant",
                            "content": [
                                {"type": "reasoning", "text": "Pensamiento de prueba"},
                                {"type": "text", "text": "Respuesta final generada"},
                            ],
                        }
                    ]
                }
            if method == "DELETE" and path == "/api/session/session-123":
                return {"status": "deleted"}
            return {}

        bridge._execute_api = MagicMock(side_effect=fake_api)

        result = bridge.ask(
            prompt="Refactoriza esta función",
            model_id="deepseek-v4.1-flash-free",
            cleanup=True,
        )

        self.assertEqual(result["session_id"], "session-123")
        self.assertEqual(result["text"], "Respuesta final generada")
        self.assertEqual(result["reasoning"], "Pensamiento de prueba")
        self.assertEqual(result["model"], "opencode/deepseek-v4.1-flash-free")

        # Verificar que se llamó a DELETE para limpiar
        bridge._execute_api.assert_any_call("DELETE", "/api/session/session-123")


if __name__ == "__main__":
    unittest.main()
