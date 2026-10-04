# Bitácora de uso de IA — San Camilo en Línea

> Este archivo contiene inicialmente las dos interacciones exigidas durante E2.
> En E7 deberán completarse como mínimo cinco interacciones en total.

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|---|---|---|---|---|---|
| 1 | 03/10/2026 | ChatGPT | Generar 3 alternativas arquitectónicas para San Camilo en Línea considerando plazo, equipo, presupuesto y atributo crítico de usabilidad. | Monolito en capas, monolito modular y microservicios; recomendó monolito modular por equilibrio entre simplicidad y modificabilidad. | Se contrastó la recomendación con R-01, R-03, QA-01 y la matriz ponderada. | Aceptada |
| 2 | 03/10/2026 | ChatGPT | Actuar como abogado del diablo y criticar el monolito modular seleccionado. | Señaló riesgos de acoplamiento entre módulos, punto único de falla, crecimiento de la base de datos y dependencia de servicios externos. | Se mantuvo la alternativa, pero se consideraron interfaces claras entre módulos y adaptadores para servicios externos. | Corregida |

## Anexo: prompts completos

### Prompt 1 — Generación de alternativas

Actúa como arquitecto de software senior con experiencia en sistemas web para pequeños comercios.

Contexto: **San Camilo en Línea** es una plataforma para realizar pedidos a los puestos del Mercado San Camilo. Los clientes pueden consultar catálogos por puesto, realizar pedidos con productos de varios puestos, registrar el pago mediante Yape y elegir recojo o delivery. Los comerciantes reciben confirmaciones por WhatsApp.

Actores: cliente, comerciante y repartidor.

Atributo crítico: capacidad de interacción. Un comerciante con poca experiencia digital debe poder publicar un producto en máximo 3 toques desde un celular de gama baja.

Restricciones:
- MVP en producción en 1 mes.
- Equipo de **[REEMPLAZAR POR EL NÚMERO REAL DE INTEGRANTES] developers**.
- Tecnologías dominadas: **[REEMPLAZAR POR LAS TECNOLOGÍAS REALES DEL EQUIPO]**.
- Presupuesto bajo.
- Uso principalmente desde dispositivos móviles.

Tarea: propón 3 alternativas de estilo arquitectónico. Para cada alternativa indica fortalezas, debilidades, riesgos y qué atributos de calidad favorece o penaliza.

Formato: tabla comparativa en Markdown y, al final, una recomendación justificada.

No inventes APIs ni capacidades de servicios externos; si no estás seguro, indícalo.

### Resumen de la respuesta de IA

La IA propuso las siguientes alternativas:

1. **Monolito en capas:** simple, económico y rápido de implementar, pero con riesgo de mayor acoplamiento.
2. **Monolito modular:** un único despliegue organizado en módulos de dominio, con buen equilibrio entre simplicidad operativa y modificabilidad.
3. **Microservicios:** mayor independencia y escalabilidad, pero con mayor complejidad de despliegue, monitoreo y comunicación.

La recomendación fue **monolito modular**, debido al plazo corto, presupuesto reducido y necesidad de mantener separados los principales módulos del sistema.

---

### Prompt 2 — Crítica adversarial

Ahora actúa como **abogado del diablo**.

Critica la alternativa **Monolito Modular** recomendada para San Camilo en Línea.

Considera las restricciones de un MVP de 1 mes, equipo reducido, presupuesto bajo, uso desde celulares de gama baja y dependencias externas como WhatsApp y el mecanismo de pago con Yape.

Responde:
1. ¿Qué supuestos podrían no cumplirse?
2. ¿Qué podría fallar en producción?
3. ¿Qué costos ocultos podría tener?
4. Enumera los 5 riesgos más importantes.
5. Propón una táctica de mitigación para cada riesgo.

### Resumen de la crítica de IA

La crítica identificó los siguientes riesgos principales:

1. Los módulos pueden terminar excesivamente acoplados si no se respetan sus interfaces.
2. Al existir un solo despliegue, una falla grave puede afectar a toda la aplicación.
3. Una única base de datos puede convertirse en un punto de contención conforme aumente la carga.
4. Las integraciones con servicios externos pueden fallar o cambiar.
5. Si el sistema crece significativamente, algunos módulos podrían necesitar escalar de manera independiente.

El equipo mantuvo el **monolito modular** porque estos riesgos pueden mitigarse y no superan, para el MVP actual, el costo y complejidad de adoptar microservicios.
