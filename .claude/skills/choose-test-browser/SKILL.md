---
name: choose-test-browser
description: Decide si una prueba en navegador se hace en el Chrome del usuario (MCP de Chrome DevTools conectado a su navegador, p. ej. Chrome de Windows) o con un script de Playwright, y cómo hacerla gastando pocos tokens. Úsala siempre antes de probar, verificar o explorar una aplicación web en un navegador, en cualquier proyecto, salvo que el usuario haya indicado ya la herramienta para esa prueba.
---

# Elegir navegador para pruebas: Chrome del usuario o Playwright

Decisión tomada por el usuario a partir de una comparativa real (8 pruebas hechas en paralelo con las dos herramientas el 23/11/2026). Si el usuario pide expresamente una herramienta, manda su petición.

## Regla

- **Por defecto, Playwright.** Baterías de pruebas, regresiones tras una corrección, pruebas que se repiten entre rondas y cualquier prueba con más de 3-4 pasos.
- **Chrome del usuario (MCP)** solo cuando:
  - Hay que explorar algo desconocido: comportamiento que no se entiende, localizar selectores, métodos o el flujo real de una pantalla.
  - El usuario quiere verlo en su navegador o validar diseño a ojo.
  - Es una comprobación puntual de 1-3 pasos que no se va a repetir.
- **No hacer la misma prueba en las dos herramientas** salvo que el usuario lo pida: los resultados coincidieron en 8 de 8 casos y duplica el gasto.
- Flujo típico: explorar en Chrome lo justo y pasar a Playwright en cuanto se sabe qué comprobar.

## Por qué (datos de la comparativa)

| Indicador (8 pruebas) | Chrome (MCP) | Playwright |
|---|---|---|
| Llamadas a herramientas | ~163 | 13 ejecuciones (8 sin fallos de entorno) |
| Salida devuelta | ~40 KB + 4 capturas | ~17 KB, sin capturas |
| Resultados iguales | 8/8 | 8/8 |
| Errores nuevos descubiertos | 3 | 0 (repetía lo ya explorado) |

El coste en tokens lo marca sobre todo el **número de llamadas** (cada una vuelve a procesar todo el contexto) y las capturas o snapshots. El texto corto devuelto por un script es barato. Playwright gasta unas 10-12 veces menos llamadas; Chrome es mejor para descubrir problemas porque permite ir paso a paso.

## Cómo hacerlo con Playwright

- Un script por batería que haga todos los pasos y **imprima solo un JSON corto de resultados** (ok/fallo por comprobación y el dato mínimo para entenderlo). Sin capturas salvo que hagan falta.
- Lógica de la prueba en ficheros JS comunes que se puedan cargar tanto con `page.evaluate` como con `evaluate_script` del MCP, para cambiar de herramienta sin reescribir.
- Evitar los fallos de entorno que obligaron a repetir ejecuciones:
  - Fijar el viewport al tamaño del navegador del usuario.
  - No localizar elementos por posición en pantalla; usar selectores, textos o iconos.
  - Contemplar menús plegados, pestañas restauradas o diálogos abiertos tras recargar.
  - Esperas explícitas a selectores en vez de tiempos fijos.
- Preparación (`npm install`, arrancar el navegador) una vez por sesión.
- Guardar los scripts reutilizables donde sobrevivan (ver las reglas de persistencia del CLAUDE.md global), no solo en el scratchpad.

## Cómo hacerlo con Chrome del usuario (MCP)

- Usar `evaluate_script` que devuelva JSON corto; **evitar `take_snapshot` y `take_screenshot`** salvo que haga falta ver el diseño.
- Agrupar varios pasos en un solo `evaluate_script` cuando sea posible, en vez de una llamada por clic.
- No encadenar llamadas que dependen de un paso que puede fallar: comprobar el resultado antes de seguir.
- Si el MCP solo lee scripts de una carpeta concreta (p. ej. el scratchpad), copiarlos allí antes.
- Usar `type_text` cuando un campo no reacciona a cambios de valor programáticos (validaciones que dependen de eventos de teclado).
