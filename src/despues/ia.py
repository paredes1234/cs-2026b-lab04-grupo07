"""E5: normalización segura de nombres de productos de San Camilo.

Strategy + Adapter + Decorator + Chain of Responsibility.
No se requieren claves de API ni servicios reales. Python 3.10+.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol


def _nombre_clave(texto: str) -> str:
    return " ".join(texto.casefold().split())


class ProveedorLLM(ABC):
    """Strategy: permite sustituir un LLM por otra implementación."""

    @abstractmethod
    def normalizar_nombre(self, nombre: str) -> str:
        raise NotImplementedError


class ClienteLLMExterno(Protocol):
    """Interfaz ajena simulada; en el futuro puede reemplazarse por un SDK."""

    def completar(self, prompt: str) -> str: ...


class AdaptadorClienteLLM(ProveedorLLM):
    """Adapter: adapta completar(prompt) a normalizar_nombre(nombre)."""

    def __init__(self, cliente: ClienteLLMExterno) -> None:
        self._cliente = cliente

    def normalizar_nombre(self, nombre: str) -> str:
        prompt = (
            "Corrige solamente errores de escritura del nombre del producto. "
            "Devuelve únicamente el nombre corregido, sin precios, unidades "
            "ni información adicional.\nProducto: " + nombre
        )
        return self._cliente.completar(prompt)


class Guardrail(ABC):
    """Eslabón del patrón Chain of Responsibility."""

    def __init__(self, siguiente: Guardrail | None = None) -> None:
        self._siguiente = siguiente

    def validar(self, entrada: str, salida: str) -> str:
        salida = self._comprobar(entrada, salida)
        if self._siguiente is not None:
            return self._siguiente.validar(entrada, salida)
        return salida

    @abstractmethod
    def _comprobar(self, entrada: str, salida: str) -> str:
        raise NotImplementedError


class GuardrailSoloNombre(Guardrail):
    """Bloquea precios, números, instrucciones y respuestas no nominales."""

    def _comprobar(self, entrada: str, salida: str) -> str:
        salida = " ".join(salida.split())
        if not salida or len(salida) > 60:
            raise ValueError("IA: nombre vacío o excesivamente largo")
        if not all(caracter.isalpha() or caracter.isspace() for caracter in salida):
            raise ValueError("IA: respuesta contiene precios, números o signos")
        if len(salida.split()) > 5:
            raise ValueError("IA: la respuesta no parece un nombre de producto")
        return salida


class GuardrailCatalogo(Guardrail):
    """No permite inventar un producto: exige la forma canónica permitida."""

    def __init__(self, alias: dict[str, str], siguiente: Guardrail | None = None) -> None:
        super().__init__(siguiente)
        self._alias = {_nombre_clave(k): _nombre_clave(v) for k, v in alias.items()}

    def _comprobar(self, entrada: str, salida: str) -> str:
        canonico = self._alias.get(_nombre_clave(entrada))
        if canonico is None:
            raise ValueError("IA: nombre de entrada fuera del catálogo permitido")
        if _nombre_clave(salida) != canonico:
            raise ValueError("IA: la respuesta cambió el producto o inventó uno")
        return canonico


class ConGuardrails(ProveedorLLM):
    """Decorador que valida la salida del proveedor antes de entregarla."""

    def __init__(self, interno: ProveedorLLM, cadena: Guardrail) -> None:
        self._interno = interno
        self._cadena = cadena

    def normalizar_nombre(self, nombre: str) -> str:
        if not nombre.strip():
            raise ValueError("IA: debe indicarse un nombre de producto")
        salida = self._interno.normalizar_nombre(nombre)
        return self._cadena.validar(nombre, salida)


class ConCache(ProveedorLLM):
    """Decorator: almacena solo resultados que superaron los guardrails."""

    def __init__(self, interno: ProveedorLLM) -> None:
        self._interno = interno
        self._cache: dict[str, str] = {}
        self.aciertos = 0

    def normalizar_nombre(self, nombre: str) -> str:
        clave = _nombre_clave(nombre)
        if clave in self._cache:
            self.aciertos += 1
            return self._cache[clave]
        resultado = self._interno.normalizar_nombre(nombre)
        self._cache[clave] = resultado
        return resultado


def crear_normalizador(cliente: ClienteLLMExterno, alias: dict[str, str]) -> ConCache:
    """Orden importante: Adapter -> guardrails -> caché; no cachear inválidos."""
    guardrails = GuardrailSoloNombre(GuardrailCatalogo(alias))
    proveedor: ProveedorLLM = AdaptadorClienteLLM(cliente)
    protegido: ProveedorLLM = ConGuardrails(proveedor, guardrails)
    return ConCache(protegido)
