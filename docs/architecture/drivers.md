# Drivers arquitectónicos — San Camilo en Línea

## Contexto del caso

**San Camilo en Línea** es una plataforma para realizar pedidos a los puestos del Mercado San Camilo, con opción de recojo o delivery. Los actores principales son el **cliente**, el **comerciante** y el **repartidor**. El MVP contempla catálogo por puesto, pedidos con productos de varios puestos, pago con Yape y confirmación por WhatsApp al comerciante.

El atributo de calidad crítico es la **capacidad de interacción (usabilidad)**: un comerciante con poca experiencia digital debe poder publicar un producto en **máximo 3 toques desde un celular de gama baja**.

## 1. Requisitos funcionales clave

| ID | Requisito | Actor | Prioridad |
|---|---|---|---|
| RF-01 | Publicar, modificar y retirar productos de su puesto. | Comerciante | Alta |
| RF-02 | Consultar el catálogo de productos organizado por puesto. | Cliente | Alta |
| RF-03 | Crear un pedido con productos de diferentes puestos del mercado. | Cliente | Alta |
| RF-04 | Seleccionar recojo en el mercado o entrega por delivery. | Cliente | Alta |
| RF-05 | Registrar el pago del pedido mediante Yape. | Cliente | Alta |
| RF-06 | Recibir confirmación del pedido mediante WhatsApp. | Comerciante | Alta |
| RF-07 | Consultar pedidos de delivery asignados y actualizar su estado. | Repartidor | Media |

## 2. Atributos de calidad priorizados

1. **Capacidad de interacción (usabilidad)** — Es el atributo crítico del caso; el comerciante debe publicar productos con una interacción mínima desde un celular de gama baja.
2. **Rendimiento** — El catálogo y los pedidos deben responder adecuadamente desde conexiones móviles.
3. **Disponibilidad y fiabilidad** — Una falla temporal de un servicio externo no debe provocar la pérdida de un pedido.
4. **Modificabilidad** — Debe ser posible cambiar módulos como pagos, catálogo o delivery sin afectar innecesariamente al resto del sistema.
5. **Seguridad** — Deben protegerse los datos de usuarios, pedidos y operaciones asociadas al pago.

## 3. Restricciones

| ID | Tipo | Restricción |
|---|---|---|
| R-01 | Plazo | El MVP debe estar en producción en un plazo máximo de 1 mes. |
| R-02 | Equipo | **Completar antes de entregar:** indicar el número real de integrantes del grupo y las tecnologías que realmente dominan. |
| R-03 | Presupuesto | El presupuesto es bajo; se debe minimizar el uso de infraestructura y servicios de pago innecesarios. |
| R-04 | Normativa | El tratamiento de datos personales debe considerar la normativa peruana de protección de datos aplicable. |
| R-05 | Dispositivos | La interfaz debe funcionar correctamente desde navegadores móviles y celulares de gama baja. |
| R-06 | Integraciones | WhatsApp y el mecanismo de pago con Yape son dependencias externas; su indisponibilidad no debe impedir registrar un pedido. |

> **Nota:** R-02 debe reemplazarse con los datos reales del grupo, porque la guía exige que la restricción de equipo no sea copiada del ejemplo.

## 4. Escenarios de atributos de calidad

| ID | Atributo | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida |
|---|---|---|---|---|---|---|---|
| QA-01 | Capacidad de interacción | Comerciante con poca experiencia digital | Desea publicar un nuevo producto | Celular de gama baja, operación normal | Interfaz de gestión de productos | El sistema permite ingresar los datos básicos y publicar el producto | **Publicación en ≤ 3 toques** |
| QA-02 | Rendimiento | Cliente | Consulta el catálogo de un puesto | Conexión móvil, operación normal | Módulo Catálogo | El sistema obtiene y muestra los productos disponibles | **p95 ≤ 2 s** |
| QA-03 | Disponibilidad / fiabilidad | Servicio externo de WhatsApp | El servicio no responde al enviar una confirmación | Operación normal | Módulo de Notificaciones | El pedido permanece registrado y la notificación se programa para reintento | **0 pedidos perdidos y reintento ≤ 10 min** |

> QA-01 usa el dato medible definido por el caso. Los valores de QA-02 y QA-03 son metas verificables propuestas por el equipo para completar los escenarios exigidos por la guía.
