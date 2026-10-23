"""Ejecuta todos los chequeos de calidad del proyecto con un solo comando:

    python scripts/check.py

Requiere:  pip install -r requirements-dev.txt
Devuelve código de salida distinto de 0 si algún chequeo falla (útil para CI).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

CHECKS = [
    ("Aislamiento (import-linter)",
     [PY, "-c", "from importlinter.cli import lint_imports_command; lint_imports_command()"]),
    ("Código inseguro (Bandit)", [PY, "-m", "bandit", "-r", "app", "run.py"]),
    ("Código sin usar (ruff)", [PY, "-m", "ruff", "check", "."]),
    ("Código muerto (vulture)", [PY, "-m", "vulture"]),
    ("Duplicación (pylint R0801)",
        [PY, "-m", "pylint", "--disable=all", "--enable=duplicate-code", "--fail-under=8.1", "app"]),
    ("Pruebas (pytest)", [PY, "-m", "pytest", "-q"]),
]


def main() -> int:
    results = []
    for name, cmd in CHECKS:
        print(f"\n=== {name} ===", flush=True)
        ok = subprocess.run(cmd, cwd=ROOT, check=False).returncode == 0
        results.append((name, ok))

    print("\n=== Resumen ===")
    for name, ok in results:
        print(f"  {'OK   ' if ok else 'FALLA'}  {name}")
    return 0 if all(ok for _, ok in results) else 1


if __name__ == "__main__":
    sys.exit(main())
