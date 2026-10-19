# Bitácora de IA — Laboratorio 06 (borrador inicial)

> El Lab 06 exige registrar las interacciones con IA. A continuación se ofrece el registro de la ayuda en esta conversación; el equipo debe completar los campos de verificación/decisión tras revisar el modelo. No se simulan interacciones adicionales.

| Fecha | Herramienta | Solicitud / prompt de trabajo | Propuesta | Verificación | Decisión |
|---|---|---|---|---|---|
| 2026-10-18 | ChatGPT (GPT-6) | Revisar la guía docente del Lab 06 y el caso San Camilo en Línea de los Labs 04–05; preparar E1 (inventario/contexto), E2 (contenedores) y E3 (componentes) en un único `workspace.dsl`, sin copiar AgroConecta. | Inventario de personas y sistemas; contenedores PWA, API, Celery, base relacional y Redis; componentes conforme a `paquetes.puml`. | **Pendiente del equipo:** contrastar rutas y archivos reales, confirmar motor de BD, ejecutar Structurizr CLI y revisar C4. | **Pendiente de decisión:** aceptar o corregir cada punto después de las verificaciones. |
| 18/10/2026 | Claude Code (Opus 5.5) | Validar `workspace.dsl` con Structurizr CLI y, si falla por la vista dinámica, hacer la corrección mínima. | `validate` falla en la línea 109: el paso 7 `notificaciones -> redis` no existe en el modelo. Propone usar la relación existente `pedidos -> redis` (línea 64). | Se ejecutó `validate` antes (falla) y después (código 0). La relación de la línea 64 tiene la misma tecnología ("Protocolo Redis/TCP"). Los aliases `bd` y `redis` ya eran correctos (P2 no aplica). | Aceptada (commit `fb95ec5`; P3 en `revision-c4.md`). |
| 18/10/2026 | Claude Code (Opus 5.5) | Revisar `export/` e `img/` de E6 y, si no corresponden al modelo, regenerarlos desde `workspace.dsl`. | Detecta que los 10 archivos de `export/` son de un "Sistema ERP Multimodular" (SUNAT, API Gateway, FastAPI, AWS) y que `img/` no existe. Regenera las 5 vistas en C4-PlantUML y Mermaid y los 5 PNG. | Se revisaron los 5 PNG: muestran San Camilo, los nombres y tecnologías del `.dsl`. `grep` de "ERP/SUNAT/FastAPI/AWS" en `export/` e `img/` sin resultados. `contexto-manual.puml` y `comparacion.md` no se tocaron. | Aceptada (commit `8c8f838`; P1 en `revision-c4.md`). |
| 18/10/2026 | Claude Code (Opus 5.5) | Prompt IA 2 (anexo): revisor C4 de las 5 vistas con la lista de c4model.com y líneas del `.dsl`. | 11 hallazgos: tecnología en contexto, etiqueta `Externo`, leyenda, dos rutas a WhatsApp, falta `worker -> bd`, flecha implícita worker → API, pasos 3–4 sin tecnología, paso worker → notificaciones, externos en despliegue, acrónimos, ruido de `compartido`. | Cada hallazgo se contrastó con el `.dsl`, los `.puml` exportados y los PNG. 3 falsos positivos: FP-1 (tecnología en nivel 1), FP-2 (la leyenda la genera el exportador) y FP-3 (pasos 3–4 heredan "Llamada interna Python"). | Corregida: se aceptan los hallazgos válidos (P4, P5, P6, P10) y se rechazan FP-1 a FP-3. Hallazgos 8, 9 y 11: <PENDIENTE: confirmar Cristhian>. |
| 18/10/2026 | Claude Code (Opus 5.5) | Prompt IA 3 (anexo): explicar la arquitectura en 120 palabras o menos para público no técnico. | Párrafo de 123 palabras que agrega "sin pasar por tiendas", "funciona sin conexión", "de forma segura", "en menos de 10 minutos" y omite el módulo `compartido`. | Cada frase se buscó en el `.dsl`. Ninguna de esas cuatro afirmaciones está en el modelo (vienen de ADR-002 y QA-03 o son inventadas) y el `api` tiene 6 componentes, no 5. | Corregida: `explicacion.md` con 118 palabras y tabla "Correcciones aplicadas". |

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

## Anexo: prompts de E4–E7 (Claude Code, 18/10/2026)

No teníamos la guía del Lab 06, así que el Prompt IA 2 y el Prompt IA 3 se adaptaron; no son el texto oficial. <PENDIENTE: confirmar Cristhian — reemplazar por el texto de la guía si se consigue>.

**Instrucción de validación y exportación (filas de `fb95ec5` y `8c8f838`), resumida:**

> Valida `docs/architecture/c4/workspace.dsl` con Structurizr. Si falla por la vista dinámica, haz la corrección mínima para que valide usando los aliases reales (`bd`, `redis`) y una relación que exista (`pedidos -> redis`). Si `export/` tiene el ERP, regenera la exportación desde `workspace.dsl` a Mermaid y C4-PlantUML en `export/` y los PNG en `img/`. No toques `contexto-manual.puml` ni `comparacion.md`.

**Prompt IA 2 (segundo revisor):**

> Actúa como revisor C4. Aplica la lista de revisión de c4model.com (general: título, tipo y alcance, leyenda; elementos: nombre, tipo, descripción, tecnología, acrónimos, formas y colores; relaciones: descripción, tecnología/protocolo, dirección) a estas 5 vistas del workspace.dsl adjunto: Contexto, Contenedores, Componentes, ConfirmarYPagar y Despliegue. Indica cada hallazgo con la vista y la línea del .dsl. No propongas cambios de estilo arquitectónico.
>
> [contenido de `workspace.dsl` del commit `fb95ec5`]

**Prompt IA 3 (explicación):**

> Explica esta arquitectura en 120 palabras o menos para un público no técnico. Usa solo lo que está en el workspace.dsl adjunto.
>
> [contenido de `workspace.dsl` del commit `fb95ec5`]
