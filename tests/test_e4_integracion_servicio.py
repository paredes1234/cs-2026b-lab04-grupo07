"""Pruebas de integración de Observer con el flujo de pedidos de E1-E3."""
from unittest.mock import patch
import pytest

from src.despues.eventos import (
    PublicadorEventos,
    NotificadorComerciantes,
    AuditoriaPedidos,
)
from src.despues.decoradores import ConRegistroEventos
from src.despues.servicio import ServicioPedidosProcesadorRefactorizado


class InventarioSimulado:
    def __init__(self, suficiente=True):
        self.suficiente = suficiente
        self.liberaciones = []

    def reservar_stock(self, producto_id, cantidad):
        return self.suficiente

    def liberar_stock(self, producto_id, cantidad):
        self.liberaciones.append((producto_id, cantidad))


class PagoSimulado:
    def procesar_pago(self, monto, token_tarjeta):
        return "TX-123"


def test_e4_pago_exitoso_publica_una_vez_y_notifica_puestos():
    eventos = PublicadorEventos()
    bandeja, auditoria, registro_decorador = [], [], []
    eventos.suscribir("pedido_pagado", ConRegistroEventos(
        NotificadorComerciantes(bandeja), registro_decorador
    ))
    eventos.suscribir("pedido_pagado", AuditoriaPedidos(auditoria))
    servicio = ServicioPedidosProcesadorRefactorizado(
        inventario=InventarioSimulado(), publicador_eventos=eventos
    )
    puestos = [
        {"id": "P1", "celular": "999111222"},
        {"id": "P2", "celular": "999333444"},
    ]

    with patch("src.despues.servicio.PagoFactory.obtener", return_value=PagoSimulado()):
        resultado = servicio.confirmar_y_pagar(
            "PED-17", "PROD-1", 2, 16.0, "TOKEN-FALSO", puestos=puestos
        )

    assert resultado == {
        "pedido_id": "PED-17", "estado": "PAGADO", "transaccion_id": "TX-123"
    }
    assert [x["puesto_id"] for x in bandeja] == ["P1", "P2"]
    assert auditoria == [{"evento": "pedido_pagado", "pedido_id": "PED-17"}]
    assert registro_decorador[0]["tipo"] == "suscriptor_ejecutado"
    assert servicio.conn.execute("SELECT estado FROM pedidos WHERE id = ?", ("PED-17",)).fetchone() == ("PAGADO",)


def test_e4_sin_stock_no_publica_eventos():
    eventos = PublicadorEventos()
    auditoria = []
    eventos.suscribir("pedido_pagado", AuditoriaPedidos(auditoria))
    servicio = ServicioPedidosProcesadorRefactorizado(
        inventario=InventarioSimulado(suficiente=False), publicador_eventos=eventos
    )

    with pytest.raises(RuntimeError, match="Stock insuficiente"):
        servicio.confirmar_y_pagar("PED-18", "PROD-1", 2, 16.0, "TOKEN-FALSO")

    assert auditoria == []
    assert servicio.conn.execute("SELECT count(*) FROM pedidos").fetchone()[0] == 0


def test_e4_error_del_suscriptor_no_simula_fallo_de_pago():
    class SuscriptorConError:
        def actualizar(self, evento, datos):
            raise RuntimeError("WhatsApp simulado no responde")

    eventos = PublicadorEventos()
    eventos.suscribir("pedido_pagado", SuscriptorConError())
    servicio = ServicioPedidosProcesadorRefactorizado(
        inventario=InventarioSimulado(), publicador_eventos=eventos
    )

    with patch("src.despues.servicio.PagoFactory.obtener", return_value=PagoSimulado()):
        resultado = servicio.confirmar_y_pagar("PED-19", "PROD-1", 1, 8.0, "TOKEN-FALSO")

    assert resultado["estado"] == "PAGADO"
    assert servicio.conn.execute("SELECT estado FROM pedidos WHERE id = ?", ("PED-19",)).fetchone() == ("PAGADO",)
