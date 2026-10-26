# Registro de Olores de Código y Decisiones de Diseño

## 1. Acoplamiento Fuerte a Servicios Concretos
* **Descripción:** `ServicioPedidosProcesador` instancia directamente `PasarelaPagoClient` e `InventarioRepository`.
* **Patrón Propuesto:** Dependency Injection + Adapter / Interface.
* **Principio SOLID:** Principio de Inversión de Dependencias (DIP) y Abierto/Cerrado (OCP).
* **Decisión:** ACEPTADO.

## 2. Método Monolítico (God Method)
* **Descripción:** El método `confirmar_y_pagar` maneja validación, reintentos, stock y persistencia SQL directa.
* **Patrón Propuesto:** Command / Strategy Pattern.
* **Principio SOLID:** Principio de Responsabilidad Única (SRP).
* **Decisión:** ACEPTADO.

## 3. Manejo Explícito de Reintentos mediante Bucle Interno
* **Descripción:** Uso de un bucle `while` interno que acopla la infraestructura con la lógica de negocio.
* **Patrón Propuesto:** Retry Pattern / Decorator.
* **Principio SOLID:** Principio de Responsabilidad Única (SRP).
* **Decisión:** ACEPTADO.

## 4. Reemplazo del Estado por un Framework de Máquina de Estados Compleja
* **Propuesta de IA:** Instalar un framework externo pesado de State Machine.
* **Patrón Propuesto:** State Pattern (vía framework externo).
* **Principio SOLID:** YAGNI / KISS.
* **Decisión:** RECHAZADO.
* **Justificación:** Añade complejidad innecesaria para un flujo simple de confirmación y pago. Se optará por clases nativas de Python.