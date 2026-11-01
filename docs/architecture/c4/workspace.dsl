workspace "San Camilo en Línea" "Modelo C4 (Laboratorio 06) actualizado en el Laboratorio 08 con ADR-006 a ADR-008 y trazabilidad a escenarios [QA08-xx]." {

    !identifiers hierarchical

    model {
        // E1: Personas y sistemas (Contexto)
        cliente = person "Cliente" "Consulta productos, compra en varios puestos y paga un pedido único."
        comerciante = person "Comerciante" "Administra productos y prepara los pedidos de su puesto en uno de los tres mercados."
        repartidor = person "Repartidor" "Consulta pedidos de delivery y actualiza su entrega."

        sancamilo = softwareSystem "San Camilo en Línea" "Plataforma de compras de los mercados San Camilo, Altiplano y Río Seco: catálogo, pedidos multipuesto, pago y entrega." {
            // E2: Contenedores
            pwa = container "Aplicación web progresiva" "Interfaz móvil para clientes, comerciantes y repartidores; solo por HTTPS. [QA08-01, QA08-06]" "HTML/CSS/JavaScript + Service Worker" "Web Browser"
            api = container "Aplicación web / API" "Monolito modular (ADR-001); filtra por mercado_id de la sesión, cobra con clave de idempotencia y lee las reglas de cada mercado. [QA08-01, QA08-02, QA08-04, QA08-05, QA08-07]" "Python / Django (HTTP/JSON)" {
                // E3: Componentes internos
                catalogo = component "Catálogo" "Gestiona puestos, productos, disponibilidad y stock por mercado. [QA08-01, QA08-07]" "Módulo Python/Django"
                pedidos = component "Pedidos" "Carrito, pedido multipuesto, Pedido y PedidoPuesto; dueño del puerto Notificador; toda consulta usa WHERE id = ? AND mercado_id = ? (ADR-006). [QA08-02, QA08-05]" "Módulo Python/Django"
                pagos = component "Pagos" "Cobra mediante PuertoPago y el adaptador Yape; Decorator idempotente con registro PENDIENTE y consulta antes de reintentar (ADR-007). [QA08-04]" "Módulo Python/Django"
                notificaciones = component "Notificaciones" "Implementa Notificador y coordina el envío asíncrono de avisos al comerciante (ADR-003). [QA08-03]" "Módulo Python/Django"
                entrega = component "Entrega" "Gestiona recojo, delivery y estado de PedidoPuesto según las reglas del mercado. [QA08-07]" "Módulo Python/Django"
                mercados = component "Mercados" "Reglas comerciales de cada mercado cargadas desde mercados.json; único punto de entrada RegistroMercados (ADR-008). [QA08-07, QA08-08]" "Módulo Python + JSON"
                compartido = component "Compartido" "Tipos, identificadores y utilidades sin dependencias de los módulos de negocio." "Módulo Python/Django"
            }
            worker = container "Worker de notificaciones y conciliación" "Reintenta avisos sin bloquear el pago y concilia cada 5 min los cobros en PENDIENTE (ADR-007). [QA08-03, QA08-04]" "Python / Celery"
            bd = container "Base de datos relacional" "Una sola base para los tres mercados: tablas con mercado_id (ADR-006) e intentos_pago con clave de idempotencia (ADR-007). [QA08-04, QA08-05]" "PostgreSQL 16" "Database"
            redis = container "Cola y caché" "Cola de tareas de Celery y caché del catálogo. [QA08-01, QA08-03]" "Redis" "Queue"
        }

        pasarela = softwareSystem "Pasarela de pago Yape" "Proveedor externo utilizado mediante la interfaz PasarelaPago; integración abstracta en el MVP." "Externo"
        whatsapp = softwareSystem "Servicio de WhatsApp" "Servicio externo al que se envían las confirmaciones y notificaciones." "Externo"

        // E1: Relaciones de Contexto
        cliente -> sancamilo "Consulta el catálogo, realiza pedidos multipuesto y paga"
        comerciante -> sancamilo "Publica productos y atiende pedidos"
        repartidor -> sancamilo "Consulta entregas asignadas y actualiza su estado"
        sancamilo -> pasarela "Solicita el cobro de pedidos con Yape"
        sancamilo -> whatsapp "Envía confirmaciones a comerciantes"

        // E2: Relaciones entre Contenedores
        cliente -> sancamilo.pwa "Realiza sus compras" "HTTPS"
        comerciante -> sancamilo.pwa "Gestiona su puesto" "HTTPS"
        repartidor -> sancamilo.pwa "Consulta y actualiza entregas" "HTTPS"
        sancamilo.pwa -> sancamilo.api "Envía solicitudes y recibe respuestas" "HTTPS/JSON"
        sancamilo.api -> sancamilo.bd "Lee y registra datos de negocio" "SQL/TCP"
        sancamilo.api -> sancamilo.redis "Encola notificaciones y utiliza caché" "Protocolo Redis/TCP"
        sancamilo.worker -> sancamilo.redis "Consume tareas y registra reintentos" "Protocolo Redis/TCP"
        sancamilo.worker -> whatsapp "Envía mensajes y confirmaciones" "HTTPS/JSON"
        sancamilo.api -> pasarela "Solicita cobros con clave de idempotencia [QA08-04]" "HTTPS/JSON"
        sancamilo.worker -> sancamilo.bd "Lee y actualiza intentos_pago en PENDIENTE [QA08-04]" "SQL/TCP"
        sancamilo.worker -> pasarela "Consulta el estado de cobros pendientes por clave [QA08-04]" "HTTPS/JSON"

        // E3: Relaciones entre Componentes
        sancamilo.pwa -> sancamilo.api.catalogo "Consulta productos y puestos" "HTTPS/JSON"
        sancamilo.pwa -> sancamilo.api.pedidos "Confirma y paga pedidos" "HTTPS/JSON"
        sancamilo.pwa -> sancamilo.api.entrega "Consulta estado de recojo o delivery" "HTTPS/JSON"

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
        sancamilo.api.pedidos -> sancamilo.bd "Guarda pedidos y estados filtrados por mercado_id [QA08-05]" "SQL/TCP"
        sancamilo.api.pagos -> sancamilo.bd "Registra intentos_pago antes de cobrar [QA08-04]" "SQL/TCP"
        sancamilo.api.pedidos -> sancamilo.api.mercados "Valida monto mínimo y horario del mercado [QA08-07]" "Llamada interna Python"
        sancamilo.api.catalogo -> sancamilo.api.mercados "Consulta el horario del mercado [QA08-07]" "Llamada interna Python"
        sancamilo.api.entrega -> sancamilo.api.mercados "Consulta si hay delivery y su costo [QA08-07]" "Llamada interna Python"

        // E5: Entorno de Despliegue
        produccion = deploymentEnvironment "Producción" {
            deploymentNode "Celular del usuario" "Dispositivo de gama baja (R-05)" "Android + Chrome" {
                containerInstance sancamilo.pwa
            }
            deploymentNode "Servidor VPS en la nube" "Un único servidor para el MVP (ADR-001, R-03)" "Ubuntu 24.04 LTS, 2 vCPU, 4 GB RAM" {
                deploymentNode "Docker Compose" "Ejecuta los contenedores del MVP" "Docker 27" {
                    containerInstance sancamilo.api
                    containerInstance sancamilo.worker
                    containerInstance sancamilo.bd
                    containerInstance sancamilo.redis
                }
            }
        }
        
    }

    views {
        systemContext sancamilo "Contexto" "Nivel 1: usuarios, San Camilo en Línea y servicios externos." {
            include *
            autolayout lr
        }
        container sancamilo "Contenedores" "Nivel 2 (Lab 08): contenedores con los escenarios que atiende cada uno [QA08-xx]." {
            include *
            autolayout lr
        }
        component sancamilo.api "Componentes" "Nivel 3: componentes internos de la API, alineados con paquetes.puml (Lab 05)." {
            include *
            autolayout lr
        }
        
        // E4: Vista Dinámica Corregida
        dynamic sancamilo.api "ConfirmarYPagar" "Dinámico: pagar con Yape un pedido de varios puestos (camino de éxito, CA-1)." {
            cliente -> sancamilo.pwa "Elige «Pagar con Yape»" "HTTPS"
            sancamilo.pwa -> sancamilo.api.pedidos "POST /pedidos/{id}/pago" "HTTPS/JSON"
            sancamilo.api.pedidos -> sancamilo.api.catalogo "Reserva el stock de cada línea"
            sancamilo.api.pedidos -> sancamilo.api.pagos "Solicita el cobro"
            sancamilo.api.pagos -> pasarela "Cobra con Yape" "HTTPS/JSON"
            sancamilo.api.pedidos -> sancamilo.bd "Guarda el pedido PAGADO y sus PedidoPuesto" "SQL/TCP"
            sancamilo.api.pedidos -> sancamilo.redis "Encola una notificación por puesto" "Protocolo Redis/TCP"
            sancamilo.worker -> sancamilo.redis "Consume la tarea" "Protocolo Redis/TCP"
            sancamilo.worker -> whatsapp "Notifica al comerciante" "HTTPS/JSON"
            autolayout lr
        }

        // E5: Vista de Despliegue
        deployment sancamilo produccion "Despliegue" "Despliegue en producción (MVP): celular, VPS y Docker Compose." {
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