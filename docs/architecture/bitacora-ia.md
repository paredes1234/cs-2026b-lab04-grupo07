# Bitácora de uso de IA — San Camilo en Línea
   > Laboratorios 04 y 08. Las filas 1 a 7 son del Lab 04; las filas 8 a 14, del Lab 08.

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 03/10/2026 | ChatGPT (GPT-5.6 Sol) | Prompt 1 adaptado (E2): 3 alternativas de estilo arquitectónico para San Camilo en Línea, con plazo de 1 mes, equipo reducido, presupuesto bajo y el atributo crítico de usabilidad. | Monolito en capas, monolito modular y microservicios. Recomendó el monolito modular. | No se aceptó asumir que Yape tiene una API pública abierta, porque eso requería verificación externa. En la arquitectura se usa "Yape / proveedor de pago", sin afirmar una integración específica (ver `diagrams/arquitectura.mmd` y la sección 4 de `matriz-decision.md`). Los microservicios se analizaron y se descartaron por la complejidad de despliegue, monitoreo e infraestructura frente a R-01, R-03 y el equipo reducido. La matriz eligió el monolito modular (4,85 frente a 4,70 y 2,80). | Corregida |
| 2 | 03/10/2026 | ChatGPT (GPT-5.6 Sol) | Prompt 2 (E2): crítica adversarial ("abogado del diablo") del monolito modular. | 5 riesgos: acoplamiento entre módulos, punto único de falla por tener un solo despliegue, base de datos única como punto de contención, fallas de los servicios externos (WhatsApp, Yape) y necesidad futura de escalar módulos por separado. | Se mantuvo el monolito modular. Ningún riesgo justifica la complejidad de los microservicios para el MVP. Las mitigaciones quedaron en ADR-001 (interfaces entre módulos y adaptadores) y ADR-003 (cola con reintentos para WhatsApp). | Aceptada |
| 3 | 04/10/2026 | Gemini (modo Thinking) | Redacción y estructura de ADR-001, ADR-002 y ADR-003. | Borradores de redacción y estructura de los tres ADR. | La versión final no quedó como pedía el prompt. El prompt pedía las secciones "Drivers Relevantes" y "Alternativas Evaluadas", un monolito modular "en Django" y citar R-01, R-02, QA-01 y QA-02. Los tres ADR del repositorio siguen la plantilla de la guía (Contexto, Alternativas consideradas, Decisión y Consecuencias) y no fijan Django como tecnología. Además, ADR-001 cita los drivers completos: QA-01 a QA-03, R-03, R-05, R-06 y RF-03 a RF-06. | Corregida |
| 4 | 04/10/2026 | Claude Opus 5.5 | Generar `alternativa.puml` (E5): monolito en capas, la alternativa descartada. | Diagrama de componentes en PlantUML del monolito en capas. | La IA no incluyó la nota (`note`) que justifica el descarte según la matriz, a pesar de que el prompt la pedía de forma obligatoria y de que la guía la exige (E5, paso 3). Rodrigo la agregó a mano con el puntaje 4,70 frente a 4,85 y la modificabilidad de 3/5. | Corregida |
| 5 | 04/10/2026 | Claude Opus 5.5 | Generar `despliegue.py` (E6): vista de despliegue con Python Diagrams. | Script de Python Diagrams con infraestructura en AWS (EC2 y RDS). | (1) La IA asumió AWS, a pesar de que el prompt pedía nodos genéricos de `diagrams.onprem`. Nuestra restricción es un VPS con Docker, Nginx y Django, así que se reemplazaron las importaciones por `diagrams.onprem` (Nginx, PostgreSQL, Redis, Celery, Prometheus, Grafana). (2) La IA usó una sintaxis desactualizada de la librería `diagrams` que daba `AttributeError` al ejecutarla. Rodrigo corrigió a mano las conexiones de Celery y Redis. | Corregida |
| 6 | 04/10/2026 | Claude (Opus 5.5) | Compilar en archivos `.md` el trabajo del grupo (guía del laboratorio y avance de E1 a E6) como contexto local para Claude Code. | Archivos Markdown locales (no versionados) con la guía y la transcripción del avance de E1 a E6. | Se usaron solo como contexto. La fuente de verdad son los archivos del repositorio. Al compararlos, Claude Code encontró diferencias: el diagrama Mermaid reconstruido en el avance no es igual a `diagrams/arquitectura.mmd`, y el RF-02 del avance está desactualizado frente a `drivers.md`. Por eso se trabajó con los archivos del repositorio. | Aceptada |
| 7 | 04/10/2026 | Claude Code (Opus 5.5) | Revisar el repositorio y redactar el borrador de la bitácora (E7) y del README (E8) con los datos que reunió el grupo. | Diagnóstico del repositorio (rutas reales de E1 a E6, R-02 sin completar, falta la carpeta `img/`) y borrador de esta bitácora. | Cristhian revisó el borrador antes del commit. Las fechas salen de `git log`. Los datos que no se conocían quedaron marcados como pendientes en lugar de inventarse. | Aceptada |
| 8 | [fecha E1] | [herramienta] | Prompt IA 1 (Lab 08, E1): escenarios de calidad de seis partes para el crecimiento con los mercados Altiplano y Río Seco, con (importancia, dificultad). | Ocho escenarios medibles. Calificó QA08-05 (aislamiento de datos entre mercados) como (M,M). | Con más mercados y comerciantes hay más datos que proteger, y un pedido visible para otro mercado es grave. Se subió a (H,H) y se anotó en el árbol de utilidad. | Corregida |
| 9 | [fecha E2] | [herramienta] | Prompt IA 2 (Lab 08, E2): conceptos de diseño para QA08-05. | Filtro por `mercado_id`, PostgreSQL RLS, base de datos por mercado y filtrado solo en la interfaz. | Prototipo en SQLite: sin filtro se expusieron 100 registros ajenos en 100 intentos; con filtro, 0, y 12 de 12 lecturas propias. La base por mercado sube el costo y el mantenimiento. El filtro solo en la interfaz no protege lo que envía la API. RLS queda pendiente por la configuración extra. | Aceptada (filtro; 2 alternativas rechazadas) |
| 10 | [fecha E4] | [herramienta] | Prompt IA 2 (Lab 08, E4): conceptos para QA08-04, cobros sin duplicados. | Reintentos sin clave (línea base), sin reintento, cobro idempotente, circuit breaker y transacción distribuida (2PC). | Monte Carlo (`fitness/cobros.py`: 100 pedidos, 10 timeouts, 50 % tardíos, 10 % de fallas en reintentos, 3 intentos): la base duplicó 8 cobros (5,52 en promedio en 1000 corridas). Sin reintento no duplica pero se pierden 10 ventas. Con idempotencia: 0 duplicados y 100 de 100 pedidos. El breaker no distingue un timeout tardío de uno temprano; el proveedor no participa en un 2PC. | Aceptada (idempotencia; 3 alternativas rechazadas) |
| 11 | [fecha E4] | [herramienta] | Prompt IA 2 (Lab 08, E4): conceptos para QA08-07, alta de mercados. | Condicionales por mercado, módulo `mercados` con reglas como datos, motor de reglas (DSL) y una instancia por mercado. | `fitness/alta_mercados.py` con difflib: con condicionales se modifican 3 módulos `.py` (meta ≤ 2); con configuración, 0. La configuración no reduce líneas (9 frente a 6). El DSL excede el plazo y el equipo; una instancia por mercado triplica despliegues y contradice el ADR-001. | Aceptada (reglas como datos; 3 alternativas rechazadas) |
| 12 | [fecha E7] | [herramienta] | Prompt IA 3 (Lab 08, E7): evaluador adversario ATAM-lite sobre el árbol, los ADR-006 a 008 y las simulaciones. | [hallazgo real de la IA que sí se confirmó] | [cómo lo verificaron contra el repositorio] | [Aceptada / Corregida] |
| 13 | [fecha E7] | [herramienta] | Prompt IA 3 (Lab 08, E7): el mismo evaluador adversario. | **[FALSO POSITIVO: copiar el hallazgo exacto que dio la IA]** | **[evidencia que lo refuta: archivo, línea, número o prueba]** | **Rechazada (falso positivo)** |
| 14 | 31/10/2026 | Claude | Redacción de `atam-lite.md`, del script de la matriz de riesgos y de la sección del README (E7 y E8) a partir del informe del Lab 08. | Tablas de hallazgos, matriz de probabilidad e impacto, mitigaciones y el texto del README. | Se ejecutó `python fitness/matriz_riesgos.py` y generó la matriz. Los números (100 → 0, 8 → 0, 3 → 0 módulos) se contrastaron con `iteracion-1.md` a `-3.md` y los ADR. La probabilidad y el impacto de cada riesgo son juicio del equipo y se ajustaron. | Corregida |
> Los prompts completos están en el "Anexo: prompts", al final de este archivo.
> Nunca se incluyen datos personales ni información confidencial en un prompt.

