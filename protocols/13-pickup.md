# Protocol 13: Pick Up (Resume a Parked Continuation)

Resume work from a continuation parked by [Protocol 12 (Park)](12-park.md). Loads the briefing, re-grounds in the canonical surfaces and live state, then continues the work queue — built for a **fresh session with no memory** of where the work stopped.

## Trigger

- "Pick up `<slug>`" / "resume `<slug>`" / "let's continue the `<project>` work."
- "What can I resume?" → list the **Open** table from `continuations/_index.md`.

## Steps

### 1. Find the continuation

If given a slug, read `continuations/<slug>.md`. If not, read `continuations/_index.md` → **Open** table and either resume the obvious one or ask which.

### 2. Re-ground — don't trust the doc blindly

The doc reflects what was true **when it was parked**. Verify before acting: a parked doc is a `[recalled:]`-tier source (see `CLAUDE.md` → Doing Tasks §5), not ground truth.

- **Read the canonical surfaces it names** — the project's `CLAUDE.md`, its overview page, the latest session log. These are fresher than the parked doc.
- **Confirm live state** — `git log` and `git status` in the repos involved, health of anything deployed, test status. **Reconcile any drift** between the doc's Done/Next lists and reality; other sessions may have moved things.
- **Re-read any protocol** the work will execute, per the re-read-on-invocation rule.

### 3. Resume the queue

Start from the doc's **Next (priority order)**, top item first — honoring deferred tags and the user's *current* intent, which outranks what past-them wrote down. Confirm scope before a large build.

### 4. Re-park or close

- Made progress but **not done** → **re-park** (Protocol 12 steps 1-2: update the doc and the `parked:` date) before stopping, so the next pickup is clean.
- **Finished** the whole task → move its index row to **Done**, set the doc's `status: done`, and ship via [Protocol 7](7-commit-and-ship.md).

Leaving a picked-up continuation neither re-parked nor closed is the one failure mode of this pair: the index then claims a state that no longer exists, and the next pickup re-grounds against a lie.

## Notes

- **The doc is a starting point, not gospel.** On any conflict, **live state wins** — re-ground first (step 2). A stale parked doc that gets trusted blindly is worse than no doc, because it reads as authoritative.

## Related

- [Protocol 12: Park](12-park.md) — stashes the continuation this resumes
- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md)
