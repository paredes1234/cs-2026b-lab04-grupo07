# Bitácora de IA — Laboratorio 06 (borrador inicial)

> El Lab 06 exige registrar las interacciones con IA. A continuación se ofrece el registro de la ayuda en esta conversación; el equipo debe completar los campos de verificación/decisión tras revisar el modelo. No se simulan interacciones adicionales.

| Fecha | Herramienta | Solicitud / prompt de trabajo | Propuesta | Verificación | Decisión |
|---|---|---|---|---|---|
| 2026-10-18 | ChatGPT (GPT-6) | Revisar la guía docente del Lab 06 y el caso San Camilo en Línea de los Labs 04–05; preparar E1 (inventario/contexto), E2 (contenedores) y E3 (componentes) en un único `workspace.dsl`, sin copiar AgroConecta. | Inventario de personas y sistemas; contenedores PWA, API, Celery, base relacional y Redis; componentes conforme a `paquetes.puml`. | **Pendiente del equipo:** contrastar rutas y archivos reales, confirmar motor de BD, ejecutar Structurizr CLI y revisar C4. | **Pendiente de decisión:** aceptar o corregir cada punto después de las verificaciones. |
| 18/10/2026 | Claude Code (Opus 5.5) | Validar `workspace.dsl` con Structurizr CLI y, si la vista dinámica falla, hacer la corrección mínima. | `validate` falla en la línea 109: el paso 7 `notificaciones -> redis` no existe en el modelo. Propone usar la relación existente `pedidos -> redis` (línea 64). | Se ejecutó `validate` antes (falla) y después (código 0). La relación de la línea 64 tiene la misma tecnología. Los aliases `bd` y `redis` ya eran correctos. Contradicción con E4.2: se corrige el artefacto equivocado (sección III de la guía). | Aceptada (commit `fb95ec5`; P3 en `revision-c4.md`). |
| 18/10/2026 | Claude Code (Opus 5.5) | Revisar `export/` e `img/` de E6 y, si no corresponden al modelo, regenerarlos desde `workspace.dsl`. | Detecta que los 10 archivos de `export/` son de un "Sistema ERP Multimodular" (SUNAT, API Gateway, FastAPI, AWS) y que `img/` no existe. Regenera las 5 vistas en C4-PlantUML y Mermaid y los 5 PNG (Paso 4 de la guía). | Se revisaron los 5 PNG: son de San Camilo, con los nombres y tecnologías del `.dsl`. Una búsqueda de "ERP/SUNAT/FastAPI/AWS" en `export/` e `img/` no encontró nada. `contexto-manual.puml` y `comparacion.md` no se tocaron. | Aceptada (commit `8c8f838`; P1 en `revision-c4.md`). |
| 18/10/2026 | Claude Code (Opus 5.5) | Revisión C4 y explicación con prompts **adaptados** (sin la guía): lista de c4model.com sobre el `.dsl` y "explica esta arquitectura en 120 palabras para un público no técnico". | `revision-c4.md` con 13 criterios propios, 11 hallazgos de la IA (3 falsos positivos) y `explicacion.md` de 118 palabras. | No usaba la Tabla 3 ni los Prompts IA 2 y 3 de la guía, como exige E7. | Rechazada: se rehízo con los prompts oficiales de la guía (commits `eba91f1` y `ec1e63a` revertidos en `41ea28f` y `04c3890`). |
| 19/10/2026 | Claude Code (Opus 5.5) | Prompt IA 2 oficial (Paso 10) sobre los 5 `.puml` de `export/`. | Tabla de 45 filas (vista, pregunta, cumple, evidencia, corrección): 11 "No". Externos como `System(...)`, acrónimos, dos flechas a WhatsApp, `worker → api` con "Celery/Python", contexto sin protocolo y elementos duplicados en `ConfirmarYPagar.puml`. | Cada "No" se contrastó con `workspace.dsl` y los PNG. 2 falsos positivos: FP-1 (protocolo en nivel 1, Tabla 8 de la guía) y FP-2 (los elementos duplicados en el `.puml` salen una sola vez en el PNG). | Corregida: se aceptan P4, P6, P10 y los acrónimos; se rechazan FP-1 y FP-2. Ver "Segundo revisor (IA)" en `revision-c4.md`. |
| 19/10/2026 | Claude Code (Opus 5.5) | Prompt IA 3 oficial (Paso 11), dirigido a la directiva de la asociación de comerciantes, sobre `export/Contexto.puml`. | Explicación de 118 palabras: qué hace el sistema, las 3 personas, Yape y WhatsApp, y "si alguno de esos servicios falla, los pedidos no se pierden". | Cada frase se buscó en `workspace.dsl`. El modelo no tiene comportamiento ante fallas de Yape (la dinámica solo cubre CA-1); los reintentos solo existen para WhatsApp (líneas 23 y 46). El repartidor "actualiza su estado" (línea 34), no "avisa cuando completa". | Corregida: `explicacion.md` con 112 palabras y la tabla "Correcciones aplicadas". |

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

## Anexo: prompts oficiales usados en E7 (19/10/2026)

**Prompt IA 2 — Auditor C4 (Paso 10 de la guía, textual):**

> Actúa como revisor de diagramas de arquitectura. Evalúa estas vistas exportadas de un modelo C4 [pegar los .puml o adjuntar las imágenes] con la lista de revisión de c4model.com: generales, elementos y relaciones.
> Responde en una tabla (vista, pregunta de la lista, cumple sí/no, evidencia, corrección sugerida).
> No inventes problemas: si algo cumple, indícalo.

Se pegaron los 5 archivos de `docs/architecture/c4/export/*.puml` (commit `8c8f838`).

**Prompt IA 3 — Explicación para público no técnico (Paso 11 de la guía; solo cambian el público y el caso):**

> Explica el siguiente diagrama de contexto a la directiva de la asociación de comerciantes del Mercado San Camilo, que no es técnica, en máximo 120 palabras: qué hace el sistema, quién lo usa y de qué servicios externos depende. Evita la jerga técnica. [vista de contexto exportada]

Se pegó `docs/architecture/c4/export/Contexto.puml` (commit `8c8f838`).

**Instrucción de las filas del 18/10 (validación y exportación), resumida:**

> Valida `workspace.dsl` con Structurizr. Si falla por la vista dinámica, haz la corrección mínima usando los aliases reales (`bd`, `redis`) y una relación que exista (`pedidos -> redis`). Si `export/` tiene el ERP, regenera la exportación desde `workspace.dsl` a Mermaid y C4-PlantUML en `export/` y los PNG en `img/`. No toques `contexto-manual.puml` ni `comparacion.md`.
