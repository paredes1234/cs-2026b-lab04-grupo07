from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID, uuid4
from decimal import Decimal

class EstadoPedido(Enum):
    BORRADOR = "BORRADOR"
    PAGO_PENDIENTE = "PAGO_PENDIENTE"
    PAGADO = "PAGADO"
    CANCELADO = "CANCELADO"

class EstadoPedidoPuesto(Enum):
    RECIBIDO = "RECIBIDO"
    LISTO = "LISTO"
    RECOGIDO = "RECOGIDO"
    ENTREGADO = "ENTREGADO"
    RECHAZADO = "RECHAZADO"

class ModalidadEntrega(Enum):
    RECOJO = "RECOJO"
    DELIVERY = "DELIVERY"

@dataclass
class Cliente:
    id: UUID = field(default_factory=uuid4)
    nombre: str = ""

@dataclass
class Puesto:
    id: UUID = field(default_factory=uuid4)
    nombre: str = ""
    celular_whatsapp: str = ""

@dataclass
class Producto:
    id: UUID = field(default_factory=uuid4)
    nombre: str = ""
    precio: Decimal = Decimal("0.0")
    stock: int = 0

    def reservar_stock(self, cantidad: int) -> None:
        if self.stock < cantidad:
            raise ValueError("Stock insuficiente")
        self.stock -= cantidad

    def liberar_stock(self, cantidad: int) -> None:
        self.stock += cantidad

@dataclass
class LineaPedido:
    producto: Producto
    cantidad: int
    precio_unitario: Decimal

    def calcular_subtotal(self) -> Decimal:
        return self.precio_unitario * Decimal(self.cantidad)

@dataclass
class Pago:
    id: UUID = field(default_factory=uuid4)
    monto: Decimal = Decimal("0.0")
    referencia_yape: str = ""
    aprobado: bool = False

@dataclass
class PedidoPuesto:
    id: UUID = field(default_factory=uuid4)
    puesto: Puesto = field(default_factory=Puesto)
    estado: EstadoPedidoPuesto = EstadoPedidoPuesto.RECIBIDO
    lineas: List[LineaPedido] = field(default_factory=list)
    monto_devolver: Decimal = Decimal("0.0")

    def marcar_listo(self) -> None:
        self.estado = EstadoPedidoPuesto.LISTO

    def rechazar(self, motivo: str) -> None:
        self.estado = EstadoPedidoPuesto.RECHAZADO

    def registrar_recojo(self) -> None:
        self.estado = EstadoPedidoPuesto.RECOGIDO

    def registrar_entrega(self) -> None:
        self.estado = EstadoPedidoPuesto.ENTREGADO

@dataclass
class Pedido:
    id: UUID = field(default_factory=uuid4)
    cliente: Cliente = field(default_factory=Cliente)
    estado: EstadoPedido = EstadoPedido.BORRADOR
    modalidad: ModalidadEntrega = ModalidadEntrega.RECOJO
    lineas: List[LineaPedido] = field(default_factory=list)
    pedidos_puesto: List[PedidoPuesto] = field(default_factory=list)
    pago: Optional[Pago] = None

    def confirmar(self) -> None:
        if not self.lineas:
            raise ValueError("El pedido debe contener al menos una línea (C3)")
        for linea in self.lineas:
            linea.producto.reservar_stock(linea.cantidad)
        self.estado = EstadoPedido.PAGO_PENDIENTE

    def calcular_total(self) -> Decimal:
        return sum(linea.calcular_subtotal() for linea in self.lineas)

    def registrar_pago(self, pago: Pago) -> None:
        self.pago = pago
        self.estado = EstadoPedido.PAGADO

    def dividir_por_puesto(self) -> List[PedidoPuesto]:
        return self.pedidos_puesto

    def cancelar(self, motivo: str) -> None:
        self.estado = EstadoPedido.CANCELADO
        for linea in self.lineas:
            linea.producto.liberar_stock(linea.cantidad)

class PasarelaPago(ABC):
    @abstractmethod
    def cobrar(self, monto: Decimal, celular_yape: str, referencia: str) -> Pago:
        pass

class Notificador(ABC):
    @abstractmethod
    def notificar_pedido_puesto(self, pedido_puesto: PedidoPuesto) -> None:
        pass

class RepositorioPedidos(ABC):
    @abstractmethod
    def buscar(self, id: UUID) -> Optional[Pedido]:
        pass

    @abstractmethod
    def guardar(self, pedido: Pedido) -> None:
        pass

class YapeAdapter(PasarelaPago):
    def cobrar(self, monto: Decimal, celular_yape: str, referencia: str) -> Pago:
        raise NotImplementedError("Integración con la Pasarela de Yape")

class WhatsAppNotificador(Notificador):
    def notificar_pedido_puesto(self, pedido_puesto: PedidoPuesto) -> None:
        raise NotImplementedError("Integración con la API de WhatsApp")