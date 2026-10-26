import pytest
from src.antes.servicio import ServicioPedidosProcesador

@pytest.fixture
def servicio():
    return ServicioPedidosProcesador(db_path=":memory:")

CASOS_PRUEBA = [
    # (id, prod_id, cant, monto, token, max_reintentos, resultado_esperado, excepcion_esperada)
    ("PED-01", "PROD-1", 2, 100.0, "TOK-OK", 1, "PAGADO", None),                     # 1. Éxito estándar
    ("PED-02", "PROD-2", 1, 50.0,  "TOK-OK", 1, None, RuntimeError),                # 2. Error sin stock
    ("PED-03", "PROD-1", 0, 100.0, "TOK-OK", 1, None, ValueError),                  # 3. Límite cantidad 0
    ("PED-04", "PROD-1", 1, -10.0, "TOK-OK", 1, None, ValueError),                  # 4. Límite monto negativo
    ("PED-05", "PROD-1", 1, 50.0,  "INVALIDO", 1, None, ValueError),                # 5. Error datos tarjeta
    ("PED-06", "PROD-1", 1, 50.0,  "TIMEOUT", 1, None, RuntimeError),                 # 6. Fallo por reintentos agotados
    ("PED-07", "PROD-1", 10, 500.0, "TOK-OK", 1, "PAGADO", None),                    # 7. Límite stock exacto
    ("PED-08", "PROD-08", 1, 50.0, "TIMEOUT", 2, None, RuntimeError)                # 8. Reintento fallido múltiple
]

@pytest.mark.parametrize(
    "pedido_id, prod_id, cantidad, monto, token, reintentos, estado_esperado, excepcion",
    CASOS_PRUEBA
)
def test_caracterizacion_flujo_pedido(servicio, pedido_id, prod_id, cantidad, monto, token, reintentos, estado_esperado, excepcion):
    if excepcion:
        with pytest.raises(excepcion):
            servicio.confirmar_y_pagar(pedido_id, prod_id, cantidad, monto, token, max_reintentos=reintentos)
    else:
        resultado = servicio.confirmar_y_pagar(pedido_id, prod_id, cantidad, monto, token, max_reintentos=reintentos)
        assert resultado["estado"] == estado_esperado
        
        # Verificar estado observable en la DB activa
        conn = servicio._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT estado FROM pedidos WHERE id = ?", (pedido_id,))
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == estado_esperado