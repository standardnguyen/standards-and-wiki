# Protocol 19: Cold Read

Synthesize the failures. Pick a few tasks a fresh session might plausibly be handed, fire each at a reader you have not primed, and watch what it cannot find or cannot act on — then patch the wiki where the gap was.

Most substrate patching is **reactive**: a real session trips on a gap during real work, and the gap gets fixed after it has already cost something. This is the proactive mirror — instead of waiting to be tripped on, it manufactures the trips. A whole class of hazards lives in pages nobody has had a reason to open yet, and going looking is the only thing that finds them.

## Trigger

"Run Protocol 19", "cold read", "stress the wiki" — or after any change you suspect left a gap you cannot see from inside.

Segment this from the other audits: [Protocol 9](9-human-readability-audit.md) asks whether a page *parses* (a validator reads it and scores it); Protocol 19 asks whether a reader *acts correctly* from it. [Protocol 2](2-spot-check.md) asks whether two pages agree; Protocol 19 asks whether one page is findable and sufficient. Neither of those puts a reader into a task and watches where it goes, which is the whole instrument here.

**Not for routine sessions.** The apparatus cost is real — launching a reader, running a scenario to completion, observing, patching, then re-firing to verify — and a scenario can take a while. Run it when there is intent to stress the substrate, or after a change you suspect left a gap; not as a step appended to every maintenance pass.

## The rule that makes it work

🔴 **The reader must be a separate process — a fresh session of some agent, launched with no knowledge of the work being tested.** Not the author re-reading its own edits; not an agent spawned *inside* the session that made them, because that inherits the conversation, the framing, and the same blind spots. It is you talking to yourself under a different name.

The full mechanism, and why a same-frame reviewer agrees most confidently exactly where the frame is wrong: [the second opinion that shares your blind spot](../casebook/the-second-opinion-that-shares-your-blind-spot.md). Read it before your first run — this protocol is that entry's defense, mechanized.

Two honest limits: a second instance of the same harness buys the isolation but **not** a different lineage, so it shares that harness's reading habits. And the process boundary is what supplies the isolation — a different model name or agent label supplies none.

<!-- Customize: name the agent you launch a reader with, and the command that launches it in a fresh
     session. The requirement is a new process with a cold context; the tool is yours. -->
<!-- Customize: if you have more than one harness available, note which to reach for when the
     question is specifically "would a *different* reader misread this." -->

## Procedure

**1. Pick 1–3 scenarios.** Not a sweep — a few, run deep. Three sources, any combination:

| Source | Shape | What it catches |
|---|---|---|
| **A recent session log** | Re-pose a real situation as a fresh task: *"you got asked to do X. start working."* | Whether the wiki *as it stands now* would route a cold session the way the original session was routed — or only after the user's nudges. |
| **A user-chosen area** | The operator names something they suspect is thin. | Adversarial, and cheap: it tests their own intuition about which pages are underspecified. |
| **A random page + invented task** | Sample a page at random, invent a plausible task that would route through it. | Gaps in the pages nobody thinks about. Same adversarial shape as Protocol 2's random pair, aimed at the page instead of the contradiction. |

**2. Phrase each as a fresh-session prompt.** No history, no priming, no "here's what I changed, check it." The reader loads context through its normal mechanism — root `CLAUDE.md`, whatever it greps for. What is reachable from a cold start is the measurement; hand-holding poisons it.

**3. Fire it and watch.** Send the prompt into the reader's session and observe. Capture its path — what it read, what it tried, where it stalled, what it concluded. Do not intervene until it finishes or clearly stalls. A loop or a stall is a finding, not a failed run.

**4. Classify each trip.** Every trip is one of three general categories, plus one this protocol uniquely surfaces:

| Type | Shape | Where the fix lands |
|---|---|---|
| **Missing context** | Needed a procedure, path, definition, or convention that is documented somewhere it did not load. | Move the doc to a surface that auto-loads, or add a cross-link from a page it does load. |
| **Tooling blindness** | Framed a failure as "there's no way to do this" when the capability exists — an unauthenticated request read as a missing tool, a permission error read as absence. | The page for that tool, or the environment surface it misread. |
| **Posture** | Over-cautious: asks before acting on something already authorized, stops mid-flow to reconfirm, reads a queued state as "needs a human click." | Root `CLAUDE.md` as a cross-cutting behavioral rule, or a project-scoped note if it should not apply globally. |
| **Cold-discovery failure** | Could not find a page **that exists**. Greps the wrong vocabulary, scans the wrong directory, gives up before reaching the canonical doc. | A cross-link *from where it actually looked* to the canonical page; an alias or rename on the canonical title; a pointer from root `CLAUDE.md` if the rule is broadly applicable. |

