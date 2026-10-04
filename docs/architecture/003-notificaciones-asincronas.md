# ADR-003: Enviar las confirmaciones de WhatsApp de forma asíncrona con reintentos

- Estado: Aceptado
- Fecha: 2026-10-01
- Decisores: Flores Nuñez Rodrigo Francisco, Jimenez Paredes Fabricio Gabriel, Bravo Arredondo Cristhian Matías

## Contexto
Cada pedido debe confirmarse por WhatsApp al comerciante (RF-06). WhatsApp es un servicio
externo que puede estar indisponible (R-06). El escenario QA-03 exige que, si el servicio
externo no responde, el pedido permanezca registrado (0 pedidos perdidos) y la notificación se
reintente en ≤ 10 min. Además, el cliente no debe esperar a un tercero para ver su pedido
confirmado (QA-02), y el equipo es pequeño (R-02) con presupuesto bajo (R-03).

## Alternativas consideradas
1. Llamada síncrona a WhatsApp dentro de la petición del pedido: la más simple, pero si
   WhatsApp falla o demora, el pedido se retrasa o falla.
2. Cola de tareas en el mismo servidor (p. ej., Celery con Redis): el pedido se guarda primero
   y la notificación se encola con reintentos automáticos.
3. Broker de mensajería dedicado (p. ej., RabbitMQ): más robusto, pero agrega un servicio
   completo que operar, sobredimensionado para un MVP.

## Decisión
Usaremos una cola de tareas ejecutada en el mismo servidor. El módulo Carrito y Pedidos
registra el pedido en la base de datos y encola la tarea; el módulo Notificaciones la envía por
WhatsApp y la reintenta con espera creciente hasta lograrlo, con el primer reintento antes de
10 min. Una notificación no entregada queda marcada como pendiente en la base de datos.

## Consecuencias
- Positivas: el pedido nunca se pierde por una falla de WhatsApp (QA-03); la respuesta al
  cliente es rápida (QA-02); la cola también sirve de caché del catálogo sin agregar servicios.
- Negativas / riesgos: se agregan dos procesos que operar y monitorear (worker y cola);
  la notificación puede llegar con retraso (consistencia eventual); si la cola pierde tareas,
  deben recuperarse desde las notificaciones marcadas como pendientes en la base de datos.
