# The check that ran on nothing

## The shape

You have a lookup layer: a set of hand-curated aliases that route certain words in a request to the right page. It runs on every request. For weeks it routes nothing on three of its keys, and you read that as three quiet topics.

The keys were dead the day they were written. A noise filter upstream of the lookup — written to drop incidental words from prose — dropped those three keys before the alias table was ever consulted. The lookup was correct. The table was correct. The lookup never received the input it keys on.

The same shape, elsewhere:

- A deduplication step keyed on a session identity. One caller passes the bare request and no identity, so every call looks like a new session, nothing is ever deduplicated, and there is no error anywhere.
- A drift checker compares the wiki against a local clone of another repo. The clone is five commits behind. The checker finds no drift, because the drift is in the five commits it cannot see.
- A checker that defaults to the uncommitted working-tree diff, run after you have committed everything. The diff is empty. The checker exits 0, and it could not have done anything else.

In every case the output is the correct output for the input it got. The input was empty, stale, or someone else's.

## Why it survives review

Because "nothing to report" is the most common legitimate result a check has. A filter that matches nothing on a quiet day and a filter that was handed nothing look identical: same exit code, same empty output, same silence. Nobody reviews silence.

And the review that did happen looked at the right place for the wrong question. The reviewer read the matching logic and confirmed it was correct, which it was. The defect is upstream of the logic, in the plumbing that delivers its input — a stage nobody thinks of as part of the check.

## The general form

**An empty result is evidence about the world only if the input arrived. A check that never confirms its input will report clean on no input, forever.**

This is distinct from a search that was too narrow (*zero occurrences is not absence*). There the search ran on the wrong set. Here it ran on no set at all, or on a set that cannot contain the answer — and the output does not distinguish the two from a genuine negative.

The recurring ways the input fails to arrive:

| failure | what the check sees |
|---|---|
| an upstream filter strips the keys | text without the words it keys on |
| a caller omits a required field | a default value that matches nothing |
| a local copy is behind its source | a snapshot that predates the change |
| a default scope holds none of your work | an empty diff, or someone else's diff |
| a hook is wired to the wrong event | no invocations at all |

## What it costs

A guard that has been off for its whole life, reported as on for its whole life. Every day the check reports clean adds one more day of false history to the record, and the record is what the next reader trusts.

The second cost is that the absence of findings gets cited. "The checker found no drift" goes into a summary, and becomes the reason nobody looks by hand.

## The defense

1. **Make the check report what it received, not only what it found.** "0 findings in 412 inputs" and "0 findings in 0 inputs" are different results. A count of inputs processed costs one line and turns the silent case into a visible one.
2. **Fail when the input is empty or unreachable.** A checker that cannot refresh its reference copy should exit with an error, not reconcile against the copy it has. Refusing to answer is better than answering about the past.
3. **Diff old and new behaviour over real inputs** when you change a filter or a pipeline stage. Run both versions over a corpus of real requests and compare what each one keys on. A filter tuned for one class of input will strip another class silently, and only a comparison shows it.
4. **Name the scope you are checking.** When you hand a checker a scope, hand it your own changes by identifier, not a default range or the working tree. A default is a scope you did not choose.

## The trigger

A check, filter, hook or integration returns nothing, and you are about to read that as nothing to report.

Ask one question first: **what input did this run on, and did that input contain anything that could have matched?** If you cannot answer from the output, the check does not tell you.
