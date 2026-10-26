import uuid

class PasarelaPagoClient:
    """Simulación del servicio externo de pagos con su propia interfaz."""
    def cobrar_tarjeta(self, monto: float, token_tarjeta: str) -> dict:
        if token_tarjeta == "INVALIDO":
            raise ValueError("Tarjeta declinada por fondos insuficientes o datos erróneos.")
        if token_tarjeta == "TIMEOUT":
            raise ConnectionError("Timeout al conectar con la pasarela de pagos.")
        return {"status": "SUCCESS", "transaccion_id": f"PAY-{uuid.uuid4().hex[:8]}"}

class InventarioRepository:
    """Simulación del repositorio/servicio de inventario."""
    def __init__(self):
        self.stock = {"PROD-1": 10, "PROD-2": 0}

    def verificar_y_descontar(self, producto_id: str, cantidad: int) -> bool:
        if self.stock.get(producto_id, 0) >= cantidad:
            self.stock[producto_id] -= cantidad
            return True
        return False

    def devolver_stock(self, producto_id: str, cantidad: int):
        if producto_id in self.stock:
            self.stock[producto_id] += cantidad