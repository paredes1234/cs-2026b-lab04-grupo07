"""E4: patrón Observer para los eventos de San Camilo en Línea.

No conecta con WhatsApp real. La bandeja simula la cola de avisos del MVP.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Protocol


class Suscriptor(Protocol):
    def actualizar(self, evento: str, datos: dict[str, Any]) -> None: ...


class PublicadorEventos:
    """Publicador que no conoce las implementaciones de los suscriptores."""

    def __init__(self) -> None:
        self._suscriptores: dict[str, list[Suscriptor]] = defaultdict(list)

    def suscribir(self, evento: str, suscriptor: Suscriptor) -> None:
        if suscriptor not in self._suscriptores[evento]:
            self._suscriptores[evento].append(suscriptor)

    def publicar(self, evento: str, datos: dict[str, Any]) -> None:
        # Se entrega una copia para que un observador no altere lo que ve otro.
        for suscriptor in tuple(self._suscriptores.get(evento, ())):
            suscriptor.actualizar(evento, dict(datos))


class NotificadorComerciantes:
    """Suscriptor: simula encolar confirmaciones para los puestos."""

    def __init__(self, bandeja: list[dict[str, str]]) -> None:
        self.bandeja = bandeja

    def actualizar(self, evento: str, datos: dict[str, Any]) -> None:
        if evento != "pedido_pagado":
            return
        for puesto in datos.get("puestos", []):
            self.bandeja.append({
                "canal": "whatsapp_simulado",
                "pedido_id": str(datos["pedido_id"]),
                "puesto_id": str(puesto["id"]),
                "destino": str(puesto["celular"]),
            })


class AuditoriaPedidos:
    """Segundo suscriptor: registra la acción sin copiar teléfonos."""

    def __init__(self, registros: list[dict[str, str]]) -> None:
        self.registros = registros

    def actualizar(self, evento: str, datos: dict[str, Any]) -> None:
        self.registros.append({
            "evento": evento,
            "pedido_id": str(datos["pedido_id"]),
        })
