# ADR-010: Arquitectura del sistema agéntico

- Estado: Propuesto para revisión del equipo
- Fecha: 2026-11-21
- Proyecto: San Camilo en Línea · Grupo 07 · Laboratorio 10

## Contexto

El equipo usó un agente para analizar y proponer cambios en pedidos, pagos e inventario. Los casos de estudio fueron los reintentos que podían duplicar un cobro (ISSUE-01), las reservas de stock que quedaban retenidas al fallar una estrategia de pago (ISSUE-02) y la pérdida de precisión por representar importes con `float` (ISSUE-03). La decisión considera el riesgo del cambio, el costo de la coordinación y la evidencia necesaria para que una persona pueda aceptar una propuesta.

## Decisión

| Aspecto | Arquitectura elegida |
|---|---|
| Arquetipo | **ReAct.** El agente emite una decisión estructurada. El contrato valida su forma y la política evalúa la acción antes de permitir que se ejecute. La observación alimenta la decisión siguiente. El modelo puede ser interactivo o reproducir decisiones grabadas. |
| Coordinación | **Agente único** para cambios acotados de menor riesgo. **Planificador, ejecutor y revisor crítico** cuando el cambio toca pagos o inventario y hay caminos de error que revisar. El planificador formula el plan sin herramientas. El revisor inspecciona el diff, lee el código y puede ejecutar pruebas, sin editar archivos. |
| Herramientas | Se usan lectura y búsqueda de código, mapa de firmas con `mapa_repo`, ejecución de pruebas, edición por reemplazo de un fragmento exacto y consulta de diferencias. La política asigna herramientas por rol y restringe los comandos a una lista permitida. El ejecutor trabaja en una copia desechable preparada desde el commit de E3. |
| Memoria | Cada agente conserva su objetivo, decisiones y observaciones en su historial de corto plazo. El ejecutor puede guardar hasta 20 notas de 300 caracteres en `notas.md` de la tarea. El revisor puede leerlas. Las trazas JSONL se guardan como evidencia para análisis posterior. |
| Límites | El agente único tiene un presupuesto de 15 pasos para acciones. En la coordinación, los presupuestos son 2 para el planificador, 12 por ejecutor y 8 por revisor, con un máximo de 2 rondas. La política protege `tests/` frente a `editar_archivo`. Los accesos mediante las herramientas de archivo se resuelven dentro de la copia de trabajo. |
| Rol humano | **Etapa 2, revisor.** Con `--humano` un integrante aprueba o rechaza cada edición que supera los controles previos. La decisión queda registrada. El equipo revisa el diff y las pruebas finales y decide si aprueba y fusiona el PR. El orquestador ejecuta las pruebas finales de forma independiente de lo que declare el agente. |

## Alternativas descartadas

| Alternativa | Motivo |
|---|---|
| Usar un flujo fijo para resolver los tres issues | La secuencia de revisión cambia con los archivos encontrados y los resultados de las pruebas. Un flujo fijo sí sirve para preparar la copia y ejecutar la verificación final. |
| Usar siempre un agente único | En ISSUE-02, la prueba específica pasó, pero la propuesta dejó dos caminos sin liberar el stock. El revisor detectó ambos al contrastar el diff con el comportamiento esperado. |
| Usar siempre la coordinación actor-crítico | En ISSUE-02, el costo pasó de 6 a 17 acciones y de 7 506 a 40 250 caracteres de contexto. Ese costo se reserva para cambios cuyo impacto justifica la revisión adicional. |
| Usar memoria persistente o vectorial compartida entre tareas | El historial y las notas por tarea cubren el alcance del laboratorio. En ISSUE-03, el mapa y las notas aportaron un hallazgo de tipos, pero la ejecución aumentó de 12 a 14 pasos y de 18 993 a 26 645 caracteres. |
| Otorgar escritura directa al repositorio principal o delegar la fusión al agente | La evidencia todavía exige revisión humana. En ISSUE-01 el agente declaró resuelta la tarea después de que pytest interrumpiera la colección con errores de importación. |

## Consecuencias

- La revisión crítica añade una comprobación contra el comportamiento esperado del issue. En ISSUE-02 detectó la reserva retenida ante un intento de cobro previo y ante una excepción al ejecutar el pago. La segunda ronda atendió ambas observaciones. El orquestador registró 49 pruebas aprobadas y un fallo correspondiente al ISSUE-03.
- La aprobación por edición y los registros facilitan la auditoría. En la variante supervisada de ISSUE-02 se registraron tres aprobaciones y una observación humana sobre dos pruebas que faltaban para los hallazgos del revisor.
- La copia de trabajo reduce el riesgo de modificar el repositorio original. El control de rutas y comandos opera en la aplicación. Para usarlo fuera del laboratorio haría falta aislamiento a nivel del sistema operativo y control de los subprocesos.
- El costo medido corresponde a las ejecuciones documentadas. El contexto final del ISSUE-01 quedó sin medición porque se guardaron observaciones recortadas y se omitió el total histórico.

## Evidencia

- [Diseño y máquina de estados](../../../agentes/diseno/estados.puml)
- [Coordinación del ISSUE-02](../../../agentes/coordinacion.md)
- [Herramientas y memoria del ISSUE-03](../../../agentes/herramienta-memoria.md)
- [Aprobación humana y etapas de delegación](../../../agentes/delegacion.md)
- [Métricas y trayectoria de E7](../../../agentes/observacion.md)
- [Bitácora de IA](../../../agentes/bitacora-ia.md)
