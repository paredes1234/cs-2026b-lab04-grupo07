from abc import ABC, abstractmethod

class PuertoPago(ABC):
    """Interfaz abstracta para el servicio de pagos (DIP)."""
    @abstractmethod
    def procesar_pago(self, monto: float, token: str) -> str:
        """Procesa el pago y retorna el ID de transacción."""
        pass

class PuertoInventario(ABC):
    """Interfaz abstracta para el repositorio de inventario (DIP)."""
    @abstractmethod
    def reservar_stock(self, producto_id: str, cantidad: int) -> bool:
        """Reserva o descuenta el stock de un producto."""
        pass

    @abstractmethod
    def liberar_stock(self, producto_id: str, cantidad: int) -> None:
        """Libera o restaura el stock de un producto."""
        pass