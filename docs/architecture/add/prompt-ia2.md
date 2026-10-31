# Prompt IA 2 — Tácticas candidatas de la primera iteración ADD

**Caso:** San Camilo en Línea · **Laboratorio:** 08 · **Ejercicio:** E2 · **Herramienta:** ChatGPT

## Prompt adaptado al proyecto

> Actúa como arquitecto de software que aplica ADD 3.0. Nuestro sistema **San Camilo en Línea** es un monolito modular (ADR-001, Lab 04), con módulos Catálogo, Pedidos, Pagos, Notificaciones y Entrega. Actualmente se amplía para incorporar **Altiplano y Río Seco** además de San Camilo; cada mercado tendrá comerciantes y reglas independientes. Restricciones vigentes: equipo de 3 desarrolladores, presupuesto bajo y un mes para evolucionar el MVP.
>
> **Escenario de E1 a resolver:** QA08-05 (importancia H, dificultad H): un comerciante autenticado intenta consultar pedidos de otro mercado; en **100 intentos cruzados** entre los tres mercados se deben exponer **0 registros de otros mercados**. El elemento a refinar es la API y el repositorio de pedidos.
>
> **Tarea:** propone **4 conceptos de diseño** que atiendan el aislamiento de datos (p. ej. control por mercado en cada consulta, seguridad de filas de PostgreSQL, base por mercado, filtrado en frontend). Para cada concepto indica qué mejora, qué empeora, riesgos, esfuerzo relativo y compatibilidad con el ADR-001. Recomienda uno como primer paso viable para el equipo y **rechaza al menos una alternativa con argumentos**.
>
> No presupongas que PostgreSQL RLS está desplegado: en el Lab 06 PostgreSQL fue propuesta tecnológica por confirmar y el prototipo del Lab 07 usa SQLite. **No inventes resultados de rendimiento ni de seguridad**. Para demostrar el escenario, sugiere un prototipo reproducible con datos ficticios que compare el **número de registros ajenos expuestos** antes y después sobre exactamente 100 intentos; incluye un control positivo de lecturas legítimas. No confundas una prueba sintética con una validación de seguridad del sistema real.

## Propuestas evaluadas y revisión

| Propuesta candidata | Evaluación tras revisión del caso | Decisión |
|---|---|---|
| Columna `mercado_id` y consultas de repositorio obligatoriamente acotadas por mercado autenticado | Implementable en monolito modular; exige cobertura de *todas* las rutas y contexto de autenticación confiable | **Aceptada para prototipo E2** |
| Row-Level Security de PostgreSQL además del alcance en la aplicación | Protección en profundidad para consultas mal implementadas; requiere PostgreSQL confirmado, políticas y pruebas de sesiones/roles | **A evaluar en siguiente iteración; no se declara implementada** |
| Base de datos independiente para cada mercado | Aislamiento fuerte, pero tres bases, tres juegos de migraciones y mayor carga de respaldo/operación | **Rechazada para MVP** |
| Filtrado de mercado solo en PWA/frontend | Sencillo visualmente, pero la API seguiría enviando registros ajenos a clientes no autorizados | **Rechazada por insegura** |

**Verificación:** se construyó un prototipo SQLite con 12 pedidos sintéticos de los tres mercados, se simularon 100 accesos cruzados con semilla fija 2026 y se comprobó el resultado con Pytest. Los resultados están en `iteracion-1.md` y `resultados-aislamiento.json`.

**Alcance y cuidado:** el código de producción no se modifica en esta iteración. El contexto de mercado autenticado está supuesto; no se demuestra autenticación real ni una política RLS de PostgreSQL.
