# E7. Verificación de los diagramas con pyreverse

Generamos el diagrama de clases desde el código con pylint 4.1.3 (pyreverse) y lo comparamos con `docs/design/clases.puml` y con los cuatro diagramas de patrones.

```bash
pyreverse -o puml -p patrones -d docs/design/patrones/pyreverse \
  src.despues.adaptadores src.despues.decoradores src.despues.dominio src.despues.estados \
  src.despues.estrategias src.despues.eventos src.despues.factory src.despues.ia \
  src.despues.puertos src.despues.servicio
```

Salida: `pyreverse/classes_patrones.puml` y `img/classes_patrones.png` (28 clases). Pasamos los módulos uno por uno porque `src/despues/` no tiene `__init__.py`, y con la carpeta como argumento pyreverse falla ("No module named __init__").

## Diagramas por patrón

| Diagrama | Patrones (estereotipo) | Clases del código |
|---|---|---|
| `pagos.puml` → `img/pagos.png` | Strategy, Adapter, Factory | `PuertoPago`, `AdaptadorPasarelaPago`, `PagoFactory`, `PuertoInventario`, `AdaptadorInventarioRepository` |
| `estados.puml` → `img/estados.png` | State | `PedidoPuesto`, `EstadoPedidoPuesto` y 5 estados |
| `eventos.puml` → `img/eventos.png` | Observer, Decorator | `PublicadorEventos`, `Suscriptor`, `NotificadorComerciantes`, `AuditoriaPedidos`, `ConRegistroEventos` |
| `ia.puml` → `img/ia.png` | Strategy, Adapter, Decorator, Chain of Responsibility | `ProveedorLLM`, `AdaptadorClienteLLM`, `ConGuardrails`, `ConCache`, `Guardrail` y 2 guardrails |

## Comparación con el código

| # | Lo que dice pyreverse | Diagramas | Decisión |
|---|---|---|---|
| 1 | 27 de sus 28 clases aparecen en los diagramas con el mismo nombre (falta solo `PoliticaReintentos`, fila 5). `PasarelaPagoClient` e `InventarioRepository` están en `src/antes/externos.py`. | Coinciden. | Sin cambios. |
| 2 | Herencias: 2 adaptadores → puertos, 5 estados → `EstadoPedidoPuesto`, 3 clases → `ProveedorLLM`, 2 guardrails → `Guardrail`. | Coinciden. | Sin cambios. |
| 3 | `NotificadorComerciantes`, `AuditoriaPedidos` y `ConRegistroEventos` **no heredan** de `Suscriptor`. | Los dibujamos como realización (`<|..`). | Se mantiene: `Suscriptor` es un `Protocol` (tipado estructural) y las tres clases cumplen `actualizar()`. pyreverse no detecta Protocol. |
| 4 | El servicio depende de `AdaptadorInventarioRepository` (concreto). | Dibujamos la dependencia hacia `PuertoInventario`. | Se mantiene. pyreverse la infiere del valor por defecto del constructor; el atributo acepta cualquier `PuertoInventario` (así lo usa `InventarioSimulado` en las pruebas E4). |
| 5 | `PoliticaReintentos` está aislada: nadie la usa. | No aparece en los diagramas. | La dejamos fuera porque no es un patrón aplicado. Hallazgo para el grupo: el bucle de reintentos sigue en `confirmar_y_pagar` (CC 11). |
| 6 | El servicio no se relaciona con `PedidoPuesto` ni con `ProveedorLLM`. | `clases.puml` lo aclara en una nota. | State e IA están implementados y probados, pero todavía no están conectados al flujo de pago. |
| 7 | Pyreverse no tiene `Pedido`, `LineaPedido`, `Producto`, `Puesto`, `Cliente`, `Pago`, `PedidoController` ni `RepositorioPedidos`. | Siguen en `clases.puml` como diseño del Lab 05. | Se mantienen, con una nota que separa lo implementado de lo diseñado. |

## Cambios en `docs/design/clases.puml` (Lab 05)

- El `enum EstadoPedidoPuesto` pasa a ser una clase abstracta `<<State>>` con 5 subclases.
- `PasarelaPago`/`YapeAdapter` pasan a ser `PuertoPago <<Strategy>>`, `AdaptadorPasarelaPago <<Adapter>>` y `PagoFactory <<Factory>>`.
- `Notificador`/`WhatsAppNotificador` pasan a ser el Observer (`PublicadorEventos`, `Suscriptor` y 2 suscriptores) y el Decorator `ConRegistroEventos`.
- `ServicioPedidos` pasa a ser `ServicioPedidosProcesadorRefactorizado`, con la firma real de `confirmar_y_pagar`.
- Nuevo paquete `catalogo.ia` con la normalización de nombres (E5).
