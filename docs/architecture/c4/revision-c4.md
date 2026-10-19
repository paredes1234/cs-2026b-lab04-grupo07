# E7. Revisión del modelo C4 — San Camilo en Línea

**Fecha:** 18/10/2026. **Revisa:** Cristhian Bravo (con Claude Code como apoyo).
**Modelo revisado:** `workspace.dsl` del commit `fb95ec5` (después de corregir el paso 7 de la vista dinámica) e imágenes de `img/`, regeneradas desde ese modelo en el commit `8c8f838`.

> **Nota sobre la lista:** no teníamos la guía del Lab 06 al hacer esta revisión, así que no usamos la Tabla 3 textual. La lista se adaptó de la *review checklist* de c4model.com (secciones General, Elementos y Relaciones). <PENDIENTE: confirmar Cristhian — reemplazar por los criterios exactos de la Tabla 3 si se consigue la guía>.

Validación: `structurizr validate` (Structurizr CLI v2025.11.09) falla en la línea 109 con el modelo de `9b01511` y termina con código 0 después de `fb95ec5` (ver P3).

## Criterios usados

| Id | Criterio |
|---|---|
| G1 | ¿La vista tiene título? |
| G2 | ¿Se entiende el tipo de diagrama (nivel C4)? |
| G3 | ¿Se entiende el alcance de la vista? |
| G4 | ¿Tiene leyenda o clave? |
| E1 | ¿Cada elemento tiene nombre? |
| E2 | ¿Se entiende el tipo de cada elemento (persona, sistema, sistema externo, contenedor, componente, nodo)? |
| E3 | ¿Cada elemento tiene descripción de lo que hace? |
| E4 | ¿Se indica la tecnología (niveles 2 y 3, y despliegue)? |
| E5 | ¿Se explican los acrónimos y abreviaturas? |
| E6 | ¿Tienen significado explicado los colores y formas? |
| R1 | ¿Cada flecha tiene descripción? |
| R2 | ¿Cada flecha indica tecnología o protocolo (cuando aplica)? |
| R3 | ¿La dirección de cada flecha es clara y coherente con el modelo y los ADR? |

## 1. Contexto (`img/Contexto.png`)

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `systemContext sancamilo "Contexto" "Nivel 1: …"` (línea 88). |
| G2 | Sí | El título exportado es "System Context View" y la descripción dice "Nivel 1". |
| G3 | Sí | Un solo sistema propio (`sancamilo`), 3 personas y 2 sistemas externos (`include *`, línea 89). |
| G4 | Sí | `SHOW_LEGEND(true)` en `export/Contexto.puml` línea 30; la leyenda muestra "person" y "system". |
| E1 | Sí | Los 6 elementos tienen nombre (líneas 7–11, 28–29). |
| E2 | **No** | Yape y WhatsApp tienen la etiqueta `Externo` (líneas 28–29), pero en el PNG salen azules como el sistema propio y la leyenda no tiene "external system". `export/Contexto.puml` usa `System(...)` y no `System_Ext(...)` (P6). |
| E3 | Sí | Todas las personas y sistemas tienen descripción (líneas 7–11, 28–29). |
| E4 | No aplica | En el nivel 1 no se pide tecnología. |
| E5 | **No** | "MVP" en la descripción de Yape (línea 28) no se explica. |
| E6 | **No** | El gris `#737A86` del estilo `Externo` (líneas 131–134) no aparece en el PNG ni en la leyenda. En `export/Contexto.mmd` sí sale gris. |
| R1 | Sí | Las 5 relaciones tienen descripción (líneas 32–36). |
| R2 | No aplica | Nivel 1: la tecnología es opcional (ver falso positivo FP-1). |
| R3 | Sí | Personas → sistema; sistema → Yape y WhatsApp. Coincide con RF-05 y ADR-003. |

