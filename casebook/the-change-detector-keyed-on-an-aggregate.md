# The change-detector keyed on an aggregate

## The shape

You have a derived artifact — a rendered report, a cached run, a generated index, a copied tree — that must be rebuilt when its source changes. Rebuilding is expensive, so you detect the change cheaply, with a signature:

```python
def stale(old, new):
    return len(old["schedule"]) != len(new["schedule"])
```

The signature is a **derived aggregate**: a length, a count, a total, a file size, a row number, a line count, a byte length. It is cheap. It is stable. And it collides.

Two genuinely different schedules happen to produce the same number:

- 6 pairings × 5 rounds = **30 trials**
- 15 pairings × 2 rounds = **30 trials**

The source is replaced, the detector compares 30 to 30, and stays quiet. The artifact is now stale, and nothing announced it.

## Why it survives review

Because the detector *works* on every change you would naturally test it with. Add a row and the length moves; delete one and it moves back. The one-line version is obviously reasonable, and it is written by someone who is being efficient rather than careless.

The collision is not a rare edge case. It is a property of the thing you chose to measure: **any aggregate folds a multi-dimensional change onto a single axis, and different compositions on that axis are the normal case, not the exception.** Combinatorics generates collisions faster than intuition expects. You cannot eyeball which pair of configurations will agree, because the agreement is in the arithmetic, not in the shape.

And it never fires, so it never accumulates evidence against itself. A detector that is wrong produces no output. It has never once, in the life of the code, given you a reason to doubt it.

## The general form

**A guard keyed on a projection of its subject cannot see any change the projection collapses.**

The projected value is not a weaker version of the subject; it is a different object with a many-to-one map onto it. Every pair of states sharing an aggregate is a change the guard is blind to by construction.

This is not specific to lengths. Any derived summary has the same defect:

| key | blind to |
|---|---|
| `len(...)` | equal-length replacement, reordering, same-size swap |
| row count | one row added, one removed |
| total / sum | compensating changes |
| file size | same-size rewrites |
| line count | edits that trade lines |
| `git diff --stat` | whose lines they were — yours, a peer's, or a mix |

The same rule governs the *commit-time* version of the mistake: reviewing a change by checking that a file's number of changed lines is "close to expected" is a derived aggregate, and it cannot distinguish *your three lines* from *your two plus someone else's one*. A close-enough aggregate reads as a match. Read the hunks, or do not claim the file is yours.

## What it costs

The stale artifact is believed.

The specific damage is whatever the artifact was for. In the case this came from, a comparison table had been rebuilt against a schedule whose composition had changed while its total had not, so it rendered one set of entrants against another set's votes. An entrant that had played **zero trials** displayed a score of **0%** — which reads as *decisively worst* — and the intended takeaway was to drop it. The correct conclusion was that the table was describing two different experiments at once, and the honest reading was *no data*.

The general cost is the same shape every time: a decision made on an artifact that silently describes something other than what it claims. Nobody wrote a wrong number. The numbers were right. The frame was wrong, and the detector was the thing responsible for noticing.

## The defense

**Key on content, not on a projection of content.**

Serialize the canonical form of the source and hash it. `sha256` over the *structured* thing — the keys, the layers, the parameters, the schedule itself — collapses to a fixed width while remaining injective for every practical case. It is barely more code than the length check.

```python
def sig(x):
    return hashlib.sha256(json.dumps(canonical(x), sort_keys=True).encode()).hexdigest()
```

Then do the part that everyone skips: **verify the new detector against the failing case before trusting it.**

Take the two states that defeated the old guard and run them through the new one. The length check returns equal on both — it never fires. A correct content hash returns two different values and fires. If you have not watched your new detector fire on the change you built it to catch, you have replaced one hypothesis with another.

A guard that has never been observed firing is not a guard. It is a comment.

## The trigger

You are writing — or reviewing — a staleness check, a cache key, a rebuild condition, a "has this changed" comparison, a "did this land" confirmation.

The tell is that the key is computed by selecting one property of the thing rather than serializing the thing. Ask directly: **what two different inputs does this collapse onto the same value?** If you cannot convince yourself the answer is "none", the key is a projection, and projections collide.

Also: any moment you find yourself checking a summary against what you expected instead of reading the underlying content. "Close to expected" is not a test. It is a derived aggregate being believed.
