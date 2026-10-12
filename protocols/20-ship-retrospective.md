# Protocol 20: Ship Retrospective

A step of every full [Protocol 7](7-commit-and-ship.md) run. It asks one question of the run so far: how could Protocol 7 itself, or the protocols it called, have gone better? It answers from evidence and ends in at most three small proposals, so the shipping procedure improves a little each time it runs instead of only when someone remembers to audit it.

## Trigger

Runs inside a full Protocol 7 (one that reviewed, swept and committed real work), not on a one-commit ship. With session logging configured, it slots into Protocol 7 §6: after the session log is written and its index row added (items 1–3), before §6 item 4 stages and commits the log, so what the retro writes ships in the same push as the log. With no session logging configured, run it after §6 and put its output in the continuation prompt (§7) instead (see step 4).

It sees only the run up to that point. Anything after it is outside its evidence.

The user can say **"skip the retro"** for a run. Skip it out loud, per Protocol 7's skip rule.

<!-- Customize: if your Protocol 7 writes the session log before the main commit, run this step after the log and before that commit instead. The rule is the same: after the log exists, before the commit that ships it. -->

## Procedure

### 1. Gather evidence

One pass by the working session, or by one fresh agent when the session is deep into its context. Answer from evidence, not from memory:

- **Cost.** Use your harness's usage or cost report if it has one, windowed to this run, and give the whole-session figure beside it, because the session's earlier work is priced in the unwindowed one. If there is no such report, count turns, tool calls and retries from the transcript.
- **Failures.** Which casebook entries (`casebook/`) describe something that happened in this run.
- **Rework.** What the run did twice.

The pass may read the session log and the session transcript. Reading is not displaying: the secrets rules in root `AGENTS.md` still govern what you print.

### 2. Ask three questions

1. Where did the run spend the most time or tokens, and was it needed?
2. Which step failed, was skipped, or was redone, and which casebook entry names it?
3. Which mistake repeated that no casebook entry names?

### 3. Write at most three proposals

Each proposal is three parts: **the proposal, its evidence, the cheapest change that would fix it.** Class each one:

1. **Certain.** Propose it through a reviewable commit, never a silent edit: make the edit. Have one reviewer check the diff cold: a fresh process given only the diff and the goal, not this session's context, and on a different model too when you have one. A reviewer that shares the author's context shares its blind spot ([casebook](../casebook/the-second-opinion-that-shares-your-blind-spot.md)). Then commit it as its own commit, so it stays reviewable on the PR, and sweep it like any other change: run Protocol 7 §2d's grep on that commit, and [Protocol 23](23-propagation-sweep.md) if it changes how a mechanism works, because a protocol edit is restated by the README, the protocol table and the checklists. Treat the reviewer's output as a claim: verify a correction it makes, and check the reverse if it agrees too quickly. If the reviewer disagrees, the proposal is uncertain: undo the edit and route it as below.
2. **Uncertain.** Do not edit. Hand it to the user as a note, in the report and in the session log.

A proposal that would grow a protocol must name what it would remove. Protocols are read on every run, so growth is a cost every future run pays (root `AGENTS.md` → substrate edit hygiene).

<!-- Customize: route uncertain proposals wherever your user reviews things: an inbox, an issue tracker, a notes page. -->

### 4. Record it

Add a `## Ship retrospective` section to the session log with one line per proposal, ending in its route: `implemented, checked by <reviewer>` or `noted for the user`. Then return to Protocol 7 §6 item 4.

No session log? Put the same lines in the continuation prompt (§7) instead, and push any certain-class commits first (Protocol 7 §4), because §6 items 4 and 5 only run when logging is configured and nothing else would push them.

## Notes

- **Three is a ceiling, not a target.** A run with nothing to propose records that and moves on.
- **Evidence or nothing.** A proposal with no evidence from this run is an opinion; drop it or make it a note.
- **The user is the reader.** Certain edits reach them on the PR; uncertain ones as notes. Nothing here changes a protocol without a commit they can review.

## Related

- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md) — the run this step sits inside
- [Protocol 10: Codify Drift Check](10-codify-drift-check.md) — when a repeated mistake should become a structural check
- [Protocol 18: Tighten](18-tighten.md) — when the problem was finding something, not doing it
- [Casebook](../casebook/_index.md) — the named failure mechanisms question 2 checks against
