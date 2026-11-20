# Lienzo de diseño del sistema agéntico
## Proyecto: San Camilo en Línea

### 1. Tipo de agente
Se utilizará un agente de software encargado de analizar problemas del proyecto, revisar el código y proponer soluciones. Su trabajo estará enfocado en los módulos de pedidos, pagos e inventario.

**Justificación:** El proyecto contiene diferentes módulos relacionados entre sí, por lo que un agente puede ayudar a identificar errores y proponer mejoras sin modificar directamente todo el sistema.

### 2. Arquetipo del agente
Se utilizará el arquetipo ReAct (razonamiento y acción), mediante el cual el agente analiza el problema, decide qué herramienta utilizar, observa el resultado y continúa hasta encontrar una posible solución.

**Justificación:** Este enfoque permite que el agente revise el código paso a paso y compruebe sus decisiones mediante las herramientas disponibles.

### 3. Herramientas
El agente utilizará herramientas para:
- Leer archivos del proyecto.
- Buscar funciones y clases.
- Revisar las pruebas existentes.
- Ejecutar pruebas automatizadas.
- Proponer cambios en los archivos.

**Justificación:** Estas herramientas permiten analizar el código antes de proponer una modificación y comprobar si la solución funciona.

### 4. Memoria
Se utilizará memoria de corto plazo para conservar el issue que se está resolviendo, los archivos revisados, las hipótesis y los resultados de las pruebas.

**Justificación:** Esto evita que el agente pierda el contexto durante el análisis de un problema.

### 5. Coordinación
Para esta primera versión se utilizará un agente único que realizará el análisis y propondrá una solución. La revisión final estará a cargo de un integrante del equipo.

**Justificación:** El proyecto puede comenzar con una estructura sencilla, evitando agregar varios agentes cuando todavía se están evaluando las tareas principales.

### 6. Participación humana
El agente podrá analizar el código y proponer modificaciones, pero un integrante del equipo deberá revisar y aprobar los cambios antes de incorporarlos al proyecto.

**Justificación:** Esto evita que una modificación incorrecta afecte el funcionamiento de San Camilo en Línea.

### 7. Control y seguridad
Las decisiones del agente deberán cumplir el formato establecido por el contrato. También se limitarán las herramientas disponibles y se comprobarán los resultados mediante pruebas automatizadas.

**Justificación:** El agente no debe ejecutar acciones fuera de las permitidas ni modificar el proyecto sin una revisión previa.

### Tareas que realizará el agente
1. Analizar los problemas relacionados con el procesamiento de pedidos y pagos.
2. Identificar los archivos y funciones involucrados.
3. Revisar las pruebas existentes y proponer nuevas pruebas.
4. Proponer una solución para el problema encontrado.
5. Ejecutar las pruebas y presentar los resultados para su revisión.