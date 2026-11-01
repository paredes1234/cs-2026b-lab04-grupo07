"""Entrega con reglas de mercado embebidas (alternativa A, sintética)."""


def costo_delivery(mercado_id):
    if mercado_id == "SAN_CAMILO":
        return 5
    elif mercado_id == "ALTIPLANO":
        raise ValueError("Altiplano no ofrece delivery")
    elif mercado_id == "RIO_SECO":
        return 7
    raise KeyError(mercado_id)
