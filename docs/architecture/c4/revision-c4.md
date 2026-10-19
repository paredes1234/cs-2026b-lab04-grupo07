# E7. Revisión del modelo C4 — San Camilo en Línea

**Fecha:** 19/10/2026. **Revisa:** Cristhian Bravo, con Claude Code como segundo revisor.
**Revisamos:** `workspace.dsl` (validado con Structurizr CLI, código de salida 0), los `.puml` de `export/` y los PNG de `img/`, todos generados desde el mismo modelo (commit `8c8f838`).

## Lista de revisión (Tabla 3 de la guía, sección 1.4)

| Grupo | Id | Pregunta de revisión |
|---|---|---|
| General | G1 | ¿Tiene título? |
| General | G2 | ¿Se entiende de qué tipo de diagrama se trata y cuál es su alcance? |
| General | G3 | ¿Tiene leyenda? |
| Elementos | E1 | ¿Cada elemento tiene nombre, tipo (persona, sistema, contenedor o componente), descripción de lo que hace y, si corresponde, tecnología? |
| Elementos | E2 | ¿Se entienden los acrónimos, colores, formas, íconos, bordes y tamaños? |
| Relaciones | R1 | ¿Cada flecha tiene una etiqueta que describe su intención? |
| Relaciones | R2 | ¿La etiqueta coincide con la dirección de la flecha? |
| Relaciones | R3 | ¿Se indica la tecnología o el protocolo (HTTPS, SQL, MQTT)? |
| Relaciones | R4 | ¿Se entienden los estilos de línea y las puntas de flecha? |

## 1. Contexto — `img/Contexto.png`, `export/Contexto.puml`

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `systemContext sancamilo "Contexto" "Nivel 1: usuarios, San Camilo en Línea y servicios externos."` (línea 88). |
| G2 | Sí | Título "System Context View" y "Nivel 1": un solo sistema con sus 3 personas y 2 sistemas externos (`include *`, línea 89). |
| G3 | Sí | `SHOW_LEGEND(true)` (`export/Contexto.puml`, línea 30); el PNG muestra la leyenda "person" y "system". |
| E1 | Sí | Las 3 personas (líneas 7–9), el sistema (línea 11) y los 2 externos (líneas 28–29) tienen nombre, tipo y descripción. En el nivel 1 no corresponde tecnología. |
| E2 | **No** | Yape y WhatsApp tienen la etiqueta `Externo` con estilo gris (líneas 28–29 y 131–134), pero el exportador los escribe como `System(...)` y no como `System_Ext(...)`. En el PNG salen azules como San Camilo y la leyenda no tiene "external system" (P6). "MVP" (línea 28) no se explica. |
| R1 | Sí | Las 5 flechas tienen un verbo con intención: "Solicita el cobro de pedidos con Yape", "Envía confirmaciones a comerciantes" (líneas 32–36). |
| R2 | Sí | Personas → sistema; sistema → Yape y WhatsApp. Cada etiqueta se lee en el sentido de la flecha. |
| R3 | No aplica | En el nivel 1 no se exige tecnología. La guía lo marca como falso positivo en la Tabla 8, y la lista de E1 pide que "el diagrama de contexto no muestra tecnologías internas". Los protocolos están en el nivel 2 (líneas 39–47). |
| R4 | Sí | Todas las relaciones usan el mismo estilo de línea continua con una punta. |

## 2. Contenedores — `img/Contenedores.png`, `export/Contenedores.puml`

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `container sancamilo "Contenedores" "Nivel 2: …"` (línea 92). |
| G2 | Sí | "Container View" con el borde "San Camilo en Línea [System]" que agrupa los 5 contenedores. |
| G3 | Sí | `SHOW_LEGEND(true)` (`export/Contenedores.puml`, línea 44). |
| E1 | Sí | `pwa`, `api`, `worker`, `bd` y `redis` tienen nombre, descripción y tecnología: HTML/CSS/JavaScript + Service Worker, Python / Django, Python / Celery, PostgreSQL 16, Redis (líneas 13–25). |
| E2 | **No** | Externos sin distinguir (P6). Las formas de cilindro (`bd`) y tubo (`redis`) (líneas 143–148) no aparecen explicadas en la leyenda. "PWA" (título) y "API" no se explican. |
| R1 | Sí | Todas las flechas tienen etiqueta con intención (líneas 39–47 y las implícitas que salen de las líneas 64–66). Observación: hay dos flechas hacia WhatsApp, desde `worker` y desde `api` (P4). |
| R2 | Sí | Las etiquetas coinciden con la dirección. |
| R3 | **No** | Casi todas las flechas indican protocolo, pero `worker → api` "Ejecuta tareas del módulo Notificaciones" tiene "Celery/Python" (`export/Contenedores.puml`, línea 41). No es un protocolo entre dos procesos: el worker no llama a la API, ejecuta el código del módulo dentro de su propio proceso (P10). |
| R4 | Sí | Estilo de línea único. |

