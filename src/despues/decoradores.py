"""E4: Decorator de registro de eventos, sin alterar el suscriptor envuelto."""
from __future__ import annotations

from typing import Any
from src.despues.eventos import Suscriptor


class ConRegistroEventos:
    """Registra la ejecución exitosa de otro suscriptor (Decorator)."""

    def __init__(self, interno: Suscriptor, registro: list[dict[str, str]]) -> None:
        self._interno = interno
        self._registro = registro

    def actualizar(self, evento: str, datos: dict[str, Any]) -> None:
        self._interno.actualizar(evento, datos)
        # Solo metadatos no sensibles: jamás copiar teléfonos al log.
        self._registro.append({
            "tipo": "suscriptor_ejecutado",
            "evento": evento,
            "pedido_id": str(datos["pedido_id"]),
        })
