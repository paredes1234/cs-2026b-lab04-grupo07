"""Prepara una copia desechable del repositorio para cada ejecución (el agente nunca toca el original).

La copia parte de agentes/trabajo/ (estado después de E2) y agrega fitness/, prompts/ y seguridad/ de la raíz:
sin ellas, 2 módulos de prueba fallan al importarse, pytest se interrumpe y el agente no ve el resultado
de las pruebas de los issues (es lo que ocurrió en la traza de E2).
"""
import shutil, pathlib

AGENTES = pathlib.Path(__file__).resolve().parents[1]
REPO = AGENTES.parent
APOYO = ("fitness", "prompts", "seguridad")          # solo se leen; las pruebas los importan
IGNORAR = shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc")


def preparar(nombre: str) -> tuple[pathlib.Path, pathlib.Path]:
    """Crea agentes/ejecuciones/<nombre>/{trabajo,original} y devuelve ambas rutas."""
    base = AGENTES / "ejecuciones" / nombre
    shutil.rmtree(base, ignore_errors=True)
    for destino in ("original", "trabajo"):
        shutil.copytree(AGENTES / "trabajo", base / destino, ignore=IGNORAR)
        for carpeta in APOYO:
            shutil.copytree(REPO / carpeta, base / destino / carpeta, ignore=IGNORAR)
    return base / "trabajo", base / "original"
