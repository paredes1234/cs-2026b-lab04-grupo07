# E6. Métricas y trade-off — San Camilo en Línea

## 1. Complejidad ciclomática y líneas de código

Mediciones con **Radon** sobre los directorios completos `src/antes` y
`src/despues`. **CC** es la complejidad ciclomática. **SLOC** representa
las líneas de código fuente sin comentarios ni líneas en blanco.

| Métrica | Antes | Después |
|---|---:|---:|
| CC promedio general de Radon (clases, funciones y métodos) | 3.27 | 1.99 |
| CC promedio solo por función/método (sin clases) | 3.00 | 1.69 |
| CC máxima por función/método | 10 | 11 |
| SLOC | 80 | 401 |
| Bloques analizados por Radon (C, M, F) | 11 | 92 |
| Funciones y métodos únicos (M, F) | 8 | 64 |
| Archivos Python | 2 | 10 |

El promedio general se obtiene contando las clases además de sus métodos,
igual que `radon cc -s -a`. El promedio por función/método excluye las
clases y **cada método se cuenta una sola vez**.

La CC promedio general disminuyó de **3.27** a
**1.99**, mientras que las SLOC aumentaron de
**80** a **401**. Sin embargo, la mayor CC de un método
cambió de **10** a **11**; por ello,
no todos los métodos se volvieron más simples. El código después incluye
más módulos y funcionalidad de IA, de modo que esta comparación no mide
rendimiento ni garantiza equivalencia estricta del alcance funcional.

### Complejidad de cada función/método: antes

| Archivo | Función o método | CC | Grado |
|---|---|---:|:---:|
| `src/antes/externos.py` | `InventarioRepository.__init__` | 1 | A |
| `src/antes/externos.py` | `InventarioRepository.devolver_stock` | 2 | A |
| `src/antes/externos.py` | `InventarioRepository.verificar_y_descontar` | 2 | A |
| `src/antes/externos.py` | `PasarelaPagoClient.cobrar_tarjeta` | 3 | A |
| `src/antes/servicio.py` | `ServicioPedidosProcesador.__init__` | 2 | A |
| `src/antes/servicio.py` | `ServicioPedidosProcesador._get_connection` | 2 | A |
| `src/antes/servicio.py` | `ServicioPedidosProcesador._init_db` | 2 | A |
| `src/antes/servicio.py` | `ServicioPedidosProcesador.confirmar_y_pagar` | 10 | B |

**Promedio por método antes:** 3.00.

### Complejidad de cada función/método: después

