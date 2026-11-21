"""Proveedor de normalización con plantillas versionadas y salida validada."""
from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path

from jinja2 import Environment, StrictUndefined
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

from .ia import ClienteLLMExterno, ProveedorLLM


RAIZ = Path(__file__).resolve().parents[2]
NORMALIZACION = RAIZ / "prompts" / "normalizacion"
PLANTILLAS = {
    "v2": NORMALIZACION / "v2.txt",
    "v3": NORMALIZACION / "v3.txt",
    "v4": RAIZ / "seguridad" / "v4.txt",
}


class SalidaInvalida(ValueError):
    """El proveedor devolvió una respuesta que no se puede entregar al llamador."""


class GeneradorNormalizacion(ProveedorLLM):
    def __init__(
        self,
        cliente: ClienteLLMExterno,
        catalogo: Iterable[str],
        *,
        version: str = "v4",
    ) -> None:
        if version not in PLANTILLAS:
            raise ValueError(f"Versión de normalización no compatible: {version}")
        self._cliente = cliente
        self._catalogo = tuple(catalogo)
        esquema = json.loads((NORMALIZACION / "esquema.json").read_text(encoding="utf-8"))
        self._validador = Draft7Validator(esquema)
        entorno = Environment(autoescape=False, undefined=StrictUndefined)
        entorno.filters["dump"] = lambda valor: json.dumps(valor, ensure_ascii=False)
        self._plantilla = entorno.from_string(PLANTILLAS[version].read_text(encoding="utf-8").strip())

    def normalizar_nombre(self, nombre: str, *, id_registro: str = "normalizacion") -> str:
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,60}", id_registro):
            raise ValueError("IA: identificador de registro inválido")
        if not nombre.strip() or len(nombre) > 60:
            raise ValueError("IA: nombre vacío o excesivamente largo")
        if not all(caracter.isalpha() or caracter == " " for caracter in nombre):
            raise ValueError("IA: el nombre solo admite letras y espacios")

        prompt = self._plantilla.render(
            id=id_registro,
            entrada=nombre,
            catalogo=json.dumps(self._catalogo, ensure_ascii=False),
        )
        texto = self._cliente.completar(prompt)
        try:
            respuesta = json.loads(texto)
        except (json.JSONDecodeError, TypeError) as error:
            raise SalidaInvalida("La respuesta no es JSON válido") from error
        try:
            self._validador.validate(respuesta)
        except ValidationError as error:
            raise SalidaInvalida("La respuesta no cumple el JSON Schema") from error

        if respuesta["id"] != id_registro or respuesta["entrada"] != nombre:
            raise SalidaInvalida("La respuesta cambió el ID o la entrada original")
        producto = respuesta["producto"]
        if producto != "desconocido" and producto not in self._catalogo:
            raise SalidaInvalida("El producto devuelto está fuera del catálogo")
        return producto
