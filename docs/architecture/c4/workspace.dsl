workspace "San Camilo en Línea" "Modelo C4 (E1-E3, Laboratorio 06). Continuación de la arquitectura de los Labs 04 y 05." {

    !identifiers hierarchical

    model {
        // E1: personas y sistemas (contexto)
        cliente = person "Cliente" "Consulta productos, compra en varios puestos y paga un pedido único."
        comerciante = person "Comerciante" "Administra productos y prepara los pedidos de su puesto."
        repartidor = person "Repartidor" "Consulta pedidos de delivery y actualiza su entrega."

        sancamilo = softwareSystem "San Camilo en Línea" "Plataforma de compras del Mercado San Camilo: catálogo, pedidos multipuesto, pago y entrega." {

        }

        pasarela = softwareSystem "Pasarela de pago Yape" "Proveedor externo utilizado mediante la interfaz PasarelaPago; integración abstracta en el MVP." "Externo"
        whatsapp = softwareSystem "Servicio de WhatsApp" "Servicio externo al que se envían las confirmaciones y notificaciones." "Externo"

        // E1: las relaciones de contexto describen una intención, sin detallar tecnologías internas.
        cliente -> sancamilo "Consulta el catálogo, realiza pedidos multipuesto y paga"
        comerciante -> sancamilo "Publica productos y atiende pedidos"
        repartidor -> sancamilo "Consulta entregas asignadas y actualiza su estado"
        sancamilo -> pasarela "Solicita el cobro de pedidos con Yape"
        sancamilo -> whatsapp "Envía confirmaciones a comerciantes"


    }

    views {
        systemContext sancamilo "Contexto" "Nivel 1: usuarios, San Camilo en Línea y servicios externos." {
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
