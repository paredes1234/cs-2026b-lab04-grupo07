import sqlite3
from src.antes.externos import PasarelaPagoClient, InventarioRepository

class ServicioPedidosProcesador:
    """Versión 'antes': Monolítica y acoplada a implementaciones concretas."""
    def __init__(self, db_path=":memory:"):
        self.pasarela = PasarelaPagoClient()
        self.inventario = InventarioRepository()
        self.db_path = db_path
        # Si es en memoria, mantenemos una conexión activa para que la DB no se destruya
        self.conn = sqlite3.connect(self.db_path) if self.db_path == ":memory:" else None
        self._init_db()

    def _get_connection(self):
        if self.conn:
            return self.conn
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id TEXT PRIMARY KEY,
                producto_id TEXT,
                cantidad INTEGER,
                monto REAL,
                estado TEXT,
                transaccion_id TEXT
            )
        """)
        conn.commit()
        if not self.conn:
            conn.close()

    def confirmar_y_pagar(self, pedido_id: str, producto_id: str, cantidad: int, monto: float, token_tarjeta: str, max_reintentos: int = 1) -> dict:
        if cantidad <= 0 or monto <= 0:
            raise ValueError("La cantidad y el monto deben ser mayores a cero.")

        # 1. Verificar e inventariar
        if not self.inventario.verificar_y_descontar(producto_id, cantidad):
            raise RuntimeError("Stock insuficiente para procesar el pedido.")

        # 2. Intentar Cobro con reintentos
        intento = 0
        pago_exitoso = False
        res_pago = None
        
        while intento < max_reintentos and not pago_exitoso:
            try:
                res_pago = self.pasarela.cobrar_tarjeta(monto, token_tarjeta)
                pago_exitoso = True
            except ConnectionError as e:
                intento += 1
                if intento >= max_reintentos:
                    self.inventario.devolver_stock(producto_id, cantidad)
                    raise RuntimeError(f"Error de red tras {max_reintentos} reintentos: {str(e)}")
            except ValueError as e:
                self.inventario.devolver_stock(producto_id, cantidad)
                raise e

        # 3. Persistir en DB
        conn = self._get_connection()
        conn.execute(
            "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?)",
            (pedido_id, producto_id, cantidad, monto, "PAGADO", res_pago["transaccion_id"])
        )
        conn.commit()
        if not self.conn:
            conn.close()

        return {
            "pedido_id": pedido_id,
            "estado": "PAGADO",
            "transaccion_id": res_pago["transaccion_id"]
        }