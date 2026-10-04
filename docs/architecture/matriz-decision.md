# Matriz de decisión — San Camilo en Línea

## 1. Alternativas arquitectónicas

A partir de los drivers definidos en `drivers.md`, se comparan tres estilos arquitectónicos para el MVP de **San Camilo en Línea**.

### A. Monolito en capas

El sistema se implementa como una sola aplicación organizada en capas de presentación, lógica de negocio y acceso a datos. Su principal ventaja es la simplicidad para desarrollar y desplegar el MVP, aunque puede generar mayor acoplamiento entre funcionalidades conforme el sistema crece.

### B. Monolito modular

El sistema mantiene un único despliegue, pero se divide internamente en módulos con responsabilidades claras, por ejemplo: Catálogo, Pedidos, Pagos, Delivery/Recojo y Notificaciones. Permite conservar una operación sencilla y, al mismo tiempo, mejorar la modificabilidad.

### C. Microservicios

Las funcionalidades principales se separan en servicios independientes que se comunican mediante red. Facilita la escalabilidad y el despliegue independiente, pero introduce mayor complejidad de infraestructura, comunicación, monitoreo y operación.

---

## 2. Criterios y pesos

Los criterios se derivan de los drivers definidos en `drivers.md`.

| Criterio | Peso | Justificación (driver relacionado) |
|---|---:|---|
| Capacidad de interacción y soporte móvil | 25 % | QA-01 y R-05: el comerciante debe publicar un producto en ≤ 3 toques desde un celular de gama baja. |
| Tiempo de entrega | 25 % | R-01: el MVP debe estar en producción en 1 mes. |
| Costo operativo | 20 % | R-03: el presupuesto del proyecto es bajo. |
| Simplicidad operativa | 15 % | R-02: un equipo reducido debe poder desarrollar, desplegar y mantener la solución. |
| Modificabilidad | 15 % | Los módulos de catálogo, pedidos, pagos, delivery y notificaciones deben poder evolucionar con el menor impacto posible. |
| **Total** | **100 %** | |

---

## 3. Matriz de decisión

Escala utilizada:

- **1:** muy malo
- **2:** malo
- **3:** regular
- **4:** bueno
- **5:** excelente

| Criterio (peso) | A. Monolito en capas | B. Monolito modular | C. Microservicios |
|---|---:|---:|---:|
| Capacidad de interacción y soporte móvil (25 %) | 5 | 5 | 4 |
| Tiempo de entrega (25 %) | 5 | 5 | 2 |
| Costo operativo (20 %) | 5 | 5 | 2 |
| Simplicidad operativa (15 %) | 5 | 4 | 1 |
| Modificabilidad (15 %) | 3 | 5 | 5 |
| **Total ponderado** | **4,70** | **4,85** | **2,80** |

### Cálculo del total ponderado

**A. Monolito en capas**

`0,25×5 + 0,25×5 + 0,20×5 + 0,15×5 + 0,15×3 = 4,70`

**B. Monolito modular**

`0,25×5 + 0,25×5 + 0,20×5 + 0,15×4 + 0,15×5 = 4,85`

**C. Microservicios**

`0,25×4 + 0,25×2 + 0,20×2 + 0,15×1 + 0,15×5 = 2,80`

---

## 4. Verificación crítica de la propuesta de IA

Durante la revisión se identificó que no se debe asumir que Yape dispone de una API pública abierta para integrarse directamente con cualquier aplicación. Por ello, en la arquitectura se evita representar una integración técnica específica no verificada y se utiliza el término **“Yape / proveedor de pago”**.

También se revisó la conveniencia de microservicios. Aunque este estilo ofrece mayor escalabilidad e independencia de despliegue, para el MVP de San Camilo en Línea introduce una complejidad operativa que no se justifica frente al plazo de un mes, el presupuesto bajo y el tamaño reducido del equipo.

---

## 5. Conclusión

La alternativa seleccionada es **B. Monolito modular**, con un puntaje ponderado de **4,85/5**.

Esta alternativa mantiene un único despliegue y un costo operativo bajo, características favorables para cumplir el plazo de un mes. Al mismo tiempo, separa las principales funcionalidades del sistema en módulos, facilitando cambios futuros sin introducir la complejidad operacional de los microservicios.

La decisión final corresponde al equipo y se basa en los drivers y restricciones establecidos en `drivers.md`.

Ver [ADR-001: Estilo arquitectónico](adr/001-estilo-arquitectonico.md).
