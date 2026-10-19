# Explicación de la arquitectura (E7)

San Camilo en Línea permite a los clientes comprar en varios puestos del Mercado San Camilo y pagar todo el pedido de una sola vez con Yape. Clientes, comerciantes y repartidores usan una aplicación web desde el navegador del celular. Detrás hay una sola aplicación central, dividida en seis módulos (catálogo, pedidos, pagos, notificaciones, entrega y uno de tipos compartidos), que guarda la información en una base de datos. Cuando se paga un pedido, el sistema deja en cola un aviso para cada puesto y un proceso aparte lo envía al comerciante por WhatsApp; si falla, lo reintenta sin hacer esperar al cliente. Todo funciona en un solo servidor en la nube, lo que mantiene bajos los costos.

> Borrador generado con el Prompt IA 3 (adaptado, sin la guía del Lab 06) y corregido por el equipo. Original en `.ia-borradores/prompt-ia3-respuesta.md` (local, no se sube).

## Correcciones aplicadas

| Frase original de la IA | Problema | Corrección |
|---|---|---|
| "una aplicación web que se instala en el celular, sin pasar por tiendas de aplicaciones" | Lo de las tiendas viene del ADR-002, no del modelo. En el `.dsl` la PWA solo dice "Interfaz móvil…" y corre en el nodo "Celular del usuario" (Android + Chrome). | "una aplicación web desde el navegador del celular" |
| "y que funciona incluso sin conexión" | Ningún elemento del modelo dice que funcione sin conexión. Que la tecnología mencione Service Worker no basta para afirmarlo. | Se eliminó. |
| "dividida en módulos (catálogo, pedidos, pagos, notificaciones y entrega)" | El contenedor `api` tiene **6** componentes; faltaba `compartido` (línea 21). | "seis módulos (… y uno de tipos compartidos)" |
| "guarda la información de forma segura" | "Segura" no aparece en el modelo; no hay elementos ni relaciones de seguridad. | "guarda la información en una base de datos" |
| "el sistema avisa a cada comerciante por WhatsApp" | Oculta el paso asíncrono que sí está en el modelo: `pedidos -> redis` (paso 7) y `worker -> whatsapp` (paso 9). | "deja en cola un aviso para cada puesto y un proceso aparte lo envía…" |
| "lo reintenta automáticamente en menos de 10 minutos" | Los 10 min vienen de QA-03/ADR-003, no del `.dsl`. El worker solo dice "reintentos sin bloquear el pago" (línea 23). | "lo reintenta sin hacer esperar al cliente" |
| (texto completo) | La respuesta de la IA tenía 123 palabras (`wc -w`): no cumplía el límite de 120 que se le pidió. | Las correcciones anteriores la dejan en 118. |

Conteo: 118 palabras en el párrafo de la explicación (`wc -w`).