## Anexo: prompts

### Interacción 1 — Generación de alternativas (E2)

```text
Actúa como arquitecto de software senior con experiencia en sistemas web para pequeños comercios.

Contexto: San Camilo en Línea es una plataforma para realizar pedidos a los puestos del Mercado San Camilo. Los clientes pueden consultar catálogos por puesto, realizar pedidos con productos de diferentes comerciantes, pagar mediante Yape y seleccionar recojo o delivery. Los comerciantes reciben confirmaciones mediante WhatsApp.

El atributo crítico es la capacidad de interacción: un comerciante con poca experiencia digital debe poder publicar un producto en máximo tres toques desde un celular de gama baja.

Restricciones: MVP en producción en un mes, equipo de 3 desarrolladores, presupuesto bajo y uso principalmente desde dispositivos móviles.

Propón tres alternativas de estilo arquitectónico. Para cada una indica fortalezas, debilidades, riesgos y los atributos de calidad que favorece o perjudica. Finalmente, recomienda una alternativa justificando la decisión.
```

### Interacción 2 — Crítica adversarial (E2)

```text
Ahora actúa como abogado del diablo y critica la alternativa de monolito modular recomendada para San Camilo en Línea.

Considera las restricciones de un MVP de un mes, equipo reducido, presupuesto bajo, celulares de gama baja y dependencia de servicios externos como WhatsApp y el mecanismo de pago con Yape.

Identifica los cinco principales riesgos de esta arquitectura y propone una posible forma de mitigarlos.
```

