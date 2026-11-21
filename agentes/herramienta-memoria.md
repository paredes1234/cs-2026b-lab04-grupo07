# E4 — Herramienta nueva y memoria de notas (Lab 10)

## 1. Qué agregamos

| Pieza | Archivo | Qué hace | Prueba |
|---|---|---|---|
| `mapa_repo(carpeta='src')` | `agente/herramientas.py` | Recorre los `.py` con `ast` y devuelve clases y funciones con línea y firma (parámetros, tipos, retorno), sin cuerpos. Respeta el sandbox. Si un archivo no compila, lo informa y sigue. | `pruebas_agente/test_e4_herramientas.py` (4 pruebas) |
| `anotar(texto)` | `agente/herramientas.py` | Agrega `- [n] texto` a `notas.md` del sandbox. Rechaza notas vacías, de más de 300 caracteres o por encima de 20 notas. | `test_notas_*`, `test_anotar_*` |
| `leer_notas()` | `agente/herramientas.py` | Devuelve las notas de la tarea. Solo lectura. | `test_notas_se_guardan_en_notas_md_y_se_leen` |
| Política | `agente/politica.py` | El ejecutor recibe las tres herramientas. El revisor solo `mapa_repo` y `leer_notas` (`SOLO_LECTURA`): puede leer la pizarra, no escribirla. | `test_revisor_puede_leer_notas_pero_no_anotar` |

Seguimos las buenas prácticas de la Sección 1.5:

- **Descripción clara.** El texto de `catalogo()` dice qué hace cada herramienta, sus parámetros, qué devuelve y cuándo usarla ("úsela antes de leer archivos completos").
- **Alcance mínimo.** Las tres herramientas son de lectura o solo escriben `notas.md`.
- **Entradas restringidas.** Las rutas pasan por `_ruta()` y las notas tienen límites.
- **Errores como observaciones.** Una carpeta inválida o una nota larga devuelven `ERROR: ...` y no lanzan una excepción.

La memoria es de tipo **notas o pizarra** (Tabla 6): vive solo durante la tarea, en la copia del sandbox, y el orquestador la copia a `trazas/<id>/notas.md` como evidencia.

### Cambios colaterales en el framework

- `ver_cambios()` ya no recibe la ruta del original como argumento: antes el modelo podía pasar `original="../../"` y leer fuera del sandbox con `_ruta_libre()`. Ahora la fija el programa en el constructor (mínimo privilegio). Prueba: `test_ver_cambios_ya_no_acepta_una_ruta_elegida_por_el_modelo`.
- `ejecutar_pruebas()` y `ejecutar_comando()` decodifican la salida en UTF-8. En Windows, un acento en la salida de pytest lanzaba `UnicodeDecodeError` dentro de la herramienta y el agente recibía un `TypeError` en lugar del resultado de las pruebas. Lo detectamos en el paso 2 de la línea base del issue 3.
- `agente/sandbox.py`: cada ejecución trabaja en `agentes/ejecuciones/<id>/` (ignorada por git), copiada de `agentes/trabajo/` más `fitness/`, `prompts/` y `seguridad/`. Sin esas carpetas, 2 módulos de prueba fallan al importarse, pytest se interrumpe y el agente no ve las pruebas de los issues. Es lo que muestra el paso 5 de `trazas/ejecutor.jsonl` (E2): `ModuleNotFoundError: No module named 'fitness'`.

## 2. Experimento: issue 3 con y sin las herramientas nuevas

Para medir el efecto, resolvimos el **mismo** issue dos veces, desde la misma copia limpia:

```
cd agentes
python orquestador.py --issue 3 --variante unico --sin-e4   # línea base: herramientas de E2
python orquestador.py --issue 3 --variante unico            # con mapa_repo, anotar y leer_notas
```

Las decisiones las tomó paso a paso un asistente de IA (Claude Code), que decidía a partir de la observación real de cada herramienta (ver la limitación de la sección 4). Quedaron grabadas en `trayectorias/issue03_unico_base/` y `trayectorias/issue03_unico/`. Las herramientas se ejecutan de verdad en cada reproducción.

