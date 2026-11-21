# E5 — Coordinación: agente único frente a actor-crítico (Lab 10)

## 1. Montaje

Resolvimos el **ISSUE-02** (stock no liberado ante un tipo de pago inválido) dos veces, cada una desde una copia limpia del sandbox:

```
cd agentes
python orquestador.py --issue 2 --variante unico   # un agente: lee, edita y verifica
python orquestador.py --issue 2 --variante multi   # planificador -> [ejecutor <-> revisor] x máx. 2 rondas -> humano
```

| Rol | Política (`orquestador.py`) | Herramientas |
|---|---|---|
| Agente único | `Politica(max_pasos=15)` | todas las del ejecutor |
| Planificador | `Politica(herramientas_permitidas=set(), max_pasos=2)` | ninguna: solo devuelve el plan |
| Ejecutor (actor) | `Politica(max_pasos=12)` | leer, buscar, editar, pruebas, comandos permitidos, `mapa_repo`, notas |
| Revisor (crítico) | `Politica(herramientas_permitidas=SOLO_LECTURA, max_pasos=8)` | `ver_cambios`, `leer_archivo`, `buscar`, `ejecutar_pruebas`, `mapa_repo`, `leer_notas` |

**Control del experimento.** En la ronda 1, el ejecutor repite exactamente las decisiones del agente único (`trayectorias/issue02_multi/ejecutor.json` es una copia de `trayectorias/issue02_unico/ejecutor.json`). Así, la única variable es la presencia del revisor y no la suerte del modelo.

## 2. Resultados (de `trazas/issue02_*/resumen.json`)

| Métrica | Agente único | Actor-crítico |
|---|---|---|
| Rondas | 1 | 2 de 2 |
| Acciones | 6 | 17 (planificador 0, ejecutor 6 + 5, revisor 4 + 2) |
| Rechazadas por el contrato | 0 | 0 |
| Bloqueadas por la política | 0 | 0 |
| Contexto final | **7 506** caracteres | **40 250** caracteres en total (planificador 863, ejecutor 7 860 + 14 436, revisor 13 290 + 3 801) |
| Costo relativo | 1× | 2,8× acciones, 5,4× contexto |
| Pruebas al final (orquestador) | 49 aprobadas, 1 fallo (ISSUE-03) | 49 aprobadas, 1 fallo (ISSUE-03) |
| `test_issue_02` | pasa | pasa |
| Veredicto | "resuelto" (autoevaluación) | `APROBADO` en la ronda 2, tras `CAMBIOS SOLICITADOS` en la 1 |

Diagrama de la trayectoria actor-crítico: `trazas/issue02_multi/trayectoria.mmd` (generado con `python agente/traza.py trazas/issue02_multi`).

### ¿El revisor encontró algo que el agente único pasó por alto?

**Sí, dos defectos reales**, ambos en `src/despues/servicio.py` y sin prueba que los cubra:

1. **Intento de cobro previo.** Si el pedido ya tiene un intento registrado (`PENDIENTE_VERIFICACION`, que deja el ISSUE-01), la línea 146 lanza `RuntimeError` después de reservar el stock (línea 120) y no lo libera.
2. **"Obtener o ejecutar".** El issue pide liberar el stock si no se puede obtener **o ejecutar** la estrategia. El agente único solo protegió `obtener()`. En `procesar_pago`, solo `ConnectionError` y `ValueError` liberaban stock: cualquier otra excepción lo retenía.

Verificamos ambos hallazgos de forma independiente, ejecutando los dos casos sobre cada resultado:

| Caso | Agente único | Actor-crítico |
|---|---|---|
| `procesar_pago` lanza `RuntimeError` | liberaciones: `[]` | `[('X', 1)]` |
| Reintento de un pedido en `PENDIENTE_VERIFICACION` | liberaciones: `[]` | `[('X', 1)]` |

El revisor los encontró porque su objetivo le pide revisar "contra lo ESPERADO en el issue, no solo contra la prueba" y porque leyó `servicio.py` completo. El agente único se guió por la prueba en rojo: cuando pasó a verde, terminó.

## 3. Conclusión (principio de parsimonia)

Para el ISSUE-02 de San Camilo en Línea, el bucle actor-crítico sí compensó su costo, aunque es 5,4 veces más caro en contexto y 2,8 veces en acciones. El cambio toca dinero e inventario, y el revisor encontró dos fugas de stock reales que ninguna prueba detectaba. Si el agente único las hubiera dejado pasar, un puesto del mercado mostraría productos agotados sin estarlo.

Aun así, la parsimonia (Albada, 2025, cap. 8) nos lleva a no usarlo siempre. Lo reservamos para los módulos de alto riesgo (`servicio.py`, pagos, inventario) y dejamos el agente único más la revisión humana para cambios de bajo riesgo, como el issue 3 de E4.

También notamos que el hallazgo salió de leer lo "Esperado" del issue. Un paso de reflexión en el agente único (arquetipo Reflexión, Tabla 3) o una prueba más completa en E1 quizá lo habrían encontrado con menos costo. No lo medimos.

## 4. Limitaciones y lo que queda para el humano

- Es una sola ejecución por variante y el mismo asistente de IA actuó como planificador, ejecutor y revisor. En un sistema real, el crítico debería usar otro prompt o, idealmente, otro modelo.
- El revisor no puede agregar pruebas (`tests/` está protegido y su política es de solo lectura). Las pruebas para los dos hallazgos quedan como tarea humana; su veredicto lo dice explícitamente.
- Los números de contexto suman los historiales de cada agente. No incluyen el prompt de sistema porque `ModeloGrabado` no lo usa.
