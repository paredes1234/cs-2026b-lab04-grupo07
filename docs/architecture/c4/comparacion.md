# Comparación — San Camilo en Línea (Lab 06)

## E4. Vista dinámica de C4 frente al diagrama de secuencia UML (Lab 05)

La secuencia UML del Lab 05 muestra 32 mensajes entre 9 líneas de vida (Cliente, PWA, PedidoController, ServicioPedidos, RepositorioPedidos, Pedido, Producto, PasarelaPago y Notificador), con el nombre y los parámetros de cada operación (confirmarYPagar, registrarPago, dividirPorPuesto, guardar), los fragmentos alt y loop, la transacción "todo o nada", el mensaje asíncrono al Notificador, los retornos (201 / 402) y la rama de error CA-2. La vista dinámica omite todo ese detalle: solo muestra 9 pasos numerados del camino de éxito entre contenedores y módulos, con su protocolo, sin ramas, retornos ni clases. La secuencia UML sirve a los developers que implementan y prueban el flujo. La vista dinámica sirve al docente, a los arquitectos y al equipo técnico para entender qué piezas intervienen y en qué orden, sin leer código.
# E6. Exportación y Comparación de Herramientas C4

En este documento se analiza la comparación entre dos enfoques para la documentación de la arquitectura C4:
1. **Modelo Exportado (DSL):** Un solo modelo fuente (`workspace.dsl`) exportado automáticamente a C4-PlantUML y Mermaid usando Structurizr CLI.
2. **Escritura a Mano (Manual):** Redacción directa de diagramas `.puml` utilizando la librería C4-PlantUML.

---

## 1. Tiempo Invertido

| Criterio | Escritura a Mano (`contexto-manual.puml`) | Modelo Exportado desde DSL (`workspace.dsl`) |
| :--- | :--- | :--- |
| **Tiempo Inicial** | **Menor al inicio** para un solo diagrama. Se escribe directamente la sintaxis y relaciones en el `.puml`. | **Mayor al inicio** para configurar Structurizr CLI, la sintaxis DSL y el pipeline de exportación. |
| **Mantenimiento a Escala** | **Alto y repetitivo.** Agregar o modificar un componente requiere actualizar manualmente múltiples diagramas. | **Mínimo.** Se edita el elemento una sola vez en el `workspace.dsl` y se vuelven a generar todas las vistas automáticamente. |
| **Generación Multiformato** | **Manual.** Hay que volver a escribir el diagrama en sintaxis Mermaid o PlantUML según el destino. | **Automatizado.** Un solo comando exporta a PlantUML, Mermaid, Structurizr y otros formatos. |

---

## 2. Errores Encontrados

| Aspecto | Escritura a Mano | Modelo Exportado desde DSL |
| :--- | :--- | :--- |
| **Inconsistencia de Nombres** | **Alta probabilidad.** Es común tener inconsistencias en nombres de componentes o descripciones entre la vista de contexto, contenedores y componentes. | **Cero inconsistencia.** Existe una única fuente de verdad (*Single Source of Truth*). La entidad definida en DSL se propaga a todas las vistas. |
| **Errores de Sintaxis** | Frecuentes al olvidar comillas, paréntesis o llamadas a macros específicas de PlantUML. | Controlados. El comando `./structurizr.sh validate` verifica la sintaxis del modelo antes de exportar. |
| **Diagramas Desactualizados** | **Muy frecuente.** Modificar la arquitectura en la implementación o en una vista suele dejar desactualizadas las demás. | **Baja.** Al cambiar el DSL y ejecutar el pipeline, todos los diagramas PNG se actualizan de forma sincronizada. |

---

## 3. Impacto de Cambios de Nombre (¿Qué pasaría si mañana cambia el nombre de un contenedor?)

### Escenario:
El contenedor `"Módulo de Comprobantes de Pago Electrónicos (CPE)"` cambia su nombre a `"Servicio de Billing y CPE"`.

* **En el Enfoque Manual:**
  1. Se debe buscar manualmente en cada uno de los archivos `.puml` creaciones o referencias a este contenedor.
  2. Editar uno a uno los archivos actualizando las cadenas de texto y aliases.
  3. Ejecutar individualmente la generación de PNGs para cada archivo afectado.
  4. **Riesgo:** Alto riesgo de olvidar actualizar alguna vista, generando documentación contradictoria o desincronizada.

* **En el Enfoque Exportado (Structurizr DSL):**
  1. Se modifica el nombre **una sola vez** en la definición del contenedor dentro de `workspace.dsl`:
     ```dsl
     cpe = container "Servicio de Billing y CPE" "Gestión y envío de CPEs a SUNAT" "Node.js / Express"
     ```
  2. Se ejecutan los comandos del pipeline:
     ```bash
     ./structurizr.sh validate -w docs/architecture/c4/workspace.dsl
     ./structurizr.sh export -w docs/architecture/c4/workspace.dsl -f plantuml/c4plantuml -o docs/architecture/c4/export
     ./structurizr.sh export -w docs/architecture/c4/workspace.dsl -f mermaid -o docs/architecture/c4/export
     java -jar plantuml.jar -tpng -o ../img docs/architecture/c4/export/*.puml
     ```
  3. **Resultado:** Todas las vistas (Contexto, Contenedores, Componentes, ConfirmarYPagar y Despliegue) quedan automáticamente actualizadas e integradas en PlantUML, Mermaid e imágenes PNG, asegurando consistencia total sin esfuerzo adicional.

---

## Conclusión

El uso de **Architecture as Code (AaC)** mediante Structurizr DSL requiere una inversión inicial en configuración, pero garantiza **mantenibilidad, consistencia y escalabilidad** a largo plazo. Para proyectos medianos o grandes como un ERP, el enfoque exportado desde DSL supera ampliamente la redacción manual de diagramas.