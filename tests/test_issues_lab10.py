from unittest.mock import patch
from decimal import Decimal
import pytest

from src.despues.servicio import ServicioPedidosProcesadorRefactorizado


class InventarioSimulado:
    def __init__(self):
        self.liberaciones = []

    def reservar_stock(self, producto_id, cantidad):
        return True

    def liberar_stock(self, producto_id, cantidad):
        self.liberaciones.append((producto_id, cantidad))


class PagoConTimeout:
    def __init__(self):
        self.llamadas = 0

    def procesar_pago(self, monto, token):
        self.llamadas += 1
        if self.llamadas == 1:
            # Simula que el proveedor cobró, pero se perdió la respuesta.
            raise ConnectionError("Timeout después de procesar el cobro")
        return "TX-123"


class PagoCapturador:
    def __init__(self):
        self.monto_recibido = None

    def procesar_pago(self, monto, token):
        self.monto_recibido = monto
        return "TX-999"


def test_issue_01_no_debe_generar_dos_cobros():
    inventario = InventarioSimulado()
    pago = PagoConTimeout()

    servicio = ServicioPedidosProcesadorRefactorizado(
        inventario=inventario
    )

    with patch(
        "src.despues.servicio.PagoFactory.obtener",
        return_value=pago
    ):
        try:
            servicio.confirmar_y_pagar(
                "PED-101",
                "PROD-1",
                1,
                10.00,
                "TOKEN-FALSO",
                max_reintentos=2
            )
        except Exception:
            pass

    # La prueba exige que el mismo pedido no genere otro cobro.
    assert pago.llamadas == 1


def test_issue_02_libera_stock_si_el_tipo_pago_es_invalido():
    inventario = InventarioSimulado()

    servicio = ServicioPedidosProcesadorRefactorizado(
        inventario=inventario
    )

    with pytest.raises(Exception):
        servicio.confirmar_y_pagar(
            "PED-102",
            "PROD-1",
            1,
            10.00,
            "TOKEN-FALSO",
            tipo_pago="TIPO_NO_REGISTRADO"
        )

    assert inventario.liberaciones == [("PROD-1", 1)]


def test_issue_03_precision_de_importes():
    inventario = InventarioSimulado()
    pago = PagoCapturador()

    servicio = ServicioPedidosProcesadorRefactorizado(
        inventario=inventario
    )

    with patch(
        "src.despues.servicio.PagoFactory.obtener",
        return_value=pago
    ):
        servicio.confirmar_y_pagar(
            "PED-103",
            "PROD-1",
            1,
            0.10 + 0.20,
            "TOKEN-FALSO"
        )

    # Exige que el servicio trabaje y envíe un Decimal exacto, no un float impreciso.
    assert isinstance(pago.monto_recibido, Decimal)
    assert pago.monto_recibido == Decimal("0.30")