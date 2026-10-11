# Historia de usuario crítica — San Camilo en Línea

Flujo elegido para el Lab 05 (Tabla 7, caso 7): **pedido a varios puestos con pago único**.

```text
HU-03: Como cliente, quiero armar un pedido con productos de varios puestos
       y pagarlo con un solo Yape, para no tener que pagarle a cada
       comerciante por separado.
       (Deriva de RF-03, RF-04, RF-05 y RF-06)

Criterios de aceptación
- CA-1 (éxito): Dado un pedido en BORRADOR con productos de 2 o más puestos,
  stock suficiente y una modalidad de entrega elegida (recojo o delivery),
  cuando lo confirmo y el pago con Yape es aprobado, entonces el pedido queda
  PAGADO, se crea un PedidoPuesto por cada puesto en estado RECIBIDO y cada
  comerciante recibe por WhatsApp solo los productos de su puesto.
- CA-2 (error de pago): Dado un pedido confirmado, cuando el pago es rechazado o
  no hay respuesta en 15 min, entonces el pedido queda CANCELADO, no se crea
  ningún PedidoPuesto y el stock reservado se libera.
- CA-3 (rechazo parcial): Dado un pedido PAGADO, cuando un comerciante rechaza su
  PedidoPuesto porque no tiene el producto, entonces solo ese PedidoPuesto queda
  RECHAZADO, se registra el monto a devolver al cliente y los demás puestos
  siguen su curso.
```

## Trazabilidad con los drivers

| Criterio | Drivers que cubre |
|---|---|
| CA-1 | RF-03 (varios puestos), RF-04 (modalidad), RF-05 (Yape), RF-06 (WhatsApp al comerciante); QA-03 y ADR-003 (la notificación no bloquea el pago) |
| CA-2 | RF-05, R-06 (Yape puede fallar o no responder) |
| CA-3 | RF-03, RF-06 (el comerciante responde por su parte del pedido) |

## Supuestos

Lo que la historia no define y el equipo decidió:

1. El tiempo límite de pago es de **15 min**, igual al ejemplo de la guía. (Confirmado por el equipo.)
2. El pago único entra a una cuenta de la plataforma. **La liquidación a cada puesto queda fuera del MVP** (R-01).
3. La devolución de un PedidoPuesto rechazado se **registra** en el sistema, pero el reembolso se hace **manualmente** fuera de la plataforma.
4. La modalidad de entrega (recojo o delivery) se elige **una vez para todo el pedido** y vale para todos sus PedidoPuesto. (Confirmado por el equipo.)
5. No se guarda el número de Yape del cliente: se usa solo para el cobro (R-04, Ley 29733).
