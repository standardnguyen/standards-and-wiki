# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

This is a personal wiki maintained as markdown files, serving as documentation for [YOUR DOMAIN HERE — e.g., a homelab, a business, a research project]. It is optionally synced to a wiki renderer (Wiki.js, MkDocs, Gollum, etc.). There is no build system, test suite, or application code.

<!-- Customize: describe your wiki's purpose, where it runs, and how it's accessed. -->

## Repository Structure

- `home.md` — Wiki homepage with section index and quick-reference table
- `infrastructure/` — [Rename or replace this section]
  - `overview.md` — Top-level overview page
- `projects/` — Active project documentation
- `ideas/` — Half-baked project ideas
- `meta/` — Wiki meta-documentation
  - `style-guide.md` — Writing conventions
  - `ai-managed-wiki.md` — How Claude Code maintains this wiki
  - `human-readability.md` — Criteria for documents that must remain executable without an LLM
- `protocols/` — Structured maintenance workflows (1-9)

<!-- Customize: update this to match your actual directory structure as it grows. -->

## Writing Conventions

- Pages use Wiki.js-style internal links: `/en/path/to/page`
- Tables are used for structured data (specs, inventories, configuration references)
- Architecture diagrams use ASCII art in fenced code blocks
- Shell commands are documented with step-by-step context explaining *why*, not just *what*
- Pages end with a "Related Pages" section linking to adjacent topics

## Workflow

- **Default branch: `dev`** — Work on the `dev` branch unless told otherwise. Simply commit to `dev` and push.
- If `dev` does not exist locally, create it from `main`: `git checkout -b dev origin/main`
- **Never rebase or bulk-stage without explicit user permission.** Concurrent sessions and background tools may modify the working tree, so `git rebase`, `git add .`, `git add -A`, and `git add -u` can silently bundle unrelated work into your commit. Always enumerate the exact paths you touched, run `git diff --cached --stat` before every commit to verify the file list is yours, and `git restore --staged <path>` on anything unfamiliar.
- When changes are ready for review, create or update a pull request from `dev` to `main`
- Never push directly to `main`; all changes go through PRs for human review

<!-- Customize: update the PR creation commands for your Git hosting platform.

GitHub example:
  gh pr create --base main --head dev --title "..." --body "..."

Forgejo/Gitea example:
  curl -s -X POST "https://your-gitea.example.com/api/v1/repos/OWNER/REPO/pulls" \
    -H "Content-Type: application/json" \
    -H "Authorization: token $TOKEN" \
    -d '{"title": "...", "body": "...", "head": "dev", "base": "main"}'
-->

## Sub-CLAUDE.md Files

Project subdirectories may have their own `CLAUDE.md` with rules that only apply inside that subtree. **These only auto-load when the working directory is inside the project dir** — if you're editing files under `projects/<project>/` from the repo root, the project's `CLAUDE.md` will NOT have been loaded.

Before making non-trivial edits inside a project subtree, run `ls <path>/CLAUDE.md` (and walk up the path checking parent dirs) and `Read` any that exist.

<!-- Customize: as projects accumulate sub-CLAUDE.md files, list them here so a session
     starting at the repo root knows which ones to skim before working in those areas. -->

## Protocols

Protocols are stored in `protocols/` as individual files. When a protocol is invoked (e.g., "run Protocol 2"), read the corresponding file before executing.

| Protocol | Description | File |
|----------|-------------|------|
| 1 | Full harmonization pass — fix contradictions, anachronisms, tone | `protocols/1-harmonize.md` |
| 2 | Random-sample spot-check for contradictions across file pairs | `protocols/2-spot-check.md` |
| 3 | Verify — generate commands to check ground truth before accepting fixes | `protocols/3-verify.md` |
| 4 | Recursive harmonize — apply Protocol 1 to recent changes, repeat until convergence | `protocols/4-recursive-harmonize.md` |
| 5 | Session log setup — create session logging infrastructure for a new project | `protocols/5-session-log-setup.md` |
| 6 | Homepage coverage — check that every wiki page is reachable from `home.md` | `protocols/6-homepage-coverage.md` |
| 7 | Commit & ship — commit, push, create/update PR, then update session logs if applicable | `protocols/7-commit-and-ship.md` |
| 8 | Design project sub-protocols — codify recurring patterns inside a project as project-scoped sub-protocols | `protocols/8-design-project-subprotocols.md` |
| 9 | Human-readability audit — validate that protocols and reference pages are executable without an LLM in the loop | `protocols/9-human-readability-audit.md` |
| 10 | Codify drift check — promote a recurring drift pattern into a permanent structural check at commit time | `protocols/10-codify-drift-check.md` |

<!-- Customize: add your own protocols as you develop repeatable workflows. -->

**Root protocols vs. sub-protocols.** The numbered protocols above are root-level — they apply across the whole wiki. Individual sub-projects may define their own **sub-protocols** in their project-local `CLAUDE.md` (or in a `subprotocols/` directory), numbered independently within the project namespace. A sub-project's "Sub-Protocol 0" is unrelated to root Protocol 0. If a project defines sub-protocols, label them "Sub-Protocol N" rather than "Protocol N" to avoid collision with the root numbering. See Protocol 8 for how to design and register them.

## Session Logging

Session logs prevent **wiki drift** — the gap between what was decided in conversation and what the wiki files actually say. They're optional but recommended for any project that involves ongoing decisions across multiple Claude Code sessions.

To set up session logging for a new project, run Protocol 5.

