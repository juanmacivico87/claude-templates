Vamos a crear la plantilla de un módulo custom de Drupal con estos parámetros recibidos como argumentos: $ARGUMENTS

Los argumentos se escriben como pares clave=valor. Claves admitidas:
- name: nombre legible del módulo, por ejemplo "Gestor de reservas".
- machine_name: identificador en minúsculas y con guiones bajos, por ejemplo "gestor_reservas". Si no se indica, se genera a partir de name. Debe ser único en el proyecto.
- namespace: namespace PSR-4 bajo Drupal\ , por ejemplo "GestorReservas". Si no se indica, se genera a partir de nombre en PascalCase.
- core: versión de Drupal objetivo, por ejemplo "11". Si no se indica, usa la versión estable actual, verificada en drupal.org.
- php: versión mínima de PHP. Si no se indica, usa la mínima que exige la versión de Drupal elegida, verificada en la documentación oficial.
- author: nombre del autor. Si no se indica, deja un marcador [AUTOR] y repórtalo.

Antes de crear nada, comprueba que tienes name. Si falta, pregúntalo y detente. Si ya existe un módulo con el mismo machine_name, no sobrescribas nada: pregunta cómo proceder. Comprueba también que `machine_name` no coincide con un módulo de núcleo o contrib instalado.

## 1. Estructura de directorios

Crea esta estructura dentro de `web/modules/custom/[machine_name]/` o en la ruta de módulos custom del proyecto:

```
[machine_name]/
├── [machine_name].info.yml     Metadatos del módulo y dependencias
├── [machine_name].module       Solo hooks procedimentales imprescindibles
├── [machine_name].install      Instalación, actualizaciones y desinstalación
├── [machine_name].services.yml Definición de servicios
├── [machine_name].routing.yml  Rutas
├── [machine_name].permissions.yml
├── [machine_name].links.menu.yml
├── [machine_name].links.task.yml (si procede)
├── composer.json
├── package.json
├── config/
│   ├── install/                Configuración por defecto al instalar
│   └── schema/                 Esquemas de configuración
├── src/
│   ├── Controller/             Controladores de rutas
│   ├── Form/                   Formularios de configuración y de entidad
│   ├── Service/                Lógica de negocio, sin dependencias directas de Drupal cuando sea posible
│   ├── EventSubscriber/        Suscriptores a eventos del núcleo
│   ├── Plugin/                 Bloques, campos, formateadores y demás plugins
│   └── Hook/                   Hooks orientados a objetos (Drupal 10+)
├── templates/                  Plantillas Twig
├── assets/
│   ├── src/                    Código fuente de JS y CSS (gestionado con npm)
│   └── dist/                   Salida compilada (generada, no editar a mano)
├── tests/
│   ├── src/Unit/
│   └── src/Kernel/
└── README.md
```

No crees carpetas vacías salvo las que la estructura marca como destino de generación (`assets/dist/`, `vendor/`, `node_modules/`).

## 2. [machine_name].info.yml

- `name`, `type: module`, `description`, `package: Custom` y `core_version_requirement` con la versión elegida (por ejemplo `^11`).
- `dependencies` solo con los módulos que el código usa de verdad. Verifica que existen en la versión de Drupal indicada.
- Ninguna dependencia innecesaria.

## 3. composer.json (backend)

- `"type": "drupal-custom-module"`.
- PHP en `require` con la versión mínima elegida.
- Autoload PSR-4: `"Drupal\\[namespace]\\": "src/"` y el espacio de pruebas correspondiente.
- En `require-dev`: PHPUnit y PHP_CodeSniffer con Drupal Coding Standards (`drupal/coder`), y PHPStan con `phpstan-drupal` si el proyecto lo usa. Verifica que las versiones son compatibles con la versión de Drupal y PHP elegidas.
- Scripts útiles: test, lint y, si procede, analyse.
- Ejecuta `composer validate` y comprueba que el autoload se regenera sin errores.
- Si el módulo se instala dentro de un proyecto Drupal gestionado con Composer, no añadas dependencias de núcleo aquí. Esas van en el `composer.json` raíz del proyecto.

