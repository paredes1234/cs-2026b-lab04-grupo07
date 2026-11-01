"""Catálogo con reglas de mercado embebidas (alternativa A, sintética)."""


def horario_atencion(mercado_id):
    if mercado_id == "SAN_CAMILO":
        return (6, 18)
    elif mercado_id == "ALTIPLANO":
        return (5, 14)
    elif mercado_id == "RIO_SECO":
        return (6, 15)
    raise KeyError(mercado_id)
