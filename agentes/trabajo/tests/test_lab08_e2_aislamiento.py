"""Pruebas del prototipo de aislamiento QA08-05."""

import pytest

from fitness.aislamiento import (
    MERCADOS,
    PEDIDOS_SINTETICOS,
    consulta_antes,
    consulta_despues,
    crear_bd_sintetica,
    ejecutar_escenario,
)


def test_baseline_deliberadamente_expone_pedido_ajeno():
    conn = crear_bd_sintetica()
    try:
        pedido_id, mercado_dueno, _ = PEDIDOS_SINTETICOS[0]
        otro_mercado = next(m for m in MERCADOS if m != mercado_dueno)
        assert consulta_antes(conn, pedido_id, otro_mercado) is not None
    finally:
        conn.close()


@pytest.mark.parametrize(
    "solicitante,mercado_objetivo",
    [(s, o) for s in MERCADOS for o in MERCADOS if s != o],
)
def test_protege_todas_las_combinaciones_cruzadas(solicitante, mercado_objetivo):
    pedido_id = next(p[0] for p in PEDIDOS_SINTETICOS if p[1] == mercado_objetivo)
    conn = crear_bd_sintetica()
    try:
        assert consulta_despues(conn, pedido_id, solicitante) is None
    finally:
        conn.close()


@pytest.mark.parametrize("mercado", MERCADOS)
def test_permite_lecturas_legitimas_del_propio_mercado(mercado):
    pedido_id = next(p[0] for p in PEDIDOS_SINTETICOS if p[1] == mercado)
    conn = crear_bd_sintetica()
    try:
        resultado = consulta_despues(conn, pedido_id, mercado)
        assert resultado is not None
        assert resultado[1] == mercado
    finally:
        conn.close()


def test_medida_qa08_05_cien_intentos_cruzados_cero_expuestos():
    resultado, filas = ejecutar_escenario(intentos=100, semilla=2026)
    assert len(filas) == 100
    assert resultado["expuestos_antes"] == 100
    assert resultado["expuestos_despues"] == 0
    assert resultado["accesos_legitimos_aprobados"] == 12
    assert resultado["objetivo_cumplido_en_prototipo"] is True


def test_reproducibilidad_con_semilla_fija():
    resumen1, filas1 = ejecutar_escenario(intentos=100, semilla=2026)
    resumen2, filas2 = ejecutar_escenario(intentos=100, semilla=2026)
    assert resumen1 == resumen2
    assert filas1 == filas2


def test_no_admite_cero_intentos():
    with pytest.raises(ValueError):
        ejecutar_escenario(intentos=0)
