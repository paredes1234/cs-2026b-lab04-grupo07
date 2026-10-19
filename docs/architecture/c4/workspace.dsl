workspace "San Camilo en Línea" "Modelo C4 (E1-E3, Laboratorio 06). Continuación de la arquitectura de los Labs 04 y 05." {

    !identifiers hierarchical

    model {
        // E1: personas y sistemas (contexto)
        cliente = person "Cliente" "Consulta productos, compra en varios puestos y paga un pedido único."
        comerciante = person "Comerciante" "Administra productos y prepara los pedidos de su puesto."
        repartidor = person "Repartidor" "Consulta pedidos de delivery y actualiza su entrega."

        sancamilo = softwareSystem "San Camilo en Línea" "Plataforma de compras del Mercado San Camilo: catálogo, pedidos multipuesto, pago y entrega." {
            // E2: cada contenedor es una unidad de ejecución o un almacén; Docker NO es un contenedor C4.
            pwa = container "Aplicación web progresiva" "Interfaz móvil para clientes, comerciantes y repartidores." "HTML/CSS/JavaScript + Service Worker" "Web Browser"
            api = container "Aplicación web / API" "Monolito modular que procesa las operaciones del sistema mediante interfaces públicas." "Python / Django (HTTP/JSON)" {
                // E3: componentes alineados con docs/design/paquetes.puml, no con el caso AgroConecta.
                catalogo = component "Catálogo" "Gestiona puestos, productos, disponibilidad y stock." "Módulo Python/Django"
                pedidos = component "Pedidos" "Carrito, pago de pedido multipuesto, Pedido y PedidoPuesto; dueño del puerto Notificador." "Módulo Python/Django"
                pagos = component "Pagos" "Gestiona cobros mediante la interfaz PasarelaPago y el adaptador Yape." "Módulo Python/Django"
                notificaciones = component "Notificaciones" "Implementa Notificador y coordina el envío de avisos al comerciante." "Módulo Python/Django"
                entrega = component "Entrega" "Gestiona recojo, delivery y actualización del estado de PedidoPuesto." "Módulo Python/Django"
                compartido = component "Compartido" "Tipos, identificadores y utilidades sin dependencias de los módulos de negocio." "Módulo Python/Django"
            }
            worker = container "Worker de notificaciones" "Ejecuta tareas asíncronas y reintentos sin bloquear el pago." "Python / Celery"
            bd = container "Base de datos relacional" "Guarda clientes, puestos, productos, pedidos y pagos." "PostgreSQL 16" "Database"
            redis = container "Cola y caché" "Gestiona la cola de tareas de Celery y el caché." "Redis" "Queue"
        }

        pasarela = softwareSystem "Pasarela de pago Yape" "Proveedor externo utilizado mediante la interfaz PasarelaPago; integración abstracta en el MVP." "Externo"
        whatsapp = softwareSystem "Servicio de WhatsApp" "Servicio externo al que se envían las confirmaciones y notificaciones." "Externo"

        // E1: las relaciones de contexto describen una intención, sin detallar tecnologías internas.
        cliente -> sancamilo "Consulta el catálogo, realiza pedidos multipuesto y paga"
        comerciante -> sancamilo "Publica productos y atiende pedidos"
        repartidor -> sancamilo "Consulta entregas asignadas y actualiza su estado"
        sancamilo -> pasarela "Solicita el cobro de pedidos con Yape"
        sancamilo -> whatsapp "Envía confirmaciones a comerciantes"

        // E2: relaciones entre contenedores, con descripción y protocolo.
        cliente -> sancamilo.pwa "Realiza sus compras" "HTTPS"
        comerciante -> sancamilo.pwa "Gestiona su puesto" "HTTPS"
        repartidor -> sancamilo.pwa "Consulta y actualiza entregas" "HTTPS"
        sancamilo.pwa -> sancamilo.api "Envía solicitudes y recibe respuestas" "HTTPS/JSON"
        sancamilo.api -> sancamilo.bd "Lee y registra datos de negocio" "SQL/TCP"
        sancamilo.api -> sancamilo.redis "Encola notificaciones y utiliza caché" "Protocolo Redis/TCP"
        sancamilo.worker -> sancamilo.redis "Consume tareas y registra reintentos" "Protocolo Redis/TCP"
        sancamilo.worker -> whatsapp "Envía mensajes y confirmaciones" "HTTPS/JSON"
        sancamilo.api -> pasarela "Solicita cobros mediante el adaptador Yape" "HTTPS/JSON"

        // E3: llamadas hacia componentes desde la PWA.
        sancamilo.pwa -> sancamilo.api.catalogo "Consulta productos y puestos" "HTTPS/JSON"
        sancamilo.pwa -> sancamilo.api.pedidos "Confirma y paga pedidos" "HTTPS/JSON"
        sancamilo.pwa -> sancamilo.api.entrega "Consulta estado de recojo o delivery" "HTTPS/JSON"

        // E3: dependencias de paquetes según Lab 05, sin ciclos.
        sancamilo.api.pedidos -> sancamilo.api.catalogo "Consulta productos, reserva y libera stock" "Llamada interna Python"
        sancamilo.api.pedidos -> sancamilo.api.pagos "Solicita y registra el cobro" "Llamada interna Python"
        sancamilo.api.notificaciones -> sancamilo.api.pedidos "Implementa el puerto Notificador y usa PedidoPuesto" "Interfaz Python"
        sancamilo.api.entrega -> sancamilo.api.pedidos "Consulta PedidoPuesto y registra recojo o entrega" "Llamada interna Python"
        sancamilo.api.catalogo -> sancamilo.api.compartido "Utiliza tipos compartidos" "Python"
        sancamilo.api.pedidos -> sancamilo.api.compartido "Utiliza tipos compartidos" "Python"
        sancamilo.api.pagos -> sancamilo.api.compartido "Utiliza tipos compartidos" "Python"
        sancamilo.api.notificaciones -> sancamilo.api.compartido "Utiliza tipos compartidos" "Python"
        sancamilo.api.entrega -> sancamilo.api.compartido "Utiliza tipos compartidos" "Python"
        sancamilo.api.pagos -> pasarela "Invoca cobrar() mediante PasarelaPago" "HTTPS/JSON"
        sancamilo.api.pedidos -> sancamilo.redis "Encola confirmaciones tras guardar el pedido" "Protocolo Redis/TCP"
        sancamilo.worker -> sancamilo.api.notificaciones "Ejecuta tareas del módulo Notificaciones" "Celery/Python"
        sancamilo.api.notificaciones -> whatsapp "Envía notificaciones del pedido" "HTTPS/JSON"
        sancamilo.api.catalogo -> sancamilo.bd "Lee productos y stock" "SQL/TCP"
        sancamilo.api.pedidos -> sancamilo.bd "Guarda pedidos y estados" "SQL/TCP"
    }

    views {
        systemContext sancamilo "Contexto" "Nivel 1: usuarios, San Camilo en Línea y servicios externos." {
            include *
            autolayout lr
        }
        container sancamilo "Contenedores" "Nivel 2: PWA, aplicación modular, worker, base de datos y Redis." {
            include *
            autolayout lr
        }
        component sancamilo.api "Componentes" "Nivel 3: componentes internos de la API, alineados con paquetes.puml (Lab 05)." {
            include *
            autolayout lr
        }
        dynamic sancamilo.api "ConfirmarYPagar" "Dinámico: pagar con Yape un pedido de varios puestos (camino de éxito, CA-1)." {
            cliente -> sancamilo.pwa "Elige «Pagar con Yape»" "HTTPS"
            sancamilo.pwa -> sancamilo.api.pedidos "POST /pedidos/{id}/pago" "HTTPS/JSON"
            sancamilo.api.pedidos -> sancamilo.api.catalogo "Reserva el stock de cada línea"
            sancamilo.api.pedidos -> sancamilo.api.pagos "Solicita el cobro"
            sancamilo.api.pagos -> pasarela "Cobra con Yape" "HTTPS/JSON"
            sancamilo.api.pedidos -> sancamilo.db "Guarda el pedido PAGADO y sus PedidoPuesto" "SQL/TCP"
            sancamilo.api.notificaciones -> sancamilo.cola "Encola una notificación por puesto" "Redis protocol"
            sancamilo.worker -> sancamilo.cola "Consume la tarea" "Redis protocol"
            sancamilo.worker -> whatsapp "Notifica al comerciante" "HTTPS/JSON"
            autolayout lr
        }
        styles {
            element "Person" {
                shape person
                background #08427B
                color #FFFFFF
            }
            element "Software System" {
                background #1168BD
                color #FFFFFF
            }
            element "Externo" {
                background #737A86
                color #FFFFFF
            }
            element "Container" {
                background #438DD5
                color #FFFFFF
            }
            element "Component" {
                background #85BBF0
                color #172334
            }
            element "Database" {
                shape cylinder
            }
            element "Queue" {
                shape pipe
            }
            element "Web Browser" {
                shape WebBrowser
            }
        }
    }
}
