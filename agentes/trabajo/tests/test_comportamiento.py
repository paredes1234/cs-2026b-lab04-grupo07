import pytest
from src.despues.estados import TransicionEstadoInvalida
from src.despues.dominio import PedidoPuesto

def test_transicion_estado_invalida_lanza_excepcion():
    """Valida la prohibición de transiciones fuera del diagrama de estados del Lab 05."""
    pedido_puesto = PedidoPuesto("PUESTO-01", "PROD-1", 1, 20.0)
    
    # 1. Intentar registrar entrega desde RECIBIDO debe fallar
    with pytest.raises(TransicionEstadoInvalida):
        pedido_puesto.registrar_entrega()
        
    # 2. Transición válida: RECIBIDO -> LISTO -> ENTREGADO
    pedido_puesto.marcar_listo()
    assert pedido_puesto.estado == "LISTO"
    
    pedido_puesto.registrar_entrega()
    assert pedido_puesto.estado == "ENTREGADO"
    
    # 3. Intentar rechazar un pedido ya ENTREGADO debe fallar
    with pytest.raises(TransicionEstadoInvalida):
        pedido_puesto.rechazar("Sin stock")