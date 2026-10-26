# ADR-005: Patrones de diseño en el flujo confirmar y pagar

- Estado: Aceptado
- Fecha: 2026-10-25
- Decisores: Flores Nuñez Rodrigo Francisco, Jimenez Paredes Fabricio Gabriel, Bravo Arredondo Cristhian Matías

## Contexto
La versión ingenua `src/antes/servicio.py` resolvía todo en `confirmar_y_pagar()`: validación, stock, cobro con reintentos en un `while` y SQL directo. Su complejidad ciclomática era 10 (B), y conocía los detalles del SDK de pagos (`cobrar_tarjeta()` responde un `dict`). Esperamos cambios en tres puntos. El primero es el medio de pago: Yape (RF-05) y quizás otros. El segundo son los avisos a varios puestos por WhatsApp (RF-06), que deben ser asíncronos y tolerar fallas (ADR-003, QA-03, R-06). El tercero es el ciclo de vida de `PedidoPuesto` (máquina de estados del Lab 05). Además, agregamos una función de IA que normaliza nombres de productos; su salida no es confiable. El plazo es un MVP en 1 mes (R-01) con 3 desarrolladores (R-02), así que solo entran patrones que eliminen un olor concreto de `olores.md` (raíz del repositorio).

## Alternativas consideradas
1. Mantener la versión antes: 80 SLOC y fácil de leer, pero cada medio de pago o aviso nuevo obliga a modificar `confirmar_y_pagar()`.
2. Aplicar solo los patrones que piden los olores: Adapter, Strategy, Factory, State, Observer, Decorator y Chain of Responsibility.
3. Usar un framework externo de máquina de estados (propuesta de la IA, olor 4): agrega una dependencia para un flujo de 6 estados.
4. Composite para el pedido de varios puestos (sugerencia de la Tabla 7 de la guía): `Pedido`, `PedidoPuesto` y `LineaPedido` del Lab 05 ya modelan la estructura y no hay recursión.

## Decisión
Usaremos la alternativa 2:
- **Adapter + Strategy + Factory** para pagos: `PuertoPago`, `AdaptadorPasarelaPago` y `PagoFactory` (registro por nombre). También `PuertoInventario` con `AdaptadorInventarioRepository`.
- **State** para `PedidoPuesto`: `EstadoPedidoPuesto` prohíbe todas las transiciones y cada estado redefine solo las del Lab 05.
- **Observer** para avisar el pago: `PublicadorEventos` con `NotificadorComerciantes` y `AuditoriaPedidos`. Reemplaza el puerto `Notificador` del ADR-004; la dependencia sigue en un solo sentido, porque el servicio solo conoce al publicador.
- **Decorator** para responsabilidades transversales: `ConRegistroEventos` (registro sin teléfonos, R-04), y `ConCache` y `ConGuardrails` en la IA.
- **Strategy + Adapter + Chain of Responsibility** para la IA: `ProveedorLLM`, `AdaptadorClienteLLM`, y `GuardrailSoloNombre` → `GuardrailCatalogo`.

Rechazamos el framework de máquina de estados (alternativa 3) y Composite (alternativa 4) por sobreingeniería para el MVP (`olores.md`, `metricas.md`).

## Consecuencias
- Positivas: el servicio no conoce el SDK de pagos; un medio nuevo se registra en `PagoFactory` sin tocar `confirmar_y_pagar()` (`test_open_closed.py`); un suscriptor nuevo no modifica el publicador; una transición inválida lanza `TransicionEstadoInvalida`; la IA se prueba con un LLM simulado y sin clave de API (`test_e5_ia.py`). Hay 18 pruebas en verde. La CC promedio baja de 3,27 a 1,99 (`metricas.md`).
- Negativas / riesgos: las SLOC suben de 80 a 401 y los archivos de 2 a 10. `confirmar_y_pagar()` pasa de CC 10 a 11, porque el bucle de reintentos sigue dentro y `PoliticaReintentos` no se usa. State e IA todavía no están conectados al flujo de pago. El único adaptador de pago es de tarjeta, no Yape. Las 8 pruebas de caracterización de E1 se borraron en E3; al ejecutarlas sobre antes y después pasan 16/16, así que el comportamiento se conservó, pero deben volver al repositorio con un fixture parametrizado. Queda como trabajo siguiente: un Decorator de reintentos sobre `PuertoPago` y un `AdaptadorYape`.
