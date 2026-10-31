"""VIOLACION DE PRUEBA (FF-06b): regla de mercado escrita fuera de src/mercados."""


def descuento(mercado_id, monto):
    if mercado_id == "ALTIPLANO":
        return monto * 0.95
    return monto
