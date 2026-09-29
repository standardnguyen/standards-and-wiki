# The Casebook

The protocols in this template tell you *what to do*. This directory tells you *what goes wrong* — the specific, recurring ways that careful work fails while looking correct.

Every entry here is a mechanism, not an anecdote. Each one was found the expensive way, in a working wiki maintained by an agent across hundreds of sessions, and each one has been stripped of the setting it was found in so that only the transferable part remains.

## Why a casebook and not more rules

A rule with no recorded reason gets re-derived, and re-derived wrongly. That is itself one of the entries here.

The protocols are deliberately terse — they are procedures you execute, and a procedure interrupted by three paragraphs of justification is a procedure people stop reading. But terseness has a cost: a reader who does not understand *why* a step exists will drop it the first time it is inconvenient, and an agent will do the same thing faster and more confidently.

So the reasons live here instead. Read this once, then read the protocols and notice which steps you now recognize.

## What every entry has in common

These are not bugs in the ordinary sense. A bug announces itself. Every mechanism in this book has the same three properties:

1. **It passes review.** Each one was written by someone being careful, read by someone being careful, and survived.
2. **Its failure mode is silent.** It does not throw. It returns a plausible value, or it returns nothing and you read nothing as absence.
3. **It is biased toward the answer you wanted.** This is the part that makes them expensive. A defect that produced alarming output would be caught in minutes. These produce *reassurance*.

If you take one thing from this directory, take that third property. **Be most suspicious of an instrument at exactly the moment it tells you the problem isn't there.**

## The chapters

### I. Checks that do not check
The guard is present, reviewed, and decorative.

- [The check that cannot stop the action](the-check-that-cannot-stop-the-action.md)
- [The correct check and the wrong outcome](the-correct-check-and-the-wrong-outcome.md)
- [A test that has never failed is a hypothesis](a-test-that-has-never-failed-is-a-hypothesis.md)
- [The relief valve wired to the kill switch](the-relief-valve-wired-to-the-kill-switch.md)

### II. Probes that lie
The measurement reports the answer you were hoping for.

- [The probe that reads the same in both branches](the-probe-that-reads-the-same-in-both-branches.md)
- [The probe that finds its subject by a property the control shares](the-probe-that-finds-its-subject-by-a-property-the-control-shares.md)
- [The change-detector keyed on an aggregate](the-change-detector-keyed-on-an-aggregate.md)
- [When you build the instrument, its bugs arrive as good news](when-you-build-the-instrument-its-bugs-arrive-as-good-news.md)

### III. Absence that isn't
Nothing found is not the same as nothing there.

- [Zero occurrences is not absence](zero-occurrences-is-not-absence.md)
- [Empty is not missing](empty-is-not-missing.md)
- [A measured absence can be a decision](a-measured-absence-can-be-a-decision.md)

### IV. Laundered confidence
How a guess becomes a fact without anyone lying.

- [Laundered confidence](laundered-confidence.md)
- [The summary compresses out the qualifier](the-summary-compresses-out-the-qualifier.md)
- [N agreeing sources are not N sources](n-agreeing-sources-are-not-n-sources.md)
- [Confidence is the broken instrument](confidence-is-the-broken-instrument.md)
- [Surface symmetry is not structural equivalence](surface-symmetry-is-not-structural-equivalence.md)
- [A normalization can carry the artifact it removes](a-normalization-can-carry-the-artifact-it-removes.md)

### V. Rules that rot
The failure modes of the instruction layer itself.

- [A rule with no recorded why](a-rule-with-no-recorded-why.md)
- [A rule can be the hazard](a-rule-can-be-the-hazard.md)
- [A pointer you don't open is not context](a-pointer-you-dont-open-is-not-context.md)
- [Injection is not consumption](injection-is-not-consumption.md)
- [A negative capability claim is a claim about scope](a-negative-capability-claim-is-a-claim-about-scope.md)

### VI. Isolation that isn't
Two things you believed were independent, and weren't.

- [The second opinion that shares your blind spot](the-second-opinion-that-shares-your-blind-spot.md)
- [Verifying your own write is a disclosure vector](verifying-your-own-write-is-a-disclosure-vector.md)
- [A redaction pattern encodes an assumption about shape](a-redaction-pattern-encodes-an-assumption-about-shape.md)

## Entry format

Every entry answers the same six questions, in the same order, so you can skim a chapter and stop at the one that describes what you are about to do:

- **The shape** — what the construct looks like
- **Why it survives review** — what makes it read as correct
- **The general form** — the mechanism with the tool stripped off
- **What it costs** — the failure when it fires
- **The defense** — what to do instead
- **The trigger** — the moment to go looking for it in your own work

The last one matters most. Several of these cannot be caught by a checklist, because you can only search for what you already know to look for. The trigger is the recognizable *situation*, so that the situation itself does the reminding.
