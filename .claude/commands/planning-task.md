Vamos a realizar la siguiente tarea: $ARGUMENTS

Antes de tocar nada, necesito que examines la aplicación, prepares un plan y tomes una línea base del estado actual. Sigue estos pasos en orden y no modifiques ningún archivo ni dato durante la fase de comprobación.

## 1. Contexto del proyecto

Lee el CLAUDE.md de la raíz. Ahí deben figurar la URL del entorno de pruebas, la plataforma (WordPress o Drupal), los comandos para listar plugins o módulos, y cómo obtener los usuarios de prueba. Si falta alguno de estos datos, indícalo en el informe final y no lo supongas.

Antes de continuar, confirma que el entorno de pruebas es el que se va a revisar y no producción. Si la URL del CLAUDE.md apunta a producción o no está clara, detente y pregúntame.

## 2. Revisión de enlaces

Usa Playwright para recorrer la aplicación y comprobar los enlaces, con estas reglas:

- Realiza solo peticiones GET. No envíes formularios, no hagas clic en botones de acción y no hagas peticiones POST.
- No sigas enlaces de cierre de sesión, eliminación, envío de correos, exportaciones pesadas o cualquier acción que cambie datos. Anota cuáles has omitido y por qué.
- Revisa los enlaces públicos sin sesión iniciada.
- Revisa los enlaces privados con sesión iniciada, una vez por cada rol de usuario de prueba disponible. Obtén las credenciales de la base de datos local o de variables de entorno, nunca de archivos versionados, y no las muestres en el informe.
- Para cada enlace comprueba:
  - Que la respuesta HTTP sea 200. Anota las redirecciones y su destino.
  - Que la página se renderiza: los componentes principales son visibles y no hay bloques vacíos ni maquetación rota.
  - Que se puede interactuar con los elementos habituales (menús, botones, enlaces de navegación, buscadores, formularios de solo lectura).
  - Que no hay errores en la consola del navegador ni avisos PHP o de plantilla visibles en pantalla.

Si Playwright no está instalado, instálalo.

## 3. Conflictos de plugins o módulos

Usa los comandos de la plataforma indicados en el CLAUDE.md. Como referencia:

- WordPress: `wp plugin list`, `wp theme list`, `wp core verify-checksums` y `wp plugin verify-checksums --all`, si WP-CLI está disponible.
- Drupal: `drush pm:list --status=enabled`, `drush status` y `drush watchdog:show --severity=Error --count=50`, si Drush está disponible.

Señala versiones desactualizadas o incompatibles, plugins o módulos con errores en los logs, y cualquier dependencia que falte. Indica la evidencia de cada caso.

## 4. Informe previo

Presenta el resultado en este orden, en prosa y con tablas solo donde aporten claridad:

1. Resumen: estado general en una o dos frases.
2. Enlaces con problemas: URL, rol, código o síntoma, y evidencia.
3. Conflictos de plugins o módulos.
4. Lo que no se ha podido comprobar y por qué.
5. Plan propuesto para la tarea, con los pasos y los archivos que se tocarían.

Termina preguntándome si quiero que empieces con el plan. No ejecutes ninguna tarea de modificación hasta que yo lo confirme.