## 2. Contenedores (`img/Contenedores.png`)

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `container sancamilo "Contenedores" "Nivel 2: …"` (línea 92). |
| G2 | Sí | Título exportado "Container View"; descripción "Nivel 2". |
| G3 | Sí | Borde "San Camilo en Línea [System]" con los 5 contenedores. |
| G4 | Sí | `SHOW_LEGEND(true)` (`export/Contenedores.puml` línea 44): person, system, container, system boundary. |
| E1 | Sí | `pwa`, `api`, `worker`, `bd`, `redis` (líneas 13–25). |
| E2 | **No** | Mismo problema que en Contexto: Yape y WhatsApp no se distinguen como externos (P6). |
| E3 | Sí | Los 5 contenedores tienen descripción (líneas 13–25). |
| E4 | Sí | HTML/CSS/JavaScript + Service Worker; Python / Django; Python / Celery; PostgreSQL 16; Redis (líneas 13–25). |
| E5 | **No** | "API" (línea 14) y "PWA" (título, línea 92) no se explican dentro de la vista. |
| E6 | **No** | Las formas `cylinder` (BD) y `pipe` (Redis) (líneas 143–148) no se explican en la leyenda. |
| R1 | Sí | Todas las flechas tienen descripción (líneas 39–47 y relaciones implícitas de 64–66). |
| R2 | Sí | Todas tienen protocolo: HTTPS, HTTPS/JSON, SQL/TCP, Protocolo Redis/TCP, Celery/Python. |
| R3 | **No** | (a) Hay dos flechas a WhatsApp: worker → WhatsApp (línea 46) y API → WhatsApp, implícita de `notificaciones -> whatsapp` (línea 66) (P4). (b) Aparece worker → API "Ejecuta tareas del módulo Notificaciones" [Celery/Python] (`export/Contenedores.puml` línea 41), implícita de la línea 65: parece una llamada por red que no existe (P10). |

## 3. Componentes (`img/Componentes.png`)

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `component sancamilo.api "Componentes" "Nivel 3: …"` (línea 96). |
| G2 | Sí | Título exportado "Component View". |
| G3 | Sí | Borde "Aplicación web / API [Container]" con 6 componentes. |
| G4 | Sí | Leyenda con system, container, component y boundaries. |
| E1 | Sí | catalogo, pedidos, pagos, notificaciones, entrega, compartido (líneas 16–21). |
| E2 | **No** | Yape y WhatsApp siguen sin distinguirse como externos (P6). |
| E3 | Sí | Los 6 componentes tienen descripción (líneas 16–21). |
| E4 | Sí | "Módulo Python/Django" en los 6 (líneas 16–21). |
| E5 | Sí | No hay acrónimos sin explicar; `PasarelaPago`, `Notificador` y `PedidoPuesto` son nombres de clases del Lab 05. |
| E6 | **No** | Igual que en Contenedores: cilindro y tubo sin explicar. |
| R1 | Sí | Todas las relaciones tienen descripción (líneas 50–68). |
| R2 | Sí | Todas indican tecnología ("Llamada interna Python", "Interfaz Python", "SQL/TCP", etc.). |
| R3 | **No** | `notificaciones -> pedidos` (línea 56) va en la dirección correcta según ADR-004. Pero `notificaciones -> whatsapp` (línea 66) y `worker -> whatsapp` (línea 46) dejan dos responsables del envío (P4). |

