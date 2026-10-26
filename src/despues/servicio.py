
import sqlite3
import logging

from src.despues.factory import PagoFactory
from src.despues.adaptadores import (
    AdaptadorInventarioRepository,
    AdaptadorPasarelaPago
)
from src.despues.eventos import PublicadorEventos


_logger = logging.getLogger(__name__)


class ServicioPedidosProcesadorRefactorizado:
    """
    Servicio de pedidos que utiliza los patrones
    Factory, Strategy, Adapter y Observer.
    """

    def __init__(
        self,
        inventario=None,
        db_path=":memory:",
        publicador_eventos=None,
        fabrica_pagos=None
    ):
        # Adaptador para gestionar el inventario
        self.inventario = (
            inventario
            if inventario is not None
            else AdaptadorInventarioRepository()
        )

        self.db_path = db_path

        # Factory: administrar las estrategias de pago
        self.fabrica_pagos = (
            fabrica_pagos
            if fabrica_pagos is not None
            else PagoFactory()
        )

        # Registrar el adaptador predeterminado
        if fabrica_pagos is None:
            self.fabrica_pagos.registrar(
                "TARJETA",
                AdaptadorPasarelaPago()
            )

        # Observer: administrar suscriptores y eventos
        self.publicador_eventos = (
            publicador_eventos
            if publicador_eventos is not None
            else PublicadorEventos()
        )

        # Inicializar la conexión a la base de datos
        self.conn = (
            sqlite3.connect(self.db_path)
            if self.db_path == ":memory:"
            else None
        )

        self._init_db()

    def _get_connection(self):
        """Obtiene la conexión a la base de datos."""
        if self.conn:
            return self.conn

        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Crea la tabla de pedidos si no existe."""
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

    def confirmar_y_pagar(
        self,
        pedido_id: str,
        producto_id: str,
        cantidad: int,
        monto: float,
        token_tarjeta: str,
        max_reintentos: int = 1,
        tipo_pago: str = "TARJETA",
        puestos=None
    ) -> dict:
        """
        Confirma y procesa el pago de un pedido.

        Después de guardar exitosamente el pedido,
        publica el evento pedido_pagado mediante Observer.
        """

        # 1. Validar los datos del pedido
        if cantidad <= 0 or monto <= 0:
            raise ValueError(
                "La cantidad y el monto deben ser mayores a cero."
            )

        # 2. Verificar y reservar el inventario
        if not self.inventario.reservar_stock(
            producto_id,
            cantidad
        ):
            raise RuntimeError(
                "Stock insuficiente para procesar el pedido."
            )

        # 3. Obtener la estrategia mediante Factory
        estrategia_pago = self.fabrica_pagos.obtener(tipo_pago)

        # 4. Procesar el pago con reintentos
        intento = 0
        transaccion_id = None

        while intento < max_reintentos:
            try:
                transaccion_id = estrategia_pago.procesar_pago(
                    monto,
                    token_tarjeta
                )
                break

            except ConnectionError as e:
                intento += 1

                if intento >= max_reintentos:
                    self.inventario.liberar_stock(
                        producto_id,
                        cantidad
                    )

                    raise RuntimeError(
                        f"Error de red tras "
                        f"{max_reintentos} reintentos: {str(e)}"
                    ) from e

            except ValueError:
                self.inventario.liberar_stock(
                    producto_id,
                    cantidad
                )
                raise

        # 5. Guardar el pedido pagado en SQLite
        conn = self._get_connection()

        conn.execute(
            "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?)",
            (
                pedido_id,
                producto_id,
                cantidad,
                monto,
                "PAGADO",
                transaccion_id
            )
        )

        conn.commit()

        if not self.conn:
            conn.close()

        # 6. Observer: publicar el evento de pago
        # Solo después de guardar exitosamente el pedido.
        datos_evento = {
            "pedido_id": pedido_id,
            "producto_id": producto_id,
            "puestos": (
                list(puestos)
                if puestos is not None
                else []
            )
        }

        try:
            self.publicador_eventos.publicar(
                "pedido_pagado",
                datos_evento
            )

        except Exception:
            # Un fallo de notificación no debe
            # provocar un aparente fallo de pago.
            _logger.exception(
                "Fallo al notificar el pedido %s ya guardado",
                pedido_id
            )

        # 7. Devolver el resultado del pedido
        return {
            "pedido_id": pedido_id,
            "estado": "PAGADO",
            "transaccion_id": transaccion_id
        }
