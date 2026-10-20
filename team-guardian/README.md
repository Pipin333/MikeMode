# Team-Guardian

Disciplina de equipo para agentes de IA, inspirada en la organizacion stgo-tomLAB: Conventional Commits, ramas con prefijo y una puerta que impide debilitar tests sin que un humano lo apruebe.

## Requisitos

- Python 3.13 (solo libreria estandar).
- Git (para el hook `commit-msg`).
- `pytest` solo para ejecutar los tests del propio plugin.

## Uso

```bash
# Instalación del hook commit-msg:
python skills/team-guardian/scripts/team_guard.py install-hook --repo-root <repo>

# Validación aislada:
python skills/team-guardian/scripts/team_guard.py check-branch feat/mi-cambio
python skills/team-guardian/scripts/team_guard.py check-commit-msg <archivo>

# Ejecución del Gate de calidad con perfiles:
python skills/team-guardian/scripts/team_guard.py gate --profile prototype
python skills/team-guardian/scripts/team_guard.py gate --profile product

# Flujo de aprobación humana de cambios en tests:
python skills/team-guardian/scripts/team_guard.py gate-test-changes --diff-file d.diff --justification j.md --approval a.json
python skills/team-guardian/scripts/team_guard.py approve-test-changes --diff-file d.diff --justification j.md --approval a.json --approver <nombre>
```

Detalle del flujo en [SKILL.md](skills/team-guardian/SKILL.md).

## Tests

```bash
python -m pytest tests -q
```

Los tests de `test_team_guard.py` y `test_gate.py` los escribieron subagentes independientes a partir de la especificación técnica, sin ver la implementación.

## Estructura

```
team-guardian/
├── plugin.json
├── README.md
├── rules/AGENTS.md
├── tests/
│   ├── test_team_guard.py
│   ├── test_hook_interpreter.py
│   └── test_gate.py
└── skills/team-guardian/
    ├── SKILL.md
    ├── references/justificacion_de_tests.md
    └── scripts/team_guard.py
```

## Estado

- `check-*`, `install-hook` y el gate de justificación de tests completados.
- `gate --profile prototype|product` completado con persistencia de evidencia en `.scratch/gate-evidence/`.
- 164 pruebas automatizadas pasando al 100%.
