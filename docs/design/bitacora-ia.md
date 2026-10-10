# Bitácora de IA — Lab 05 (UML como código)

Regla de oro: la IA propone, el equipo decide y verifica (reglas C1–C5). No se ingresaron datos personales en ningún prompt.

| # | Fecha | Herramienta | Prompt (resumen) | Propuesta de la IA | Verificación del equipo | Decisión |
|---|---|---|---|---|---|---|
| 1 | 2026-10-10 | Claude Code | E1 · Escribir `historia.md` con la HU del caso 7 ("pedido a varios puestos con pago único"), 3 criterios Dado/Cuando/Entonces y supuestos (Prompt P1). | HU-03 con CA-1 (éxito), CA-2 (pago rechazado o sin respuesta en 15 min) y CA-3 (rechazo parcial). Agregó la modalidad de entrega en CA-1 (RF-04) y dos supuestos: modalidad única por pedido y no guardar el número de Yape. | Cristhian revisó la trazabilidad con RF-03 a RF-06. Confirmó el límite de 15 min y la modalidad única por pedido. | Aceptada |
| 2 | 2026-10-10 | Claude Code | E1 · Prompt IA 1 adaptado: diagrama de clases en PlantUML para Carrito y Pedidos, Catálogo, Pagos y Notificaciones, con ADR-001 y ADR-003 (Prompt P2). | Borrador `clases-v0.puml`: 12 clases e interfaces, 3 enums y 4 paquetes. Incluía `Comerciante`, `Devolucion`, `Pago.celularYape`, líneas dentro de `PedidoPuesto` y 6 asociaciones sin multiplicidad. | Se revisó contra la lista de verificación de E1 y las reglas C3 y C5 (Prompt P3): 26 puntos, de los cuales 5 se aceptaron, 14 se corrigieron y 7 se rechazaron. Cristhian confirmó los 26. Nota: el borrador lo generó la misma sesión que luego lo revisó, así que no es una revisión independiente. | Corregida |
| 3 | 2026-10-10 | Claude Code | E1 · Revisión del borrador: ¿dónde viven las `LineaPedido`? (Prompt P3) | El borrador ponía `PedidoPuesto "1" *-- "1..*" LineaPedido` desde el carrito. | Contradice CA-2 ("no se crea ningún PedidoPuesto" si el pago falla) y el estado inicial RECIBIDO de E3. Se cambió a `Pedido *-- LineaPedido`. `dividirPorPuesto()` crea los PedidoPuesto al aprobarse el pago y estos agregan las líneas. | Corregida |
| 4 | 2026-10-10 | Claude Code | E1 · Revisión del borrador: datos sensibles (Prompt P3). | `Pago.celularYape`, `Cliente.celular`, `Cliente.direccion` y `Pedido.direccionEntrega`. | Ningún criterio los usa y son datos personales (R-04, Ley 29733). El celular se pasa como parámetro a `cobrar()` y no se guarda. Riesgo anotado: el delivery real necesitará un punto de entrega. | Rechazada |
| 5 | 2026-10-10 | Claude Code | E1 · Revisión del borrador: estados de `PedidoPuesto` (Prompt P3). | `EstadoPedidoPuesto` = PENDIENTE, RECIBIDO, ACEPTADO, LISTO, RECHAZADO, con la operación `aceptar()`. | No coincide con la Tabla 7 de la guía. Se cambió a RECIBIDO, LISTO, RECOGIDO, ENTREGADO, RECHAZADO. Se quitó `aceptar()` y se agregaron `registrarRecojo()` y `registrarEntrega()`. | Corregida |
| 6 | 2026-10-10 | Claude Code | E1 · Revisión del borrador: clases que no salen de la historia (Prompt P3). | Clase `Comerciante` (duplica el celular del puesto) y clase `Devolucion` con `estado: String`. | RF-06 notifica al puesto (`Puesto.celularWhatsApp`). La devolución solo se registra y se hace a mano (supuesto 3). Se quitó `Comerciante` y `Devolucion` pasó a ser los atributos `montoDevolver` y `motivoRechazo` de `PedidoPuesto`. | Rechazada |
| 7 | 2026-10-10 | Claude Code | E1 · Autorrevisión de `clases.puml` antes del commit (sin un prompt nuevo; la IA lo señaló por su cuenta). | La IA detectó que su propia corrección de la fila 3, `PedidoPuesto "1" o-- "1..*" LineaPedido`, obliga a que cada línea tenga siempre un PedidoPuesto, lo que no se cumple en BORRADOR ni en CANCELADO. Propuso cambiarlo a `"0..1"`. | Cristhian lo verificó contra CA-2 (sin PedidoPuesto si el pago falla) y la regla C3. Se cambió a `"0..1"` y se amplió la nota del diagrama. | Aceptada |

## Anexo: prompts

**P1 — Historia de usuario (E1, paso 1)**

```text
Escribe docs/design/historia.md siguiendo la sección 4.1 de CLAUDE.md (HU con 3 criterios
Dado/Cuando/Entonces y la sección de Supuestos). Muéstramelo y espera mi OK.
```

La sección 4.1 daba como punto de partida la HU-03 con CA-1, CA-2 y CA-3, y los supuestos de 15 min, liquidación fuera del MVP y devolución manual.

**P2 — Prompt IA 1 adaptado (E1, paso 2)**

```text
Actúa como diseñador de software orientado a objetos. Contexto: módulos Carrito y
Pedidos, Catálogo y Productos, Pagos y Notificaciones de un monolito modular
(ADR-001: puertos y adaptadores para integraciones externas como Yape y WhatsApp;
ADR-003: WhatsApp asíncrono con cola y reintentos). Historia y criterios: [historia.md].
Tarea: genera un diagrama de clases en PlantUML con atributos tipados, operaciones,
multiplicidades, una enumeración para el estado del pedido y una interfaz (puerto)
para la pasarela de pagos.
Formato: solo el código PlantUML. No agregues clases que no se deriven de la
historia; si asumes algo, indícalo en un comentario.
```

**P3 — Revisión del borrador (E1, paso 2)**

```text
Luego revísala contra la lista de verificación de E1 y las reglas C3 y C5, y muéstrame una
tabla "Propuesta de la IA | Decisión sugerida | Justificación", como la Tabla 3 de la guía.
NO escribas todavía la versión final: yo confirmo cada decisión.
```

Respuesta del equipo: "Acepto todas tus sugerencias, sigue con clases.puml final".