| Métrica (de `trazas/<id>/resumen.json`) | Línea base (`issue03_unico_base`) | Con E4 (`issue03_unico`) |
|---|---|---|
| Pasos | 12 | 14 |
| Acciones | 11 | 13 |
| Rechazadas por el contrato / bloqueadas por la política | 0 / 0 | 0 / 0 |
| Herramientas | `leer_archivo` 3, `buscar` 1, `editar_archivo` 5, `ejecutar_pruebas` 2 | `leer_archivo` 1, `mapa_repo` 1, `buscar` 1, `anotar` 2, `leer_notas` 1, `editar_archivo` 5, `ejecutar_pruebas` 2 |
| Contexto final | **18 993** caracteres (~4 700 tokens) | **26 645** caracteres (~6 700 tokens), +40 % |
| Pruebas al final (orquestador) | 49 aprobadas, 1 fallo (ISSUE-02) | 49 aprobadas, 1 fallo (ISSUE-02) |
| Cambio en el código | igual en ambos: `Decimal` con 2 decimales, columna `TEXT`, `str(monto)` en los 2 `INSERT` | igual |

### Tamaño de cada observación (medido sobre la copia original)

| Observación | Caracteres |
|---|---|
| `leer_archivo("src/despues/servicio.py")` | 7 795 |
| `leer_archivo("src/despues/dominio.py")` | 1 214 |
| `buscar("Decimal")` (línea base) | 2 166 |
| `mapa_repo("src/despues")` (con E4) | 5 658 |
| `buscar("monto\|^import\|^from")` (con E4) | **11 446** |

## 3. Resultado: ¿menos pasos o menos contexto?

**No.** Con las herramientas nuevas, el agente usó 2 pasos más y 40 % más de contexto. Las causas, según las trazas:

1. **El issue ya nombraba el archivo.** `ISSUE-03.md` dice dónde está el problema. Leer `servicio.py` (7,8 k) costó menos que el mapa de `src/despues` (5,7 k) más una búsqueda.
2. **Una búsqueda demasiado amplia.** Para no leer el archivo, el agente buscó `monto|^import|^from`. `buscar()` recorre todo el sandbox (`prompts/`, `fitness/`, `tests/`) y devolvió 11,4 k caracteres, más que leer el archivo completo. El problema está en la herramienta: no permite limitar la carpeta.
3. **Las notas cuestan pasos.** `anotar` 2 veces y `leer_notas` 1 vez suman 3 pasos. En una tarea de 12 pasos, el historial completo ya está en la ventana de contexto: la pizarra no ahorra nada.

**Lo que sí aportaron.** `mapa_repo` mostró que `PuertoPago.procesar_pago` y `AdaptadorPasarelaPago.procesar_pago` declaran `monto: float`. Ese riesgo quedó en la nota 1 y en el resumen final; la línea base no lo vio. Además, el ejecutor de la ronda 2 de E5 usó `anotar` para no perder los hallazgos del revisor (`trazas/issue02_multi/notas.md`).

**Comparación con E2.** El issue 1 se resolvió en 7 pasos con 1 acción bloqueada (`ver_cambios`), pero E2 no midió el contexto: `nucleo.py` no guarda el historial y la traza corta cada observación a 600 caracteres. Por eso agregamos `contexto_final_caracteres` a `resumen.json`. Además, E2 no es comparable directamente: es otro issue y sus pruebas no llegaron a correr.

## 4. Qué haríamos

- Agregar `buscar(patron, carpeta='src')` para limitar el alcance. Es el mismo principio de alcance mínimo de la Sección 1.5, aplicado a la salida.
- Usar `mapa_repo` cuando el issue **no** dice qué archivo tocar (exploración). Cuando el archivo se conoce, conviene leerlo directamente.
- Reservar la pizarra para tareas largas o con varios agentes, donde el historial se resume o no se comparte. En E5, el revisor no ve el historial del ejecutor y sí puede leer `notas.md`.
- Limitación del experimento: es una sola ejecución por variante, y el "modelo" fue un asistente que ya conocía el repositorio. Con otro modelo, el número de pasos puede cambiar.
