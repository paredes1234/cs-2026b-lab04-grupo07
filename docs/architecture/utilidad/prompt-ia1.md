# Prompt IA 1 — Escenarios del árbol de utilidad (Lab 08, E1)

**Herramienta:** ChatGPT. **Proyecto:** San Camilo en Línea.

> Actúa como arquitecto de software con experiencia en atributos de calidad y ADD 3.0.

> Contexto: San Camilo en Línea permite que clientes compren productos de múltiples puestos del Mercado San Camilo, paguen mediante Yape y reciban notificaciones de WhatsApp. En el Lab 04 definimos QA-02 catálogo p95 ≤ 2 segundos, QA-03 0 pedidos perdidos ante WhatsApp no disponible con reintento ≤ 10 minutos, y ADR-001 de monolito modular (catálogo, pedidos, pagos, notificaciones, entregas). Restricciones: equipo de 3, presupuesto reducido y 1 mes.

> Nuevo escenario de crecimiento (Lab 08, tabla 11): agregar los mercados Altiplano y Río Seco, cada uno con sus propias reglas y comerciantes. Atributos críticos: modificabilidad y aislamiento de datos entre mercados.

> Tarea: propón al menos 8 escenarios de calidad de seis partes (fuente, estímulo, entorno, artefacto, respuesta, medida) que cubran rendimiento, disponibilidad, seguridad y modificabilidad. Incluye por cada escenario una medida numérica y calificaciones de importancia y dificultad (H/M/L), justificadas. No propongas soluciones ni asegures que se cumplen metas que no se han medido; distingue objetivos de resultados. Respeta el monolito modular.

## Revisión del equipo

- La sugerencia preliminar de IA para **QA08-05 (acceso cruzado entre mercados)** fue **(M,M)**.
- Se corrigió a **(H,H)**: la incorporación de dos mercados con comerciantes propios eleva la gravedad de revelar pedidos ajenos y la dificultad de verificar autorizaciones en todas las rutas.
- Las metas de carga de 12 consultas/s y 5 confirmaciones/s son supuestos de escenario, no cifras extraídas de `drivers.md`.
- El detalle de los 8 escenarios finales y de la corrección queda en `escenarios.md`.
