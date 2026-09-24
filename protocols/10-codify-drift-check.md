# Protocol 10: Codify Drift Check

Promote a recurring drift pattern into a permanent structural check. This is the meta-protocol — it doesn't find drift, it turns *findings about drift* into guardrails that prevent the same drift class from recurring.

## Trigger

- "Run Protocol 10" or "Codify drift check"
- During a Protocol 2 marathon/ultramarathon: when the same drift pattern is independently rediscovered 2+ times by different agents, the main thread should surface: *"This pattern has recurred — recommend Protocol 10 to codify it."*
- After any session where a propagation failure is caught manually (e.g., the user notices a stale count, or a change that didn't propagate to every page carrying the fact).

## Input

One or more drift patterns to codify. Each pattern needs:

1. **What drifts** — the specific fact type (a count, a status, a config option, an address, etc.)
2. **Where the canonical value lives** — the authoritative source page
3. **Where copies live** — the pages that carry the value and tend to go stale
4. **What triggers the drift** — the action that changes the canonical value (adding an item, running an audit, changing a config)
5. **How to check** — a `grep`/diff command or comparison procedure that catches it in under 10 seconds

If any of these are unclear, ask — don't guess. The point of this protocol is precision; a vague check is worse than no check because it gives false confidence.

## Procedure

### 1. Validate the pattern

- Is this genuinely recurring, or a one-off? A pattern that appeared once in a Protocol 2 run is a finding, not a drift check. It needs to have been caught 2+ times independently, OR the user identifies it as structurally likely to recur.
- Is the check automatable with a `grep`/diff, or does it require reading comprehension? Only grep-checkable patterns go in the structural tables. Judgment-required checks stay as Protocol 2 spider/sweeper tasks.

### 1a. Write a RECONCILER, not a phrase-ban

This distinction decides whether the check has any future value, and it is easy to get backwards.

- A **reconciler** derives its expectation from the source of truth — it reads the authoritative file and compares. It therefore catches drift **nobody has noticed yet**.
- A **phrase-ban** greps for the specific wrong strings you just found. It catches exactly what you already caught, and then goes quiet forever.

*A check written by the author of the thing it checks inherits the author's blind spot.* If you are hardcoding a string you watched go stale, you are writing the weak kind — go find its source of truth instead and reconcile against that.

**Budget for adjudication: value-shaped checks are not clean.** A "this list or number is out of date" check measured roughly 70% precision in practice, because a number can carry a commit pin, a list can sit in a section that explains why it need not be exhaustive, and a row can be a dated changelog entry that is *supposed* to hold an old value. Teach the script your local archival conventions (strikethrough, "original follows", dated indices) or it will cry wolf and get switched off — which is the same as not having it.

**A skip-heuristic can be INVERTED by local convention.** One reconciler skipped any line containing the word `corrected` — but the house annotation for a freshly verified value is *"(count corrected `<date>` — this read N)"*, so the heuristic exempted the most recently checked number on the page, permanently and silently. Read how a convention is actually *used* before encoding it.

### 1b. Prove the check can fail — and prove each guard can fire

**Prove it on known-bad state before trusting it.** The check must FAIL on the drift you are codifying and PASS after the fix. A check first run against an already-clean tree is a hypothesis, not a guard.

- Restore the known-bad file **with a copy, not `git checkout -- <file>`** — the file may also hold uncommitted edits, and the checkout destroys them.
- Confirm the failure output **names the offending file and line**, not just "assertion failed". A count that merely went down is indistinguishable from a detector that went blind.

**Then prove each exemption too.** A reconciler accretes exemptions and skip-heuristics, and they rot silently: one guard matched a bare quoted number while the count regex required a longer form, so the two patterns could never overlap; another was tested *after* a filter that already excluded every value it could return. Both read as coverage and neither could ever fire. **A guard that cannot fire is worse than no guard** — it is the same failure as the check going quiet, wearing the costume of diligence. For every exemption, construct the input it is supposed to suppress and watch it get suppressed. If you cannot construct one, delete the guard and record why.

### 2. Write the conditional commit-time check

Add a row to a **Structural drift checks** table in your commit-and-ship protocol ([Protocol 7](7-commit-and-ship.md)). If that section doesn't exist yet, create it — a simple two-column table that the commit step consults before pushing:

| If the diff touches… | Run this check |
|----------------------|----------------|
| `<trigger file pattern>` | `<what to verify / grep command>` |

The check should be **conditional** — it only fires when the diff touches the trigger files. This keeps the commit step fast: most commits touch none of the triggers and skip every check.

### 3. (Optional) Add an unconditional sweep target

If the pattern doesn't have a clear diff trigger (e.g., "this should be checked every full maintenance pass regardless of what changed"), add it instead to whatever periodic full-tree maintenance routine you run, as an always-run sweep target rather than a conditional commit check.

### 4. Update the Protocol 2 skip list

If this pattern was discovered during a Protocol 2 marathon, add it to the register's skip categories so future agents don't re-flag instances of the pattern — the check is now structural, not per-finding.

### 5. Commit

Single commit with all changed files (the commit-and-ship protocol, the Protocol 2 register if applicable). Commit message: `protocol 10: codify drift check — <short name>`.

## Protocol 2 integration

During a Protocol 2 marathon or ultramarathon, the main thread should track which findings represent recurring patterns. When a pattern hits the 2-recurrence threshold:

1. **Machine-checkable — is a file, enum, config, or count the source of truth? Write the reconciler NOW.** Do not file it as a "Protocol 10 candidate" for later; a deterministic check against an authoritative source needs no approval, and deferring it is the exact behaviour this protocol exists to retire.
2. **Otherwise** (grep-checkable, but with no machine-readable source, so the output is a table row): log it in the register's skip categories with a note — *"Pattern identified — Protocol 10 candidate."* — and surface to the user: *"[pattern name] has recurred [N] times across [agents/waves]. Recommend running Protocol 10 to codify it as a structural check."*
3. If the user approves, execute Protocol 10 inline — adding the table rows is fast.
4. If the user defers, leave the skip-category note for the next session.

The marathon does NOT need to pause for Protocol 10 — the codification can happen between waves or after the marathon converges.
