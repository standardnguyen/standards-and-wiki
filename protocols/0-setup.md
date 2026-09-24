# Protocol 0: Setup

Guided first-run onboarding. This protocol is written to be **executed by your AI agent, with you in the passenger seat** — you answer questions, the agent does the file editing. If you were told "point your agent at this repo," this is the thing to point it at.

## Trigger

- "Run Protocol 0" / "protocol 0" / "set this up for me"
- An agent noticing this repo is still in template state (placeholder text in `CLAUDE.md` or `home.md`) should *offer* to run it.

## For the human

You need exactly three things before starting:

1. **An AI coding agent with file access**, running in a terminal in this repo's directory. Claude Code is the reference target (`cd` into the repo, run `claude`), but any agent that can read/write files and run shell commands works.
2. **This repo, cloned or forked** — under whatever name you want your wiki to have.
3. **Ten minutes.** The agent asks questions; you answer in plain sentences. There are no wrong answers — everything is editable later.

Then say: **"run protocol 0"**.

And a standing offer, from the template's author: **if you ever get confused, at this step or any other, just say "can you hold my hand through this bb" and the agent will say yes** — it switches to one-small-step-at-a-time mode, explains everything it's doing, and checks in before each change. (This is a real instruction the agent follows — it's in `CLAUDE.md` — not a decorative promise.)

## For the agent — the procedure

Work conversationally. Ask ONE question at a time, wait for the answer, act on it, show what changed. Never dump the whole interview at once, and never fill in an answer the human didn't give — a wrong guess in `CLAUDE.md` gets loaded into every future session.

### 1. Confirm the ground

- Verify you're in a git repo with this template's shape: `CLAUDE.md`, `home.md`, `protocols/`, `meta/style-guide.md` all exist. If not, stop and say what's missing.
- Check git state: `git status`, current branch, whether a remote exists. Report it in one plain sentence ("fresh clone of the template, no changes, remote points at your fork").
- If your harness reads `AGENTS.md` instead of `CLAUDE.md`, create the symlink now: `ln -s CLAUDE.md AGENTS.md`.

### 2. Interview — what is this wiki?

Ask, one at a time, in the human's own vocabulary (no jargon):

1. **"What do you want this wiki to hold?"** (home lab docs? projects? recipes? everything?) → becomes the "What This Is" section of `CLAUDE.md` and the framing of `home.md`.
2. **"Is anyone else ever going to read it, or is it just for you?"** → sets the privacy posture in `CLAUDE.md` ("this repo is private, write freely" vs. "may be shared — keep personal detail out").
3. **"Where does the repo live?"** (GitHub? self-hosted Gitea/Forgejo? nowhere yet?) → customizes the Workflow section: branch convention, PR-vs-direct-push, and — if "nowhere yet" — offer to help create a remote, or note that local-only is fine to start.
4. **"Any facts your agent should always know?"** (server names, household context, project names — whatever the human would be annoyed to re-explain every session) → seeds "Key Domain Context". If the answer is "I don't know yet," leave the section's placeholder comment in place; it fills naturally.

### 3. Apply the answers

- Edit `CLAUDE.md`: replace every `<!-- Customize: ... -->` placeholder the interview answered. Leave the ones it didn't — visible placeholders are honest; silently-invented content is not.
- Edit `home.md`: real title, one-line purpose, and section stubs matching what the human said in question 1. Delete example sections that don't apply.
- Show the human a short diff summary after each file, not a wall of text.

### 4. First real page

Ask: **"Tell me one thing you'd want documented — just talk, I'll write the page."** Take whatever they say (their backup setup, a project, their sourdough starter), write it as a proper page per `meta/style-guide.md`, link it from `home.md`, and show them. This step matters more than it looks: it converts the template from "empty scaffolding" to "my wiki" in one move, and it teaches the human that talking is the input format.

### 5. Optional power-ups (offer, don't push)

- **Synthetic-RAG hook** — "want the wiki to auto-surface relevant pages on every prompt?" If yes: wire `.claude/hooks/wiki-rag.py` per `.claude/settings.json.example`, run one test prompt, show the pointer lines. If no or confused: skip; it's off by default on purpose. (Maintained later via Protocol 11.)
- **Session logging** — briefly explain the pattern (append-only decision logs that keep future sessions honest — see `meta/mining-session-logs.md` for why this pays off), and offer to run Protocol 5 the first time a real project shows up. Not required today.

### 6. First commit + tour

- Commit what was set up (per the Workflow section just customized), with the human's okay.
- Close with a three-line tour, not a lecture:
  - *"To add anything: just tell me about it in plain words."*
  - *"To keep it healthy: say 'protocol 4' after big changes, 'protocol 2' once in a while."*
  - *"To ship: say 'protocol 7'."*
- Remind them of the hold-my-hand phrase one last time.

## Failure modes to avoid (agent, read these)

- **Do not run the whole interview as one giant message.** One question, one answer, one action.
- **Do not invent domain facts.** An unfilled placeholder beats a plausible fabrication — this file is loaded into every future session, so a guess here compounds forever.
- **Do not wire the RAG hook without asking.** It modifies the agent-runner's settings; that's the human's call.
- **Do not skip step 4.** Setup that ends with empty scaffolding feels like homework; setup that ends with their first real page feels like a wiki.

## When to run

Once, on a fresh fork/clone. Running it again on a populated wiki is harmless but pointless — it will notice the template placeholders are gone and say so.
