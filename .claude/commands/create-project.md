Vamos a crear un entorno de desarrollo dockerizado para un proyecto nuevo con estos parámetros recibidos como argumentos: $ARGUMENTS

Los argumentos se escriben como pares clave=valor. Claves admitidas:
- framework: nombre del CMS o framework (wordpress, drupal, symfony, laravel, nestjs, express, angular, nextjs, u otro indicado por el usuario).
- version: versión a usar. Si no se indica, usa la última versión estable publicada en la web oficial del proyecto.
- db: motor de base de datos (mysql, mariadb, postgresql, mongodb, sqlite u otro). Si no se indica y el framework necesita base de datos, usa mariadb y repórtalo en el resumen final.
- name: nombre del proyecto en lenguaje natural, por ejemplo "mi sitio web".

Antes de crear nada, comprueba que tienes framework y name. Si falta alguno, pregúntalo y detente.

## 1. Normalización del nombre

Convierte el nombre a minúsculas, elimina acentos, sustituye espacios y guiones por guiones bajos y quita cualquier otro carácter no alfanumérico. Por ejemplo, "Mi Sitio Web" pasa a `mi_sitio_web`. Los contenedores se llamarán `[proyecto]_app`, `[proyecto]_db` y, si procede, `[proyecto]_cache` o `[proyecto]_web`. Usa el mismo prefijo para la red y los volúmenes.

## 2. Comprobaciones previas

- Verifica que Docker y Docker Compose están instalados y en ejecución. Si no lo están, indícalo y detente.
- Comprueba que los puertos que vas a publicar (por ejemplo 8080 para la app y 3306 o 5432 para la base de datos) están libres. Si alguno está ocupado, no lo cambies en silencio: propón un puerto alternativo y espera confirmación.
- Si el directorio ya contiene un docker-compose.yml, un .env o una aplicación instalada, no sobrescribas nada. Pregunta cómo proceder.

## 3. Verificación de versiones y compatibilidad

No te fíes de la memoria para versiones. Consulta la web oficial del framework o CMS (y su documentación de requisitos) para obtener:

- La versión estable actual, si el usuario no ha indicado ninguna.
- La versión de runtime que exige esa versión (PHP, Node.js, Python, etc.).
- Los motores de base de datos que soporta oficialmente esa versión.

Si la combinación pedida no es compatible (por ejemplo, un CMS que no soporta el motor indicado), no crees el entorno. Explica el motivo y propón la alternativa más cercana soportada.

## 4. Imágenes Docker

- Usa imágenes oficiales siempre que existan, con la versión fijada en el tag. Nunca uses `latest`. Ejemplos orientativos: `wordpress:<versión>-php<X.Y>-apache`, `php:<X.Y>-fpm`, `node:<X>-alpine`, `mariadb:<versión>`, `postgres:<versión>`, `mongo:<versión>`. Verifica que el tag existe antes de usarlo.
- Si no existe imagen oficial del framework, crea un Dockerfile mínimo basado en la imagen oficial del runtime, con la versión fijada, que instale dependencias de forma reproducible (composer.lock, package-lock.json, poetry.lock o equivalente) y use un usuario no root cuando sea posible.
- Si el proyecto aún no existe, genera el esqueleto con el instalador oficial del framework dentro del contenedor, o indica el comando exacto que hay que ejecutar.

## 5. docker-compose.yml

- Define los servicios de aplicación y base de datos con los nombres indicados en el punto 1.
- Crea volúmenes nombrados para los datos de la base de datos y para los directorios que deben persistir (por ejemplo wp-content en WordPress, storage en Laravel, uploads en otros casos). No montes código fuente de forma que oculte dependencias instaladas dentro del contenedor.
- Añade `healthcheck` a la base de datos y haz que la aplicación dependa de ella con `condition: service_healthy`.
- Publica solo los puertos necesarios y enlázalos a 127.0.0.1 cuando sea posible, para que el entorno no quede expuesto en la red local.
- No pongas credenciales escritas en el docker-compose.yml. Usa variables leídas desde `.env`.

## 6. Variables de entorno y secretos

- Crea `.env` con valores generados aleatoriamente para contraseñas y claves (por ejemplo con `openssl rand -base64 32`). Nunca uses contraseñas de ejemplo ni valores por defecto de la documentación.
- Crea `.env.example` con las mismas claves y valores vacíos o de ejemplo no sensibles. Este sí puede versionarse.
- Añade `.env` al `.gitignore`. Si no existe `.gitignore`, créalo con las entradas básicas del framework y `.env`.
- Si el framework usa archivos de configuración (wp-config.php, settings.php, config/*.php, .env propio), configúralo mediante variables de entorno cuando el framework lo permita, sin editar archivos de núcleo.
- No muestres las contraseñas generadas en el chat. Indica en el resumen dónde están guardadas (`.env`) y cómo consultarlas.

## 7. Construcción y arranque

1. Construye las imágenes con `docker compose build`.
2. Levanta los servicios con `docker compose up -d`.
3. Espera a que la base de datos esté lista (healthcheck en estado healthy).
4. Comprueba con `curl` que la aplicación responde. Acepta 200 o una redirección controlada al asistente de instalación. Si devuelve error 5xx, revisa los logs con `docker compose logs` y corrige la causa antes de dar el entorno por bueno.
5. No ejecutes migraciones, seeds ni instaladores que modifiquen datos sin preguntar antes, y nunca conectes el entorno a datos de producción.

## 8. Informe final

Presenta en prosa, con una lista corta solo para las URLs y los comandos:

- Proyecto creado: nombre normalizado, framework y versión elegida, con la fuente consultada.
- Runtime y motor de base de datos, indicando si se usó un valor por defecto.
- Contenedores levantados y puertos publicados.
- Cómo obtener las credenciales (archivo `.env`, sin mostrar valores).
- Comandos útiles: arrancar, parar, ver logs y entrar en el contenedor de la aplicación.
- Pasos pendientes, por ejemplo completar el asistente de instalación o ejecutar migraciones.

Termina preguntando si quieres que haga algo más antes de dar el entorno por cerrado.