## 3. Componentes — `img/Componentes.png`, `export/Componentes.puml`

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `component sancamilo.api "Componentes" "Nivel 3: …"` (línea 96). |
| G2 | Sí | "Component View" con el borde "Aplicación web / API [Container]". |
| G3 | Sí | Leyenda con system, container, component y bordes. |
| E1 | Sí | Los 6 componentes tienen nombre, descripción y la tecnología "Módulo Python/Django" (líneas 16–21). |
| E2 | **No** | Externos sin distinguir (P6); cilindro y tubo sin explicar. |
| R1 | Sí | Todas las relaciones tienen etiqueta (líneas 50–68). Observación: `notificaciones → whatsapp` (línea 66) y `worker → whatsapp` (línea 46) duplican al responsable del envío (P4). |
| R2 | Sí | `notificaciones → pedidos` "Implementa el puerto Notificador y usa PedidoPuesto" (línea 56) va del que implementa al dueño del puerto, como dice ADR-004. No hay ciclo. |
| R3 | Sí | "Llamada interna Python", "Interfaz Python", "SQL/TCP", "Protocolo Redis/TCP", "HTTPS/JSON". Dentro de un proceso, "Celery/Python" (línea 65) describe bien que el worker usa el módulo. |
| R4 | Sí | Estilo único. |

## 4. ConfirmarYPagar (dinámica) — `img/ConfirmarYPagar.png`, `export/ConfirmarYPagar.puml`

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `dynamic sancamilo.api "ConfirmarYPagar" "Dinámico: pagar con Yape un pedido de varios puestos (camino de éxito, CA-1)."` (línea 102). |
| G2 | Sí | "Dynamic View" con pasos numerados del 1 al 9; el alcance es el camino de éxito. |
| G3 | Sí | `SHOW_LEGEND(true)` (`export/ConfirmarYPagar.puml`, línea 55). |
| E1 | Sí | Cada participante aparece una vez en el PNG, con nombre, tipo, descripción y tecnología. |
| E2 | **No** | "CA-1" (criterio de aceptación 1 de HU-03, Lab 05) no se explica; externos sin distinguir (P6). |
| R1 | Sí | Los 9 pasos tienen verbo (líneas 103–111). |
| R2 | Sí | Por ejemplo, paso 8 `worker → redis` "Consume la tarea": el worker es quien lee la cola. |
| R3 | Sí | Los 9 pasos tienen tecnología; los pasos 3 y 4 la toman de las relaciones de las líneas 54–55 (`export/ConfirmarYPagar.puml`, líneas 47–48). |
| R4 | Sí | Estilo único con numeración. |

Cada paso corresponde a una relación del modelo (requisito de E4) desde el commit `fb95ec5`. Antes, `validate` fallaba en la línea 109 (P3).

## 5. Despliegue — `img/Despliegue.png`, `export/Despliegue.puml`

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `deployment sancamilo produccion "Despliegue" "Despliegue en producción (MVP): celular, VPS y Docker Compose."` (línea 116). |
| G2 | Sí | "Deployment View … Producción" con nodos anidados (líneas 71–83). |
| G3 | Sí | Leyenda con container y node. |
| E1 | Sí | Nodos con tecnología: Android + Chrome; Ubuntu 24.04 LTS, 2 vCPU, 4 GB RAM; Docker 27 (líneas 72–76). Están las instancias de los 5 contenedores (líneas 73, 77–80). |
| E2 | **No** | "R-05", "R-03", "ADR-001" (líneas 72 y 75), "MVP" y "VPS" no se explican; cilindro y tubo sin explicar. |
| R1 | Sí | Las 5 flechas tienen etiqueta. |
| R2 | Sí | Coinciden con la dirección. |
| R3 | **No** | `worker → api` "Ejecuta tareas del módulo Notificaciones" [Celery/Python] dentro de Docker Compose (`export/Despliegue.puml`) muestra una comunicación por red que no existe (P10). |
| R4 | Sí | Estilo único. |

## Resumen

| Vista | Sí | No | No aplica |
|---|---|---|---|
| Contexto | 7 | 1 | 1 |
| Contenedores | 7 | 2 | 0 |
| Componentes | 8 | 1 | 0 |
| ConfirmarYPagar | 8 | 1 | 0 |
| Despliegue | 7 | 2 | 0 |

