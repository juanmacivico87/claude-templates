Explora este repositorio y crea o actualiza el archivo CLAUDE.md de la raíz con la información que un agente necesita en cada sesión.

Reglas:

- Incluye únicamente lo que no sea evidente leyendo el código:
  - Comandos de build, test y run, con su forma exacta de ejecución.
  - Estructura de directorios relevante, explicando qué contiene cada parte importante.
  - Convenciones de código que se desvíen de lo habitual o que no se deduzcan de los archivos de configuración.
  - Gotchas no obvios: dependencias frágiles, pasos de orden obligatorio, variables de entorno necesarias, errores frecuentes y sus soluciones.
- Incluye las siguientes preferencias generales:
  - Responde siempre en español, salvo que te pida otro idioma.
  - En el caso de que te pida el mensaje para un commit, responde en inglés.
  - Antes de borrar archivos o ejecutar comandos destructivos, descríbelos y espera mi confirmación.
- Incluye los siguientes estándares de desarrollo:
  - El código (nombres de variables, funciones, clases y comentarios) se escribe siempre en inglés y utilizando el estándar lower camel case (lowerCamelCase).
  - Una clase o función hace una sola cosa. Si una función necesita un comentario para explicar qué hace en un bloque interno, extrae ese bloque a una función con nombre claro.
  - Prefiere composición e inyección de dependencias frente a herencia, salvo que el framework la exija.
  - No añadas parámetros booleanos para cambiar el comportamiento de una función. Crea dos funciones con nombres explícitos.
  - Funciones de menos de 30 líneas y máximo 3 niveles de anidación. Si se supera, justifícalo o refactoriza.
  - No dupliques código bajo ningún concepto. En el caso de que tengas que duplicar código para casos de uso distintos, extrae el bloque a una nueva función.
  - Al modificar código existente, no refactorices fuera del alcance de la tarea. Propón la mejora aparte.
  - Nombres descriptivos en inglés. Evita abreviaturas y nombres genéricos como `$data` o `handle()`.
- Además, si el proyecto es para WordPress, incluye también estos estándares de desarrollo:
  - Los hooks y callbacks de WordPress se registran en clases de integración, no mezclados con la lógica de negocio.
  - La lógica de negocio no depende directamente de funciones globales de WordPress (`get_option`, `wpdb`, etc.) cuando puede recibirlas por constructor. Así es testeable.
- No incluyas descripciones genéricas del lenguaje o del framework, ni explicaciones de lo que es evidente al abrir un archivo.
- Si el CLAUDE.md ya existe, consérvalo y actualiza solo lo que haya cambiado. Elimina lo que ya no sea cierto.
- Verifica los comandos antes de escribirlos cuando sea posible.

Indicaciones adicionales del usuario: $ARGUMENTS