# E6 — Humano en el circuito y delegación progresiva (Lab 10)

## 1. Aprobación humana de cada edición

`agente/humano.py` define `AprobadorConsola`, que se conecta a `Politica.aprobar_edicion` del ejecutor:

```
cd agentes
python orquestador.py --issue 2 --variante multi --humano
```

| Patrón (Tabla 8) | Cómo lo aplicamos | Prueba (`pruebas_agente/test_e6_humano.py`) |
|---|---|---|
| Aprobar o rechazar | Cada `editar_archivo` del ejecutor espera la respuesta. `n` lo bloquea con "El revisor humano rechazó la edición", y el agente recibe ese motivo como observación. | `test_s_aprueba_...`, `test_n_rechaza_...` |
| Revisar llamadas a herramientas | Antes de preguntar, se muestran el archivo y el fragmento `antes` / `después`. | `test_se_muestra_la_edicion_antes_de_preguntar` |
| Validar la entrada humana | Solo `s` o `n`: `si`, `S`, `y` o vacío se rechazan y se vuelve a preguntar. Tras 3 respuestas inválidas, la edición se rechaza (falla segura). | `test_respuesta_invalida_...`, `test_sin_respuesta_valida_...` |
| Revisar y editar (parcial) | Tras `s` o `n`, la persona puede dejar una observación ("aprobada, pero falta una prueba"). No cambia la edición: queda en el registro. | `test_la_observacion_humana_...`, `test_observacion_vacia_...` |
| Registro | Cada decisión va a `trazas/<id>/aprobaciones.jsonl` con la ruta, el resultado y las respuestas escritas. Se guarda el rol ("integrante del grupo"), no el nombre. | `test_cada_decision_queda_registrada_sin_datos_personales` |

El orden de las capas importa: primero se aplican el contrato, la lista de herramientas, la lista de comandos y las rutas protegidas, y solo después se pregunta al humano. Una edición de `tests/` se bloquea sin consultar a nadie (`test_la_ruta_protegida_se_bloquea_antes_de_molestar_al_humano`). Así, el humano solo ve lo que la política ya permite.

Antes de E6, `aprobar_edicion` era un atributo de clase sin anotación: no era un campo del `dataclass` y no se podía pasar como `Politica(aprobar_edicion=...)`. Lo convertimos en campo.

### Ejecución con el humano en el circuito

```
python orquestador.py --issue 2 --variante multi --humano --respuestas trayectorias/issue02_multi/aprobaciones_humanas.json
```

Las decisiones las tomó un integrante del grupo, que revisó las 3 ediciones del ejecutor. Quedaron transcritas en `trayectorias/issue02_multi/aprobaciones_humanas.json` para que la ejecución sea reproducible (campo `origen` del registro). Sin `--respuestas`, el orquestador pregunta por consola.

| # | Ronda | Edición (`src/despues/servicio.py`) | Decisión | Observación registrada |
|---|---|---|---|---|
| 1 | 1 | `try/except ValueError` alrededor de `fabrica_pagos.obtener()` | `s` (aprobada) | — |
| 2 | 2 | `liberar_stock` antes del `RuntimeError` por intento de cobro previo | `s` (aprobada) | — |
| 3 | 2 | `except ValueError` → `except Exception` en `procesar_pago` | `s` (aprobada) | "except Exception es amplio; se acepta porque relanza el error y no hay doble liberación, pero antes de llevarlo a src/ faltan pruebas para un RuntimeError en procesar_pago y para el reintento de un pedido en PENDIENTE_VERIFICACION." |

Resultado (`trazas/issue02_multi_humano/`): 3 de 3 ediciones aprobadas, 0 respuestas inválidas y 1 observación. El revisor dio `APROBADO` en la ronda 2. Pruebas: 49 de 50 (la falla es del ISSUE-03). `cambios.diff` es idéntico al de la variante sin humano. La observación coincide con el punto (3) del revisor: los dos hallazgos siguen sin prueba propia y quedan como tarea humana antes de fusionar a `src/`.