El "No" que se repite en las 5 vistas es E2: la notación no distingue a los sistemas externos y deja acrónimos sin explicar. Es un problema de exportación y redacción, no del modelo. Los "No" de R3 (P10) y las observaciones de R1 (P4) son más graves porque son del modelo: confunden a quien lee quién envía a WhatsApp y cómo se comunica el worker. La lista tampoco detecta todo: P5 (falta `worker → bd`) cumple las 9 preguntas y solo aparece al comparar con ADR-003.

## Segundo revisor (IA)

Usamos el **Prompt IA 2** de la guía (Paso 10) sobre los 5 `.puml` de `export/`. La respuesta completa sin editar está en `.ia-borradores/prompt-ia2-oficial.md` (local) y el prompt, en el anexo de `bitacora-ia.md`. La IA marcó 11 "No" y dio "Sí" al resto. Abajo están los 11 "No" (agrupados) y un resumen de los "Sí", verificados por el equipo contra `workspace.dsl` y los PNG.

| Vista | Pregunta de la lista | Cumple (IA) | Evidencia (IA) | Corrección sugerida (IA) | Verificación del equipo |
|---|---|---|---|---|---|
| Contexto | ¿Se indica la tecnología o el protocolo? | No | Las 5 `Rel` tienen `$techn=""`. | Agregar "HTTPS" / "HTTPS/JSON". | **Falso positivo (FP-1).** En el nivel 1 no se exigen tecnologías: lo dice la Tabla 8 de la guía para el mismo caso y la lista de E1 pide no mostrar tecnologías internas en el contexto. Los protocolos ya están en el nivel 2 (líneas 39–47). Se rechaza. |
| ConfirmarYPagar | ¿Cada elemento tiene nombre, tipo, descripción…? | No | Cliente, PWA, Worker, BD, Redis, Yape y WhatsApp se declaran dos veces (dentro y fuera de `System_Boundary`). | Declarar cada elemento una sola vez. | **Falso positivo (FP-2).** La duplicación existe en el texto de `export/ConfirmarYPagar.puml`, pero `img/ConfirmarYPagar.png` muestra cada elemento **una sola vez**: PlantUML usa la primera declaración de cada alias. En `workspace.dsl` cada elemento se define una vez (líneas 7–29). La IA juzgó el diagrama por el texto exportado y no por cómo se dibuja. Además, ese `.puml` lo genera Structurizr CLI: editarlo a mano rompería la regla de fuente única. Se rechaza. |
| Contexto, Contenedores, Componentes, ConfirmarYPagar | ¿Se entienden los acrónimos, colores, formas…? | No | Yape y WhatsApp como `System(...)`, no `System_Ext(...)`. | Usar `System_Ext(...)`. | **Válido (P6).** Confirmado en los PNG. La corrección no se hace en el `.puml`, porque se regenera, sino en el modelo o en el exportador. |
| Contexto, Contenedores, ConfirmarYPagar, Despliegue | (misma pregunta) | No | "MVP", "PWA", "API", "CA-1", "R-05", "R-03", "ADR-001", "VPS" sin explicar. | Explicarlos en la descripción. | **Válido (baja).** Confirmado (criterio E2 de las tablas). |
| Contenedores, Componentes | ¿Cada flecha tiene una etiqueta que describe su intención? | No | Dos flechas hacia WhatsApp (`worker` y `api` / `notificaciones`). | Un solo responsable del envío. | **Válido como hallazgo (P4), pero mal ubicado.** Las dos flechas sí tienen etiqueta con intención, así que la pregunta R1 se cumple. El problema es de modelo: hay dos responsables del envío (líneas 46 y 66) y ADR-003 dice que el envío es asíncrono. |
| Contenedores, Despliegue | ¿Se indica la tecnología o el protocolo? | No | `worker → api` con "Celery/Python". | Quitar la relación del nivel 2 o mostrar la comunicación vía Redis. | **Válido (P10).** Confirmado en `export/Contenedores.puml` (línea 41) y en `img/Despliegue.png`. Sale de la relación de componentes de la línea 65. |
| Todas | G1, G2, G3, E1 (salvo FP-2), R2, R4 | Sí | Títulos, leyendas, tecnologías y dirección correctos. | — | **Correcto (cumple).** Coincide con nuestra revisión. Observación de la IA sobre Despliegue (no muestra Yape ni WhatsApp): la vista de despliegue muestra lo que desplegamos y los externos no los desplegamos nosotros; mostrarlos es opcional. |

