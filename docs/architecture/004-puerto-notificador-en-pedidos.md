# ADR-004: Ubicar el puerto Notificador en el paquete pedidos

- Estado: Aceptado
- Fecha: 2026-10-10
- Decisores: Flores Nuñez Rodrigo Francisco, Jimenez Paredes Fabricio Gabriel, Bravo Arredondo Cristhian Matías

## Contexto
En el diagrama de paquetes del Lab 05 (E5) se detectó un ciclo entre `pedidos` y `notificaciones`: `ServicioPedidos` usa el puerto `Notificador` (RF-06), y la operación `notificarPedidoPuesto(pp)` recibe un `PedidoPuesto`, que pertenece a `pedidos`. El ADR-001 exige módulos con interfaces explícitas y sin dependencias cíclicas, y el ADR-003 define que la notificación por WhatsApp es asíncrona (QA-03, R-06). El equipo es pequeño (R-02) y el MVP debe salir en 1 mes (R-01), así que la solución debe ser simple.

## Alternativas consideradas
1. Dejar el puerto `Notificador` en `notificaciones`: es lo que ya existía, pero crea el ciclo `pedidos <-> notificaciones` y los dos módulos quedan acoplados.
2. Mover el puerto `Notificador` a `pedidos` (inversión de dependencia): `notificaciones` lo realiza con `WhatsAppNotificador` y solo depende de `pedidos`.
3. Crear un DTO de notificación en `compartido`: rompe el ciclo, pero agrega una clase y una conversión que no se justifican para el MVP.

## Decisión
Usaremos la alternativa 2. El puerto `Notificador` pertenece al paquete `pedidos`; el paquete `notificaciones` contiene el adaptador `WhatsAppNotificador`, que lo realiza. La dependencia queda en un solo sentido: `notificaciones -> pedidos`.

## Consecuencias
- Positivas: sin ciclos (C4); el dominio de pedidos no conoce WhatsApp; cambiar de canal (por ejemplo SMS) solo requiere un nuevo adaptador.
- Negativas / riesgos: `notificaciones` queda atado al modelo de `pedidos` (`PedidoPuesto`); si ese modelo cambia, el adaptador también debe cambiar.