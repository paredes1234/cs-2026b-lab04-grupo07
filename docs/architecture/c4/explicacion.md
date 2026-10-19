# Explicación de la arquitectura para la directiva de comerciantes (E7)

San Camilo en Línea es una plataforma para comprar en el Mercado San Camilo desde el celular. La usan tres tipos de personas: los clientes, que revisan los productos de varios puestos, arman un solo pedido y lo pagan de una vez; los comerciantes, que publican sus productos y atienden los pedidos de su puesto; y los repartidores, que ven las entregas que les tocan y actualizan su estado. Para funcionar, la plataforma depende de dos servicios de otras empresas: Yape, que cobra los pedidos, y WhatsApp, por donde cada comerciante recibe la confirmación de sus ventas. Si WhatsApp falla, el pedido ya quedó guardado y el aviso se vuelve a enviar.

> Redactada con el Prompt IA 3 de la guía (Paso 11) sobre `export/Contexto.puml`, para la directiva de la asociación de comerciantes, y corregida por el equipo contra `workspace.dsl`. Conteo con `wc -w`: 112 palabras.

## Correcciones aplicadas

| Frase original de la IA | Problema | Corrección |
|---|---|---|
| "los repartidores, que ven las entregas que les tocan y avisan cuando las completan" | El modelo dice "Consulta entregas asignadas y actualiza su estado" (`workspace.dsl`, línea 34) y "actualiza su entrega" (línea 9). No dice que el repartidor avise al terminar. | "…y actualizan su estado" |
| "Si alguno de esos servicios falla, los pedidos no se pierden: quedan guardados y los avisos se vuelven a enviar." | Incluye a Yape, pero el modelo no tiene ningún comportamiento ante una falla de Yape: la vista dinámica solo cubre el camino de éxito (CA-1, línea 102). Los reintentos existen solo para las notificaciones: el worker "Ejecuta tareas asíncronas y reintentos sin bloquear el pago" (línea 23) y envía a WhatsApp (línea 46). Que el pedido quede guardado antes del aviso sale de los pasos 6 y 7 de la dinámica (líneas 108–109). La frase es casi igual a la del ejemplo de AgroConecta de la guía: la IA copió el patrón del ejemplo. | "Si WhatsApp falla, el pedido ya quedó guardado y el aviso se vuelve a enviar." |

Lo que se mantuvo, verificado en `workspace.dsl`: "desde el celular" (nodo "Celular del usuario", línea 72); las tres personas y sus actividades (líneas 7–9 y 32–34); Yape cobra (línea 35) y WhatsApp confirma a los comerciantes (línea 36). La respuesta original tenía 118 palabras, dentro del límite.