| Archivo | Función o método | CC | Grado |
|---|---|---:|:---:|
| `src/despues/adaptadores.py` | `AdaptadorInventarioRepository.__init__` | 2 | A |
| `src/despues/adaptadores.py` | `AdaptadorInventarioRepository.liberar_stock` | 1 | A |
| `src/despues/adaptadores.py` | `AdaptadorInventarioRepository.reservar_stock` | 1 | A |
| `src/despues/adaptadores.py` | `AdaptadorPasarelaPago.__init__` | 2 | A |
| `src/despues/adaptadores.py` | `AdaptadorPasarelaPago.procesar_pago` | 1 | A |
| `src/despues/decoradores.py` | `ConRegistroEventos.__init__` | 1 | A |
| `src/despues/decoradores.py` | `ConRegistroEventos.actualizar` | 1 | A |
| `src/despues/dominio.py` | `PedidoPuesto.__init__` | 3 | A |
| `src/despues/dominio.py` | `PedidoPuesto.estado` | 1 | A |
| `src/despues/dominio.py` | `PedidoPuesto.marcar_listo` | 1 | A |
| `src/despues/dominio.py` | `PedidoPuesto.rechazar` | 1 | A |
| `src/despues/dominio.py` | `PedidoPuesto.registrar_entrega` | 1 | A |
| `src/despues/dominio.py` | `PedidoPuesto.registrar_recojo` | 1 | A |
| `src/despues/estados.py` | `EstadoEntregado.nombre` | 1 | A |
| `src/despues/estados.py` | `EstadoListo.nombre` | 1 | A |
| `src/despues/estados.py` | `EstadoListo.registrar_entrega` | 1 | A |
| `src/despues/estados.py` | `EstadoListo.registrar_recojo` | 1 | A |
| `src/despues/estados.py` | `EstadoPedidoPuesto.marcar_listo` | 1 | A |
| `src/despues/estados.py` | `EstadoPedidoPuesto.nombre` | 1 | A |
| `src/despues/estados.py` | `EstadoPedidoPuesto.rechazar` | 1 | A |
| `src/despues/estados.py` | `EstadoPedidoPuesto.registrar_entrega` | 1 | A |
| `src/despues/estados.py` | `EstadoPedidoPuesto.registrar_recojo` | 1 | A |
| `src/despues/estados.py` | `EstadoRechazado.nombre` | 1 | A |
| `src/despues/estados.py` | `EstadoRecibido.marcar_listo` | 1 | A |
| `src/despues/estados.py` | `EstadoRecibido.nombre` | 1 | A |
| `src/despues/estados.py` | `EstadoRecibido.rechazar` | 1 | A |
| `src/despues/estados.py` | `EstadoRecogido.nombre` | 1 | A |
| `src/despues/estados.py` | `EstadoRecogido.registrar_entrega` | 1 | A |
| `src/despues/estrategias.py` | `PoliticaReintentos.__init__` | 1 | A |
| `src/despues/estrategias.py` | `PoliticaReintentos.ejecutar` | 7 | B |
| `src/despues/eventos.py` | `AuditoriaPedidos.__init__` | 1 | A |
| `src/despues/eventos.py` | `AuditoriaPedidos.actualizar` | 1 | A |
| `src/despues/eventos.py` | `NotificadorComerciantes.__init__` | 1 | A |
| `src/despues/eventos.py` | `NotificadorComerciantes.actualizar` | 3 | A |
| `src/despues/eventos.py` | `PublicadorEventos.__init__` | 1 | A |
| `src/despues/eventos.py` | `PublicadorEventos.publicar` | 2 | A |
| `src/despues/eventos.py` | `PublicadorEventos.suscribir` | 2 | A |
| `src/despues/eventos.py` | `Suscriptor.actualizar` | 1 | A |
| `src/despues/factory.py` | `PagoFactory.__init__` | 1 | A |
| `src/despues/factory.py` | `PagoFactory.obtener` | 2 | A |
| `src/despues/factory.py` | `PagoFactory.registrar` | 1 | A |
| `src/despues/ia.py` | `AdaptadorClienteLLM.__init__` | 1 | A |
| `src/despues/ia.py` | `AdaptadorClienteLLM.normalizar_nombre` | 1 | A |
| `src/despues/ia.py` | `ClienteLLMExterno.completar` | 1 | A |
| `src/despues/ia.py` | `ConCache.__init__` | 1 | A |
| `src/despues/ia.py` | `ConCache.normalizar_nombre` | 2 | A |
| `src/despues/ia.py` | `ConGuardrails.__init__` | 1 | A |
| `src/despues/ia.py` | `ConGuardrails.normalizar_nombre` | 2 | A |
| `src/despues/ia.py` | `Guardrail.__init__` | 1 | A |
| `src/despues/ia.py` | `Guardrail._comprobar` | 1 | A |
| `src/despues/ia.py` | `Guardrail.validar` | 2 | A |
| `src/despues/ia.py` | `GuardrailCatalogo.__init__` | 2 | A |
| `src/despues/ia.py` | `GuardrailCatalogo._comprobar` | 3 | A |
| `src/despues/ia.py` | `GuardrailSoloNombre._comprobar` | 7 | B |
| `src/despues/ia.py` | `ProveedorLLM.normalizar_nombre` | 1 | A |
| `src/despues/ia.py` | `_nombre_clave` | 1 | A |
| `src/despues/ia.py` | `crear_normalizador` | 1 | A |
| `src/despues/puertos.py` | `PuertoInventario.liberar_stock` | 1 | A |
| `src/despues/puertos.py` | `PuertoInventario.reservar_stock` | 1 | A |
| `src/despues/puertos.py` | `PuertoPago.procesar_pago` | 1 | A |
| `src/despues/servicio.py` | `ServicioPedidosProcesadorRefactorizado.__init__` | 6 | B |
| `src/despues/servicio.py` | `ServicioPedidosProcesadorRefactorizado._get_connection` | 2 | A |
| `src/despues/servicio.py` | `ServicioPedidosProcesadorRefactorizado._init_db` | 2 | A |
| `src/despues/servicio.py` | `ServicioPedidosProcesadorRefactorizado.confirmar_y_pagar` | 11 | C |

**Promedio por método después:** 1.69.

## 2. Trade-off (7 líneas)

1. Se separaron las responsabilidades de pagos, estados, notificaciones y normalización de productos.
2. Strategy, Adapter y Factory permiten cambiar adaptadores de pago con menor acoplamiento.
3. State delimita transiciones válidas y Observer desacopla el procesamiento de los avisos.
4. Decorator agrega registro y caché, mientras que los guardrails validan las respuestas simuladas de IA.
5. La complejidad promedio general disminuyó, aunque el método más complejo pasó de CC 10 a 11.
6. El costo fue aumentar las líneas de código, los módulos, las abstracciones y la cantidad de pruebas.
7. La versión inicial habría sido suficiente para un prototipo simple con un único proveedor y sin ampliaciones.

## 3. Patrón que se decidió no aplicar: Composite

Se evaluó Composite porque un pedido puede contener productos de varios
puestos. Sin embargo, `Pedido`, `PedidoPuesto` y `LineaPedido` del Lab 05
representan la estructura necesaria. No se requiere tratar elementos
individuales y agrupaciones de forma recursiva mediante la misma interfaz.
Incorporar Composite al MVP agregaría una jerarquía sin una necesidad
actual demostrada, por lo que se decidió no aplicarlo.

## Comandos ejecutados

```bash
.venv/bin/radon cc -s -a src/antes
.venv/bin/radon cc -s -a src/despues
.venv/bin/radon raw -s src/antes
.venv/bin/radon raw -s src/despues
.venv/bin/python scripts/generar_metricas_lab07.py
.venv/bin/python -m pytest -q
```
