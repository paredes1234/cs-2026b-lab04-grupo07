# San Camilo en Línea — Laboratorio 04: Fundamentos de arquitectura de software

Construcción de Software · EPIS-UNSA · 2026-B · Grupo 07

## Integrantes

| Nombre | Rol en el laboratorio |
|--------|-----------------------|
| Flores Nuñez Rodrigo Francisco | Diagramador |
| Jimenez Paredes Fabricio Gabriel | Redactor de drivers |
| Bravo Arredondo Cristhian Matías | Verificador de IA |

## Caso

**San Camilo en Línea** es una plataforma para hacer pedidos a los puestos del Mercado San Camilo, con recojo en el mercado o delivery. Los actores son el cliente, el comerciante y el repartidor.
El MVP incluye un catálogo por puesto, pedidos con productos de varios puestos, pago con Yape y confirmación del pedido al comerciante por WhatsApp.
**Atributo de calidad crítico:** la capacidad de interacción. Un comerciante con poca experiencia digital debe poder publicar un producto en **3 toques o menos desde un celular de gama baja** (QA-01).
Para cumplirlo, elegimos un **monolito modular** ([ADR-001](docs/architecture/001-estilo-arquitectonico.md)) con una **PWA** mobile-first ([ADR-002](docs/architecture/002-pwa-vs-app-nativa.md)).

## Arquitectura elegida

```mermaid
flowchart TB

    CL["Cliente"]
    CO["Comerciante"]
    RE["Repartidor"]

    subgraph APP["San Camilo en Línea - Monolito modular"]
        UI["Interfaz Web / PWA móvil"]

        subgraph MOD["Módulos de negocio"]
            CAT["Catálogo y Productos"]
            PED["Carrito y Pedidos"]
            PAG["Pagos"]
            DEL["Recojo y Delivery"]
            NOT["Notificaciones"]
        end

        INF["Infraestructura: repositorios y adaptadores"]

        UI --> CAT
        UI --> PED
        UI --> PAG
        UI --> DEL

        PED --> CAT
        PED --> PAG
        PED --> DEL
        PED --> NOT

        CAT --> INF
        PED --> INF
        PAG --> INF
        DEL --> INF
        NOT --> INF
    end

    DB[(Base de datos relacional)]
    YAPE["Yape / Proveedor de pago"]
    WA["Servicio de WhatsApp"]

    CL --> UI
    CO --> UI
    RE --> UI

    INF --> DB
    INF --> YAPE
    INF --> WA
```

## Decisiones arquitectónicas

- [ADR-001: Adoptar un monolito modular para el MVP](docs/architecture/001-estilo-arquitectonico.md)
- [ADR-002: Usar una PWA en lugar de una app nativa](docs/architecture/002-pwa-vs-app-nativa.md)
- [ADR-003: Enviar las confirmaciones de WhatsApp de forma asíncrona con reintentos](docs/architecture/003-notificaciones-asincronas.md)

## Documentación y diagramas

- [Drivers arquitectónicos y escenarios de calidad (E1)](docs/architecture/drivers.md)
- [Matriz de decisión (E2)](docs/architecture/matriz-decision.md)
- [Diagrama Mermaid de la arquitectura elegida (E3)](diagrams/arquitectura.mmd)
- [Alternativa descartada en PlantUML (E5)](diagrams/alternativa.puml)
- [Vista de despliegue con Python Diagrams (E6)](diagrams/despliegue.py)
- [Bitácora de uso de IA (E7)](docs/architecture/bitacora-ia.md)

## Imágenes de los diagramas

### Arquitectura elegida: monolito modular (E3, Mermaid)

![Arquitectura elegida: monolito modular](diagrams/img/arquitectura.png)

### Alternativa descartada: monolito en capas (E5, PlantUML)

![Alternativa descartada: monolito en capas](diagrams/img/alternativa.png)

### Vista de despliegue (E6, Python Diagrams)

![Vista de despliegue](diagrams/img/despliegue.png)

## Reflexión sobre el uso de la IA

La IA nos ayudó a avanzar más rápido. Con ChatGPT generamos y comparamos alternativas, y le pedimos una crítica adversarial. Gemini nos dio borradores de los ADR, Claude escribió el código de PlantUML y de Python Diagrams, y Claude Code nos ayudó a ordenar la bitácora y este README.
También cometió errores. Asumió infraestructura en AWS aunque nuestra restricción era un VPS. Usó una sintaxis desactualizada de la librería `diagrams`, que daba `AttributeError`. Omitió la nota de descarte del PlantUML aunque se la pedimos.
Además, no aceptamos dar por hecho que Yape tiene una API pública abierta sin verificarlo, así que en la arquitectura dejamos "Yape / proveedor de pago".
Aprendimos a contrastar cada propuesta con nuestras restricciones (plazo de 1 mes, presupuesto bajo, equipo de 3), a ejecutar y validar todo el código generado y a no afirmar capacidades de servicios externos sin documentación oficial.
La IA propone, pero el equipo decide y verifica.

