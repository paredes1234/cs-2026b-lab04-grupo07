"""Reglas comerciales por mercado (E4 Lab 08, iteración 3; ADR-008, QA08-07, QA08-08).

Cada mercado se describe con datos, no con código: un mercado nuevo es una
entrada más en mercados.json. Pedidos y Catálogo consultan las reglas por
mercado_id y nunca preguntan "if mercado == ...".
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

RECOJO = "RECOJO"
DELIVERY = "DELIVERY"


class ReglaIncumplida(ValueError):
    """El pedido no cumple una regla comercial de su mercado."""


@dataclass(frozen=True)
class ReglasMercado:
    mercado_id: str
    nombre: str
    monto_minimo: Decimal
    permite_delivery: bool
    costo_delivery: Decimal
    hora_apertura: int
    hora_cierre: int

    def costo_envio(self, modalidad: str) -> Decimal:
        if modalidad == RECOJO:
            return Decimal("0")
        if not self.permite_delivery:
            raise ReglaIncumplida(f"{self.nombre} no ofrece delivery")
        return self.costo_delivery

    def validar_pedido(self, monto: Decimal, modalidad: str, hora: int) -> None:
        """Lanza ReglaIncumplida con el primer incumplimiento encontrado."""
        if monto < self.monto_minimo:
            raise ReglaIncumplida(
                f"{self.nombre}: el monto mínimo es S/ {self.monto_minimo}")
        if not self.hora_apertura <= hora < self.hora_cierre:
            raise ReglaIncumplida(
                f"{self.nombre}: atiende de {self.hora_apertura} a {self.hora_cierre} h")
        self.costo_envio(modalidad)

    @classmethod
    def desde_dict(cls, datos: dict) -> "ReglasMercado":
        return cls(
            mercado_id=datos["mercado_id"],
            nombre=datos["nombre"],
            monto_minimo=Decimal(str(datos["monto_minimo"])),
            permite_delivery=bool(datos["permite_delivery"]),
            costo_delivery=Decimal(str(datos.get("costo_delivery", 0))),
            hora_apertura=int(datos["hora_apertura"]),
            hora_cierre=int(datos["hora_cierre"]),
        )