## 4. ConfirmarYPagar — dinámica (`img/ConfirmarYPagar.png`)

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `dynamic sancamilo.api "ConfirmarYPagar" "Dinámico: …"` (línea 102). |
| G2 | Sí | Título exportado "Dynamic View" y pasos numerados 1–9. |
| G3 | Sí | "camino de éxito, CA-1" (línea 102): solo el flujo de pago correcto. |
| G4 | Sí | `SHOW_LEGEND(true)` (`export/ConfirmarYPagar.puml` línea 55). |
| E1 | Sí | Todos los participantes tienen nombre. |
| E2 | **No** | Yape y WhatsApp sin distinción de externos (P6). |
| E3 | Sí | Cada participante muestra su descripción del modelo. |
| E4 | Sí | Contenedores y componentes muestran su tecnología. |
| E5 | **No** | "CA-1" (línea 102) no se explica; es el criterio de aceptación 1 de HU-03 (Lab 05). |
| E6 | **No** | Cilindro y tubo sin explicar. |
| R1 | Sí | Los 9 pasos tienen descripción (líneas 103–111). |
| R2 | Sí | Los 9 pasos tienen tecnología; los pasos 3 y 4 la toman de la relación del modelo (`export/ConfirmarYPagar.puml` líneas 47–48). |
| R3 | Sí | Después de `fb95ec5` cada paso corresponde a una relación del modelo y `validate` termina con código 0. Antes no: el paso 7 `notificaciones -> redis` no existía (P3). |

## 5. Despliegue (`img/Despliegue.png`)

| Criterio | Sí/No | Evidencia |
|---|---|---|
| G1 | Sí | `deployment sancamilo produccion "Despliegue" "…"` (línea 116). |
| G2 | Sí | Título exportado "Deployment View: San Camilo en Línea - Producción". |
| G3 | Sí | Entorno `Producción` (línea 71): celular y VPS con Docker Compose. |
| G4 | Sí | Leyenda con container y node. |
| E1 | Sí | Nodos "Celular del usuario", "Servidor VPS en la nube", "Docker Compose" (líneas 72–76). |
| E2 | Sí | Los nodos (cajas con borde) se distinguen de las instancias de contenedor (azules). |
| E3 | Sí | Cada nodo tiene descripción (líneas 72, 75, 76). |
| E4 | Sí | Android + Chrome; Ubuntu 24.04 LTS, 2 vCPU, 4 GB RAM; Docker 27 (líneas 72–76). |
| E5 | **No** | "R-05", "R-03", "ADR-001" (líneas 72, 75), "VPS" y "MVP" no se explican. |
| E6 | **No** | Cilindro y tubo sin explicar. |
| R1 | Sí | Todas las flechas tienen descripción. |
| R2 | Sí | Todas indican protocolo. |
| R3 | **No** | Dentro de Docker Compose aparece worker → API "Ejecuta tareas del módulo Notificaciones" [Celery/Python] (P10). En producción el worker no llama a la API: corre el código del módulo dentro de su propio proceso. |

## Resumen

| Vista | Sí | No | No aplica |
|---|---|---|---|
| Contexto | 8 | 3 | 2 |
| Contenedores | 9 | 4 | 0 |
| Componentes | 10 | 3 | 0 |
| ConfirmarYPagar | 10 | 3 | 0 |
| Despliegue | 10 | 3 | 0 |

Los "No" que se repiten son de notación (P6 y formas sin explicar) y de acrónimos. Los "No" de R3 son de modelo (P4, P10) y son los más importantes, porque confunden a quien lee la arquitectura.

## Segundo revisor (IA)

Prompt IA 2 (adaptado, ver `bitacora-ia.md`) aplicado al `.dsl` de `fb95ec5`. Respuesta original sin editar en `.ia-borradores/prompt-ia2-respuesta.md` (local). La IA revisó solo el texto del `.dsl`; el equipo verificó cada hallazgo contra el `.dsl`, los `.puml` exportados y los PNG.

> Limitación: el segundo revisor fue Claude Code en la misma sesión que nos ayudó con la revisión, no una IA independiente.

