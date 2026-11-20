# ISSUE-03: Uso de números decimales para los importes de pago

## Observado
El procesamiento de pedidos recibe y almacena el monto como `float` en `src/despues/servicio.py`. Este tipo de dato puede producir diferencias de precisión al realizar operaciones con importes monetarios.

## Esperado
Los importes deben manejarse con una representación decimal adecuada para evitar diferencias en los céntimos durante los cálculos y el almacenamiento.

## Prueba que lo reproduce
Realizar operaciones con importes decimales, por ejemplo 0.10 + 0.20, y comprobar que el resultado monetario sea exactamente 0.30.

## Archivos relacionados
`src/despues/servicio.py`
`src/despues/dominio.py`