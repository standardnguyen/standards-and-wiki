# A normalization can carry the artifact it removes

## The shape

You have a comparison you know is confounded. The raw measure tracks the confounder almost perfectly, so the comparison is really a restatement of the confounder wearing the name of the outcome. Measured on a record of nightly sleep:

| relationship | *r* | reading |
|---|---:|---|
| nights are longer → stage minutes | **+0.64** | the raw total is a duration artifact |
| nights are longer → stage *share* | **−0.45** | …and the normalized measure is one too, in the other direction |
| nights are longer → residual against the duration-conditional expectation | ≈ 0 | by construction |

The fix everyone reaches for is the middle row: **divide by the confounder.** A 735-minute night with 155 minutes of the stage looks deficient once you divide — 21%, against a 26% median — and the conclusion reverses from "unremarkable" to "bottom fifth."

The share is not clean. It correlates with the same confounder at −0.45. A long night scores a low share *automatically*. So a long night is now declared deficient on a measure that penalizes length, which is the same error with the sign flipped.

## Why it survives review

Because dividing by the confounder **is** the textbook fix. It is what "controlling for" means in casual use, it is what a careful analyst reaches for, and the arithmetic is trivially correct. Nobody reviewing the step sees a mistake, because there is no mistake in the step — only in the assumption under it, which is not on the page.

There is a second reason, specific to this failure: **the normalized measure usually produces a number, and a number invites a conclusion.** The raw measure was already suspect, so nobody trusted the first reading. The corrected reading arrives with a fix's credentials and gets published.

## The general form

**A normalization removes the artifact only if the new measure is independent of the thing you normalized away.**

Dividing by a variable is not the same as removing it. When the numerator and the denominator both move with the confounder, the ratio moves too — and it can move in the *opposite* direction, because the confounder is now in the denominator. That reversed-sign case is the dangerous one, because it doesn't look like a wash. It looks like a finding, and it reverses your conclusion, which reads as an improvement.

Rates, shares, per-capita figures, percentages, indexed values, normalized scores — all of them are ratios, and all of them inherit whatever the denominator carries.

## What it costs

You republish the same error wearing a fix's clothes and a fix's confidence.

That is strictly worse than the original. The original was known to be confounded, so it was stated with a caveat and read with one. The corrected version is trusted — it is the one a later reader lifts, because it is the one that survived the correction. The inverted conclusion can then propagate into anything downstream: a decision, a design, a message to someone who will act on it.

The second cost is a lost chain. Once the corrected measure is on the page, the confounded original looks *superseded* rather than *retracted*, so a later reader has no reason to go back and ask whether the fix was tested.

## The defense

**Test the fix as a measurement in its own right.**

The step that is missing, every time, is one line: correlate the *normalized* measure against the thing you normalized away.

```python
# the fix looked finished here
share = stage_minutes / total_minutes

# the step nobody wrote
r = correlate(total_minutes, share)      # −0.45 → still confounded
```

If that number is not approximately zero, the normalized measure is still carrying the artifact, and you have not corrected anything.

The stronger form is a **duration-conditional expectation**: fit the outcome against the confounder, then report the *residual*, not the raw value or the ratio. This is not a ratio at all — it is what the observation would have been if the confounder had been average. Compare a night against its own duration, not against the sample median, which silently assumes the sample is all the same length.

Two habits that come free with this:

- **State the direction of the residual.** "+2.6 points above expectation" and "−2.6 points below" are different findings, and the wrong one is invisible without a sign.
- **Keep the worked example reproducible.** Publish the command that regenerates the residual, and pin the window it was computed against. A correction that later readers cannot re-run will eventually be trusted on the strength of having been a correction.

## The trigger

You are about to resolve a confounded comparison with **"but per-capita," "as a share," "normalized," "adjusted for," or "as a percentage."** That sentence is the failure.

And the sharper tell, which needs no vocabulary at all: **the fix produced a tidy reversal of the original conclusion.** A measure that flips a result from "fine" to "deficient" — or the reverse — has just demonstrated that it moves with the same variable the original moved with. A correction that changes the *size* of an effect is doing its job; one that changes the *sign of the verdict* is the case to check.