| # | Hallazgo de la IA | Vista | Verificación del equipo | ¿Válido / Falso positivo? |
|---|---|---|---|---|
| 1 | Las relaciones del contexto (líneas 32–36) no tienen tecnología. | Contexto | En C4 la tecnología de las relaciones se pide en los niveles 2 y 3. En el nivel 1 el lector (docente, comerciante) solo necesita saber qué se intercambia. Las mismas relaciones sí tienen protocolo en Contenedores (líneas 39–47). | **Falso positivo (FP-1)** |
| 2 | Yape y WhatsApp usan la etiqueta `Externo`, que no es la convencional, y pueden salir como sistema interno. | Contexto, Contenedores | Confirmado: `export/Contexto.puml` usa `System(...)`, el PNG los pinta azules y la leyenda no tiene "external system". En Mermaid sí salen grises (`#737a86`). | Válido (P6) |
| 3 | No se define una leyenda en el `.dsl`. | Todas | Structurizr genera la leyenda al exportar: los 5 `.puml` tienen `SHOW_LEGEND(true)` y los 5 PNG muestran "Legend". No hace falta declararla en el `.dsl`. Lo que sí falta es que la leyenda explique externos y formas, pero eso ya es el hallazgo 2. | **Falso positivo (FP-2)** |
| 4 | Dos caminos hacia WhatsApp (líneas 46 y 66). | Contenedores, Componentes | Confirmado: en `img/Contenedores.png` salen dos flechas a WhatsApp, desde Worker y desde API. | Válido (P4) |
| 5 | El worker no se relaciona con la BD, pero ADR-003 dice que la notificación no entregada queda pendiente en la BD. | Contenedores | Confirmado: no existe `worker -> bd`. ADR-003, línea 26: "queda marcada como pendiente en la base de datos". | Válido (P5) |
| 6 | La relación de la línea 65 crea una flecha worker → API que parece una llamada por red. | Contenedores, Despliegue | Confirmado en `export/Contenedores.puml` línea 41 y en `img/Despliegue.png`. | Válido (P10, nuevo) |
| 7 | Los pasos 3 y 4 de la dinámica (líneas 105–106) no tienen tecnología. | ConfirmarYPagar | Cuando un paso no indica tecnología, Structurizr lo asocia con la relación existente del modelo (líneas 54 y 55) y usa su tecnología. `export/ConfirmarYPagar.puml` líneas 47–48 muestra `$techn="Llamada interna Python"` en ambos pasos, y el PNG también. La IA leyó el texto del `.dsl` sin considerar cómo resuelve Structurizr los pasos. | **Falso positivo (FP-3)** |
| 8 | Falta el paso worker → notificaciones entre los pasos 8 y 9. | ConfirmarYPagar | La relación existe (línea 65), así que el paso sería válido. Pero agregarlo también repetiría P10 en la dinámica. | Válido como mejora. <PENDIENTE: confirmar Cristhian — ¿se agrega o se deja en 9 pasos?> |
| 9 | La vista de despliegue no muestra Yape ni WhatsApp. | Despliegue | La vista de despliegue muestra lo que **nosotros** desplegamos; Yape y WhatsApp no los desplegamos. Las relaciones hacia ellos ya están en Contexto y Contenedores. Agregarlos es opcional. | Falso positivo parcial. <PENDIENTE: confirmar Cristhian> |
| 10 | Acrónimos sin explicar (CA-1, R-05, R-03, ADR-001, PWA, VPS, API). | Varias | Confirmado (criterio E5 de las tablas). | Válido (baja) |
| 11 | `compartido` agrega ruido con 5 flechas iguales. | Componentes | Es cierto que agrega flechas, pero `compartido` sale de `paquetes.puml` (Lab 05) y muestra la regla de que los módulos dependen de él y no al revés. Quitarlo ocultaría esa regla. | Válido como observación; se rechaza el cambio. <PENDIENTE: confirmar Cristhian> |

**Falso positivo principal (FP-3):** la IA marcó como error que los pasos 3 y 4 no tienen tecnología. Lo detectamos con el criterio R2: al revisar el PNG exportado, los dos pasos sí muestran `[Llamada interna Python]`. El error de la IA fue revisar solo el texto y no el resultado del modelo: en una vista dinámica, Structurizr reutiliza la relación que ya existe entre esos dos elementos.

