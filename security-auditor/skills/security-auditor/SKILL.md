---
name: security-auditor
description: Auditoría de seguridad estática formal y detección determinista de vulnerabilidades (CVEs, OWASP Top 10, Secrets) basada en Semgrep y el marco metodológico de Trail of Bits. Úsalo antes de hacer deploys, al auditar código sensible (autenticación, parsers, DOM XSS, SQL queries) o para cazar secretos antes de commitear.
---

# 🛡️ Security Auditor Skill (Semgrep & Trail of Bits Framework)

Security Auditor dota al agente de un **escudo inmunológico determinista** impulsado por el motor de análisis estático **Semgrep** y las metodologías de auditoría de **Trail of Bits**. Cierra la brecha estocástica de los LLMs analizando árboles sintácticos (AST/CST) con reglas formales en tiempo lineal $O(N)$ sin falsos positivos alucinados.

---

## 🎯 Cuándo Usar Esta Habilidad
- **Auditoría Pre-Deploy / Pre-PR**: Escaneo preventivo de seguridad antes de fusionar ramas críticas o desplegar a producción.
- **Detección de Vectores OWASP Top 10**:
  - Inyecciones (SQLi, Command Injection, NoSQL Injection).
  - **DOM XSS y Reflected XSS** (ej. manipulación insegura de `innerHTML` o `location.hash`).
  - Server-Side Request Forgery (SSRF) y Cross-Site Request Forgery (CSRF).
  - Deserialización insegura (`pickle`, `yaml.load` sin SafeLoader).
- **Caza de Secretos (Secrets Leak)**: Detección de claves de API (`AIza...`, `sk-...`), tokens JWT, certificados y contraseñas quemadas en código fuente.
- **Auditoría de Dependencias y Docker**: Escaneo de `Dockerfile` en busca de usuarios root o malas prácticas de containerización.

---

## 🔒 Salvaguardas Obligatorias (Directivas de Balthasar-2)

1. **Privacidad Radical (`--metrics=off`)**:
   - **OBLIGATORIO en cada ejecución**: Jamás omitir la bandera `--metrics=off`. Garantiza que ningún fragmento de código, hash o metadato sea enviado a servidores externos de telemetría.
2. **Límite Férreo de Recursos**:
   - Limitar memoria a 2 GB (`--max-memory=2048`).
   - Timeout de escaneo de 60 segundos por regla para prevenir ataques de *Catastrophic Backtracking* (ReDoS).
3. **Exclusiones Estrictas de Escaneo**:
   - Excluir siempre carpetas pesadas o dependencias externas:
     `--exclude="node_modules" --exclude=".venv" --exclude="venv" --exclude=".git" --exclude="dist" --exclude="build"`
4. **On-Demand**: Ejecución episódica a petición del usuario o durante revisiones de seguridad, jamás como proceso persistente.

---

## 🚀 Flujo de Ejecución

### 1. Invocación Asistida mediante Runner Seguro
El plugin incluye un runner en Python que aplica automáticamente `--metrics=off`, límites de memoria y exclusiones de carpetas:

```powershell
python "C:\Users\Petiso\.gemini\config\plugins\security-auditor\skills\security-auditor\scripts\run_audit.py" --target "<ruta_del_proyecto>"
```

### 2. Comandos CLI Directos

* **Escaneo de Seguridad Estándar (Alto Impacto y Confianza)**:
  ```powershell
  & "$HOME\.local\bin\semgrep.exe" scan --config="p/default" --metrics=off "<ruta_del_proyecto>"
  ```

* **Auditoría Exhaustiva (Trail of Bits + Security Audit)**:
  ```powershell
  & "$HOME\.local\bin\semgrep.exe" scan --config="p/security-audit" --config="p/trailofbits" --metrics=off "<ruta_del_proyecto>"
  ```

* **Caza de Secretos (API Keys, Tokens, Credenciales)**:
  ```powershell
  & "$HOME\.local\bin\semgrep.exe" scan --config="p/secrets" --metrics=off "<ruta_del_proyecto>"
  ```

* **Exportar a Formato Estándar SARIF / JSON**:
  ```powershell
  & "$HOME\.local\bin\semgrep.exe" scan --config="p/default" --metrics=off --sarif --output="reporte_seguridad.sarif" "<ruta_del_proyecto>"
  ```

---

## 🩺 Protocolo de Remediación
Cuando el escáner reporte un hallazgo:
1. **Identifica el origen**: Archivo exacto, número de línea y CWE asociado.
2. **Explica el vector de ataque**: Detalla cómo un atacante podría explotar la vulnerabilidad.
3. **Aplica el parche defensivo**: Propón o aplica inmediatamente la remediación idiomática (ej: reemplazar `innerHTML` por `textContent`, o usar parámetros ligados en SQL).
