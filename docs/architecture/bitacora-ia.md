# Bitácora de uso de IA — San Camilo en Línea

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 03/10/2026 | ChatGPT (GPT-5.6 Sol) | Prompt 1 adaptado (E2): 3 alternativas de estilo arquitectónico para San Camilo en Línea, con plazo de 1 mes, equipo reducido, presupuesto bajo y el atributo crítico de usabilidad. | Monolito en capas, monolito modular y microservicios. Recomendó el monolito modular. | No se aceptó asumir que Yape tiene una API pública abierta, porque eso requería verificación externa. En la arquitectura se usa "Yape / proveedor de pago", sin afirmar una integración específica (ver `diagrams/arquitectura.mmd` y la sección 4 de `matriz-decision.md`). Los microservicios se analizaron y se descartaron por la complejidad de despliegue, monitoreo e infraestructura frente a R-01, R-03 y el equipo reducido. La matriz eligió el monolito modular (4,85 frente a 4,70 y 2,80). | Corregida |
| 2 | 03/10/2026 | ChatGPT (GPT-5.6 Sol) | Prompt 2 (E2): crítica adversarial ("abogado del diablo") del monolito modular. | 5 riesgos: acoplamiento entre módulos, punto único de falla por tener un solo despliegue, base de datos única como punto de contención, fallas de los servicios externos (WhatsApp, Yape) y necesidad futura de escalar módulos por separado. | Se mantuvo el monolito modular. Ningún riesgo justifica la complejidad de los microservicios para el MVP. Las mitigaciones quedaron en ADR-001 (interfaces entre módulos y adaptadores) y ADR-003 (cola con reintentos para WhatsApp). | Aceptada |
| 3 | 04/10/2026 | Gemini (modo Thinking) | Redacción y estructura de ADR-001, ADR-002 y ADR-003. | Borradores de redacción y estructura de los tres ADR. | <PENDIENTE: qué se verificó o corrigió en los borradores de los ADR> | <PENDIENTE: decisión> |
| 4 | 04/10/2026 | Claude Opus 5.5 | Generar `alternativa.puml` (E5): monolito en capas, la alternativa descartada. | Diagrama de componentes en PlantUML del monolito en capas. | La IA no incluyó la nota (`note`) que justifica el descarte según la matriz, y la guía la exige (E5, paso 3). Rodrigo la agregó a mano con el puntaje 4,70 frente a 4,85 y la modificabilidad de 3/5. | Corregida |
| 5 | 04/10/2026 | Claude Opus 5.5 | Generar `despliegue.py` (E6): vista de despliegue con Python Diagrams. | Script de Python Diagrams con infraestructura en AWS (EC2 y RDS). | (1) La IA asumió AWS. Nuestra restricción es un VPS con Docker, Nginx y Django, así que se reemplazaron las importaciones por `diagrams.onprem` (Nginx, PostgreSQL, Redis, Celery, Prometheus, Grafana). (2) La IA usó una sintaxis desactualizada de la librería `diagrams` que daba `AttributeError` al ejecutarla. Rodrigo corrigió a mano las conexiones de Celery y Redis. | Corregida |
| 6 | <PENDIENTE: fecha> | Claude (Opus 5.5) | Compilar en archivos `.md` el trabajo del grupo (guía del laboratorio y avance de E1 a E6) como contexto local para Claude Code. | Archivos Markdown locales (no versionados) con la guía y la transcripción del avance de E1 a E6. | Se usaron solo como contexto. La fuente de verdad son los archivos del repositorio. Al compararlos, Claude Code encontró diferencias: el diagrama Mermaid reconstruido en el avance no es igual a `diagrams/arquitectura.mmd`, y el RF-02 del avance está desactualizado frente a `drivers.md`. Por eso se trabajó con los archivos del repositorio. | Aceptada |
| 7 | 04/10/2026 | Claude Code (Opus 5.5) | Revisar el repositorio y redactar el borrador de la bitácora (E7) y del README (E8) con los datos que reunió el grupo. | Diagnóstico del repositorio (rutas reales de E1 a E6, R-02 sin completar, falta la carpeta `img/`) y borrador de esta bitácora. | Cristhian revisó el borrador antes del commit. Las fechas salen de `git log`. Los datos que no se conocían quedaron marcados como pendientes en lugar de inventarse. | Aceptada |

> Los prompts completos están en el "Anexo: prompts", al final de este archivo.
> Nunca se incluyen datos personales ni información confidencial en un prompt.

## Anexo: prompts

### Interacción 1 — Generación de alternativas (E2)

```text
Actúa como arquitecto de software senior con experiencia en sistemas web para pequeños comercios.

Contexto: San Camilo en Línea es una plataforma para realizar pedidos a los puestos del Mercado San Camilo. Los clientes pueden consultar catálogos por puesto, realizar pedidos con productos de diferentes comerciantes, pagar mediante Yape y seleccionar recojo o delivery. Los comerciantes reciben confirmaciones mediante WhatsApp.

El atributo crítico es la capacidad de interacción: un comerciante con poca experiencia digital debe poder publicar un producto en máximo tres toques desde un celular de gama baja.

Restricciones: MVP en producción en un mes, equipo de [número real de integrantes] desarrolladores, presupuesto bajo y uso principalmente desde dispositivos móviles.

Propón tres alternativas de estilo arquitectónico. Para cada una indica fortalezas, debilidades, riesgos y los atributos de calidad que favorece o perjudica. Finalmente, recomienda una alternativa justificando la decisión.
```

### Interacción 2 — Crítica adversarial (E2)

```text
Ahora actúa como abogado del diablo y critica la alternativa de monolito modular recomendada para San Camilo en Línea.

Considera las restricciones de un MVP de un mes, equipo reducido, presupuesto bajo, celulares de gama baja y dependencia de servicios externos como WhatsApp y el mecanismo de pago con Yape.

Identifica los cinco principales riesgos de esta arquitectura y propone una posible forma de mitigarlos.
```

### Interacción 3 — Redacción de ADR-001, ADR-002 y ADR-003

<PENDIENTE: prompt>

### Interacción 4 — Generación de `alternativa.puml`

<PENDIENTE: prompt>

### Interacción 5 — Generación de `despliegue.py`

<PENDIENTE: prompt>

### Interacción 6 — Compilación del trabajo del grupo en archivos `.md`

<PENDIENTE: prompt>

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

Prompt de redacción del README (E8): <PENDIENTE: prompt de E8>
