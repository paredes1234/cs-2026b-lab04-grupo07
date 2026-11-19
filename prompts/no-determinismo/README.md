# E7.3 · No determinismo

**Prompt:** `prompts/normalizacion/v3.txt`, la mejor versión evaluada con promptfoo (9/10).
**Casos:** B02 (`papa amarila`), B06 (`queso fsc`) y B08 (`papa`).
**Modelo:** Qwen2.5-1.5B-Instruct GGUF Q4_K_M, el mismo de las grabaciones de E4. El archivo coincide con el SHA-256 publicado (`6a1a2eb6…407e`). Se ejecutó con llama-cpp-python 0.3.36 (`create_chat_completion`, plantilla de chat del modelo y 160 tokens como máximo).
**Reproducir:** `python prompts/no_determinismo.py <modelo.gguf>`. Las 18 respuestas están sin editar en `t0/` y `t07/`. `resultados.json` guarda cada salida con sus aserciones B1 a B4.

| Configuración | Corrida | B02 | B06 | B08 | Aprobados |
|---|---|---|---|---|---:|
| Grabación de E4 (llama.cpp b6766, t = 0, semilla 42) | — | `papa amarilla` ✅ | `queso fresco` ✅ | `papa canchán` ❌ | 2/3 |
| t = 0, semilla 42 | 1, 2 y 3 (idénticas) | bloque ```` ```json ````, `desconocido` ❌ | bloque, `desconocido` ❌ | bloque, `desconocido` ❌ | 0/3 en cada una |
| t = 0,7, semilla 1 | 1 | JSON, `papa amarilla`, pero la `entrada` quedó como `papa amarilla` ❌ (B3) | `queso fresco` ✅ | `desconocido` ✅ | 2/3 |
| t = 0,7, semilla 2 | 2 | bloque, `desconocido` ❌ | bloque, `desconocido` ❌ | bloque, `desconocido` ❌ | 0/3 |
| t = 0,7, semilla 3 | 3 | bloque, `desconocido` ❌ | bloque, `queso fresco` ❌ | bloque, `desconocido` ❌ | 0/3 |

En B02 el modelo corrigió también la `entrada` (`papa amarilla`) en las seis corridas que la devolvieron, aunque el prompt pide copiarla literalmente.

## Qué cambió y qué implica (5 líneas)

1. Con t = 0 y la misma semilla, las tres corridas fueron idénticas entre sí, pero distintas de la grabación de E4. Lo que cambió fue el entorno de ejecución (llama-cpp-python 0.3.36 con la plantilla de chat, en vez de llama.cpp b6766): el modelo pasó a envolver el JSON en ```` ```json ```` y a responder `desconocido`.
2. Con t = 0,7 cambiaron el formato (JSON directo o bloque Markdown) y el producto entre corridas: B06 fue `queso fresco`, `desconocido` y `queso fresco`; la tasa varió entre 0/3 y 2/3.
3. B08 dio `desconocido`, el valor esperado, en las seis corridas nuevas. La grabación de E4 había dado `papa canchán`, así que el 9/10 de la v3 describe una sola muestra, no el comportamiento estable del prompt.
4. Una grabación solo vale para la configuración en que se hizo (modelo, versión del motor, plantilla, temperatura y semilla). Hay que guardar esos datos con cada grabación y volver a grabar todo cuando cambie alguno.
5. Para las pruebas automatizadas, la CI debe evaluar las grabaciones, que son reproducibles, y no llamar al modelo en vivo. Al regrabar conviene tomar varias muestras por caso y exigir que todas pasen. El código debe validar la salida (`GeneradorNormalizacion` rechaza el bloque Markdown) en lugar de suponer un formato.
