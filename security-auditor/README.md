# 🛡️ Security Auditor Plugin for Antigravity

Plugin para auditorías estáticas formales de seguridad y detección determinista de vulnerabilidades (CVEs, OWASP Top 10, fugas de secretos) utilizando el motor **Semgrep** y los patrones metodológicos de **Trail of Bits**.

---

## 🌟 Características Principales
* **Análisis AST Determinista**: Evalúa Árboles de Sintaxis Concreta con complejidad $O(N)$ sin las alucinaciones probabilísticas típicas de los LLMs.
* **Cobertura Multi-Lenguaje**: Python, JavaScript, TypeScript, Go, Java, Rust, C/C++, Dockerfiles, Terraform, etc.
* **Perfiles de Escaneo**:
  * `default`: Vulnerabilidades de alto impacto y alta confianza (`p/default`).
  * `audit`: Auditoría profunda con reglas de Trail of Bits (`p/security-audit`, `p/trailofbits`).
  * `secrets`: Caza de claves de API quemadas y credenciales (`p/secrets`).
  * `all`: Cobertura exhaustiva consolidada.
* **Salvaguardas de Balthasar-2**:
  * **Privacidad 100% garantizada**: `--metrics=off` activo incondicionalmente en cada escaneo para impedir fuga de telemetría de código.
  * **Límite de memoria**: Tope de 2 GB de RAM para proteger la máquina anfitriona.
  * **Exclusión automática**: Omite dependencias pesadas (`node_modules`, `.venv`, `.git`).

---

## 🛠️ Instalación y Requisitos
Utiliza el binario oficial de Semgrep instalado a través de `uv` o `pip`:

```bash
python -m uv tool install semgrep
# O alternativamente:
pip install semgrep
```

El ejecutable queda disponible en `~/.local/bin/semgrep.exe`.

---

## 📖 Uso

### Vía Runner Seguro en Python (Recomendado)
```bash
# Escaneo de seguridad estándar
python skills/security-auditor/scripts/run_audit.py --target "C:\ruta\a\tu\proyecto"

# Auditoría exhaustiva con reglas de Trail of Bits
python skills/security-auditor/scripts/run_audit.py --target "C:\ruta\a\tu\proyecto" --mode audit

# Caza de secretos y API keys
python skills/security-auditor/scripts/run_audit.py --target "C:\ruta\a\tu\proyecto" --mode secrets
```

### Vía CLI Directa
```powershell
& "$HOME\.local\bin\semgrep.exe" scan --config="p/default" --metrics=off "C:\ruta\a\tu\proyecto"
```