**Falsos positivos identificados: 2.** El más claro es **FP-2**. La IA leyó dos declaraciones del mismo alias en el `.puml` y concluyó que el diagrama repite elementos. Lo detectamos con la pregunta E1 de la lista: al revisar el PNG, cada elemento aparece una vez. **FP-1** es el mismo falso positivo que la guía muestra en la Tabla 8.

## Hallazgos y acciones

La guía (sección III) pide: "si encuentran una contradicción, corrijan el artefacto equivocado y regístrenlo en la bitácora". Así se justifican las dos correcciones que ya hicimos a E4 y E6. Las dos están registradas en `bitacora-ia.md`.

| # | Hallazgo | Estado | Evidencia | Acción | Responsable |
|---|---|---|---|---|---|
| P1 | E6 era de otro sistema ("Sistema ERP Multimodular": SUNAT, API Gateway, FastAPI, AWS). Contradice la regla de fuente única. | ✅ Confirmado. Exportación corregida. | `export/` en `9b01511` (10 archivos del ERP); `contexto-manual.puml` línea 6; `comparacion.md` sección E6 ("Servicio de Ventas e Ingresos"). | Se corrigió el artefacto equivocado: `export/` e `img/` regenerados desde `workspace.dsl` (commit `8c8f838`). Falta rehacer `contexto-manual.puml` y la sección E6 de `comparacion.md` para el mismo contexto (E6.2). | Rodrigo y Fabricio. <PENDIENTE: confirmar Cristhian> |
| P2 | Aliases `sancamilo.db` / `sancamilo.cola` en la dinámica. | ❌ No aplica en el repo | `workspace.dsl` líneas 108–110 usan `bd` y `redis`. Solo el código de E4 en el informe Word tiene `db` y `cola`. | Actualizar el informe. | Compañeros (informe) |
| P3 | El paso 7 `notificaciones → redis` no existía en el modelo. Contradice E4.2 ("cada paso debe corresponder a una relación ya existente"). | ✅ Corregido | `validate` fallaba en la línea 109. | Se cambió a `pedidos → redis` (relación de la línea 64), commit `fb95ec5`. | Cristhian |
| P4 | Dos responsables del envío a WhatsApp. | ✅ Confirmado | Líneas 46 y 66; `img/Contenedores.png`. | Dejar solo `worker → whatsapp` o explicar que el worker ejecuta `notificaciones`. | <PENDIENTE: confirmar Cristhian> |
| P5 | Falta `worker → bd`, aunque ADR-003 dice que la notificación no entregada queda pendiente en la BD. | ✅ Confirmado | ADR-003 línea 26; no hay relación worker → bd. | `sancamilo.worker -> sancamilo.bd "Marca notificaciones pendientes" "SQL/TCP"`. | <PENDIENTE: confirmar Cristhian> |
| P6 | En C4-PlantUML los externos no se distinguen. | ✅ Confirmado | `System(...)` en `export/*.puml`; PNG azules. En `export/Contexto.mmd` sí salen grises. | Investigar cómo marca externos el exportador C4-PlantUML. | <PENDIENTE: confirmar Cristhian> |
| P7 | El despliegue no tiene Nginx ni Prometheus/Grafana del Lab 04. | ✅ Confirmado | `diagrams/despliegue.py` líneas 35, 42–43. | Agregar Nginx como `infrastructureNode` o documentar que se omite en el MVP. | <PENDIENTE: confirmar Cristhian> |
| P8 | PostgreSQL 16 sigue "pendiente de confirmación". | ✅ Confirmado | `inventario.md` línea 36. | El equipo confirma el motor. | Equipo |
| P9 | Las referencias del informe son del Lab 05. | ✅ Confirmado | Informe: [1] OMG UML, [2] Fowler, [3] Pyreverse. | Agregar las referencias C4 de la sección V de la guía. | Cristhian |
| P10 | La relación implícita `worker → api` [Celery/Python] parece una llamada por red. | ✅ Confirmado (segundo revisor) | Línea 65; `export/Contenedores.puml` línea 41; `img/Despliegue.png`. | Se resuelve junto con P4. | <PENDIENTE: confirmar Cristhian> |
| P11 | El Mermaid exportado (el que va en el README) no tiene leyenda y usa flechas punteadas sin explicar (R4). | ✅ Confirmado | `export/Contexto.mmd`: flechas `-. .->`, sin leyenda. | Aceptarlo como limitación del exportador Mermaid; los PNG con leyenda están enlazados en el README. | <PENDIENTE: confirmar Cristhian> |
