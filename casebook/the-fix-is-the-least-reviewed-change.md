# The fix is the least-reviewed change

## The shape

You ship a change, then run a review pass over it: a set of reviewers each reading the commits you made, looking for facts that went stale elsewhere in the wiki. They find several. You fix them, in a follow-up commit. The review pass is done.

In one cycle of the maintainer's own work, measured end to end (n = 1, not a general rate), roughly a third of all the stale facts found were defects the *previous fix* had introduced. Three commits were reviewed by nothing at all, because every review's scope had been fixed before those commits existed.

The defects clustered in one place: the fix's annotations. Not the corrected value — the sentence around it. A correction note with a date. A running count. An attribution of who found what. A claim about where the record now lives. Each one is a new fact, written fast, by someone whose attention was on the value being corrected.

## Why it survives review

Because the review was scoped to the original change, and the fix arrived after the scope was set. Nobody decided not to review the fix; the review simply could not see it.

And because a fix feels like the end of the risk, not a source of it. The original change was the uncertain thing; the fix is the response to having found the uncertainty. It is small, it is targeted, and it was written in direct reply to a finding — so it inherits the finding's authority. *Surface symmetry is not structural equivalence* names the sharp form: a correction inherits the confidence of the thing it corrects, so the moment you write one is the moment your confidence is least earned.

The annotations get the least attention of all. They are not the point of the fix; they are its paperwork.

## The general form

**Every fix is a new change with its own defects, and it is usually reviewed less than the change it fixes. A review scoped before the fix exists cannot see it.**

Two mechanisms make it worse over time:

- **Each rewrite adds a claim.** A class of defect that will not converge is often one where every fix removes one false statement by asserting a new one about a second place. The count of claims stays constant; only their location moves.
- **Correction notes compete with content.** A page repaired several times, with a note for each repair, can end up with over a quarter of its text describing its own past errors, and its key finding buried two thirds of the way down. The page is more correct and less usable at once.

## What it costs

A review pass that reports itself complete while a third of its yield is defects it generated. The next pass then spends its budget finding the previous pass's mistakes, which looks like a steady stream of real findings and is partly a loop.

## The defense

1. **Re-scope each later review round onto the fix commits the earlier rounds produced.** A scope frozen at launch measures a tree that no longer exists. Name the fix commits explicitly when you hand a reviewer its scope.
2. **Keep fix notes minimal.** Correct the value. Do not add a date, a count, an attribution or a running total unless the reader of the page needs it. Every added clause is a new fact to keep true.
3. **Do not keep running totals in flight.** A count written while the work is still moving is wrong by the time it is read.
4. **Make fixes their own commits,** so the next round can be pointed at exactly them, and run your repo's check scripts on the fix as you would on the original change.
5. **When a page has accumulated correction notes, consolidate it.** Move the history to the log and leave the page saying what is true now (see the tighten protocol).

## The trigger

You are writing the annotation on a fix: a date, a count, an attribution, a pointer, a correction note. Or you are scoping the next review round, and the scope is the original commits only.