The pattern:
- Each project with logging gets a `session-log.md` index and a `logs/` directory
- Each session gets its own file: `YYYY-MM-DD-<slug>.md`
- At the **start** of a session, read the most recent 1-2 log files to catch up
- At the **end** of a session, create a new log recording decisions, actions, and next steps

<!-- Customize: as you add projects with session logging, add a section for each one here.
Follow this pattern:

## Session Logging (Project Name)

Any session that involves [trigger conditions] **must** create a log file in `path/to/logs/` before ending.

**File naming:** `YYYY-MM-DD-<slug>.md`. Multiple sessions on the same day get letter suffixes.

Each log file records:
- Date and session context
- Decisions made or actions taken
- Which wiki files were updated
- Open items and next steps

After creating the log file, **add a row to the index table** in `path/to/session-log.md`.

At the **start** of any related session, read `path/to/session-log.md` to find the **most recent 1-2 log files**, then read those.
-->

## Key Domain Context

<!-- Customize: add facts about your domain that Claude Code needs to know to write
accurate documentation. Examples:

- All servers run Debian 12 with Docker Compose
- The network uses VLANs: 10 (trusted), 20 (IoT), 30 (guest)
- Storage is tiered: SSD for databases, HDD for bulk data, NAS for backups
- Public traffic routes through a reverse proxy on server X
-->

## Python

Always use virtual environments (`python3 -m venv`) for Python projects. Never `pip install` system-wide or use `--break-system-packages`.

## Doing Tasks

Coding-behavior rules. These are also encoded in the Claude Code harness system prompt, but pinned here as durable insurance against harness drift.

**0. Gather context before acting.** Synthetic RAG is a real cost-saver. Err toward *more* context-gathering than less, especially on anything non-trivial.

- Before non-trivial work, identify the project/domain and check for a sub-`CLAUDE.md` — read it, even if CWD wouldn't auto-load it. Walk up the directory tree if unsure.
- **Re-read protocols on invocation.** When you're about to execute any numbered protocol, read `protocols/<N>-*.md` from disk in the same response — even if you've executed it before. Protocols change; cached mental models drift. The failure mode this rule prevents: an agent executes a protocol from memory, the file has been edited, and the run ships against the stale procedure.
- **Grep first, even when you're sure.** For any proper noun the user mentions that you don't already have loaded context for — service names, paths, container names, project names, tool names — grep the wiki *before* deciding what it refers to. Do **not** pre-judge ambiguity; the failure mode is exactly the case where you confidently assumed the wrong noun class. **The wiki is your infinite context.** The cost of one extra grep is ~30s; the cost of acting on a wrong assumption is ~5min plus a wrong-tree investigation the user then has to redirect.
- **For incident-shape prompts, wiki first, live-state second.** When the user says something is failing, filling up, erroring, broken, slow, or not working — grep the wiki for the relevant `_index.md` / runbook / session-log entries *before* spinning up live-state probes. The wiki captures procedures, lessons-learned, and prior-incident write-ups that you do not have internally. The LLM bias toward "tools = visible progress, docs = invisible" is real; counter it explicitly.
- Skim the 1-2 most recent relevant session log entries before doing project work.
- If the task is *broad* or spans multiple areas (3+ likely queries), spawn an Explore subagent rather than serially grepping yourself.
- Bias: *"I'd rather spend 30 seconds on a grep than 5 minutes acting on a bad assumption."*
- Trivial-task gate: skip the preflight for clearly-scoped one-shots ("rename this variable", "what's in this file"). The preflight is for work whose scope touches the wider knowledge graph.

**1. Think before coding.** Don't assume. Don't hide confusion. Surface tradeoffs.

- State your assumptions explicitly. If uncertain, ask.
- If multiple reasonable interpretations exist, present them — don't silently pick one. The cost of one clarifying question is lower than the cost of building the wrong thing.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

**2. Simplicity first.** Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked. No abstractions for single-use code. No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios. Trust internal code and framework guarantees; only validate at system boundaries.
- If you write 200 lines and it could be 50, rewrite it.

**3. Surgical changes — but propagate completely.** Touch only what you must, but follow every change to its edges.

- Don't "improve" adjacent code, comments, or formatting in passing.
- Don't refactor things that aren't broken.
- Match the existing style even if you'd write it differently.
- Every changed line should trace directly to what was asked.
- When your edits orphan an import/variable/function, clean those up — but don't sweep pre-existing dead code unless asked.
- **Propagation rule:** When you change a fact (a count, an address, a status, a name, a date, a price), `grep -rn "<old value>"` across the wiki before committing and update every page that carries the stale value. On a large wiki the same fact often appears in many places; changing one page and leaving the others is the single largest source of wiki drift. If the grep turns up pages you're unsure about, list them for the user rather than skipping silently.
- **Homeless information rule:** When a session produces a new fact or reference that should be in the wiki but has no obvious page to live on, **do not silently drop it.** Search for candidate pages (`grep -ri` for related terms), and either add it to the best-fit existing page or create a new one. If genuinely unsure where it belongs, surface it to the user: *"I learned X but there's no wiki page for it — should I add it to Y, create a new page, or note it in the session log?"* The failure mode: the agent discovers a fact, notes it internally, and moves on without persisting it anywhere — the next session has no way to know.

**4. Goal-driven execution.** Define success criteria. Loop until verified.

Transform tasks into verifiable goals: "Add validation" → "Write tests for invalid inputs, then make them pass." "Fix the bug" → "Write a test that reproduces it, then make it pass." For multi-step tasks, state a brief plan with per-step verification before executing.

Strong success criteria let Claude loop independently. Weak criteria ("make it work") force constant clarification.
