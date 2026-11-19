"""E7.3 (Lab 09): ejecuta el mejor prompt 3 veces sobre los mismos 3 casos y compara.

Prompt: prompts/normalizacion/v3.txt (la mejor versión evaluada con promptfoo, 9/10).
Modelo: Qwen2.5-1.5B-Instruct GGUF Q4_K_M, el mismo de las grabaciones de E4,
ejecutado con llama-cpp-python. Dos configuraciones:
  - t0:   temperatura 0 y semilla 42 (como las grabaciones de E4).
  - t07:  temperatura 0,7 y semillas 1, 2 y 3 (similar a un asistente de chat).
Cada respuesta se guarda sin editar en prompts/no-determinismo/<config>/<corrida>/<id>.txt
y se evalúa con las mismas cuatro aserciones B1 a B4 de promptfooconfig.yaml.

Uso:  python prompts/no_determinismo.py RUTA_AL_MODELO.gguf
Requiere: llama-cpp-python, Jinja2, jsonschema, PyYAML.
"""
import json
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, StrictUndefined
from jsonschema import Draft7Validator
from llama_cpp import Llama

RAIZ = Path(__file__).resolve().parent
NORM = RAIZ / "normalizacion"
SALIDA = RAIZ / "no-determinismo"
CASOS = ("B02", "B06", "B08")
CATALOGO = '["papa canchán", "papa amarilla", "cebolla roja", "limón sutil", "tomate italiano", "queso fresco"]'
CONFIGS = {"t0": [(0.0, 42)] * 3, "t07": [(0.7, 1), (0.7, 2), (0.7, 3)]}
ESQUEMA = Draft7Validator(json.loads((NORM / "esquema.json").read_text(encoding="utf-8")))


def aserciones(salida, caso):
    """B1 a B4 de promptfooconfig.yaml, en Python."""
    try:
        d = json.loads(salida)
    except json.JSONDecodeError:
        return {"B1": False, "B2": False, "B3": False, "B4": False}
    cat = json.loads(CATALOGO)
    return {
        "B1": ESQUEMA.is_valid(d),
        "B2": d.get("producto") == "desconocido" or d.get("producto") in cat,
        "B3": d.get("id") == caso["id"] and d.get("entrada") == caso["entrada"],
        "B4": d.get("producto") == caso["esperado"],
    }


def main(modelo):
    entorno = Environment(autoescape=False, undefined=StrictUndefined)
    entorno.filters["dump"] = lambda v: json.dumps(v, ensure_ascii=False)
    plantilla = entorno.from_string((NORM / "v3.txt").read_text(encoding="utf-8"))
    casos = {c["vars"]["id"]: c["vars"] for c in yaml.safe_load((NORM / "casos.yaml").read_text(encoding="utf-8"))}
    llm = Llama(model_path=modelo, n_ctx=2048, verbose=False)
    filas = []
    for config, corridas in CONFIGS.items():
        for n, (temp, semilla) in enumerate(corridas, start=1):
            carpeta = SALIDA / config / f"corrida{n}"
            carpeta.mkdir(parents=True, exist_ok=True)
            for cid in CASOS:
                caso = casos[cid]
                prompt = plantilla.render(id=cid, entrada=caso["entrada"], catalogo=CATALOGO)
                r = llm.create_chat_completion(messages=[{"role": "user", "content": prompt}],
                                               temperature=temp, seed=semilla, max_tokens=160)
                texto = r["choices"][0]["message"]["content"]
                (carpeta / f"{cid}.txt").write_text(texto, encoding="utf-8")
                a = aserciones(texto, caso)
                filas.append({"config": config, "corrida": n, "temperatura": temp, "semilla": semilla,
                              "caso": cid, "salida": texto, "aprobado": all(a.values()), **a})
                print(config, n, cid, "OK" if all(a.values()) else "FALLO", texto.replace("\n", " ")[:90])
    (SALIDA / "resultados.json").write_text(json.dumps(filas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
