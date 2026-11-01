# ADR-008: Reglas de cada mercado en un módulo propio, cargadas desde configuración

- Estado: Aceptado
- Fecha: 2026-10-31
- Decisores: Flores Nuñez Rodrigo Francisco, Jimenez Paredes Fabricio Gabriel, Bravo Arredondo Cristhian Matías
- Iteración ADD: 3 (`docs/architecture/add/iteracion-3.md`)

## Contexto
Altiplano y Río Seco llegan con sus propias reglas: monto mínimo, horario de atención y delivery. Si cada módulo resuelve esas reglas con `if mercado == ...`, cada mercado nuevo toca Catálogo, Pedidos y Entrega. QA08-07 (H,H) exige **≤ 2 módulos existentes modificados y ≤ 2 días de trabajo por mercado**; QA08-08 (H,M) exige cambiar una regla de Río Seco sin afectar a los otros mercados. Seguimos con el monolito modular (ADR-001) y con Strategy y Factory del Lab 07 (ADR-005).

## Alternativas consideradas
1. Condicionales `if mercado == ...` en cada módulo.
2. Módulo `mercados` con las reglas como datos (`mercados.json`) y un único punto de entrada, `RegistroMercados.obtener(mercado_id)`.
3. Motor de reglas genérico (DSL): flexible, pero excede R-01 y R-02 para 5 parámetros.
4. Una instancia desplegada por mercado: contradice ADR-001 y R-03.

## Decisión
Usaremos la alternativa 2, implementada en `src/mercados/` (`reglas.py`, `registro.py`, `mercados.json`). Ningún módulo fuera de `src/mercados` escribe el identificador de un mercado, y `mercados` no depende de pedidos ni pagos. Si un mercado necesita una regla que no sea un parámetro, se agregará una Strategy registrada en el mismo registro (como `PagoFactory`), con un ADR nuevo.

## Evidencia
Experimento `fitness/alta_mercados.py`: agrega un cuarto mercado sobre copias temporales y cuenta los cambios con `difflib`.

| Medida (alta de 1 mercado) | 1. Condicionales | **2. Configuración** | Meta QA08-07 |
|---|---:|---:|---:|
| Módulos `.py` existentes modificados | 3 | **0** | ≤ 2 |
| Archivos modificados | 3 | 1 (`mercados.json`) | — |
| Líneas cambiadas | 6 | 9 | — |

Los días de trabajo no se midieron. FF-03 (`.importlinter`), FF-06 y FF-07 (`tests/test_fitness.py`) protegen la decisión en cada Pull Request.

## Consecuencias
- Positivas: se cumple la medida de módulos de QA08-07 (0 de ≤ 2); una regla cambia en un solo lugar y no afecta a los otros mercados (QA08-08, FF-07); las reglas pueden revisarse sin leer código.
- Negativas / riesgos (trade-off aceptado): no se ahorran líneas (9 frente a 6), solo se concentran en un archivo. La configuración se lee al arrancar, así que un cambio de regla exige reiniciar la aplicación. El punto de sensibilidad es la disciplina del equipo: un `if mercado == "ALTIPLANO"` en Pedidos rompe la táctica, y por eso FF-06 lo detecta en la CI.
