# ISSUE-01: Posibles cobros duplicados por reintentos

## Observado
En `src/despues/servicio.py`, el método `confirmar_y_pagar()` vuelve a llamar al proveedor de pagos cuando ocurre un `ConnectionError`. Actualmente no utiliza una clave de idempotencia ni consulta el resultado del primer intento antes de reintentar.

## Esperado
Un mismo pedido debe generar como máximo un cobro, incluso cuando el proveedor haya procesado el pago pero se pierda la respuesta por un problema de conexión.

## Prueba que lo reproduce
Simular un proveedor que procesa el primer cobro, pero devuelve un error de conexión. Después, comprobar que el reintento no genera un segundo cobro para el mismo pedido.

## Archivo relacionado
`src/despues/servicio.py`

## Referencia
`docs/architecture/adr/007-cobros-idempotentes.md`