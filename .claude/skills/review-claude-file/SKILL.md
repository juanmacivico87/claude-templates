---
name: review-claude-file
description: Comprueba si el CLAUDE.md del repositorio sigue siendo fiel al código y propone cambios cuando detecte que está desfasado. Úsala al empezar una sesión en un repositorio que tiene CLAUDE.md, tras cambios importantes en build, dependencias, estructura o scripts, o cuando un comando documentado falla. No modifica el archivo sin confirmación del usuario.
---

# Revisar CLAUDE.md

Tu objetivo es detectar si el CLAUDE.md de la raíz describe algo que ya no es cierto, y proponer correcciones concretas. No reescribas el archivo entero ni añadas contenido nuevo que no sea necesario.

## Procedimiento

1. **Localiza el archivo.** Busca CLAUDE.md en la raíz del repositorio. Si no existe, no propongas nada: indica que puede crearse con `/create-claude-file`.

2. **Contrasta cada afirmación con el código.** Revisa en particular:
  - Comandos de build, test y run. Verifica que existen en composer.json, package.json, Makefile, pyproject.toml, scripts de CI u otros archivos equivalentes, y que la forma de ejecutarlos coincide.
  - Rutas y directorios mencionados. Comprueba que existen y que siguen teniendo el contenido descrito.
  - Versiones, dependencias y variables de entorno citadas.
  - Convenciones y gotchas. Si un problema descrito ya está resuelto en el código o en la configuración, márcalo como obsoleto.

3. **Identifica señales de desfase.** Son motivos suficientes para proponer un cambio:
  - Un comando documentado no existe o falla.
  - Una ruta ha cambiado de sitio o ya no existe.
  - Hay un directorio nuevo y relevante que no aparece en la estructura.
  - Una herramienta o dependencia documentada ha sido sustituida.
  - Un gotcha ya no aplica.

4. **Filtra el ruido.** No propongas cambios por cuestiones de estilo, redacción o detalles que no afectan a cómo trabajaría un agente. Si no hay desfase relevante, no digas nada sobre el archivo y continúa con la tarea que te haya pedido el usuario.

5. **Presenta una propuesta.** Para cada cambio indica:
  - La línea o sección afectada, con el texto actual y el propuesto.
  - La evidencia, citando el archivo y la parte del código que lo demuestra.

  Termina preguntando si quieres que aplique los cambios. Ofrece un máximo de cinco cambios por propuesta.

6. **Aplica solo tras confirmación.** Haz cambios mínimos y no añadas nada que sea evidente leyendo el código.