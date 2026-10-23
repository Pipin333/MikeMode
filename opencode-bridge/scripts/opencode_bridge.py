"""Puente local entre Google Antigravity y el daemon de OpenCode.

Permite delegar tareas analíticas, refactorizaciones y contrastes de código
hacia modelos gratuitos locales o remotos (DeepSeek V4.1, GLM-5.3, Nemotron)
orquestados por el servidor en segundo plano de OpenCode.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional

OPENCODE_CLI_DEFAULT_PATH = os.path.expandvars(
    r"%APPDATA%\ai.opencode.desktop\cli\2.1.4-x64\opencode-cli.exe"
)

SENSITIVE_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}", re.IGNORECASE),
    re.compile(r"gsk_[a-zA-Z0-9_-]{20,}", re.IGNORECASE),
    re.compile(r"AIzaSy[a-zA-Z0-9_-]{30,}", re.IGNORECASE),
    re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[^\s'\"]+", re.IGNORECASE),
]


def sanitize_prompt(text: str) -> str:
    """Remueve o redacta posibles secretos del prompt antes de delegar.

    Args:
        text: Cadena de texto que contiene el prompt o fragmento de código.

    Returns:
        Cadena sanitizada con los patrones sensibles reemplazados por [REDACTED].
    """
    sanitized = text
    for pattern in SENSITIVE_PATTERNS:
        sanitized = pattern.sub(r"[REDACTED_CREDENTIAL]", sanitized)
    return sanitized


class OpenCodeBridgeError(Exception):
    """Excepción base para errores de comunicación con OpenCode."""


class OpenCodeBridge:
    """Cliente para la API local de OpenCode mediante su CLI oficial."""

    def __init__(self, cli_path: Optional[str] = None) -> None:
        """Inicializa el conector con la ruta al binario opencode-cli.

        Args:
            cli_path: Ruta alternativa a opencode-cli.exe. Si es None,
                se busca en la ruta estándar de AppData.
        """
        self.cli_path = cli_path or OPENCODE_CLI_DEFAULT_PATH
        if not os.path.exists(self.cli_path):
            raise OpenCodeBridgeError(
                f"No se encontró el ejecutable de OpenCode en: {self.cli_path}. "
                "Verifica que OpenCode Desktop esté instalado."
            )

    def _execute_api(self, method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ejecuta una llamada al comando 'opencode api' vía subprocess.

        Args:
            method: Método HTTP (GET, POST, DELETE, etc.).
            path: Ruta relativa del endpoint (ej. '/api/info').
            body: Diccionario JSON opcional para el cuerpo de la petición.

        Returns:
            Respuesta decodificada en formato diccionario.

        Raises:
            OpenCodeBridgeError: Si el subproceso falla o devuelve código no cero.
        """
        cmd = [self.cli_path, "api", method, path]
        if body is not None:
            cmd.extend(["-d", json.dumps(body)])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise OpenCodeBridgeError(f"Timeout al comunicarse con OpenCode ({method} {path})") from exc
        except Exception as exc:
            raise OpenCodeBridgeError(f"Error al ejecutar opencode-cli: {exc}") from exc

        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip()
            raise OpenCodeBridgeError(
                f"Error en OpenCode API [{result.returncode}]: {error_msg}"
            )

        output = result.stdout.strip()
        if not output:
            return {}

        try:
            return json.loads(output)
        except json.JSONDecodeError as exc:
            raise OpenCodeBridgeError(f"Respuesta JSON inválida de OpenCode: {output[:200]}") from exc

    def check_status(self) -> Dict[str, Any]:
        """Verifica la conectividad y estado del daemon de OpenCode.

        Returns:
            Diccionario con versión, PID y URLs activas del servidor.
        """
        return self._execute_api("GET", "/api/info")

    def list_available_models(self) -> List[str]:
        """Obtiene el listado de modelos actualmente registrados en OpenCode.

        Returns:
            Lista de identificadores de modelos (ej. 'opencode/deepseek-v4.1-flash-free').
        """
        res = subprocess.run(
            [self.cli_path, "models"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
            check=False,
        )
        if res.returncode != 0:
            raise OpenCodeBridgeError(f"Error al listar modelos: {res.stderr}")
        return [line.strip() for line in res.stdout.strip().splitlines() if line.strip()]

    def ask(
        self,
        prompt: str,
        model_id: str = "deepseek-v4.1-flash-free",
        provider_id: str = "opencode",
        agent: str = "general",
        title: str = "Antigravity Delegation",
        cleanup: bool = True,
    ) -> Dict[str, Any]:
        """Crea una sesión efímera, envía el prompt sanitizado y retorna la respuesta.

        Args:
            prompt: Instrucción o código a consultar.
            model_id: Identificador del modelo (ej. 'deepseek-v4.1-flash-free', 'glm-5.3-flash-free').
            provider_id: Proveedor en OpenCode (normalmente 'opencode' u 'ollama').
            agent: Tipo de agente en OpenCode ('general' o 'build').
            title: Título legible para la sesión.
            cleanup: Si es True, elimina la sesión al terminar para evitar residuos.

        Returns:
            Diccionario con 'text' (respuesta), 'reasoning' (pensamiento si existe) y 'model'.
        """
        clean_prompt = sanitize_prompt(prompt)

        # 1. Crear sesión
        session_payload = {
            "title": title,
            "agent": agent,
            "model": {
                "id": model_id,
                "providerID": provider_id,
            },
        }
        session_res = self._execute_api("POST", "/api/session", session_payload)
        session_id = session_res.get("data", {}).get("id")
        if not session_id:
            raise OpenCodeBridgeError(f"No se pudo crear la sesión en OpenCode: {session_res}")

        try:
            # 2. Enviar prompt
            prompt_payload = {"text": clean_prompt}
            self._execute_api("POST", f"/api/session/{session_id}/prompt", prompt_payload)

            # 3. Esperar finalización del bucle de inferencia
            self._execute_api("POST", f"/api/experimental/session/{session_id}/wait")

            # 4. Recuperar mensajes
            messages_res = self._execute_api("GET", f"/api/session/{session_id}/message")
            messages = messages_res.get("data", [])

            response_texts: List[str] = []
            reasoning_texts: List[str] = []

            for msg in messages:
                if msg.get("type") == "assistant":
                    for part in msg.get("content", []):
                        part_type = part.get("type")
                        if part_type == "text" and part.get("text"):
                            response_texts.append(part["text"])
                        elif part_type == "reasoning" and part.get("text"):
                            reasoning_texts.append(part["text"])

            full_text = "\n\n".join(response_texts).strip()
            full_reasoning = "\n\n".join(reasoning_texts).strip()

            return {
                "session_id": session_id,
                "model": f"{provider_id}/{model_id}",
                "text": full_text,
                "reasoning": full_reasoning,
            }
        finally:
            if cleanup:
                try:
                    self._execute_api("DELETE", f"/api/session/{session_id}")
                except Exception:
                    pass


def main() -> None:
    """Punto de entrada de línea de comandos para la herramienta."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Puente de delegación entre Antigravity y OpenCode"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando: status
    subparsers.add_parser("status", help="Comprueba el estado del daemon de OpenCode")

    # Subcomando: models
    subparsers.add_parser("models", help="Lista los modelos activos en OpenCode")

    # Subcomando: ask
    ask_parser = subparsers.add_parser("ask", help="Envía una consulta a un modelo delegado")
    ask_parser.add_argument("--prompt", "-p", required=True, help="Texto o instrucción a procesar")
    ask_parser.add_argument(
        "--model",
        "-m",
        default="deepseek-v4.1-flash-free",
        help="ID del modelo (default: deepseek-v4.1-flash-free)",
    )
    ask_parser.add_argument(
        "--provider",
        default="opencode",
        help="Proveedor en OpenCode (default: opencode)",
    )
    ask_parser.add_argument(
        "--agent",
        default="general",
        choices=["general", "build"],
        help="Tipo de agente en OpenCode",
    )
    ask_parser.add_argument(
        "--keep-session",
        action="store_true",
        help="No eliminar la sesión al terminar",
    )
    ask_parser.add_argument(
        "--json",
        action="store_true",
        help="Emitir la salida en formato JSON estructurado",
    )

    args = parser.parse_args()
    bridge = OpenCodeBridge()

    try:
        if args.command == "status":
            info = bridge.check_status()
            print(f"🟢 OpenCode Daemon activo: v{info.get('version')} (PID {info.get('pid')})")
            print(f"URL: {info.get('urls', ['http://127.0.0.1:28894'])[0]}")

        elif args.command == "models":
            models = bridge.list_available_models()
            print(f"Modelos disponibles en OpenCode ({len(models)}):")
            for m in models:
                print(f"  - {m}")

        elif args.command == "ask":
            res = bridge.ask(
                prompt=args.prompt,
                model_id=args.model,
                provider_id=args.provider,
                agent=args.agent,
                cleanup=not args.keep_session,
            )
            if args.json:
                print(json.dumps(res, indent=2, ensure_ascii=False))
            else:
                if res.get("reasoning"):
                    print(f"--- [PENSAMIENTO / REASONING ({res['model']})] ---")
                    print(res["reasoning"])
                    print("-" * 50)
                print(res["text"])

    except OpenCodeBridgeError as err:
        print(f"❌ Error en OpenCodeBridge: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
