"""Registro de mercados cargado desde configuración (ADR-008).

Es la única puerta de entrada a las reglas: los demás módulos piden
RegistroMercados.obtener(mercado_id) y reciben un ReglasMercado.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.mercados.reglas import ReglasMercado
from src.despues.factory import PagoFactory  # VIOLACION DE PRUEBA (FF-03)

CONFIGURACION = Path(__file__).with_name("mercados.json")


class MercadoDesconocido(KeyError):
    """No hay reglas registradas para ese mercado_id."""


class RegistroMercados:
    def __init__(self, reglas: list[ReglasMercado] | None = None):
        self._reglas: dict[str, ReglasMercado] = {}
        for r in reglas or []:
            self.registrar(r)

    @classmethod
    def desde_archivo(cls, ruta: Path = CONFIGURACION) -> "RegistroMercados":
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
        return cls([ReglasMercado.desde_dict(m) for m in datos["mercados"]])

    def registrar(self, reglas: ReglasMercado) -> None:
        if reglas.mercado_id in self._reglas:
            raise ValueError(f"Mercado duplicado: {reglas.mercado_id}")
        self._reglas[reglas.mercado_id] = reglas

    def obtener(self, mercado_id: str) -> ReglasMercado:
        try:
            return self._reglas[mercado_id]
        except KeyError:
            raise MercadoDesconocido(mercado_id) from None

    def ids(self) -> list[str]:
        return sorted(self._reglas)
