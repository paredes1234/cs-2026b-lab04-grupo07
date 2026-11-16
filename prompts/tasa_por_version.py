"""Calcula la tasa de aprobación por versión y por aserción a partir de resultados.json de promptfoo.

Uso:  python prompts/tasa_por_version.py prompts/criterios/resultados.json
Un caso aprueba solo si pasan TODAS sus aserciones.
"""
import json
import sys
from collections import defaultdict


def _filas(datos):
    r = datos.get("results", datos)
    return r.get("results", r) if isinstance(r, dict) else r


def main(ruta):
    datos = json.load(open(ruta, encoding="utf-8"))
    por_version, por_asercion, fallos = defaultdict(list), defaultdict(lambda: defaultdict(list)), defaultdict(list)
    for fila in _filas(datos):
        version = (fila.get("prompt") or {}).get("label") or str(fila.get("promptIdx"))
        id_caso = (fila.get("vars") or {}).get("id", "?")
        por_version[version].append(bool(fila.get("success")))
        malas = []
        for comp in (fila.get("gradingResult") or {}).get("componentResults", []) or []:
            metrica = (comp.get("assertion") or {}).get("metric") or (comp.get("assertion") or {}).get("type")
            por_asercion[version][metrica].append(bool(comp.get("pass")))
            if not comp.get("pass"):
                malas.append(str(metrica).split("_")[0])
        if malas:
            fallos[version].append(f"{id_caso}({','.join(malas)})")
    print(f"{'Versión':8} {'Casos OK':>9} {'Tasa':>8}   Casos con fallos")
    for v, res in sorted(por_version.items()):
        print(f"{v:8} {sum(res):>4}/{len(res):<4} {100*sum(res)/len(res):7.1f}%   {' '.join(fallos[v])}")
    print("\nPor aserción:")
    for v in sorted(por_asercion):
        print(f"  {v}: " + ", ".join(f"{m} {sum(x)}/{len(x)}" for m, x in sorted(por_asercion[v].items())))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "prompts/criterios/resultados.json")
