# ISSUE-02: Reserva de inventario no liberada ante un tipo de pago inválido

## Observado
En `src/despues/servicio.py`, el método `confirmar_y_pagar()` reserva el inventario antes de obtener la estrategia de pago. Si el tipo de pago no existe, puede producirse una excepción sin liberar el stock reservado.

## Esperado
Si no se puede obtener o ejecutar una estrategia de pago, el inventario reservado debe liberarse para que el producto vuelva a estar disponible.

## Prueba que lo reproduce
Utilizar un inventario simulado, enviar un tipo de pago no registrado y comprobar que se ejecuta `liberar_stock()` después del error.

## Archivo relacionado
`src/despues/servicio.py`