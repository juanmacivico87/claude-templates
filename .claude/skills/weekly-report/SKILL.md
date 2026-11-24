---
name: weekly-report
description: Genera el informe de forma de trabajo con Claude Code. Analiza las transcripciones de todas las sesiones (de cualquier proyecto) de los últimos días y propone recomendaciones concretas para trabajar de forma más óptima. Úsala cuando el usuario pida su informe semanal, un informe de cómo trabaja, recomendaciones para mejorar su uso de Claude Code, o cuando el aviso de inicio de sesión indique que toca el informe del lunes.
---

# Informe semanal de forma de trabajo

Objetivo: observar cómo trabaja el usuario con Claude Code y darle recomendaciones accionables, priorizadas y apoyadas en evidencia de sus propias sesiones. Nada de consejos genéricos: cada recomendación debe citar algo que haya pasado de verdad.

## 1. Recoger datos

- Periodo: por defecto, desde el último informe (`~/.claude/reports/.last-report` guarda la fecha) o 7 días si no hay ninguno. Si el usuario indica otro periodo, úsalo.
- Ejecuta el extractor y guarda la salida en el scratchpad (no en el contexto entero de golpe si es grande):
  `python3 ~/.claude/tools/weekly-report/extract.py <days> > <scratchpad>/summary.json`
  (si no existe ahí, búscalo en `.claude/tools/weekly-report/extract.py` del proyecto actual)
- El JSON trae `totals`, `top_bash_programs` y, por sesión (`sessions`): `project`, `prompts` (recortados), `slash_commands`, `skills`, `tools`, `bash`, `mcp`, `tool_errors`, `permission_denials`, `compactions`, `turn_duration_min` (minutos de trabajo de Claude), `edited_files` (editados 3+ veces), `subagents`, `corrections` e `pasted_images`.
- Contexto de configuración que debes contrastar:
  - `~/.claude/settings.json` (permisos, hooks, plugins, modo) y los `.claude/settings*.json` de los proyectos activos.
  - `~/.claude/CLAUDE.md`, el CLAUDE.md de cada proyecto activo y lo que importe.
  - Skills (`~/.claude/skills/`) y comandos (`~/.claude/commands/`) existentes, y la memoria (`~/.claude/projects/*/memory/`).
  - El informe anterior en `~/.claude/reports/`, para hacer seguimiento.
- Si un dato no se entiende con el resumen, consulta la transcripción concreta con `grep` o `sed -n` acotados. No leas transcripciones enteras: algunas pesan cientos de MB.

## 2. Analizar

Busca patrones, no anécdotas. Áreas a revisar:

1. **Tareas repetidas**: prompts parecidos en varias sesiones o proyectos → candidatos a skill, comando slash, plantilla o script. Comprueba antes si ya existe uno que no se está usando.
2. **Calidad de los prompts**: peticiones ambiguas que acabaron en correcciones, falta de criterio de aceptación, contexto que el usuario repite en cada sesión y debería estar en CLAUDE.md o memoria.
3. **Correcciones y retrabajo**: mensajes de "no, eso no", archivos editados muchas veces, errores que se repiten. Identifica la causa raíz (falta de contexto, instrucción en CLAUDE.md desfasada, herramienta mal elegida).
4. **Gestión del contexto**: sesiones muy largas, compactaciones frecuentes, mezcla de temas en una misma sesión → `/clear`, sesiones separadas por tarea, subagentes para exploración, planes guardados en `~/.claude`.
5. **Permisos y fricción**: denegaciones y comandos frecuentes que podrían ir en la lista `allow` (solo lectura o claramente seguros), o reglas de auto mode que bloquean trabajo legítimo.
6. **Errores de herramientas recurrentes**: comandos que fallan siempre igual (rutas, versiones de node/nvm, timeouts) → documentarlos en el CLAUDE.md del proyecto o crear un script.
7. **Funcionalidades infrautilizadas** que encajarían con lo observado: modo plan, hooks, worktrees, `/schedule` o `/loop`, subagentes, skills existentes, `/code-review`, Monitor para procesos largos, elección de modelo y esfuerzo.
8. **Coste y tiempo**: dónde se va el tiempo de Claude (minutos de turno, subagentes) y si compensa.

Respeta las preferencias ya fijadas en `~/.claude/CLAUDE.md` y la memoria: no recomiendes lo contrario de algo que el usuario ya decidió, salvo que la evidencia diga que le perjudica, y entonces explícalo.

## 3. Redactar el informe

Escribe en español, directo y breve. Guárdalo en `~/.claude/reports/informe-AAAA-MM-DD.md` con esta estructura:

```
# Informe de trabajo con Claude Code — <periodo>

## Resumen en cifras
Tabla corta: sesiones, proyectos, prompts, horas de trabajo de Claude, compactaciones, errores, denegaciones, correcciones.

## Lo que ya funciona bien
2-4 puntos, con evidencia.

## Recomendaciones
Máximo 5-7, ordenadas por impacto/esfuerzo. Para cada una:
### N. <título>  ·  Impacto: alto/medio/bajo  ·  Esfuerzo: bajo/medio/alto
- **Qué he visto:** evidencia concreta (proyecto, fecha, cifra o prompt resumido).
- **Por qué importa:** coste actual en tiempo, tokens o retrabajo.
- **Qué hacer:** acción exacta (texto para CLAUDE.md, entrada de permisos, borrador de skill, hábito concreto).
- **Lo aplico yo:** sí/no, y qué cambiaría.

## Seguimiento del informe anterior
Qué recomendaciones se aplicaron, cuáles no y si se nota el efecto.
```

Reglas:
- No copies al informe credenciales, tokens, contraseñas ni datos personales que aparezcan en los prompts.
- No inventes datos: si algo no se puede medir con lo disponible, dilo.
- Si la semana tuvo poca actividad, haz un informe corto; no rellenes.

## 4. Cerrar

1. Escribe la fecha de hoy (AAAA-MM-DD) en `~/.claude/reports/.last-report`.
2. Muestra al usuario un resumen de 5-10 líneas con las recomendaciones principales y la ruta completa del informe.
3. Ofrece aplicar las recomendaciones que se puedan aplicar (CLAUDE.md, permisos, skills, hooks). No cambies nada sin su confirmación.
