Vamos a crear un entorno de desarrollo dockerizado para un sitio WordPress con estos parámetros recibidos como argumentos: $ARGUMENTS

Los argumentos se escriben como pares clave=valor. Claves admitidas:
- name: nombre del proyecto en lenguaje natural, por ejemplo "mi sitio web". Obligatorio.
- version: versión de WordPress. Si no se indica, usa la última versión estable publicada en wordpress.org.
- php: versión de PHP. Si no se indica, usa la mínima recomendada por la versión de WordPress elegida, verificada en la documentación oficial, y repórtalo.
- db: mysql o mariadb. Si no se indica, usa mariadb y repórtalo. Cualquier otro motor no es compatible con WordPress: explícalo y detente.

Antes de crear nada, comprueba que tienes name. Si falta, pregúntalo y detente.

## 1. Normalización del nombre

Convierte el nombre a minúsculas, elimina acentos, sustituye espacios y guiones por guiones bajos y quita cualquier otro carácter no alfanumérico. Por ejemplo, "Mi Sitio Web" pasa a `mi_sitio_web`. Los contenedores se llamarán `[proyecto]_app`, `[proyecto]_db` y, si procede, `[proyecto]_phpmyadmin`. Usa el mismo prefijo para la red y los volúmenes.

## 2. Comprobaciones previas

- Verifica que Docker y Docker Compose están instalados y en ejecución. Si no lo están, indícalo y detente.
- Comprueba que los puertos a publicar (por ejemplo 8080 para WordPress y 3306 para la base de datos, si se expone) están libres. Si alguno está ocupado, propón un alternativo y espera confirmación.
- Si el directorio ya contiene un docker-compose.yml, un .env o una instalación de WordPress, no sobrescribas nada. Pregunta cómo proceder.

## 3. Verificación de versiones

Consulta en wordpress.org la versión estable actual (si no se indicó otra) y los requisitos mínimos de PHP y MySQL/MariaDB de esa versión. No te fíes de la memoria. Anota la fuente en el informe.

## 4. Imagen de la aplicación con WP-CLI

La imagen oficial `wordpress` no incluye WP-CLI de forma garantizada, así que crea un Dockerfile propio basado en ella:

- Base: `wordpress:<versión>-php<X.Y>-apache`, con la versión fijada. Nunca `latest`. Verifica que el tag existe antes de usarlo.
- Instala WP-CLI descargándolo desde su fuente oficial (`https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar`) y verifica su funcionamiento con `wp --info`. Colócalo en `/usr/local/bin/wp`.
- Ejecuta el contenedor con un usuario coherente con los permisos de `wp-content`, de modo que WP-CLI y Apache puedan escribir en él.
- Añade `less` o las utilidades que necesite WP-CLI solo si hacen falta.

## 5. docker-compose.yml

- Servicio `[proyecto]_app` con el Dockerfile anterior, dependiente de `[proyecto]_db` con `condition: service_healthy`.
- Servicio `[proyecto]_db` con imagen oficial de MySQL o MariaDB fijada a una versión concreta, healthcheck y volumen nombrado para los datos.
- Volumen nombrado para `wp-content` (temas, plugins, uploads), para que persista y no quede atrapado en la imagen.
- Publica el puerto de WordPress enlazado a 127.0.0.1. No publiques la base de datos al host salvo que el usuario lo pida.
- Ninguna credencial escrita en el compose. Todo desde `.env`.

## 6. Variables y secretos

- Genera `.env` con contraseñas aleatorias (por ejemplo `openssl rand -base64 32`) para la base de datos y las claves de WordPress. Nunca valores de ejemplo.
- Genera `.env.example` con las mismas claves y valores vacíos. Este sí puede versionarse.
- Añade `.env` al `.gitignore`, junto con `wp-content/uploads/` si el proyecto no versiona medios.
- Configura WordPress mediante las variables de la imagen oficial (`WORDPRESS_DB_HOST`, `WORDPRESS_DB_USER`, `WORDPRESS_DB_PASSWORD`, `WORDPRESS_DB_NAME`). No edites `wp-config.php` a mano.
- No muestres las contraseñas en el chat. Indica dónde están y cómo consultarlas.

## 7. Arranque

1. `docker compose build`.
2. `docker compose up -d`.
3. Espera a que la base de datos esté healthy.
4. Comprueba con `curl` que la home responde 200 o redirige al asistente de instalación. Si hay 5xx, revisa `docker compose logs` y corrige antes de dar el entorno por bueno.
5. Verifica dentro del contenedor con `docker compose exec [proyecto]_app wp --info`.
6. No instales WordPress con datos de producción ni ejecutes `wp search-replace`, `wp db import` ni instaladores sin preguntar antes.

Si el usuario quiere instalación automática, puedes proponer `wp core install` con los datos que indique, pero solo tras confirmación.

## 8. Informe final

Presenta en prosa, con una lista corta solo para URLs y comandos:

- Proyecto creado: nombre normalizado, versión de WordPress y PHP, con la fuente consultada.
- Valores por defecto usados (versión, PHP, motor de base de datos).
- Contenedores y puertos publicados.
- Dónde están las credenciales (`.env`), sin mostrar valores.
- Comandos útiles: arrancar, parar, logs y uso de WP-CLI (`docker compose exec [proyecto]_app wp ...`).
- Pasos pendientes, por ejemplo completar la instalación o crear el primer plugin con `/nuevo-plugin-wp`.

Termina preguntando si quieres algo más antes de dar el entorno por cerrado.