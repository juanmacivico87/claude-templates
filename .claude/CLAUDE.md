# Preferencias globales

## Idioma

- Habla siempre en español con el usuario: mensajes, resúmenes y también las preguntas de AskUserQuestion (texto, cabecera, opciones y descripciones).
- El código va siempre en inglés: comentarios, nombres de variables, funciones, constantes, claves de JSON generados y nombres de archivos, scripts y skills. Solo quedan en español los datos que deben coincidir con texto en español (por ejemplo, patrones que buscan frases escritas por el usuario).
- Los mensajes de commit van en inglés.

## Sesiones

- Una sesión por tarea o fase. Cuando se cierre una fase (cambios commiteados o tarea entregada), guarda en memoria el estado y lo pendiente, y sugiere al usuario continuar con `/clear` o en una sesión nueva, sobre todo si la sesión ya es larga o ha tenido compactaciones.
- Al empezar una sesión que retoma un trabajo, lee primero la memoria de estado correspondiente en lugar de reconstruir el contexto desde cero.
- Usa rutas absolutas en los comandos; no des por hecho que el directorio de trabajo sigue siendo la raíz del proyecto.

## Persistencia de archivos

El ordenador se reinicia cada día, y en cada reinicio pueden borrarse archivos fuera de `~/.claude`. Cualquier archivo que pueda perderse con un reinicio y que no esté versionado en git (CLAUDE.md, notas, planes, configuraciones locales, scripts auxiliares, etc.) se guarda dentro de `~/.claude`, nunca solo en el proyecto ni en `/tmp`.

- Archivos de un proyecto: `~/.claude/projects/<ruta-del-proyecto-con-guiones>/` (por ejemplo, `/home/juanmacivico87/projects/foo` → `~/.claude/projects/-home-juanmacivico87-projects-foo/`).
- Si el proyecto necesita ver el archivo en su propia carpeta (por ejemplo, un CLAUDE.md), deja en el proyecto solo un CLAUDE.md de una línea que lo importe: `@~/.claude/projects/<ruta-del-proyecto-con-guiones>/CLAUDE.md`.
- Al terminar, indica siempre la ruta completa donde ha quedado guardado cada archivo.