### Interacción 3 — Redacción de ADR-001, ADR-002 y ADR-003

Prompt reportado por el integrante (corresponde al ADR-001):

```text
Actúa como arquitecto de software. Redacta el ADR-001 en formato Markdown estructurado (Contexto, Drivers Relevantes, Alternativas Evaluadas, Decisión y Consecuencias) para justificar la adopción de un Monolito Modular en Django para el proyecto 'San Camilo en Línea'. Incluye referencias explícitas a los requerimientos R-01, R-02 y los atributos de calidad QA-01 y QA-02.
```

### Interacción 4 — Generación de `alternativa.puml`

```text
Genera el código en PlantUML (.puml) para la segunda mejor alternativa arquitectónica de 'San Camilo en Línea' (Monolito en Capas tradicional). Muestra los componentes de UI, Lógica de Negocio y Datos, los actores principales y los servicios externos. Debes incluir obligatoriamente una nota (note) de 3 a 5 líneas explicando por qué fue descartada según la matriz de decisión (puntaje 4.70/5 frente al Monolito Modular).
```

### Interacción 5 — Generación de `despliegue.py`

```text
Escribe un script ejecutable en Python usando la librería diagrams (from diagrams import ...) para representar la vista de infraestructura y despliegue del proyecto 'San Camilo en Línea'. Usa nodos genéricos de infraestructura (diagrams.onprem) para representar: Nginx como Reverse Proxy, el contenedor Django (Monolito Modular), el Celery Worker, Redis como broker, PostgreSQL, Prometheus/Grafana y los servicios externos (WhatsApp API y Yape). Muestra el flujo de conexiones entre cada componente.
```

### Interacción 6 — Compilación del trabajo del grupo en archivos `.md`

```text
Haz un archivo .md con toda la información del PDF de la guía del laboratorio. Se lo voy a entregar a Claude Code como contexto del proyecto.
```

```text
Haz un archivo .md con lo avanzado hasta el momento en el laboratorio, es decir, lo que mis compañeros hicieron en los ejercicios anteriores. Se lo voy a entregar a Claude Code como contexto del proyecto.
```

```text
Haz un archivo CLAUDE.md para Claude Code, que sirva como contexto del proyecto y que no se guarde en el repositorio de GitHub. Considera que mi trabajo ahora es hacer E7 (bitacora-ia.md) y E8 (README.md).
```