## Hallazgos y acciones

| # | Hallazgo | Estado | Evidencia | Acción | Responsable |
|---|---|---|---|---|---|
| P1 | E6 era de un "Sistema ERP Multimodular" (SUNAT, API Gateway, FastAPI, AWS). | ✅ Confirmado. Exportación corregida. | `export/` en `9b01511` (10 archivos ERP); `contexto-manual.puml` línea 6 ("Sistema ERP"); `comparacion.md` sección E6 ("Servicio de Ventas e Ingresos"). | `export/` e `img/` regenerados desde el `.dsl` en `8c8f838`. Falta rehacer `contexto-manual.puml` y la sección E6 de `comparacion.md` para San Camilo. | Compañeros (E6). <PENDIENTE: confirmar Cristhian> |
| P2 | Aliases `sancamilo.db`/`sancamilo.cola` en la dinámica. | ❌ No aplica en el repo | `workspace.dsl` líneas 108–110 ya usan `bd` y `redis`. El error solo está en el texto del informe Word (E4). | Actualizar el código de E4 en el informe. | Compañeros (informe) |
| P3 | Paso 7 `notificaciones -> redis` no existe en el modelo. | ✅ Confirmado y corregido | `validate` fallaba en la línea 109. | Se cambió a `pedidos -> redis` (relación de la línea 64) en `fb95ec5`. | Cristhian |
| P4 | Dos rutas a WhatsApp. | ✅ Confirmado | Líneas 46 y 66; `img/Contenedores.png`. | Propuesta: dejar solo `worker -> whatsapp` y cambiar la línea 66 por la relación del worker, o explicar que el worker ejecuta `notificaciones`. | <PENDIENTE: confirmar Cristhian> |
| P5 | Falta `worker -> bd` (notificación pendiente, ADR-003). | ✅ Confirmado | ADR-003, línea 26; no hay relación worker → bd. | Propuesta: `sancamilo.worker -> sancamilo.bd "Marca notificaciones pendientes" "SQL/TCP"`. | <PENDIENTE: confirmar Cristhian> |
| P6 | El tipo externo no se distingue en C4-PlantUML. | ✅ Confirmado (solo en C4-PlantUML) | `export/Contexto.puml` usa `System(...)`; `img/Contexto.png` azul; en `export/Contexto.mmd` sí sale gris. | Investigar cómo marca externos el exportador C4-PlantUML, o exportar también con el formato PlantUML de Structurizr, que respeta los estilos. | <PENDIENTE: confirmar Cristhian> |
| P7 | Despliegue sin Nginx ni Prometheus/Grafana del Lab 04. | ✅ Confirmado | `diagrams/despliegue.py` líneas 35, 42–43; `workspace.dsl` líneas 71–83 no los tienen. | Agregar Nginx como `infrastructureNode` o documentar que se omite en el MVP. | <PENDIENTE: confirmar Cristhian> |
| P8 | PostgreSQL 16 sigue "pendiente de confirmación". | ✅ Confirmado | `inventario.md` línea 36; `bitacora-ia.md` línea 17. | El equipo confirma el motor o lo cambia en `workspace.dsl` línea 24. | Equipo |
| P9 | Referencias del informe Word son del Lab 05. | ✅ Confirmado | Informe: [1] OMG UML, [2] Fowler, [3] Pyreverse. | Agregar c4model.com, Structurizr DSL, C4-PlantUML y Mermaid C4. | Cristhian (cuestionario) |
| P10 | Relación implícita worker → API parece llamada por red. | ✅ Nuevo (segundo revisor) | Línea 65; `export/Contenedores.puml` línea 41; `img/Despliegue.png`. | Se resuelve junto con P4 si el worker deja de apuntar a `api.notificaciones` o se cambia la descripción. | <PENDIENTE: confirmar Cristhian> |
