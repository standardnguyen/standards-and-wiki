# Protocol 12: Park (Stash a Resumable Continuation)

Stash a **self-contained, wiki-persisted continuation** for the current work so it can be picked up cleanly in a future session — days later, in a fresh context, after the conversation has been compacted or discarded. The parked doc is a *briefing*, not a transcript: it tells a cold session what the task is, what's done, what's next, and how to verify — everything needed to resume **without this conversation**.

Sibling of [Protocol 13 (Pick Up)](13-pickup.md), which resumes one. The two are a pair; neither is much use alone.

## Trigger

"Park this" / "stash a continuation" / "save this so I can pick it up later" / "I'm stopping but want to be able to trigger it whenever I come back."

**Park vs. the ephemeral continuation prompt.** [Protocol 7](7-commit-and-ship.md) ends every run by emitting a continuation prompt in a code block. That is for *"resume right now, or in the next message"* — it lives in the chat and dies with it. Park is for *"resume next week, fresh"* — it lives in the wiki and is retrievable by name. When the honest answer to "how do I pick this back up?" is **"next week, cold,"** park it.

## Steps

### 1. Write the continuation doc

Create `continuations/<slug>.md`. The slug is the task's **stable identity** (e.g. `nas-migration`) — reuse the same slug when re-parking the same task so pickups stay idempotent: one task, one file, updated in place.

Include, in this order:

- **Header** — `title`, `status: open`, `parked: <YYYY-MM-DD>`. (Use frontmatter if your renderer reads it; a plain header block is fine otherwise.)
- **What this is** — one paragraph: the task, the goal, who it's for.
- **Load first (canonical surfaces)** — the pages a cold session must read: the project's `CLAUDE.md`, its overview/index page, the latest session log. *Point, don't duplicate* — those pages are fresher than the parked doc will be.
- **Infra / loop** — how to build, test, deploy, and ship this work: the dev-loop commands, the never-do rules, the repos and branches involved.
- **Done** — what's already shipped, with commit SHAs and PR numbers, so a pickup doesn't redo it.
- **Next (priority order)** — the work queue, top item first, each with enough detail to start on. Flag anything explicitly deferred ("after X", "not until Y ships").
- **Gotchas / decisions** — non-obvious constraints, scope calls already made, traps, concurrency hazards.
- **First move on pickup** — the literal first action: *"read the project overview and this doc, confirm live state, then start `<top item>`."*

Write for a **cold reader** — a future session, a smaller model, no memory of this conversation. Apply Protocol 7's comprehensiveness posture: over-explain, spell out the obvious, include the failure mode you almost left out.

### 2. Index it

Add (or update, if re-parking) a row in `continuations/_index.md` under **Open**:

```
| [<slug>](<slug>.md) | <project> | <parked-date> | <one-line next move> |
```

### 3. Tell the user the trigger

Report the slug and how to resume: *"parked as `<slug>` — say 'pick up `<slug>`' (or run Protocol 13) whenever you're back."* A parked continuation nobody knows the name of is not parked.

### 4. Ship it

A parked continuation is a wiki edit — commit it, normally as part of a [Protocol 7](7-commit-and-ship.md) close-out.

## Notes

- **Park beats remember.** The doc *is* the memory. Don't rely on the next session reconstructing context from session logs — logs record what happened, not what to do next.
- **Re-park freely.** Every pickup that doesn't finish should re-park (update the doc and the `parked:` date) so the continuation never goes stale.
- **One task, one slug.** Don't spawn a new file per park of the same task — update in place. The index row tracks the latest state.

## Related

- [Protocol 13: Pick Up](13-pickup.md) — resumes a parked continuation
- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md) — close-out, where parking usually happens
