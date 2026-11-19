"""Compuerta de la CI (E7): exige una tasa mínima solo a la versión vigente del prompt.

promptfoo termina con código 100 si cualquier caso falla, y las versiones v1 y v2
fallan a propósito porque son la línea base. Este script lee el JSON de promptfoo,
muestra la tasa de cada versión y falla solo si la versión indicada queda por debajo
del mínimo.

Uso:  python prompts/verificar_tasas.py resultados.json --version v3 --minimo 85
"""
import argparse
import json
import sys
from collections import defaultdict


def tasas(ruta):
    datos = json.load(open(ruta, encoding="utf-8"))
    r = datos.get("results", datos)
    filas = r.get("results", r) if isinstance(r, dict) else r
    por_version = defaultdict(list)
    for fila in filas:
        etiqueta = (fila.get("prompt") or {}).get("label") or str(fila.get("promptIdx"))
        por_version[etiqueta.partition(":")[0]].append(bool(fila.get("success")))
    return {v: (sum(x), len(x)) for v, x in sorted(por_version.items())}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("resultados")
    p.add_argument("--version", required=True)
    p.add_argument("--minimo", type=float, default=85.0)
    a = p.parse_args()

    t = tasas(a.resultados)
    for v, (ok, total) in t.items():
        print(f"{v:4} {ok:>3}/{total:<3} {100 * ok / total:6.1f} %")
    if a.version not in t:
        sys.exit(f"No hay resultados de {a.version}")
    ok, total = t[a.version]
    tasa = 100 * ok / total
    if tasa < a.minimo:
        sys.exit(f"{a.version}: {tasa:.1f} % es menor que el mínimo de {a.minimo:.0f} %")
    print(f"{a.version}: {tasa:.1f} % cumple el mínimo de {a.minimo:.0f} %")


if __name__ == "__main__":
    main()