Limitación: con `ModeloGrabado`, las decisiones ya están grabadas. Si el humano rechaza una edición, el agente recibe el bloqueo como observación, pero la decisión siguiente no cambia. Para ver una reacción real ante el rechazo hay que usar `--interactivo`.

## 2. Hoja de ruta de delegación (Albada, 2025, cap. 13)

La autonomía crece con la evidencia. Para cada etapa, definimos qué puede hacer el agente en San Camilo en Línea y qué deben mostrar las trazas (`trazas/<id>/resumen.json`, `*.jsonl`, `aprobaciones.jsonl`) para pasar a la siguiente.

| Etapa (rol humano) | Qué hace la persona | Permisos del agente | Evidencia para pasar a la siguiente |
|---|---|---|---|
| **1. Ejecutor** | Escribe el cambio. El agente solo sugiere. | Solo lectura: `leer_archivo`, `buscar`, `mapa_repo`, `ejecutar_pruebas`, `leer_notas`. Sin `editar_archivo` ni `ejecutar_comando`. | En ≥ 3 issues, el diagnóstico del agente (archivo y causa) coincide con el arreglo humano, y 0 decisiones son rechazadas por el contrato en las últimas 2 tareas. |
| **2. Revisor** *(hoy)* | Aprueba o rechaza **cada** edición (`--humano`) y el PR. | Edita en una copia del sandbox con `aprobar_edicion`. Comandos solo de la lista (`pytest`, `radon`, `lint-imports`, `git status/diff`). `tests/` protegido. Máx. 12 pasos y 2 rondas. | En ≥ 5 issues: ≥ 90 % de ediciones aprobadas sin cambios, 0 intentos de editar `tests/`, 0 comandos bloqueados por inyección, y el resumen final del agente coincide siempre con las pruebas que corre el orquestador. |
| **3. Colaborador** | Ya no aprueba cada edición: revisa el diff completo y el veredicto del revisor antes del PR. | Igual que la etapa 2, pero sin `aprobar_edicion`. El revisor (crítico) es obligatorio en pagos e inventario. | En ≥ 10 PR: ningún defecto encontrado por humanos después de un `APROBADO` del revisor, y cada hallazgo del revisor confirmado con una prueba nueva. |
| **4. Gobernador** | Define la política (herramientas, rutas, límites, módulos de riesgo) y audita las trazas por muestreo. | Abre el PR solo. Puede fusionar cambios de bajo riesgo (documentación, `src/mercados/` con `test_fitness.py` en verde). Pagos e inventario siguen requiriendo aprobación humana. | Etapa de llegada. Se retrocede de etapa si una auditoría encuentra un defecto en `main` causado por el agente, o un intento de inyección que pasó la política. |

## 3. Dónde dejamos hoy al agente y por qué

En la **etapa 2 (revisor)**. Las trazas no justifican avanzar:

- **El agente afirmó algo que las pruebas no mostraban.** En E2 (`trazas/ejecutor.jsonl`, pasos 5–7), `ejecutar_pruebas` devolvió `ModuleNotFoundError: No module named 'fitness'` y la colección de pruebas se interrumpió. Aun así, el agente terminó con "Se resolvió el ISSUE-01". Por eso el orquestador ahora vuelve a correr las pruebas por su cuenta (`pruebas_finales` en `resumen.json`).
- **El agente único pasó por alto 2 defectos** en el ISSUE-02 que el revisor sí encontró (`coordinacion.md`). Sin crítico ni humano, habrían llegado al PR.
- **A favor:** en las 4 ejecuciones de E4 y E5 hubo 0 rechazos del contrato y 0 bloqueos de la política, y el agente nunca intentó editar `tests/`. Pero son solo 2 issues, y la etapa 2 pide ≥ 5.

Para pasar a **colaborador** necesitamos 5 issues más con el registro de `aprobaciones.jsonl` y las métricas de la tabla anterior.
