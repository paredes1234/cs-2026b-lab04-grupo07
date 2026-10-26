import sqlite3
from src.despues.factory import PagoFactory
from src.despues.adaptadores import AdaptadorInventarioRepository

class ServicioPedidosProcesadorRefactorizado:
    """Servicio sin bloques if/elif para variaciones; utiliza Factory y Adapter/Strategy."""
    def __init__(self, inventario=None, db_path=":memory:"):
        self.inventario = inventario or AdaptadorInventarioRepository()
        self.db_path = db_path
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

    def confirmar_y_pagar(self, pedido_id: str, producto_id: str, cantidad: int, monto: float, token_tarjeta: str, max_reintentos: int = 1, tipo_pago: str = "TARJETA") -> dict:
        if cantidad <= 0 or monto <= 0:
            raise ValueError("La cantidad y el monto deben ser mayores a cero.")

        if not self.inventario.reservar_stock(producto_id, cantidad):
            raise RuntimeError("Stock insuficiente para procesar el pedido.")

        # Obtener la estrategia mediante la Factory (sin condicionales complejos)
        estrategia_pago = PagoFactory.crear_pago(tipo_pago)

        intento = 0
        transaccion_id = None
        while intento < max_reintentos:
            try:
                transaccion_id = estrategia_pago.procesar_pago(monto, token_tarjeta)
                break
            except ConnectionError as e:
                intento += 1
                if intento >= max_reintentos:
                    self.inventario.liberar_stock(producto_id, cantidad)
                    raise RuntimeError(f"Error de red tras {max_reintentos} reintentos: {str(e)}")
            except ValueError as e:
                self.inventario.liberar_stock(producto_id, cantidad)
                raise e

        conn = self._get_connection()
        conn.execute(
            "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?)",
            (pedido_id, producto_id, cantidad, monto, "PAGADO", transaccion_id)
        )
        conn.commit()
        if not self.conn:
            conn.close()

        return {
            "pedido_id": pedido_id,
            "estado": "PAGADO",
            "transaccion_id": transaccion_id
        }