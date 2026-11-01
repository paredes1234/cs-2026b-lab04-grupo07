# ADR-006: Aislar los pedidos de cada mercado con `mercado_id` en el repositorio

- Estado: Aceptado
- Fecha: 2026-10-31
- Decisores: Flores Nuñez Rodrigo Francisco, Jimenez Paredes Fabricio Gabriel, Bravo Arredondo Cristhian Matías
- Iteración ADD: 1 (`docs/architecture/add/iteracion-1.md`)

## Contexto
El sistema crece de un mercado a tres: San Camilo, Altiplano y Río Seco, cada uno con sus comerciantes (escenario de crecimiento, caso 7). Con una sola base de datos (ADR-001), un comerciante podría leer pedidos de otro mercado. QA08-05 (H,H) exige **0 registros ajenos expuestos en 100 intentos cruzados**. Seguimos con 1 mes (R-01), 3 desarrolladores (R-02), presupuesto bajo (R-03) y datos personales que proteger (R-04).

## Alternativas consideradas
1. Columna `mercado_id` y toda consulta del repositorio acotada al mercado de la sesión autenticada.
2. Row-Level Security (RLS) de PostgreSQL: defensa en la base de datos, pero exige políticas, roles y pruebas de conexión.
3. Una base de datos por mercado: aislamiento físico, pero triplica migraciones, respaldos y costo.
4. Filtrar solo en la PWA: la API seguiría entregando registros ajenos.

## Decisión
Usaremos la alternativa 1. El `mercado_id` se toma de la sesión autenticada, nunca de un parámetro del cliente, y toda lectura usa `WHERE id = ? AND mercado_id = ?`. RLS (alternativa 2) queda como refuerzo cuando PostgreSQL esté confirmado. Rechazamos la 3 por costo de operación y la 4 por insegura.

## Evidencia
Prototipo `fitness/aislamiento.py` (SQLite en memoria, 12 pedidos sintéticos, semilla 2026):

| Medida QA08-05 | Antes (sin filtro) | Después (con `mercado_id`) | Meta |
|---|---:|---:|---:|
| Registros ajenos expuestos en 100 intentos | 100 | **0** | 0 |
| Lecturas propias permitidas | — | 12/12 | 12/12 |

La fitness function FF-04 (`tests/test_fitness.py`) repite la medición en cada Pull Request.

## Consecuencias
- Positivas: se cumple QA08-05 en el prototipo; seguimos con una sola base y un solo despliegue (ADR-001); agregar un mercado no exige otra base.
- Negativas / riesgos (trade-off aceptado): cada consulta y cada prueba lleva una condición más. El punto de sensibilidad es que **todas** las consultas apliquen el filtro: un endpoint que lo omita vuelve a exponer datos. FF-04 solo cubre el prototipo; en la API real hará falta una prueba por endpoint o RLS.
