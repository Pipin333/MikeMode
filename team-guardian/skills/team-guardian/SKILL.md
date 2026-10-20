---
name: team-guardian
description: >-
  Aplica disciplina de equipo a agentes: valida ramas y commits (Conventional Commits), instala un hook commit-msg y bloquea el cierre de una tarea cuando el agente borra o altera aserciones de tests hasta que el usuario apruebe una justificacion detallada. Usalo al commitear, abrir PRs o tocar tests existentes.
---

# Team-Guardian

Herramienta unica: `scripts/team_guard.py` (Python 3.13, solo libreria estandar).

## Comandos

```bash
# Validaciones puntuales
python <ruta_plugin>/skills/team-guardian/scripts/team_guard.py check-branch feat/login-form
python <ruta_plugin>/skills/team-guardian/scripts/team_guard.py check-commit-msg .git/COMMIT_EDITMSG
python <ruta_plugin>/skills/team-guardian/scripts/team_guard.py install-hook --repo-root .

# Gate de calidad con perfiles ('prototype' o 'product')
python <ruta_plugin>/skills/team-guardian/scripts/team_guard.py gate --profile prototype
python <ruta_plugin>/skills/team-guardian/scripts/team_guard.py gate --profile product

# Flujo de revisión de tests sensibles
git diff > .scratch/tests.diff
python <ruta_plugin>/skills/team-guardian/scripts/team_guard.py gate-test-changes \
  --diff-file .scratch/tests.diff \
  --justification .scratch/justificacion-tests.md \
  --approval .scratch/aprobacion-tests.json
```

Codigos de salida: `0` correcto, `1` incumplimiento o bloqueo, `2` uso o archivo invalido.

## Flujo del gate de tests

1. `gate-test-changes` detecta en archivos de test: aserciones eliminadas o modificadas, tests borrados y `skip` agregados.
2. Sin cambios sensibles responde `pass`.
3. Con cambios, el agente escribe la justificacion (ver [justificacion_de_tests.md](./references/justificacion_de_tests.md)) y la explica al usuario.
4. Solo el usuario ejecuta `approve-test-changes ... --approver <nombre>`. La aprobacion queda atada al hash del diff.
5. Estados: `pass`, `blocked_missing_justification`, `blocked_pending_approval`, `approved`.

## Limite conocido

Un agente con acceso a la terminal podria ejecutar el comando de aprobacion. La defensa real es que el usuario revise la justificacion y que la fusion exija una revision humana del PR.
