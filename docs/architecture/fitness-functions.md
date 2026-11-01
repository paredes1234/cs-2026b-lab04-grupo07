# E5. Fitness functions en integración continua

Se ejecutan en cada Pull Request con `.github/workflows/fitness.yml`: primero `lint-imports` y luego `python -m pytest -v`.

```bash
pip install import-linter pytest
lint-imports              # esperado: 3 kept, 0 broken
python -m pytest -v       # esperado: 40 passed
```

## Catálogo

| ID | Tipo | Qué verifica | Origen | Archivo | Degradación que detecta |
|---|---|---|---|---|---|
| FF-01 | Estructural (`layers`) | `servicio` → adaptadores, decoradores, dominio, factory, ia → eventos, estados, puertos, estrategias; sin ciclos y sin imports hacia arriba | ADR-001 | `.importlinter` | Un puerto o estado que importe al servicio (ciclo) o dos piezas del mismo nivel acopladas |
| FF-02 | Estructural (`forbidden`) | Solo `adaptadores` importa directamente `src.antes` (clientes externos) | ADR-005 (Adapter) | `.importlinter` | El servicio vuelve a llamar al SDK de pagos (`cobrar_tarjeta()`) sin pasar por `PuertoPago` |
| FF-03 | Estructural (`forbidden`) | `src.mercados` no importa pedidos, pagos ni el Lab 07 | ADR-008 | `.importlinter` | Las reglas de mercado se acoplan al flujo de pago y dejan de poder cambiarse solas |
| FF-04 | Calidad | 0 registros ajenos en 100 intentos cruzados; 12/12 lecturas propias | QA08-05, ADR-006 | `tests/test_fitness.py` | Alguien quita el filtro `mercado_id` de la consulta |
| FF-05 | Calidad | 0 cobros duplicados con 10 timeouts en 100 pedidos, y en 1000 corridas; 100/100 confirmados | QA08-04, ADR-007 | `tests/test_fitness.py` | Se reintenta el cobro sin clave de idempotencia o sin consultar antes |
| FF-06 | Calidad | Alta de un mercado con ≤ 2 módulos `.py` modificados; ningún literal de mercado fuera de `src/mercados` | QA08-07, ADR-008 | `tests/test_fitness.py` | Aparece un `if mercado == "ALTIPLANO"` en Pedidos, Catálogo o Pagos |
| FF-07 | Calidad | Cambiar una regla de Río Seco no altera las de San Camilo ni Altiplano | QA08-08, ADR-008 | `tests/test_fitness.py` | Reglas compartidas entre mercados o una configuración global |

FF-05 tiene un control (`test_ff05b_la_linea_base_si_duplica`): si la simulación dejara de producir duplicados con la táctica actual, FF-05 pasaría sin probar nada.

## Violación de prueba

En la rama `lab08/e5-violacion` introdujimos dos violaciones y luego las revertimos:

| Commit | Cambio |
|---|---|
| `6d52792` | `src/mercados/registro.py` importa `src.despues.factory` (rompe FF-03) y se agrega `src/despues/promociones.py` con `if mercado_id == "ALTIPLANO"` (rompe FF-06) |
| `847afc5` | Revierte el commit anterior |

### Salida con la violación (`6d52792`)

```text
$ lint-imports
FF-01 Capas del flujo de pago sin ciclos (ADR-001) KEPT
FF-02 Solo los adaptadores importan los clientes externos (ADR-005) KEPT
FF-03 Las reglas de mercado no dependen de pedidos ni pagos (ADR-008) BROKEN

Contracts: 2 kept, 1 broken.

FF-03 Las reglas de mercado no dependen de pedidos ni pagos (ADR-008)
src.mercados is not allowed to import src.despues:
-   src.mercados.registro -> src.despues.factory (l.13)
```

Código de salida: 1, así que el job `arquitectura` se detiene en este paso.

```text
$ python -m pytest -q tests/test_fitness.py
>       assert modulos_con_literales_de_mercado(RAIZ / "src" / carpeta) == []
E       AssertionError: assert ['promociones.py'] == []
FAILED tests/test_fitness.py::test_ff06b_sin_reglas_de_mercado_fuera_del_modulo_mercados[despues]
1 failed, 8 passed in 0.45s
```

### Salida tras revertir (`847afc5`)

```text
$ lint-imports
Contracts: 3 kept, 0 broken.
$ python -m pytest -q
40 passed in 0.50s
```

## Límites

- FF-04 y FF-05 corren sobre prototipos (`fitness/aislamiento.py`, `fitness/cobros.py`), no sobre la API real. Detectan que se quitó la táctica del prototipo, no del código de producción.
- FF-06 busca literales de mercado con `ast`. No detecta una regla escrita con un número mágico sin nombrar al mercado.
- FF-02 permite imports indirectos (`allow_indirect_imports`): el servicio llega a `src.antes` a través del adaptador, que es justamente lo que pide ADR-005.
