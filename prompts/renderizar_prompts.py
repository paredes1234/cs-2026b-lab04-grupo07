"""Genera el texto EXACTO de cada prompt (versión x caso) para pegarlo en el asistente.

Uso (desde la raíz del repo):
    python prompts/renderizar_prompts.py v1
    python prompts/renderizar_prompts.py v2 v3

Escribe prompts/criterios/renderizados/<version>/<id>.txt y lista qué grabaciones faltan.
Requiere:  pip install pyyaml
"""
import pathlib
import sys

import yaml

RAIZ = pathlib.Path(__file__).parent / "criterios"


def main(versiones):
    casos = yaml.safe_load((RAIZ / "casos.yaml").read_text(encoding="utf-8"))
    for v in versiones:
        plantilla = (RAIZ / f"{v}.txt").read_text(encoding="utf-8").rstrip("\n")
        salida = RAIZ / "renderizados" / v
        salida.mkdir(parents=True, exist_ok=True)
        faltan = []
        for caso in casos:
            id_caso, historia = caso["vars"]["id"], caso["vars"]["historia"]
            prompt = plantilla.replace("{{id}}", id_caso).replace("{{historia}}", historia)
            (salida / f"{id_caso}.txt").write_text(prompt, encoding="utf-8")
            if not (RAIZ / "grabaciones" / v / f"{id_caso}.txt").is_file():
                faltan.append(id_caso)
        print(f"{v}: {len(casos)} prompts en {salida}")
        print(f"{v}: faltan grabaciones de -> {', '.join(faltan) if faltan else 'ninguna'}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["v1"])