The last one is the category only a cold read produces. Reactive patching sees it occasionally, but real work usually begins with the user pointing at the right page — this protocol removes the pointing.

**5. Pattern of three before patching.** One trip is an anecdote — log it, don't patch. A patch is earned when the same shape recurs across three cold reads, or two cold reads plus one real session's failure, or when a single occurrence was severe enough to be decisive on its own (the reader was about to do something destructive). Single-trip patches accumulate as noise. The log is the long memory that makes the third occurrence visible.

**6. Patch the substrate.** One canonical home, a date, and a one-line *why*; cross-reference where it is broadly applicable; no scattershot duplication. Apply the substrate posture from [Protocol 7](7-commit-and-ship.md#posture-wiki-as-substrate) — *write for a cold reader who cannot ask* — because this protocol is that posture's actual audience.

**7. Re-fire to verify the patch (convergence loop).** A patch is a claim; the retry is the test.

- **Convergence is narrow:** the reader navigates past *the gap you patched*, on its own. Not a perfect run — new findings are fine. Only that gap counts.
- **A fresh process every retry.** The reader that just lived through the unpatched scenario is contaminated; measuring from a warm context measures whether its memory covered for the gap, not whether the wiki did.
- **If the trip recurs, revise — don't add more words.** Usual causes: the patch landed somewhere the reader never loads (a cold-discovery failure *on the patch itself*); the prose is still too terse to act on; the canonical home is not where a cold reader would look.
- **If a new trip appears, classify it.** One *upstream* of the original suggests your patch confused an adjacent page — regression-shaped, fix it. One *downstream* is simply the next layer down: log it for its own pattern-of-three and do not patch it inside this loop.
- **Cap: three retry cycles per scenario.** If the same trip survives three revisions, the gap is **structural** — no amount of documentation closes it (a capability that genuinely does not exist, an environment problem, a limit of the reader). Log it as such and stop. A structural verdict is a legitimate result, not a failed run.

⚠️ **Convergence and pattern-of-three answer different questions.** Pattern-of-three decides *whether to patch at all*; convergence decides *whether one specific patch worked*. Both apply, and neither substitutes for the other.

**8. Log the session.** Scenarios fired verbatim; the reader's actual first-pass path; trips, classified; patches, with why; per-scenario retry history and final state (`converged` / `structural` / converged with a downstream finding); trips that have not yet ripened into patches; and any apparatus glitch that polluted the signal, so the next run recognizes it.

## Anti-patterns

- **Don't prime the reader.** Any framing before the scenario fires dissolves the independence you paid for.
- **Don't reuse a warm session.** A fresh process each time, including each retry.
- **Don't patch on cold-read evidence alone if the patch is broad.** A trip that *only* ever surfaces here may be exercising a path real work never takes. Bias toward gaps real work would also hit.
- **Don't mistake a reader failure for a substrate failure.** If the reader hallucinated a path that does not exist or lost track of its own tools, that is a limit of the reader; patches go to what the substrate *says*, not to compensate for it.

## Related

- [The second opinion that shares your blind spot](../casebook/the-second-opinion-that-shares-your-blind-spot.md) — why the target must be a separate process, and what isolation does and does not buy
- [Protocol 9: Human-Readability Audit](9-human-readability-audit.md) — the comprehension variant: does the page parse for a weak reader?
- [Protocol 2: Spot-Check](2-spot-check.md) — disagreement *between* pages; this one is about a reader's inability to find or use one
- [Protocol 14: UI Convergence](14-ui-convergence.md) — the same recursive fresh-process loop, applied to a user-facing surface instead of prose
- [Protocol 7: Commit & Ship](7-commit-and-ship.md) — the wiki-as-substrate posture this protocol tests, and where patches ship from
