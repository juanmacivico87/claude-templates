Vamos a crear la plantilla de un plugin de WordPress con estos parámetros recibidos como argumentos: $ARGUMENTS

Los argumentos se escriben como pares clave=valor. Claves admitidas:
- name: nombre legible del plugin, por ejemplo "Gestor de reservas".
- slug: identificador en minúsculas y con guiones, por ejemplo "gestor-reservas". Si no se indica, se genera a partir de nombre.
- namespace: namespace raíz PSR-4, por ejemplo "GestorReservas". Si no se indica, se genera a partir de nombre en PascalCase.
- author: nombre del autor. Si no se indica, deja un marcador [AUTOR] y repórtalo.
- php: versión mínima de PHP. Si no se indica, usa la mínima que exige la versión actual de WordPress, verificada en la documentación oficial.

Antes de crear nada, comprueba que tienes nombre. Si falta, pregúntalo y detente. Si el directorio de destino ya contiene un plugin con el mismo slug, no sobrescribas nada: pregunta cómo proceder.

## 1. Estructura de directorios

Crea esta estructura dentro de `wp-content/plugins/[slug]/` o en el directorio de trabajo indicado:

```
[slug]/
├── [slug].php              Archivo principal con cabecera del plugin
├── composer.json
├── package.json
├── readme.txt              Formato de WordPress.org
├── readme.md
├── uninstall.php
├── src/                    Código PHP, PSR-4 bajo el namespace raíz
│   ├── Plugin.php          Arranque: registra los servicios e integraciones
│   ├── Admin/              Pantallas y hooks del área de administración
│   ├── Frontend/           Hooks y shortcodes públicos
│   ├── Services/           Lógica de negocio, sin dependencias directas de WordPress cuando sea posible
│   └── Integrations/       Registro de hooks y filtros agrupados por responsabilidad
├── assets/
│   ├── src/                Código fuente de JS y CSS (lo gestiona npm)
│   │   ├── admin/
│   │   └── public/
│   └── dist/               Salida compilada (generada, no editar a mano)
├── templates/              Plantillas HTML parciales
├── languages/              Archivos de traducción
└── tests/
    ├── Unit/
    └── Integration/
```

No crees carpetas vacías sin contenido útil, salvo las que la estructura marca como destino de generación (`assets/dist/`, `vendor/`, `node_modules/`).

## 2. composer.json (backend)

- `"type": "wordpress-plugin"`.
- PHP en `require` con la versión mínima elegida.
- Autoload PSR-4 con el namespace raíz apuntando a `src/`.
- En `require-dev`: PHPUnit y, si procede, PHP_CodeSniffer con WordPress Coding Standards y PHPStan. Verifica las versiones compatibles con la versión de PHP elegida antes de fijarlas.
- Scripts útiles: test, lint y, si procede, analyse.
- Ejecuta `composer install` y comprueba que `vendor/autoload.php` se genera.

## 3. package.json (frontend)

- Dependencias de build (por ejemplo webpack, vite o @wordpress/scripts, según lo que se decida) en `devDependencies`. Si no se indica otra cosa, usa @wordpress/scripts.
- Scripts: build, start (desarrollo con watch) y lint.
- Destino de la compilación: `assets/dist/`.
- Ejecuta `npm install` y comprueba que el build inicial termina sin errores.
- Añade `node_modules/` al `.gitignore`, junto con `vendor/` y `assets/dist/` si el proyecto decide no versionar la salida compilada.

## 4. Archivo principal del plugin

- Cabecera completa: Plugin Name, Description, Version, Requires at least, Requires PHP, Author, Text Domain (igual que el slug), Domain Path (`/languages`) y License.
- Comprobación de acceso directo: salir si `ABSPATH` no está definido.
- Constantes con el prefijo elegido: ruta, URL y versión.
- Carga del autoloader de Composer.
- Arranque mediante `Plugin::init()` en el hook `plugins_loaded`, no directamente en el archivo principal.
- Hooks de activación y desactivación registrados con funciones que delegan en clases, no con lógica suelta.

## 5. Clases base

- `src/Plugin.php`: clase con método `init()` que instancia las integraciones y las registra. Recibe sus dependencias por constructor siempre que sea posible.
- Una clase por responsabilidad en `Integrations/`, con un método `register()` que añade los hooks.
- Ninguna clase de negocio llama directamente a funciones globales de WordPress si puede recibir esos datos como parámetros o mediante una interfaz.

## 6. Frontend

- En `assets/src/admin/` y `assets/src/public/` crea un punto de entrada JS y un CSS vacío con un comentario de cabecera.
- Encola los assets desde las clases de `Admin/` y `Frontend/` usando las rutas de `assets/dist/` y el número de versión del plugin como versión del recurso.
- No cargues scripts en todas las páginas: limita el encolado a la pantalla o contexto en el que se usan.

## 7. Calidad y seguridad mínima

- Todo el código PHP sigue PSR-4 y PSR-12. Nombres de clases en PascalCase, métodos en camelCase, en inglés.
- Escapa salidas con funciones de WordPress (`esc_html`, `esc_attr`, `esc_url`), sanea entradas (`sanitize_text_field`, etc.) y comprueba nonces y capacidades en cualquier acción de administración.
- `uninstall.php` solo elimina datos del plugin si el usuario lo ha configurado para ello, y nunca borra datos de otros plugins.
- Incluye `index.php` vacío en los directorios PHP para evitar listados de directorio.

## 8. Verificación

- Ejecuta `composer validate` y `composer dump-autoload`.
- Ejecuta el build de npm y comprueba que `assets/dist/` contiene los archivos esperados.
- Si WP-CLI y un entorno WordPress están disponibles, activa el plugin con `wp plugin activate [slug]` y revisa los logs en busca de errores. Si no lo están, indícalo.
- No instales el plugin en un sitio de producción ni ejecutes migraciones o acciones que modifiquen datos.

## 9. Informe final

Presenta en prosa, con una lista corta solo para rutas y comandos:

- Plugin creado: nombre, slug, namespace y versión mínima de PHP, con la fuente consultada para la versión de WordPress.
- Valores que se han generado por defecto (namespace, autor) para que el usuario los revise.
- Resultado de `composer install`, `npm install` y el build.
- Qué se ha verificado y qué no.
- Próximos pasos recomendados, por ejemplo definir la primera funcionalidad o configurar tests.

Termina preguntando si quieres que cree alguna funcionalidad concreta sobre esta base.