# Informe de Round-Trip e Ingeniería Inversa (E6) - San Camilo en Línea

## Comparación entre el Diagrama de Diseño (E1) y el Reconstruido desde Código (E6)

| Diferencia observada | Causa | Acción |
| :--- | :--- | :--- |
| No aparece la composición `Pedido–LineaPedido` ni `Pedido–PedidoPuesto`; las colecciones figuran como atributos `list[LineaPedido]` y `list[PedidoPuesto]`. | `pyreverse` no infiere asociaciones desde colecciones tipadas. | Documentar la limitación; el diagrama de diseño se mantiene. |
| No hay multiplicidades en ninguna relación. | El código no expresa multiplicidades. | Agregar validación en `confirmar()` para que el pedido tenga al menos una línea (C3). |
| Las interfaces (`PasarelaPago`, `Notificador`, `RepositorioPedidos`) salen como clases, con sus métodos `{abstract}`, y los adaptadores muestran `{abstract}` aunque son concretos. | Python implementa interfaces con `ABC` y los adaptadores lanzan `Not NotImplementedError`. | Aceptable en Python; se documenta. |
| Las asociaciones con `Producto`, `Puesto`, `Cliente` y `Pago` figuran como atributos sin tipo (`producto`, `puesto`, `cliente`). | `pyreverse` no infiere tipos de campos sin hint en `dataclasses` con `from __future__ import annotations`. | Documentar la limitación. |
| Nombres en `snake_case` (`calcular_total`, `marcar_listo`) frente a `camelCase` del diagrama. | Convención de estilo en Python (PEP 8). | Aceptable; se documenta la equivalencia (C5). |
| Los atributos de enumeración salen como `name`, sin los valores (`BORRADOR`, `RECIBIDO`, etc.). | `pyreverse` solo muestra el atributo heredado de `Enum`. | Documentar la limitación; los valores quedan en el diagrama de diseño. |
| Faltan `PedidoController` y las relaciones de uso de `ServicioPedidos` hacia los puertos. | El esqueleto solo cubre el módulo de dominio; las dependencias de uso se pasan por constructor. | Documentar; el diagrama de diseño se mantiene. |