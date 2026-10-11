# Protocol 23: Propagation Sweep

When a commit changes a fact, find every other live page that still carries the old value, and fix it. This is the full version of the sweep that [Protocol 7](7-commit-and-ship.md) §2d starts: §2d is the grep you run while shipping; when the diff holds factual corrections, it hands the commit SHAs to this protocol.

A correction that lands on one page contradicts every carrier that still states the old value. Summary tables, indexes, hub descriptions and cross-references are where the old value survives, and those are the pages a cold session reads first ([The summary compresses out the qualifier](../casebook/the-summary-compresses-out-the-qualifier.md)).

## Trigger

"Run Protocol 23", "sweep these commits", or Protocol 7 §2d on any commit that changes a fact (a number, date, count, status, name, path, address or price) or changes how a mechanism works. It also runs standalone on named commit SHAs. On someone else's pushed work, the sweep hands facts back to the owner (`file:line`, the claim, the evidence) and edits nothing.

Skip the whole protocol only for a leaf page with no cross-references (a recipe, a journal entry, a standalone log), and say so in the ship report. Steps 4 and 5 (the agent waves and judging) are skipped when the diff holds no factual corrections at all, as Protocol 7 §2d says; steps 2 and 3 still run. A silent skip reads the same as a sweep that was never run.

## Procedure

### 1. Resolve the scope

Commit your change first, then record the SHA of each commit you made as you make it (`git rev-parse HEAD` in the same invocation as the commit, or the hash the commit prints), confirm each with `git show --stat <sha>`, and hand exactly those SHAs to wave 1. On a shared checkout `HEAD` may already be a peer's commit, so a `rev-parse` run later names the wrong one. Never hand an agent `git diff --cached` or a `..HEAD` range: HEAD moves while a wave runs, so one range string names a different set at launch and at report. On a shared checkout, build your file list with `git show --name-only <sha>` on each of your own commits, not from a span between two of them, which fills with other sessions' work.

### 2. Run the deterministic checks first

Run your repo's check scripts (the [Protocol 10](10-codify-drift-check.md) table in Protocol 7 §2e, or the manual checks there if you have no scripts) before any agent launches. They catch the machine-readable facts for free; the agents are for what is left.

Treat a checker's output as positive candidates, never as proof that nothing else is stale. Exit 0 asserts one narrow proposition, not coverage ([Zero occurrences is not absence](../casebook/zero-occurrences-is-not-absence.md)). If a checker defaults to comparing against the working tree, give it the explicit commit range, or it will read other people's uncommitted edits and cannot fail on a tree holding none of your work.

### 3. Grep the changed values yourself

Before you push, grep every changed value at HEAD, plus the mechanism's plain-English name and its status words. This step is never deferred, even when the agent waves are.

- **Grep the shape, not only the value.** For a changed count, range or status, also grep its phrasings: `N items`, `items N-M`, "highest", "latest", "currently". The old string shows where the fact was last written the same way, not everywhere it lives.
- **Grep the rest of the block.** When a fix corrects one entry of a status list, check its sibling lines, blanket quantifiers (`all N`, `the rest`, `everything else`) and its `updated <date>` stamp.
- **A retraction has no old value.** Nothing in "we no longer do X" matches a search for X's replacement, so grep the retracted claim's own words.
- **Exclude logs by path** (`--exclude-dir=logs`), never by filtering lines that contain `/logs/`, which also hides live pages that merely link to a log. Logs are history and are never retro-edited.
- **Multi-pass documents.** When a later section corrects an earlier claim, fix the original claim and every summary that quotes it.

### 4. Run at most three finder waves

Each wave is read-only finder agents handed the SHAs from step 1 (wave 1) or the fix commits the previous wave produced (waves 2 and 3, step 7), **never your own list of changed facts**. A summarised list caps coverage at what you noticed, at the moment your context is fullest, and the gap is silent ([The second opinion that shares your blind spot](../casebook/the-second-opinion-that-shares-your-blind-spot.md)).

The finder job:

1. Extract every changed fact from the diff text of those SHAs as an old→new pair. Never from conversation memory. Report the pairs.
2. Grep each old value across the whole repo (pages, `CLAUDE.md`, hooks and scripts, anything that restates facts), excluding logs by path.
3. Report every surviving carrier as `file:line`, a verbatim quote, and a same-fact or coincidental-string judgment.

Rules for the waves:

- **Width.** At most three finders at once; two by default, split by duty: one on literal values (old and new values, identifiers, counts, status literals), one on reworded mentions (plain-English names, status words, summary rows, dropped qualifiers). Same-prompt finders duplicate each other's hits, so extra width buys spend, not coverage. <!-- Customize: your concurrency cap. -->
- **Stop after three waves, then push.** Waves 2 and 3 re-scope onto the fix commits the earlier waves produced (step 7). There is no run-until-dry: in the one cycle where this was audited (n = 1, and confounded with the re-scoping), later waves of the same question returned almost nothing real, and whatever leaks is caught by the next session's first wave.
- **A fourth wave only for a new question** — a different lens or scope, stated in one sentence in the finder prompt. What decays is the question, not the corpus.
- **Don't poll.** Launch a wave and wait for it. If you stop early, say "stopped at N waves", never "converged".
- **Don't steer.** Never tell finders what result you expect or which error is costlier.
- **Pin each agent's model explicitly.** An unpinned agent inherits the session's model, so a change of session default silently reroutes the whole fleet. Keep finders off any tool that touches live infrastructure or queues human approvals; a sweep is read-only text work.