## Arquitectura C4 (Lab 06)

Modelamos la arquitectura de San Camilo en Línea con el modelo C4, en cinco vistas: contexto, contenedores, componentes, dinámica (ConfirmarYPagar) y despliegue.
La fuente única es [`docs/architecture/c4/workspace.dsl`](docs/architecture/c4/workspace.dsl) (Structurizr DSL). Las exportaciones de `export/` y las imágenes de `img/` se generan desde ese archivo.

### Diagrama de contexto (Mermaid, copiado de `export/Contexto.mmd`)

```mermaid
graph LR
  linkStyle default fill:#ffffff

  subgraph diagram ["System Context View: San Camilo en Línea"]
    style diagram fill:#ffffff,stroke:#ffffff

    1["<div style='font-weight: bold'>Cliente</div><div style='font-size: 70%; margin-top: 0px'>[Person]</div><div style='font-size: 80%; margin-top:10px'>Consulta productos, compra en<br />varios puestos y paga un<br />pedido único.</div>"]
    style 1 fill:#08427b,stroke:#052e56,color:#ffffff
    16["<div style='font-weight: bold'>Pasarela de pago Yape</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>Proveedor externo utilizado<br />mediante la interfaz<br />PasarelaPago; integración<br />abstracta en el MVP.</div>"]
    style 16 fill:#737a86,stroke:#50555d,color:#ffffff
    17["<div style='font-weight: bold'>Servicio de WhatsApp</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>Servicio externo al que se<br />envían las confirmaciones y<br />notificaciones.</div>"]
    style 17 fill:#737a86,stroke:#50555d,color:#ffffff
    2["<div style='font-weight: bold'>Comerciante</div><div style='font-size: 70%; margin-top: 0px'>[Person]</div><div style='font-size: 80%; margin-top:10px'>Administra productos y<br />prepara los pedidos de su<br />puesto.</div>"]
    style 2 fill:#08427b,stroke:#052e56,color:#ffffff
    3["<div style='font-weight: bold'>Repartidor</div><div style='font-size: 70%; margin-top: 0px'>[Person]</div><div style='font-size: 80%; margin-top:10px'>Consulta pedidos de delivery<br />y actualiza su entrega.</div>"]
    style 3 fill:#08427b,stroke:#052e56,color:#ffffff
    4["<div style='font-weight: bold'>San Camilo en Línea</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>Plataforma de compras del<br />Mercado San Camilo: catálogo,<br />pedidos multipuesto, pago y<br />entrega.</div>"]
    style 4 fill:#1168bd,stroke:#0b4884,color:#ffffff

    1-. "<div>Consulta el catálogo, realiza<br />pedidos multipuesto y paga</div><div style='font-size: 70%'></div>" .->4
    2-. "<div>Publica productos y atiende<br />pedidos</div><div style='font-size: 70%'></div>" .->4
    3-. "<div>Consulta entregas asignadas y<br />actualiza su estado</div><div style='font-size: 70%'></div>" .->4
    4-. "<div>Solicita el cobro de pedidos<br />con Yape</div><div style='font-size: 70%'></div>" .->16
    4-. "<div>Envía confirmaciones a<br />comerciantes</div><div style='font-size: 70%'></div>" .->17

  end
```

### Vistas

- [Contexto (nivel 1)](docs/architecture/c4/img/Contexto.png)
- [Contenedores (nivel 2)](docs/architecture/c4/img/Contenedores.png)
- [Componentes (nivel 3)](docs/architecture/c4/img/Componentes.png)
- [Dinámica: ConfirmarYPagar](docs/architecture/c4/img/ConfirmarYPagar.png)
- [Despliegue](docs/architecture/c4/img/Despliegue.png)

### Documentos del Lab 06

- [Modelo: `workspace.dsl`](docs/architecture/c4/workspace.dsl)
- [Inventario de elementos (E1)](docs/architecture/c4/inventario.md)
- [Comparaciones (E4 y E6)](docs/architecture/c4/comparacion.md)
- [Revisión C4 (E7)](docs/architecture/c4/revision-c4.md)
- [Explicación de la arquitectura (E7)](docs/architecture/c4/explicacion.md)
- [Bitácora de IA (Lab 06)](docs/architecture/c4/bitacora-ia.md)