### Interacción 7 — Borrador de la bitácora (E7) y del README (E8)

Prompt de diagnóstico:

```text
Lee CLAUDE.md, guia-lab04.md y avance-lab04.md. Mi tarea es hacer E7 (bitacora-ia.md) y E8 (README.md).

Antes de escribir nada:
1. Revisa el estado real del repositorio (git status, git branch, ls -R docs/) y dime qué archivos de E1 a E6 ya existen y con qué nombres.
2. Confirma que CLAUDE.md, guia-lab04.md y avance-lab04.md NO aparecen en git status.
3. Dame la lista de datos que te faltan para completar la bitácora y el README (fechas, herramientas, roles, número de grupo, interacciones 4 y 5, etc.).

No crees ni modifiques archivos todavía. Primero respóndeme con ese diagnóstico y tus preguntas.
```

Prompt de redacción de la bitácora: además de las instrucciones de formato, incluía los datos que reportó cada integrante sobre su uso de la IA (herramienta, para qué la usó y qué corrigió). Esos datos están resumidos en la tabla de arriba.

```text
Escribe docs/architecture/bitacora-ia.md con la plantilla de la guía. Trabaja directamente en main, sin crear ramas. Muéstramelo antes de hacer commit. [...]
Reglas:
1. Las fechas salen de git log (fecha del commit de cada entregable). Si una fila no tiene commit asociado, pon <PENDIENTE: fecha>.
2. Una fila por interacción real. Mínimo 5. [...]
3. Decisión: Aceptada, Corregida o Rechazada según lo que dice arriba, con la evidencia que dieron mis compañeros. [...]
4. Los prompts de E2 están completos en avance-lab04.md; ponlos en el "Anexo: prompts". Para las filas sin prompt conocido, escribe <PENDIENTE: prompt> y no lo inventes.
```

Prompt para preparar el README (E8). Se le pidió a Claude Code que generara el prompt de E8 a partir del contexto, sin ejecutarlo:

```text
Revisa los cambios que hice, no incluyas, el cuestionario ni cambioas aun , complete los prompts. Ahora necesito que me generes un prompt en base a lo que sabes del contexto para generar el E8, SOLO GENERALO AUN NO EJECUTES , tambien no te preocupes por commits yo los voy a hacer
```

Prompt de E8 que generó Claude Code. Se envió con los roles ya completos:

```text
Lee CLAUDE.md, guia-lab04.md y avance-lab04.md. Ahora haz E8: escribe README.md en la raíz del repositorio, usando la plantilla de la guía (Paso 9). Trabaja en main. No hagas commit ni git add; yo hago los commits. Muéstrame el README antes de darlo por terminado.

Reglas:
- No modifiques ningún otro archivo (los de E1 a E7 son de mis compañeros o ya están revisados).
- No menciones CLAUDE.md, guia-lab04.md ni avance-lab04.md en el README.
- No pongas datos personales (celulares, números de Yape, nombres de comerciantes).
- Español simple y directo, como estudiantes de Ingeniería de Sistemas.
- No inventes nada. Si falta un dato, deja <PENDIENTE: ...> y avísame.

Contenido del README:

1. Título y subtítulo:
   # San Camilo en Línea — Laboratorio 04: Fundamentos de arquitectura de software
   Construcción de Software · EPIS-UNSA · 2026-B · Grupo 07

2. Integrantes (tabla Nombre | Rol en el laboratorio):
   - Flores Nuñez Rodrigo Francisco — Diagramador
   - Jimenez Paredes Fabricio Gabriel — Redactor de drivers
   - Bravo Arredondo Cristhian Matías — Verificador de IA

3. Caso (4–6 líneas): pedidos a los puestos del Mercado San Camilo con recojo o delivery; actores cliente, comerciante y repartidor; catálogo por puesto, pedido a varios puestos, pago con Yape y confirmación por WhatsApp al comerciante. Atributo crítico: capacidad de interacción, un comerciante con poca experiencia digital publica un producto en ≤ 3 toques desde un celular de gama baja (QA-01). Mencionar que la arquitectura elegida es un monolito modular con PWA (ADR-001 y ADR-002).

4. Arquitectura elegida: un bloque ```mermaid con el contenido EXACTO de diagrams/arquitectura.mmd (cópialo del archivo, no de avance-lab04.md, sin cambiar nada). Después del bloque, compáralo con el archivo (diff) y confirma que son idénticos.

