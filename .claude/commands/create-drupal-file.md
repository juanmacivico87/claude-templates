Vamos a crear un entorno de desarrollo dockerizado para un sitio Drupal con estos parámetros recibidos como argumentos: $ARGUMENTS

Los argumentos se escriben como pares clave=valor. Claves admitidas:
- name: nombre del proyecto en lenguaje natural, por ejemplo "mi sitio web". Obligatorio.
- version: versión de Drupal, por ejemplo 11. Si no se indica, usa la última versión estable publicada en drupal.org.
- php: versión de PHP. Si no se indica, usa la mínima que exige la versión de Drupal elegida, verificada en drupal.org, y repórtalo.
- db: mariadb, mysql o postgresql. Si no se indica, usa mariadb y repórtalo. Otros motores no son compatibles: explícalo y detente.

Antes de crear nada, comprueba que tienes name. Si falta, pregúntalo y detente.

## 1. Normalización del nombre

Convierte el nombre a minúsculas, elimina acentos, sustituye espacios y guiones por guiones bajos y quita cualquier otro carácter no alfanumérico. Por ejemplo, "Mi Sitio Web" pasa a `mi_sitio_web`. Los contenedores se llamarán `[proyecto]_app`, `[proyecto]_db` y, si procede, `[proyecto]_adminer`. Usa el mismo prefijo para la red y los volúmenes.

## 2. Comprobaciones previas

- Verifica que Docker y Docker Compose están instalados y en ejecución. Si no lo están, indícalo y detente.
- Comprueba que los puertos a publicar están libres. Si alguno está ocupado, propón uno alternativo y espera confirmación.
- Si el directorio ya contiene un docker-compose.yml, un .env o una instalación de Drupal, no sobrescribas nada. Pregunta cómo proceder.

## 3. Verificación de versiones

Consulta en drupal.org la versión estable actual (si no se indicó otra), la versión de PHP que exige y los motores de base de datos soportados. No te fíes de la memoria. Anota la fuente en el informe.

## 4. Imagen de la aplicación con Drush

Drupal no incluye Drush en la imagen oficial de Apache, así que crea un Dockerfile propio:

- Base: `php:<X.Y>-apache` con la versión de PHP fijada. Nunca `latest`. Verifica que el tag existe.
- Instala las extensiones PHP que exige Drupal para esa versión (por ejemplo gd, pdo_mysql o pdo_pgsql, opcache, zip) según el motor elegido, leyendo los requisitos oficiales.
- Instala Composer desde la imagen oficial de Composer o su instalador verificado.
- Habilita `mod_rewrite` y configura el `DocumentRoot` en `web/`.
- Instala Drupal con `composer create-project drupal/recommended-project:<versión>` dentro del directorio de trabajo, si el proyecto aún no existe, y luego `composer require drush/drush` dentro del proyecto. Verifica con `drush --version`.
- Usa un usuario coherente con los permisos de `web/sites/default/files`, que debe ser escribible.

## 5. docker-compose.yml

- Servicio `[proyecto]_app` con el Dockerfile anterior, dependiente de `[proyecto]_db` con `condition: service_healthy`.
- Servicio `[proyecto]_db` con imagen oficial del motor elegido, fijada a una versión concreta, healthcheck y volumen nombrado.
- Volumen nombrado para `web/sites/default/files`, para que los archivos subidos persistan.
- Publica el puerto de la aplicación enlazado a 127.0.0.1. No publiques la base de datos al host salvo que el usuario lo pida.
- Si se pide un cliente web para la base de datos, añade Adminer con imagen fijada, enlazado también a 127.0.0.1.
- Ninguna credencial escrita en el compose. Todo desde `.env`.

## 6. Variables y secretos

- Genera `.env` con contraseñas aleatorias (por ejemplo `openssl rand -base64 32`) para la base de datos y el hash salt de Drupal. Nunca valores de ejemplo.
- Genera `.env.example` con las mismas claves y valores vacíos. Este sí puede versionarse.
- Añade `.env` al `.gitignore`, junto con `web/sites/default/files/` y `web/sites/default/settings.local.php` si contienen datos locales.
- Configura la conexión mediante variables de entorno leídas desde `settings.php`, o mediante un `settings.local.php` que las lea. No escribas credenciales en `settings.php` ni modifiques archivos de núcleo.
- Asegura que `settings.php` no sea escribible tras la instalación, según la guía oficial de Drupal.
- No muestres las contraseñas en el chat. Indica dónde están y cómo consultarlas.

## 7. Arranque

1. `docker compose build`.
2. `docker compose up -d`.
3. Espera a que la base de datos esté healthy.
4. Comprueba con `curl` que la aplicación responde 200 o redirige al instalador. Si hay 5xx, revisa `docker compose logs` y corrige antes de dar el entorno por bueno.
5. Verifica dentro del contenedor con `docker compose exec [proyecto]_app drush status`.
6. No ejecutes `drush site:install` sobre datos existentes, `drush sql:drop`, importaciones de base de datos ni `drush updatedb` sin preguntar antes.

Si el usuario quiere instalación automática, puedes proponer `drush site:install` con los datos que indique, solo tras confirmación.

## 8. Informe final

Presenta en prosa, con una lista corta solo para URLs y comandos:

- Proyecto creado: nombre normalizado, versión de Drupal y PHP, con la fuente consultada.
- Valores por defecto usados (versión, PHP, motor de base de datos).
- Contenedores y puertos publicados.
- Dónde están las credenciales (`.env`), sin mostrar valores.
- Comandos útiles: arrancar, parar, logs y uso de Drush (`docker compose exec [proyecto]_app drush ...`).
- Pasos pendientes, por ejemplo completar la instalación o crear el primer módulo con `/nuevo-modulo-drupal`.

Termina preguntando si quieres algo más antes de dar el entorno por cerrado.