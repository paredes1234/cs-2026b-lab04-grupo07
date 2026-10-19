# E1. Inventario del modelo C4 — San Camilo en Línea

**Caso:** San Camilo en Línea (grupo 07). **Alcance:** E1, E2 y E3 del Laboratorio 06. El modelo es la continuidad de los Laboratorios 04 y 05, no el caso AgroConecta que usa el profesor como ejemplo.

| Elemento | Tipo C4 | Descripción / responsabilidad | Fuente del trabajo previo |
|---|---|---|---|
| Cliente | Persona | Busca productos de varios puestos, realiza pedidos y paga. | Lab 04: `docs/architecture/drivers.md` (RF-03 a RF-05); Lab 05: `docs/design/historia.md` (HU-03). |
| Comerciante | Persona | Administra productos y prepara los pedidos de su puesto. | Lab 04: `docs/architecture/drivers.md` (RF-01, RF-06). |
| Repartidor | Persona | Consulta los pedidos asignados y registra la entrega. | Lab 04: `docs/architecture/drivers.md` (RF-04, RF-07). |
| San Camilo en Línea | Sistema de software (propio) | Compras multipuesto con pago único, recojo/delivery y confirmaciones. | Caso y ADR-001 del Lab 04. |
| Pasarela de pago Yape | Sistema de software externo | Se solicita un cobro mediante el puerto PasarelaPago. | Lab 04: RF-05 y ADR-001; Lab 05: `docs/design/clases.puml`. |
| Servicio de WhatsApp | Sistema de software externo | Recibe solicitudes de envío de notificaciones a comerciantes. | Lab 04: RF-06 y ADR-003; Lab 05: `docs/design/secuencia-pedido-multipuesto.puml`. |
| Aplicación web progresiva | Contenedor | Interfaz móvil para clientes, comerciantes y repartidores. | Lab 04: ADR-002 (PWA). |
| Aplicación web / API | Contenedor | Monolito modular que procesa casos de uso y ofrece funciones por HTTP. | Lab 04: ADR-001 y vista de despliegue (`diagrams/despliegue.py`). |
| Worker de notificaciones | Contenedor | Realiza notificaciones asíncronas con reintentos. | Lab 04: ADR-003 y `diagrams/despliegue.py`. |
| Base de datos relacional | Contenedor / almacén | Guarda datos de clientes, productos, pedidos y pagos. | Lab 04: ADR-001 y `diagrams/despliegue.py`. |
| Cola y caché | Contenedor / almacén | Redis para trabajos Celery y caché. | Lab 04: ADR-003 y `diagrams/despliegue.py`. |
| Catálogo | Componente (dentro de API) | Puestos, productos y reserva/liberación de stock. | Lab 05: `docs/design/paquetes.puml`, `docs/design/clases.puml`. |
| Pedidos | Componente (dentro de API) | Pedido, LineaPedido, PedidoPuesto, orquestación del pago. | Lab 05: `docs/design/paquetes.puml` y diagrama de secuencia. |
| Pagos | Componente (dentro de API) | Contrato PasarelaPago y adaptador del cobro. | Lab 05: `docs/design/paquetes.puml` y `docs/design/clases.puml`. |
| Notificaciones | Componente (dentro de API) | Implementación de Notificador y envío de mensajes. | Lab 05: `docs/design/paquetes.puml`, ADR-004. |
| Entrega | Componente (dentro de API) | Recojo, delivery y estados de PedidoPuesto. | Lab 05: `docs/design/paquetes.puml`, estados y actividades. |
| Compartido | Componente (dentro de API) | Identificadores y tipos comunes. | Lab 05: `docs/design/paquetes.puml`. |

## Verificación frente a los ADR y el UML

1. **ADR-001 (monolito modular):** los seis componentes son módulos dentro de una sola aplicación/API; no son seis microservicios ni seis contenedores C4.
2. **ADR-002 (PWA):** la PWA es un contenedor cliente; no es una aplicación móvil nativa independiente.
3. **ADR-003 (notificaciones):** Celery y Redis permiten encolar mensajes para que una falla de WhatsApp no pierda pedidos.
4. **ADR-004 del Lab 05:** el puerto `Notificador` pertenece a `pedidos` y `notificaciones` lo implementa. En C4, la dependencia entre estos componentes se dibuja de **Notificaciones hacia Pedidos**, no en ambos sentidos.
5. **Yape:** se considera un sistema externo, no un módulo alojado dentro de nuestra aplicación. Se usa el puerto `PasarelaPago`, sin afirmar que existe una API pública de Yape accesible directamente.
6. **No agregar Plin:** aunque la guía docente propone Yape/Plin para el caso 7, en los Labs 04 y 05 del grupo se describe pago con Yape. Agregar Plin requeriría una decisión adicional.

## Decisiones por confirmar antes de presentar E2

- **Motor de base de datos:** el Lab 04 dice "base de datos relacional" sin fijar motor ni versión. En `workspace.dsl` se propone **PostgreSQL 16** para cumplir el requisito E2 de tecnología concreta. El equipo debe aceptarlo y documentar la decisión; si ya eligió otro motor en GitHub, debe reemplazarse aquí y en el DSL.
- **Implementación de la PWA:** `HTML/CSS/JavaScript + Service Worker` es una concreción mínima de la PWA, no una afirmación de que el proyecto usa React.
- **Interfaz web/API:** el documento del Lab 04 menciona Django, y el esqueleto del Lab 05 está en Python. El DSL usa "Python / Django (HTTP/JSON)" sin agregar Django REST Framework si no fue decidido expresamente.
- **Validación C4:** este borrador debe pasar `structurizr validate` antes de subir los tres commits como entrega comprobada.
