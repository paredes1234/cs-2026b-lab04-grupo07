"""Fitness functions de calidad (E5, Lab 08): los escenarios del árbol de utilidad como pruebas.

FF-01 a FF-03 son estructurales y están en .importlinter. Si alguien quita una
táctica de las iteraciones 1 a 3, alguna de estas pruebas falla en la CI.
"""

import json
import shutil
from decimal import Decimal

import pytest

from fitness.aislamiento import ejecutar_escenario
from fitness.alta_mercados import (
    RAIZ,
    alta_con_configuracion,
    modulos_con_literales_de_mercado,
)
from fitness.cobros import montecarlo, simular
from src.mercados.registro import CONFIGURACION, MercadoDesconocido, RegistroMercados
from src.mercados.reglas import ReglaIncumplida

MAX_MODULOS_POR_MERCADO = 2      # QA08-07


def test_ff04_aislamiento_cero_registros_ajenos_en_100_intentos():
    """QA08-05 (iteración 1, ADR-006)."""
    resumen, _ = ejecutar_escenario(intentos=100, semilla=2026)
    assert resumen["intentos_cruzados"] == 100
    assert resumen["expuestos_despues"] == 0
    assert resumen["accesos_legitimos_aprobados"] == resumen["accesos_legitimos"]


def test_ff05_cero_cobros_duplicados_con_10_timeouts_en_100():
    """QA08-04 (iteración 2, ADR-007): lote del escenario y 1000 corridas."""
    lote = simular("idempotente", pedidos=100, timeouts=10, semilla=2026)
    assert lote["cobros_duplicados"] == 0
    assert lote["confirmados"] == 100
    assert montecarlo("idempotente", corridas=1000)["duplicados_max"] == 0


def test_ff05b_la_linea_base_si_duplica():
    """Control: si la simulación no detectara duplicados en la línea base, FF-05 no probaría nada."""
    assert simular("reintentos", pedidos=100, timeouts=10, semilla=2026)["cobros_duplicados"] > 0


def test_ff06_alta_de_mercado_sin_tocar_modulos_existentes():
    """QA08-07 (iteración 3, ADR-008): un mercado nuevo cambia ≤ 2 módulos .py."""
    r = alta_con_configuracion()
    assert r["mercado_nuevo_funciona"]
    assert r["modulos_existentes_modificados"] <= MAX_MODULOS_POR_MERCADO


@pytest.mark.parametrize("carpeta", ["antes", "despues", "pedidos"])
def test_ff06b_sin_reglas_de_mercado_fuera_del_modulo_mercados(carpeta):
    """Un `if mercado == "ALTIPLANO"` fuera de src/mercados rompe la táctica de la iteración 3."""
    assert modulos_con_literales_de_mercado(RAIZ / "src" / carpeta) == []


def test_ff07_cambiar_regla_de_rio_seco_no_afecta_a_otros_mercados(tmp_path):
    """QA08-08: la regla de un mercado se cambia sin alterar las de los demás."""
    original = RegistroMercados.desde_archivo()
    copia = tmp_path / "mercados.json"
    shutil.copy(CONFIGURACION, copia)
    datos = json.loads(copia.read_text(encoding="utf-8"))
    for m in datos["mercados"]:
        if m["mercado_id"] == "RIO_SECO":
            m["monto_minimo"] = 25
    copia.write_text(json.dumps(datos), encoding="utf-8")
    cambiado = RegistroMercados.desde_archivo(copia)

    assert cambiado.obtener("RIO_SECO").monto_minimo == Decimal("25")
    for otro in set(original.ids()) - {"RIO_SECO"}:
        assert cambiado.obtener(otro) == original.obtener(otro)


def test_reglas_de_mercado_se_aplican():
    registro = RegistroMercados.desde_archivo()
    with pytest.raises(ReglaIncumplida):
        registro.obtener("ALTIPLANO").costo_envio("DELIVERY")
    with pytest.raises(ReglaIncumplida):
        registro.obtener("RIO_SECO").validar_pedido(Decimal("10"), "RECOJO", 9)
    registro.obtener("SAN_CAMILO").validar_pedido(Decimal("10"), "DELIVERY", 9)
    with pytest.raises(MercadoDesconocido):
        registro.obtener("OTRO")