### 5. Judge with two lenses, batched

Dedupe candidates by `file:line` plus fact first. Then run one judge per lens over the whole wave's candidates in one pass:

- **Lens A, staleness:** is the claimed defect real at HEAD? Verify the new fact independently.
- **Lens B, past-scoping:** is the line deliberately historical? Look for a date pin, a commit hash, strikethrough, an incident or resolution block, a page-level "retired" banner, or the convention that index rows track current truth while log bodies track the record.

Confirm a candidate only when both lenses agree it is stale. **A disagreement is logged in the session log for the next session, not edited**, because a wrong edit costs more than a late one. A lens-B reason that declines jurisdiction ("an accuracy issue, not a scoping issue") is not a verdict: check that candidate against the source yourself. Adjudicate every unique candidate; batching is what makes that affordable.

If a script collects the verdicts, filter on the presence of a verdict, not on the row, and reconcile confirmed plus rejected against unique candidates minus failed agents. A crashed judge and a rejection otherwise look identical. If any run flagged a passage another run cleared, it goes to judging: a flag beats a clear.

Report both `N confirmed` and `M distinct file:line`; neither alone counts defects.

### 6. Fix: human-reaching first, then canonicalize

1. **Human-reaching fixes first.** A line meant to be spoken, a message draft, a prompt a future session executes, a number someone will quote: fix those one at a time and re-verify each against the source. Never let the finders grade severity.
2. **Canonicalize instead of updating everything.** When a fact has more than two live carriers, pick one canonical home and turn the others into pointers. Updating N carriers is work on every sweep and never reduces N. Before writing a pointer, grep the target page for the figure. Keep a figure on several pages only when it must be readable without a click.
3. **Delete counts of mutable sets; don't update them.** An updated count is true until tomorrow. Delete it and keep the command, link or enumeration that reproduces it. Keep a count only when a date bounds the set ("N records as of <date>"), or when the sentence cannot survive without it, and then say what was counted and when. Never replace a count with "about N".
4. **Report the class.** Group findings by mechanism. For any group of three or more, ask: what single rule, in one place, would have prevented all of them? Propose one rule per class: a writing rule goes in the style guide, a mechanically decidable one becomes a [Protocol 10](10-codify-drift-check.md) check, one that must fire while working goes in `CLAUDE.md`, and coincidence is reported as "no class here". Strengthen an existing rule before adding one.

Paste these three rules into every fix brief:

1. Grep the old value before every edit; when three or more other carriers exist, report them and edit none.
2. Grep the target page for what a pointer claims before writing the pointer.
3. A commit message is not a source: quote the diff or the page.

### 7. Commit fixes and re-scope

Each wave's fixes land as their own commits, staged by exact path per [Protocol 7](7-commit-and-ship.md) §3, and steps 2 and 3 rerun on them before the next wave. A wave that produced no fix commits ends the sweep. Fix commits are the highest-risk input: the defects concentrate in a fix's own annotations (dates, counts, attributions, anchors), the near-miss siblings of the edited line, and claims a fix makes about the sweep in flight.

- Never claim a fix closed a class ("fixed everywhere") beyond what you searched. Say what you searched, or search what you say.
- Keep correction notes short, and never record a running cycle's totals on a page; the next wave falsifies them. A note that a reader needs, such as the date a fact was last verified, stays; narration of the sweep itself does not.
- After any tree-wide pattern rewrite, read `git diff` of your root rules file; if that file is a symlink target (or other paths link to it), a rewrite of the linked path edits it without showing you.

After the last wave: push (when Protocol 7 called this, its §4 does the push), update the PR, and log what each wave found, plus the lens disagreements, in the session log.

## Notes

- **The checkers are free and the agents are not.** Spend agents on what the checkers cannot see.
- **Bounded beats converged.** A sweep with no reachable stop ends up billing for its own output. Three waves, then ship.
- **A wrong edit is the costlier error.** That is why disagreement logs instead of edits, and why the fix brief reports widely carried values rather than editing one of them.

## Related

- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md) — §2d calls this protocol
- [Protocol 10: Codify Drift Check](10-codify-drift-check.md) — the checkers step 2 runs, and where a class rule goes when it is mechanical
- [Protocol 4: Recursive Harmonize](4-recursive-harmonize.md) — the convergence loop for editorial drift; this protocol is deliberately bounded instead
- [Protocol 18: Tighten](18-tighten.md) — where a class rule lands so it fires
