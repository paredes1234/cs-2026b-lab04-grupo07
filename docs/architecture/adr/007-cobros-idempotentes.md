# ADR-007: Cobros idempotentes con registro PENDIENTE y consulta antes de reintentar

- Estado: Aceptado
- Fecha: 2026-10-31
- Decisores: Flores Nuñez Rodrigo Francisco, Jimenez Paredes Fabricio Gabriel, Bravo Arredondo Cristhian Matías
- Iteración ADD: 2 (`docs/architecture/add/iteracion-2.md`)

## Contexto
Con tres mercados cobrando por el mismo módulo Pagos, los timeouts del proveedor (R-06) se vuelven más frecuentes en números absolutos. `confirmar_y_pagar()` (`src/despues/servicio.py`) reintenta ante `ConnectionError` sin clave de idempotencia. Si el proveedor cobró y solo se perdió la respuesta (timeout tardío), el reintento cobra dos veces. QA08-04 (H,H) exige **0 cobros duplicados entre 100 intentos** cuando el proveedor responde con timeout en 10 de ellos. ADR-005 pide que el servicio solo conozca `PuertoPago`.

## Alternativas consideradas
1. Reintentos sin clave (lo actual): recupera timeouts, pero duplica cargos.
2. Sin reintento automático: no duplica, pero pierde la venta y deja cobros huérfanos.
3. Clave de idempotencia (`pedido_id`) + registro PENDIENTE en `intentos_pago` antes de llamar + consulta del estado tras cada timeout + conciliación de pendientes en el worker.
4. Circuit breaker: protege a un proveedor caído, pero no distingue un timeout tardío de uno temprano.
5. Transacción distribuida (2PC): el proveedor externo no participa.

## Decisión
Usaremos la alternativa 3, implementada como un Decorator sobre `PuertoPago` (Lab 07), para que `confirmar_y_pagar()` no cambie. El worker de Celery (ADR-003) concilia cada 5 minutos los intentos que siguen en PENDIENTE. Rechazamos la 1 y la 2 por la evidencia de abajo, la 4 porque no resuelve este escenario y la 5 porque no es aplicable.

## Evidencia
Monte Carlo `fitness/cobros.py`: 100 pedidos, 10 timeouts en el primer intento, 50 % de timeouts tardíos, 3 intentos como máximo.

| Táctica | Duplicados (semilla 2026) | Duplicados promedio (1000 corridas) | Máximo | Confirmados | Huérfanos promedio |
|---|---:|---:|---:|---:|---:|
| 1. Reintentos sin clave | 8 | 5,52 | 11 | 100 | 0,09 |
| 2. Sin reintento | 0 | 0 | 0 | 90 | 4,96 |
| **3. Idempotente** | **0** | **0** | **0** | **100** | **0** |

Al variar la fracción de timeouts tardíos de 0 a 1, la táctica 1 pasa de 0 a 11,07 duplicados promedio; la táctica 3 se mantiene en 0. FF-05 (`tests/test_fitness.py`) repite la medición en cada Pull Request.

## Consecuencias
- Positivas: se cumple QA08-04 en la simulación sin perder ventas; el servicio sigue dependiendo solo de `PuertoPago` (ADR-005, FF-02); cada cobro queda con un estado verificable.
- Negativas / riesgos (trade-off aceptado): una tabla más (`intentos_pago`), un estado PENDIENTE visible para el cliente y una tarea periódica en el worker. El punto de sensibilidad es el proveedor: si no acepta clave de idempotencia ni consulta por referencia, la táctica se reduce a la alternativa 2. Esto debe confirmarse con la documentación de Yape antes de implementarla.
