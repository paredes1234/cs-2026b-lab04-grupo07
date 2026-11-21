"""E4: pruebas independientes para Observer y Decorator."""
from src.despues.eventos import PublicadorEventos, NotificadorComerciantes, AuditoriaPedidos
from src.despues.decoradores import ConRegistroEventos


def _evento():
    return {
        "pedido_id": "PED-17",
        "puestos": [
            {"id": "P1", "celular": "999111222"},
            {"id": "P2", "celular": "999333444"},
        ],
    }


def test_observer_notifica_dos_puestos_y_audita():
    eventos = PublicadorEventos()
    bandeja, auditoria = [], []
    eventos.suscribir("pedido_pagado", NotificadorComerciantes(bandeja))
    eventos.suscribir("pedido_pagado", AuditoriaPedidos(auditoria))
    eventos.publicar("pedido_pagado", _evento())
    assert [aviso["puesto_id"] for aviso in bandeja] == ["P1", "P2"]
    assert auditoria == [{"evento": "pedido_pagado", "pedido_id": "PED-17"}]
    assert "celular" not in auditoria[0]  # privacidad


def test_observer_nuevo_suscriptor_no_exige_cambiar_publicador():
    eventos = PublicadorEventos()
    recibidos = []

    class SuscriptorExtra:
        def actualizar(self, evento, datos):
            recibidos.append((evento, datos["pedido_id"]))

    eventos.suscribir("pedido_pagado", SuscriptorExtra())
    eventos.publicar("pedido_pagado", _evento())
    assert recibidos == [("pedido_pagado", "PED-17")]


def test_decorator_agrega_registro_sin_modificar_aviso():
    eventos = PublicadorEventos()
    bandeja, registros = [], []
    suscriptor = ConRegistroEventos(NotificadorComerciantes(bandeja), registros)
    eventos.suscribir("pedido_pagado", suscriptor)
    eventos.publicar("pedido_pagado", _evento())
    assert len(bandeja) == 2
    assert registros == [{
        "tipo": "suscriptor_ejecutado",
        "evento": "pedido_pagado",
        "pedido_id": "PED-17",
    }]
