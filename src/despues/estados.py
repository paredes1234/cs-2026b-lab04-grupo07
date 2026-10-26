from abc import ABC

class TransicionEstadoInvalida(ValueError):
    """Excepción lanzada cuando se intenta una transición no permitida por el patrón State."""
    pass

class EstadoPedidoPuesto(ABC):
    """Clase base abstracta que prohíbe por defecto todas las transiciones."""
    
    @property
    def nombre(self) -> str:
        return "DESCONOCIDO"

    def marcar_listo(self, pedido) -> None:
        raise TransicionEstadoInvalida(f"No se puede marcar listo un pedido en estado {self.nombre}")

    def rechazar(self, pedido, motivo: str) -> None:
        raise TransicionEstadoInvalida(f"No se puede rechazar un pedido en estado {self.nombre}")

    def registrar_recojo(self, pedido) -> None:
        raise TransicionEstadoInvalida(f"No se puede registrar recojo en estado {self.nombre}")

    def registrar_entrega(self, pedido) -> None:
        raise TransicionEstadoInvalida(f"No se puede registrar entrega en estado {self.nombre}")


class EstadoRecibido(EstadoPedidoPuesto):
    @property
    def nombre(self) -> str:
        return "RECIBIDO"

    def marcar_listo(self, pedido) -> None:
        pedido.estado_actual = EstadoListo()

    def rechazar(self, pedido, motivo: str) -> None:
        pedido.motivo_rechazo = motivo
        pedido.estado_actual = EstadoRechazado()


class EstadoListo(EstadoPedidoPuesto):
    @property
    def nombre(self) -> str:
        return "LISTO"

    def registrar_recojo(self, pedido) -> None:
        pedido.estado_actual = EstadoRecogido()

    def registrar_entrega(self, pedido) -> None:
        pedido.estado_actual = EstadoEntregado()


class EstadoRecogido(EstadoPedidoPuesto):
    @property
    def nombre(self) -> str:
        return "RECOGIDO"

    def registrar_entrega(self, pedido) -> None:
        pedido.estado_actual = EstadoEntregado()


class EstadoEntregado(EstadoPedidoPuesto):
    """Estado final del ciclo."""
    @property
    def nombre(self) -> str:
        return "ENTREGADO"


class EstadoRechazado(EstadoPedidoPuesto):
    """Estado final del ciclo."""
    @property
    def nombre(self) -> str:
        return "RECHAZADO"