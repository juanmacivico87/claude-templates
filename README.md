# Claude Code templates

Personal collection of [Claude Code](https://claude.com/claude-code) configuration: slash commands, skills, hooks, permissions and helper scripts used for day-to-day web development, mainly WordPress and Drupal projects running in Docker.

> **Note:** the prompts in commands and skills are written in Spanish, because Claude is instructed to talk to the user in Spanish. Generated code, comments and commit messages are always in English.

## Contents

```
.claude/
├── CLAUDE.md                     Global preferences (language, sessions, file persistence)
├── settings.json                 Permissions and the SessionStart hook
├── commands/                     Slash commands
├── skills/                       Skills Claude loads automatically when relevant
└── tools/weekly-report/          Scripts used by the weekly-report skill and its hook
```

### Slash commands

Commands take their arguments as `key=value` pairs.

| Command | Purpose |
|---|---|
| `/create-project` | Dockerized development environment for a new project with any framework (`framework`, `name`, `version`, `db`). |
| `/create-wp-project` | Dockerized WordPress site with WP-CLI (`name`, `version`, `php`, `db`). |
| `/create-drupal-file` | Dockerized Drupal site with Drush (`name`, `version`, `php`, `db`). |
| `/create-wp-plugin` | WordPress plugin skeleton with PSR-4, Composer, npm build and tests (`name`, `slug`, `namespace`, `author`, `php`). |
| `/create-drupal-module` | Drupal custom module skeleton with services, routing, config schema and tests (`name`, `machine_name`, `namespace`, `core`, `php`, `author`). |
| `/create-claude-file` | Explores the repository and creates or updates its `CLAUDE.md`, including the development standards to follow. |
| `/planning-task` | Before starting a task: checks links with Playwright (GET only), reviews plugin/module conflicts, and proposes a plan without changing anything. |

The environment commands share the same safeguards: versions are checked against the official sites instead of memory, images are pinned (never `latest`), ports are bound to `127.0.0.1`, credentials are generated randomly into `.env` (never into `docker-compose.yml` or the chat), and existing files are never overwritten without asking.

### Skills

| Skill | When it is used |
|---|---|
| `choose-test-browser` | Before any browser test: decides between the user's Chrome (Chrome DevTools MCP) and a Playwright script, and how to run it with few tokens. Playwright by default; Chrome only for exploration, visual checks or one-off checks. |
| `review-claude-file` | When starting a session in a repo with a `CLAUDE.md`, or after changes to build, dependencies or structure: detects outdated statements and proposes up to five fixes, applied only after confirmation. |
| `weekly-report` | Analyzes the transcripts of all Claude Code sessions of the last days and writes a report with concrete, evidence-based recommendations to work better. |

### Weekly report

- `tools/weekly-report/extract.py [days]` summarizes the transcripts in `~/.claude/projects/` into a compact JSON (prompts, tools, Bash programs, errors, permission denials, compactions, corrections, subagents...).
- `tools/weekly-report/notify.sh` runs as a `SessionStart` hook. Once a day, if this week's report (Monday) has not been generated yet, it tells Claude to mention it or generate it.
- Reports are saved to `~/.claude/reports/`, and `~/.claude/reports/.last-report` stores the date of the last one.

### Permissions

`settings.json` allows read-only commands (`git status`, `git diff`, `git log`, `ls`, `cat`...), asks before destructive or installing commands (`rm`, `git checkout`, `npm install`, `composer install`, reading `.env`), and denies anything that changes history or the remote (`git commit`, `git push`, `git pull`, `git merge`, `git rebase`, `git reset --hard`...).

## Installation

The files are meant to live in your user-level Claude Code directory, `~/.claude`, so they are available in every project.

```bash
git clone https://github.com/juanmacivico87/claude-templates.git
cd claude-templates

mkdir -p ~/.claude
cp -r .claude/commands .claude/skills .claude/tools ~/.claude/
cp .claude/CLAUDE.md ~/.claude/CLAUDE.md
chmod +x ~/.claude/tools/weekly-report/*.sh ~/.claude/tools/weekly-report/*.py
```

`settings.json` is not copied blindly, because `~/.claude/settings.json` usually holds other settings: merge its `permissions` and `hooks` sections into your own file.

The hook path (`~/.claude/tools/weekly-report/notify.sh`) assumes the tools are installed in `~/.claude/tools`. If you only want the configuration for one project, you can copy the `.claude/` folder into that project instead, but then the hook path and the `weekly-report` skill paths must be adjusted.

### Requirements

- Claude Code.
- Bash, GNU `date` and Python 3 for the weekly report.
- Docker and Docker Compose for the environment commands.
- Node.js for Playwright, and optionally the Chrome DevTools MCP server, for browser tests.

## Usage examples

```
/create-wp-project name="My website" php=8.3
/create-wp-plugin name="Booking manager" author="Jane Doe"
/create-drupal-module name="Booking manager" core=11
/planning-task Update the theme header and fix the mobile menu
```

Skills don't need to be invoked: Claude loads them when the task matches their description. You can also ask for them directly, for example "generate my weekly report".
