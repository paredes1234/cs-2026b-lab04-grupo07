# ADR-001: Adoptar un monolito modular para el MVP de San Camilo en Línea

- Estado: Aceptado
- Fecha: 2026-10-01
- Decisores: Flores Nuñez Rodrigo Francisco, Jimenez Paredes Fabricio Gabriel, Bravo Arredondo Cristhian Matías

## Contexto
El MVP debe estar en producción en 1 mes (R-01) con un equipo de 3 integrantes (R-02) y
presupuesto bajo (R-03). La plataforma permite crear pedidos con productos de varios puestos
(RF-03), elegir recojo o delivery (RF-04), pagar con Yape (RF-05) y confirmar por WhatsApp al
comerciante (RF-06). WhatsApp y Yape son servicios externos que pueden fallar (R-06).
El atributo crítico es la capacidad de interacción (QA-01): un comerciante con poca
experiencia digital debe publicar un producto en ≤ 3 toques desde un celular de gama baja
(R-05). También importan el rendimiento del catálogo (QA-02), que los pedidos no se pierdan
si falla un servicio externo (QA-03) y poder modificar pagos, catálogo, delivery o
notificaciones sin afectar a todo el sistema.

## Alternativas consideradas
1. Monolito en capas (4,70 en matriz-decision.md): simple y rápido de construir, pero la
   modificabilidad (3/5) sufre porque las funciones comparten las mismas capas y se acoplan.
2. Microservicios (2,80): máxima modificabilidad y escalabilidad independiente, pero requiere
   varios despliegues, bases de datos, comunicación por red y monitoreo; excede R-01, R-02 y R-03.
3. Monolito modular (4,85): un solo despliegue con módulos de dominio y fronteras explícitas.

## Decisión
Usaremos un monolito modular con cinco módulos: Catálogo y Productos, Carrito y Pedidos,
Pagos, Notificaciones, y Recojo y Delivery. Los módulos se comunican solo mediante interfaces
públicas y se apoyan en una capa de infraestructura con repositorios y adaptadores para la base
de datos relacional, Yape (o su proveedor de pago) y WhatsApp. Se desplegará como una sola
aplicación en un único servidor.

## Consecuencias
- Positivas: un solo despliegue y bajo costo (R-01, R-03); cambiar el mecanismo de pago o de
  notificación se limita a su adaptador, sin tocar los demás módulos; si un módulo (p. ej.,
  Catálogo) necesita escalar por separado, puede extraerse más adelante con un nuevo ADR.
- Negativas / riesgos: los módulos pueden acoplarse si el equipo no respeta sus interfaces
  (se revisará en los Pull Requests y con una herramienta como import-linter en la CI); una
  falla grave afecta a toda la aplicación; la base de datos única puede ser punto de contención
  si la demanda crece mucho.
