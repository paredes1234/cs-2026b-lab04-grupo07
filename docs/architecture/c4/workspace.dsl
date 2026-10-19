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
            api = container "Aplicación web / API" "Monolito modular que procesa las operaciones del sistema mediante interfaces públicas." "Python / Django (HTTP/JSON)"
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