## 4. package.json (frontend)

- Dependencias de build (por ejemplo webpack, vite o las herramientas que decida el usuario) en `devDependencies`. Si no se indica, usa un bundler sencillo, como vite.
- Scripts: build, watch y lint.
- Salida en `assets/dist/`, con rutas que puedan referenciarse desde `*.libraries.yml`.
- Ejecuta `npm install` y comprueba que el build inicial termina sin errores.
- Añade `node_modules/` y `vendor/` al `.gitignore`. Decide con el usuario si `assets/dist/` se versiona.

## 5. Archivos YAML de registro

- `services.yml`: un servicio de ejemplo con sus argumentos inyectados por constructor, sin usar `\Drupal::service()` en el código nuevo.
- `routing.yml`: una ruta de ejemplo con `_controller` o `_form` y `_permission`, nunca sin control de acceso.
- `permissions.yml`: al menos un permiso específico del módulo.
- `links.menu.yml` y `links.task.yml`: solo si hay rutas que deban aparecer en menús.
- `libraries.yml`: si hay assets, una librería que apunte a `assets/dist/`.

## 6. Código PHP

- Todas las clases en `src/` siguen PSR-4 y PSR-12, con nombres en inglés y en PascalCase.
- Los controladores y formularios reciben sus dependencias mediante `create()` o inyección por constructor, siguiendo el patrón de Drupal.
- La lógica de negocio va en `Service/`, sin acceder directamente al contenedor global.
- No añadas lógica en el archivo `.module` salvo que el hook solo pueda implementarse ahí. En Drupal 10 o superior, usa hooks orientados a objetos en `Hook/` cuando sea posible.
- Los textos visibles se traducen con `$this->t()` o `TranslatableMarkup`, nunca concatenando cadenas.
- Escapa en las plantillas Twig (escape automático) y no uses `|raw` sin justificarlo.

## 7. Configuración

- `config/install/` queda vacío salvo que el módulo necesite configuración por defecto. Si la necesita, crea los YAML correspondientes con su esquema en `config/schema/`.
- Si el módulo define entidades de configuración, crea también sus esquemas.

## 8. Instalación y desinstalación

- `[machine_name].install` contiene solo `hook_install`, `hook_uninstall` y hooks de actualización si son necesarios, con `hook_update_N` numerados correctamente.
- `hook_uninstall` limpia la configuración y datos propios del módulo, nunca datos de otros módulos.

## 9. Calidad y seguridad mínima

- Comprueba permisos en cada ruta y en cada acción de formulario.
- Valida y sanea entradas mediante la API de formularios de Drupal.
- Nunca concatenes SQL. Usa la API de base de datos (`Connection`) con placeholders.
- Incluye al menos un test unitario en `tests/src/Unit/` para el servicio de ejemplo.

## 10. Verificación

- Ejecuta `composer validate`, `npm run build` y, si Drush está disponible, `drush pm:enable [machine_name] -y` seguido de `drush cr` y `drush watchdog:show --severity=Error --count=20`.
- Si Drush o un entorno Drupal no están disponibles, indícalo y no des la verificación por completa.
- No actives el módulo en producción ni ejecutes `hook_update_N` sobre datos reales sin preguntar antes.

## 11. Informe final

Presenta en prosa, con una lista corta solo para rutas y comandos:

- Módulo creado: nombre, machine_name, namespace, versión de Drupal y PHP elegidas, con la fuente consultada.
- Valores generados por defecto (namespace, autor) para que el usuario los revise.
- Resultado de Composer, npm y, si fue posible, de la activación con Drush.
- Qué se ha verificado y qué no.
- Próximos pasos recomendados, por ejemplo definir la primera ruta o el primer bloque.

Termina preguntando si quieres que añada alguna funcionalidad concreta sobre esta base.