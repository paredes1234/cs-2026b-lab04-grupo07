class Pedido:
    """Entidad de dominio que representa la lógica del pedido."""
    def __init__(self, pedido_id: str, producto_id: str, cantidad: int, monto: float):
        if cantidad <= 0 or monto <= 0:
            raise ValueError("La cantidad y el monto deben ser mayores a cero.")
        self.id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.monto = monto
        self.estado = "CREADO"
        self.transaccion_id = None

    def marcar_como_pagado(self, transaccion_id: str):
        self.estado = "PAGADO"
        self.transaccion_id = transaccion_id