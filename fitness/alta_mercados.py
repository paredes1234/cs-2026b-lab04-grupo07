"""E4 Lab 08, iteración 3: experimento de alta de un mercado (QA08-07).

Mide, sobre copias temporales, cuántos módulos existentes y cuántas líneas hay
que cambiar para agregar un cuarto mercado ("MERCADO_PRUEBA"):

  A. condicionales: if/elif por mercado en catálogo, pedidos y entrega
     (línea base sintética en fitness/prototipo_condicionales/).
  B. configuración: reglas en src/mercados/ (ADR-008); el mercado nuevo es
     una entrada en mercados.json.

Después de cada cambio se importa el código modificado y se comprueba que el
mercado nuevo funciona. No se modifica ningún archivo del repositorio.

Reproducir desde la raíz del repositorio:
    python -m fitness.alta_mercados
"""

from __future__ import annotations

import ast
import difflib
import importlib.util
import json
import shutil
import tempfile
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE_CONDICIONALES = RAIZ / "fitness" / "prototipo_condicionales"
MODULO_MERCADOS = RAIZ / "src" / "mercados"
MERCADOS = ("SAN_CAMILO", "ALTIPLANO", "RIO_SECO")
NUEVO = "MERCADO_PRUEBA"


def modulos_con_literales_de_mercado(carpeta: Path, mercados=MERCADOS) -> list[str]:
    """Módulos .py que contienen un identificador de mercado como literal."""
    encontrados = []
    for archivo in sorted(carpeta.rglob("*.py")):
        arbol = ast.parse(archivo.read_text(encoding="utf-8"))
        if any(isinstance(n, ast.Constant) and n.value in mercados for n in ast.walk(arbol)):
            encontrados.append(archivo.relative_to(carpeta).as_posix())
    return encontrados


def _lineas_cambiadas(antes: str, despues: str) -> int:
    return sum(1 for l in difflib.unified_diff(antes.splitlines(), despues.splitlines(), lineterm="")
               if l[:1] in "+-" and l[:3] not in ("+++", "---"))


def _importar(ruta: Path):
    spec = importlib.util.spec_from_file_location(ruta.stem, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _diferencias(original: Path, copia: Path) -> dict:
    archivos, lineas = [], 0
    for f in sorted(copia.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            antes = (original / f.relative_to(copia)).read_text(encoding="utf-8")
            n = _lineas_cambiadas(antes, f.read_text(encoding="utf-8"))
            if n:
                archivos.append(f.relative_to(copia).as_posix())
                lineas += n
    return {"archivos": archivos, "lineas": lineas}


def alta_con_condicionales() -> dict:
    """Agrega una rama elif por función con cadena de mercados, como lo haría el equipo."""
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "condicionales"
        shutil.copytree(BASE_CONDICIONALES, copia, ignore=shutil.ignore_patterns("__pycache__"))
        rama = {"catalogo.py": "return (7, 13)", "pedidos.py": "return 5", "entrega.py": "return 4"}
        for nombre in modulos_con_literales_de_mercado(copia):
            f = copia / nombre
            f.write_text(f.read_text(encoding="utf-8").replace(
                "    raise KeyError(mercado_id)",
                f'    elif mercado_id == "{NUEVO}":\n        {rama[nombre]}\n'
                "    raise KeyError(mercado_id)"), encoding="utf-8")
        cambios = _diferencias(BASE_CONDICIONALES, copia)
        funciona = (_importar(copia / "catalogo.py").horario_atencion(NUEVO) == (7, 13)
                    and _importar(copia / "pedidos.py").monto_minimo(NUEVO) == 5
                    and _importar(copia / "entrega.py").costo_delivery(NUEVO) == 4)
    modulos = [a for a in cambios["archivos"] if a.endswith(".py")]
    return {"alternativa": "A. condicionales", "modulos_existentes_modificados": len(modulos),
            "archivos": cambios["archivos"], "lineas_cambiadas": cambios["lineas"],
            "mercado_nuevo_funciona": funciona}


def alta_con_configuracion() -> dict:
    """Agrega el mercado como una entrada de mercados.json y lo carga con el registro."""
    from src.mercados.registro import RegistroMercados

    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "mercados"
        shutil.copytree(MODULO_MERCADOS, copia, ignore=shutil.ignore_patterns("__pycache__"))
        config = copia / "mercados.json"
        datos = json.loads(config.read_text(encoding="utf-8"))
        datos["mercados"].append({"mercado_id": NUEVO, "nombre": "Mercado de prueba",
                                  "monto_minimo": 5, "permite_delivery": True,
                                  "costo_delivery": 4, "hora_apertura": 7, "hora_cierre": 13})
        config.write_text(json.dumps(datos, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        cambios = _diferencias(MODULO_MERCADOS, copia)
        reglas = RegistroMercados.desde_archivo(config).obtener(NUEVO)
        reglas.validar_pedido(Decimal("20"), "DELIVERY", 9)
        funciona = reglas.costo_envio("DELIVERY") == Decimal("4")
    modulos = [a for a in cambios["archivos"] if a.endswith(".py")]
    return {"alternativa": "B. configuración (src/mercados)", "modulos_existentes_modificados": len(modulos),
            "archivos": cambios["archivos"], "lineas_cambiadas": cambios["lineas"],
            "mercado_nuevo_funciona": funciona}


def main() -> None:
    resultados = [alta_con_condicionales(), alta_con_configuracion()]
    fuera = {c: modulos_con_literales_de_mercado(RAIZ / "src" / c) for c in ("antes", "despues", "pedidos")}
    for r in resultados:
        print(f"{r['alternativa']:32s} módulos .py modificados={r['modulos_existentes_modificados']}  "
              f"archivos={r['archivos']}  líneas={r['lineas_cambiadas']}  funciona={r['mercado_nuevo_funciona']}")
    print("Literales de mercado fuera de src/mercados:", fuera)
    salida = RAIZ / "docs" / "architecture" / "add" / "resultados-alta-mercados.json"
    salida.write_text(json.dumps({"mercado_nuevo": NUEVO, "resultados": resultados,
                                  "literales_fuera_de_mercados": fuera},
                                 indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