5. Decisiones arquitectónicas, con las rutas reales:
   - [ADR-001: Monolito modular](docs/architecture/001-estilo-arquitectonico.md)
   - [ADR-002: PWA en lugar de app nativa](docs/architecture/002-pwa-vs-app-nativa.md)
   - [ADR-003: Notificaciones de WhatsApp asíncronas con reintentos](docs/architecture/003-notificaciones-asincronas.md)
   Usa como texto de cada enlace el título real que aparece en la primera línea de cada ADR (puedes acortarlo).

6. Documentación y diagramas (enlaces):
   - docs/architecture/drivers.md (E1)
   - docs/architecture/matriz-decision.md (E2)
   - diagrams/arquitectura.mmd (E3), diagrams/alternativa.puml (E5), diagrams/despliegue.py (E6)
   - docs/architecture/bitacora-ia.md (E7)
   No hay carpeta img/ con imágenes renderizadas: no enlaces imágenes que no existan.

7. Reflexión sobre el uso de la IA (5–8 líneas), coherente con docs/architecture/bitacora-ia.md:
   - En qué ayudó: generar y comparar alternativas (ChatGPT), crítica adversarial, borradores de ADR (Gemini), código de PlantUML y Python Diagrams (Claude), y organizar la bitácora y el README (Claude Code).
   - Qué errores cometió: asumir infraestructura en AWS cuando nuestra restricción era un VPS; usar sintaxis desactualizada de la librería diagrams (AttributeError); omitir la nota de descarte en el PlantUML; y la suposición no verificada de que Yape tiene una API pública abierta, que reemplazamos por "Yape / proveedor de pago".
   - Qué aprendimos a verificar: contrastar cada propuesta con nuestras restricciones (R-01, R-03, equipo reducido), ejecutar y validar el código generado, y no afirmar capacidades de servicios externos sin documentación oficial. La IA propone, el equipo decide y verifica.

Verificación antes de terminar:
- Comprueba con ls que todos los enlaces del README apuntan a archivos que existen.
- Confirma que el bloque Mermaid es idéntico a diagrams/arquitectura.mmd.
- Confirma que git status solo muestra README.md (y bitacora-ia.md si aún no lo commiteé), y nunca CLAUDE.md, guia-lab04.md ni avance-lab04.md.
- Al final, lista los <PENDIENTE: ...> que queden.
```
### Interacción 8 — Escenarios de calidad (Lab 08, E1)

```text
Actúa como arquitecto de software. Contexto: [pegar drivers.md, ADR-001 y el nuevo contexto: se suman los mercados Altiplano y Río Seco, cada uno con sus reglas y comerciantes]. Tarea: propón escenarios de calidad de seis partes (fuente, estímulo, entorno, artefacto, respuesta, medida) para rendimiento, disponibilidad, seguridad y modificabilidad. Para cada uno sugiere (importancia, dificultad) con H/M/L y justifícalo. Restricciones: medidas numéricas; no propongas soluciones todavía.
```

### Interacciones 9 a 11 — Tácticas candidatas (Lab 08, E2 y E4)

```text
Para el escenario [QA08-05 / QA08-04 / QA08-07] [pegar], propón 4 tácticas candidatas del catálogo de Bass et al. Para cada una indica: qué mejora, qué empeora, costo aproximado y complejidad para un equipo de 3 developers en 1 mes. Respeta el ADR-001 (monolito modular); si recomiendas cambiar el estilo, justifícalo con números.
```

### Interacciones 12 y 13 — Evaluador adversario (Lab 08, E7)

```text
Actúa como evaluador ATAM escéptico. Te paso el árbol de utilidad, los ADR-006 a 008, la vista de contenedores y los resultados de las simulaciones [pegar]. Para cada escenario (H,*) identifica: puntos de sensibilidad, puntos de trade-off, riesgos y no riesgos. Para cada riesgo indica probabilidad e impacto (1 a 5) y una pregunta incómoda que el equipo debería poder responder. No propongas rediseños completos; cita la evidencia que te falta.
```

### Interacción 14 — Borrador de atam-lite.md, matriz y README (E7 y E8)

```text
[pegar el prompt o resumen de lo que pidieron: completar atam-lite.md, la matriz de riesgos y la sección del README con los datos del informe del Lab 08]
```