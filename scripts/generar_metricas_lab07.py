#!/usr/bin/env python3
"""Lab 07 / E6: métricas CC y SLOC reales con Radon.

La salida de `radon cc -s -a` incluye clases y métodos. Este script
informa también el promedio de funciones/métodos sin contar clases, ni
duplicar métodos que cc_visit devuelve como bloques individuales.
Ejecutar desde la raíz del repositorio:
    .venv/bin/python scripts/generar_metricas_lab07.py
"""
from __future__ import annotations

from pathlib import Path
from statistics import mean

try:
    from radon.complexity import cc_rank, cc_visit
    from radon.raw import analyze
except ImportError as exc:
    raise SystemExit(
        "Instala Radon con: .venv/bin/python -m pip install radon"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
ANTES = ROOT / "src" / "antes"
DESPUES = ROOT / "src" / "despues"
SALIDA = ROOT / "docs" / "design" / "patrones" / "metricas.md"


def medir(carpeta: Path) -> dict:
    if not carpeta.is_dir():
        raise SystemExit(f"No se encuentra la carpeta {carpeta}")

    detalles = []
    complejidades_todos = []
    sloc = 0
    archivos = []

    for ruta in sorted(carpeta.rglob("*.py")):
        if "__pycache__" in ruta.parts:
            continue
        codigo = ruta.read_text(encoding="utf-8")
        archivos.append(ruta.relative_to(ROOT).as_posix())
        sloc += analyze(codigo).sloc

        for bloque in cc_visit(codigo):
            # Mismo criterio de `radon cc -s -a`: incluye C, M y F.
            complejidades_todos.append(bloque.complexity)

            # Radon devuelve también cada método como bloque M, además
            # del objeto clase C que contiene `methods`. No iterar
            # clase.methods: hacerlo duplicaría los métodos.
            if hasattr(bloque, "methods"):
                continue
            clase = getattr(bloque, "classname", None)
            nombre = f"{clase}.{bloque.name}" if clase else bloque.name
            detalles.append(
                (ruta.relative_to(ROOT).as_posix(), nombre, bloque.complexity)
            )

    if not detalles:
        raise SystemExit(f"No se encontraron funciones o métodos en {carpeta}")

    complejidades = [cc for _, _, cc in detalles]
    return {
        "detalles": sorted(detalles),
        "promedio_metodos": mean(complejidades),
        "promedio_radon": mean(complejidades_todos),
        "maxima_metodos": max(complejidades),
        "total_bloques": len(complejidades_todos),
        "total_metodos": len(detalles),
        "sloc": sloc,
        "archivos": archivos,
    }


def tabla(datos: dict) -> str:
    filas = [
        "| Archivo | Función o método | CC | Grado |",
        "|---|---|---:|:---:|",
    ]
    for archivo, nombre, cc in datos["detalles"]:
        filas.append(f"| `{archivo}` | `{nombre}` | {cc} | {cc_rank(cc)} |")
    return "\n".join(filas)


def generar() -> None:
    a = medir(ANTES)
    d = medir(DESPUES)
    contenido = f"""# E6. Métricas y trade-off — San Camilo en Línea

## 1. Complejidad ciclomática y líneas de código

Mediciones con **Radon** sobre los directorios completos `src/antes` y
`src/despues`. **CC** es la complejidad ciclomática. **SLOC** representa
las líneas de código fuente sin comentarios ni líneas en blanco.

| Métrica | Antes | Después |
|---|---:|---:|
| CC promedio general de Radon (clases, funciones y métodos) | {a['promedio_radon']:.2f} | {d['promedio_radon']:.2f} |
| CC promedio solo por función/método (sin clases) | {a['promedio_metodos']:.2f} | {d['promedio_metodos']:.2f} |
| CC máxima por función/método | {a['maxima_metodos']} | {d['maxima_metodos']} |
| SLOC | {a['sloc']} | {d['sloc']} |
| Bloques analizados por Radon (C, M, F) | {a['total_bloques']} | {d['total_bloques']} |
| Funciones y métodos únicos (M, F) | {a['total_metodos']} | {d['total_metodos']} |
| Archivos Python | {len(a['archivos'])} | {len(d['archivos'])} |

El promedio general se obtiene contando las clases además de sus métodos,
igual que `radon cc -s -a`. El promedio por función/método excluye las
clases y **cada método se cuenta una sola vez**.

La CC promedio general disminuyó de **{a['promedio_radon']:.2f}** a
**{d['promedio_radon']:.2f}**, mientras que las SLOC aumentaron de
**{a['sloc']}** a **{d['sloc']}**. Sin embargo, la mayor CC de un método
cambió de **{a['maxima_metodos']}** a **{d['maxima_metodos']}**; por ello,
no todos los métodos se volvieron más simples. El código después incluye
más módulos y funcionalidad de IA, de modo que esta comparación no mide
rendimiento ni garantiza equivalencia estricta del alcance funcional.

### Complejidad de cada función/método: antes

{tabla(a)}

**Promedio por método antes:** {a['promedio_metodos']:.2f}.

### Complejidad de cada función/método: después

{tabla(d)}

**Promedio por método después:** {d['promedio_metodos']:.2f}.

## 2. Trade-off (7 líneas)

1. Se separaron las responsabilidades de pagos, estados, notificaciones y normalización de productos.
2. Strategy, Adapter y Factory permiten cambiar adaptadores de pago con menor acoplamiento.
3. State delimita transiciones válidas y Observer desacopla el procesamiento de los avisos.
4. Decorator agrega registro y caché, mientras que los guardrails validan las respuestas simuladas de IA.
5. La complejidad promedio general disminuyó, aunque el método más complejo pasó de CC {a['maxima_metodos']} a {d['maxima_metodos']}.
6. El costo fue aumentar las líneas de código, los módulos, las abstracciones y la cantidad de pruebas.
7. La versión inicial habría sido suficiente para un prototipo simple con un único proveedor y sin ampliaciones.

## 3. Patrón que se decidió no aplicar: Composite

Se evaluó Composite porque un pedido puede contener productos de varios
puestos. Sin embargo, `Pedido`, `PedidoPuesto` y `LineaPedido` del Lab 05
representan la estructura necesaria. No se requiere tratar elementos
individuales y agrupaciones de forma recursiva mediante la misma interfaz.
Incorporar Composite al MVP agregaría una jerarquía sin una necesidad
actual demostrada, por lo que se decidió no aplicarlo.

## Comandos ejecutados

```bash
.venv/bin/radon cc -s -a src/antes
.venv/bin/radon cc -s -a src/despues
.venv/bin/radon raw -s src/antes
.venv/bin/radon raw -s src/despues
.venv/bin/python scripts/generar_metricas_lab07.py
.venv/bin/python -m pytest -q
```
"""
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(contenido, encoding="utf-8")
    print(f"Archivo generado: {SALIDA}")
    print(
        f"Antes: promedio Radon {a['promedio_radon']:.2f}, "
        f"promedio funciones/métodos {a['promedio_metodos']:.2f}, "
        f"SLOC {a['sloc']}"
    )
    print(
        f"Después: promedio Radon {d['promedio_radon']:.2f}, "
        f"promedio funciones/métodos {d['promedio_metodos']:.2f}, "
        f"SLOC {d['sloc']}"
    )
    print(
        f"Funciones/métodos únicos: {a['total_metodos']} antes; "
        f"{d['total_metodos']} después"
    )


if __name__ == "__main__":
    generar()
