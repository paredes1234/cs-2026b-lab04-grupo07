# ADR-002: Usar una PWA en lugar de una app nativa para clientes, comerciantes y repartidores

- Estado: Aceptado
- Fecha: 2026-10-01
- Decisores: Flores Nuñez Rodrigo Francisco, Jimenez Paredes Fabricio Gabriel, Bravo Arredondo Cristhian Matías

## Contexto
El atributo crítico es la capacidad de interacción (QA-01): un comerciante con poca
experiencia digital debe publicar un producto (RF-01) en ≤ 3 toques desde un celular de gama
baja (R-05). El catálogo debe responder con p95 ≤ 2 s desde un móvil (QA-02). El MVP debe
estar listo en 1 mes (R-01) con 3 integrantes (R-02) y presupuesto bajo (R-03). Los tres
actores (cliente, comerciante y repartidor, RF-02 a RF-07) usan el sistema desde el celular.

## Alternativas consideradas
1. App nativa (Android/iOS): mejor acceso al hardware, pero exige una o dos bases de código
   adicionales, publicación en tiendas e instalación que consume almacenamiento en equipos
   de gama baja.
2. PWA (Progressive Web App): una sola base de código web servida por el monolito, instalable
   desde el navegador, sin tiendas y con caché para el catálogo.

## Decisión
Usaremos una PWA mobile-first servida por el mismo monolito modular, con botones grandes,
formularios mínimos y un flujo de publicación de producto de máximo 3 toques. Se probará en
un celular de gama baja real antes de la entrega.

## Consecuencias
- Positivas: una sola base de código y un solo despliegue (R-01, R-02); sin costo ni trámites
  de tiendas de aplicaciones; no requiere una instalación pesada; las mejoras llegan a todos
  los usuarios al mismo tiempo.
- Negativas / riesgos: acceso limitado a funciones nativas del dispositivo (p. ej., ubicación en
  segundo plano del repartidor y notificaciones push dependen del navegador); el rendimiento
  depende del navegador del celular; el uso sin conexión es limitado.
