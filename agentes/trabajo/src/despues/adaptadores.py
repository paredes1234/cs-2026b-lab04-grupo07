from src.despues.puertos import PuertoPago, PuertoInventario
from src.antes.externos import PasarelaPagoClient, InventarioRepository

class AdaptadorPasarelaPago(PuertoPago):
    """Adaptador para encapsular la interfaz concreta de PasarelaPagoClient."""
    def __init__(self, cliente_pago: PasarelaPagoClient = None):
        self.cliente = cliente_pago or PasarelaPagoClient()

    def procesar_pago(self, monto: float, token: str) -> str:
        resultado = self.cliente.cobrar_tarjeta(monto, token)
        return resultado["transaccion_id"]

class AdaptadorInventarioRepository(PuertoInventario):
    """Adaptador para encapsular la interfaz concreta de InventarioRepository."""
    def __init__(self, repo_inventario: InventarioRepository = None):
        self.repo = repo_inventario or InventarioRepository()

    def reservar_stock(self, producto_id: str, cantidad: int) -> bool:
        return self.repo.verificar_y_descontar(producto_id, cantidad)

    def liberar_stock(self, producto_id: str, cantidad: int) -> None:
        self.repo.devolver_stock(producto_id, cantidad)