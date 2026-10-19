# Bitácora de IA — Laboratorio 06 (borrador inicial)

> El Lab 06 exige registrar las interacciones con IA. A continuación se ofrece el registro de la ayuda en esta conversación; el equipo debe completar los campos de verificación/decisión tras revisar el modelo. No se simulan interacciones adicionales.

| Fecha | Herramienta | Solicitud / prompt de trabajo | Propuesta | Verificación | Decisión |
|---|---|---|---|---|---|
| 2026-10-18 | ChatGPT (GPT-6) | Revisar la guía docente del Lab 06 y el caso San Camilo en Línea de los Labs 04–05; preparar E1 (inventario/contexto), E2 (contenedores) y E3 (componentes) en un único `workspace.dsl`, sin copiar AgroConecta. | Inventario de personas y sistemas; contenedores PWA, API, Celery, base relacional y Redis; componentes conforme a `paquetes.puml`. | **Pendiente del equipo:** contrastar rutas y archivos reales, confirmar motor de BD, ejecutar Structurizr CLI y revisar C4. | **Pendiente de decisión:** aceptar o corregir cada punto después de las verificaciones. |

## Hallazgos y correcciones propuestos (no atribuir a una IA distinta)

| Posible problema de diseño | Verificación basada en los Labs 04–05 | Corrección sugerida |
|---|---|---|
| Copiar "AgroConecta", "Productor" o "Reportes" del ZIP del docente. | El caso del equipo es San Camilo en Línea, con Cliente, Comerciante y Repartidor. | Usar los nombres y responsabilidades del grupo. |
| Representar WhatsApp o Yape como contenedores propios. | Ambos se tratan como integraciones externas en el ADR-001. | Modelarlos como `softwareSystem` con etiqueta `Externo`. |
| Representar módulos Catálogo y Pedidos como contenedores separados. | El ADR-001 determina un monolito modular. | Modelarlos como `component` dentro de la aplicación/API. |
| Crear dependencias mutuas Pedidos <-> Notificaciones. | El ADR-004 del Lab 05 coloca el puerto Notificador en Pedidos. | Dibujar Notificaciones -> Pedidos para la realización del puerto. |
| Afirmar que PostgreSQL 16 fue aprobado en el Lab 04. | El Lab 04 especifica base relacional, sin identificar motor. | Solicitar confirmación y documentar la elección en los ADR antes de entregar. |

## Prompt IA 1 — versión adaptada y reproducible para E1

> Actúa como arquitecto de software experto en modelo C4 y Structurizr DSL. Trabajamos en **San Camilo en Línea**, plataforma de pedidos multipuesto del Mercado San Camilo de Arequipa. Usa como fuente el inventario `docs/architecture/c4/inventario.md` y el ADR-001 del Laboratorio 04, que define un **monolito modular**; respeta también las decisiones de PWA (ADR-002), WhatsApp asíncrono (ADR-003) y el puerto `Notificador` en `pedidos` (ADR-004 del Lab 05). Genera un borrador `workspace.dsl` que contenga los usuarios Cliente, Comerciante y Repartidor, el sistema San Camilo en Línea, la pasarela de pago Yape y WhatsApp como sistemas externos etiquetados `Externo`. Incluye relaciones con intención explícita, una vista `systemContext` con título y descripción y `!identifiers hierarchical`. Para la futura extensión E2/E3 reserva una estructura coherente con PWA, API, worker Celery, base de datos relacional y Redis, y con los módulos Catálogo, Pedidos, Pagos, Notificaciones, Entrega y Compartido. No dibujes Docker como contenedor C4, no inventes Kafka ni Kubernetes y no sustituyas el caso por AgroConecta. Devuelve el código DSL y señala cualquier decisión tecnológica todavía sin confirmar.

Este texto es una **versión explícita para documentar y reproducir el trabajo**. El registro original de la interacción en ChatGPT fue una solicitud de revisar la guía del Lab 06 y preparar E1–E3 a partir de los Labs 04–05; por ello, no se presenta el texto anterior como una transcripción literal de ese mensaje. El equipo debe registrar las correcciones y la fecha reales de la validación final.
