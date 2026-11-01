"""Pedidos con reglas de mercado embebidas (alternativa A, sintética)."""


def monto_minimo(mercado_id):
    if mercado_id == "SAN_CAMILO":
        return 10
    elif mercado_id == "ALTIPLANO":
        return 0
    elif mercado_id == "RIO_SECO":
        return 15
    raise KeyError(mercado_id)
