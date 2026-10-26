from src.despues.estados import EstadoRecibido

class PedidoPuesto:
    """Entidad principal que delega su comportamiento de ciclo de vida al patrón State."""
    def __init__(self, id_puesto: str, producto_id: str, cantidad: int, monto: float):
        if cantidad <= 0 or monto <= 0:
            raise ValueError("La cantidad y el monto deben ser mayores a cero.")
        self.id_puesto = id_puesto
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.monto = monto
        self.transaccion_id = None
        self.motivo_rechazo = None
        self.estado_actual = EstadoRecibido()

    @property
    def estado(self) -> str:
        return self.estado_actual.nombre

    def marcar_listo(self) -> None:
        self.estado_actual.marcar_listo(self)

    def rechazar(self, motivo: str) -> None:
        self.estado_actual.rechazar(self, motivo)

    def registrar_recojo(self) -> None:
        self.estado_actual.registrar_recojo(self)

    def registrar_entrega(self) -> None:
        self.estado_actual.registrar_entrega(self)