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

1. Log it in the register's skip categories with a note: *"Pattern identified — Protocol 10 candidate."*
2. Surface to the user: *"[pattern name] has recurred [N] times across [agents/waves]. Recommend running Protocol 10 to codify it as a structural check."*
3. If the user approves, execute Protocol 10 inline (it's fast — just adding a table row).
4. If the user defers, leave the skip-category note for the next session.

The marathon does NOT need to pause for Protocol 10 — the codification can happen between waves or after the marathon converges.
