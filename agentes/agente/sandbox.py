"""Prepara una copia desechable del repositorio para cada ejecución (el agente nunca toca el original).

La copia se extrae con `git archive` del commit BASE: el estado del repositorio tras E3, con el ISSUE-01
corregido y los ISSUE-02 e ISSUE-03 en rojo. Así las trayectorias grabadas de E4–E6 se reproducen igual
aunque src/ haya cambiado después, y no hace falta versionar una copia de tests/ (sus nombres repetidos
rompían la colección de pytest en la integración continua).

De ese commit se toman agentes/trabajo/ (src, tests, issues) y fitness/, prompts/ y seguridad/: sin estas
tres carpetas, 2 módulos de prueba fallan al importarse, pytest se interrumpe y el agente no ve el
resultado de las pruebas de los issues (es lo que ocurrió en la traza de E2).
"""
import io, shutil, subprocess, tarfile, pathlib

AGENTES = pathlib.Path(__file__).resolve().parents[1]
REPO = AGENTES.parent
BASE = "fa664fd"                                      # commit "E3: máquina de estados y contrato"
TRABAJO = "agentes/trabajo/"
APOYO = ("fitness/", "prompts/", "seguridad/")        # solo se leen; las pruebas los importan


def _extraer(destino: pathlib.Path) -> None:
    tar = subprocess.run(["git", "archive", "--format=tar", BASE, TRABAJO, *APOYO],
                         cwd=REPO, capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        for m in t.getmembers():
            nombre = m.name[len(TRABAJO):] if m.name.startswith(TRABAJO) else m.name
            if not nombre or ".." in pathlib.PurePosixPath(nombre).parts:
                continue
            ruta = destino / nombre
            if m.isdir():
                ruta.mkdir(parents=True, exist_ok=True)
            elif m.isfile():
                ruta.parent.mkdir(parents=True, exist_ok=True)
                ruta.write_bytes(t.extractfile(m).read())


def preparar(nombre: str) -> tuple[pathlib.Path, pathlib.Path]:
    """Crea agentes/ejecuciones/<nombre>/{trabajo,original} y devuelve ambas rutas."""
    base = AGENTES / "ejecuciones" / nombre
    shutil.rmtree(base, ignore_errors=True)
    for destino in ("original", "trabajo"):
        _extraer(base / destino)
    return base / "trabajo", base / "original"
