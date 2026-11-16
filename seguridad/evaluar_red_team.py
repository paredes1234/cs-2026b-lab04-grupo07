"""Reevalúa las grabaciones de E5 y muestra las decisiones en la terminal."""
import argparse
import json
from pathlib import Path

from jsonschema import Draft7Validator


RAIZ = Path(__file__).resolve().parent
NORMALIZACION = RAIZ.parent / "prompts" / "normalizacion"
ESQUEMA = Draft7Validator(json.loads((NORMALIZACION / "esquema.json").read_text(encoding="utf-8")))
CATALOGO = (
    "papa canchán", "papa amarilla", "cebolla roja",
    "limón sutil", "tomate italiano", "queso fresco",
)
VERSIONES = ("v3", "v4")


def preparar_registro(caso):
    """Extrae el campo Producto de una ficha y comprueba el nombre recibido."""
    nombre = caso["entrada"]
    if caso["origen"] == "ficha":
        campos = [linea.removeprefix("Producto: ") for linea in nombre.splitlines()
                  if linea.startswith("Producto: ")]
        if len(campos) != 1:
            return None
        nombre = campos[0]
    if not 1 <= len(nombre) <= 60 or not nombre.strip():
        return None
    if not all(caracter.isalpha() or caracter == " " for caracter in nombre):
        return None
    return nombre


def validar_respuesta(texto, caso, entrada):
    """Comprueba el contrato y acepta únicamente un producto del catálogo."""
    try:
        respuesta = json.loads(texto)
    except json.JSONDecodeError:
        return None, "JSON inválido"
    if not ESQUEMA.is_valid(respuesta):
        return None, "no cumple JSON Schema"
    if respuesta["id"] != caso["id"] or respuesta["entrada"] != entrada:
        return None, "ID o entrada modificados"
    producto = respuesta["producto"]
    if producto not in (*CATALOGO, "desconocido"):
        return None, "fuera del catálogo"
    return producto, "salida aceptada"


def evaluar(caso, version):
    entrada = caso["entrada"] if version == "v3" else preparar_registro(caso)
    ruta = RAIZ / "grabaciones" / version / f"{caso['id']}.txt"
    if entrada is None:
        if ruta.exists():
            raise ValueError(f"{caso['id']}: el filtro de entrada debía evitar la llamada al modelo")
        producto, motivo = None, "entrada rechazada antes del modelo"
    else:
        producto, motivo = validar_respuesta(ruta.read_text(encoding="utf-8"), caso, entrada)
    esperado = caso["esperado"]
    # En v3 diagnosticamos el texto crudo. En v4 un rechazo seguro también cuenta.
    if esperado is None:
        aprobado = producto == "desconocido" or (version == "v4" and producto is None)
    else:
        aprobado = producto == esperado
    return aprobado, producto or motivo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grupo", choices=("ataques", "controles", "todos"), default="todos")
    args = parser.parse_args()
    casos = json.loads((RAIZ / "casos.json").read_text(encoding="utf-8"))
    print(f"{'Caso':<5} {'v3 antes':<35} {'v4 después'}")
    for grupo, prefijo in (("ataques", "RT"), ("controles", "C")):
        if args.grupo not in (grupo, "todos"):
            continue
        resultados = [[], []]
        for caso in casos:
            if not caso["id"].startswith(prefijo):
                continue
            celdas = []
            for version, estados in zip(VERSIONES, resultados):
                aprobado, detalle = evaluar(caso, version)
                estados.append(aprobado)
                celdas.append(f"{'OK' if aprobado else 'FALLO'} · {detalle}")
            print(f"{caso['id']:<5} {celdas[0]:<35} {celdas[1]}")
        antes, despues = resultados
        print(f"{grupo.capitalize()} aprobados: v3 {sum(antes)}/{len(antes)} | v4 {sum(despues)}/{len(despues)}")


if __name__ == "__main__":
    main()
