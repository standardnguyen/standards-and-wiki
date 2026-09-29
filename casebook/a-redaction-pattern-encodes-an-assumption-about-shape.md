# A redaction pattern encodes an assumption about shape

## The shape

You need to look at a config file that contains a secret. You are being careful, so you do not read it raw — you pipe it through a filter that masks anything secret-shaped before it reaches your eyes:

```bash
grep 'api_key' config.toml | sed 's/^prefix-[A-Za-z0-9]*/<redacted>/'
```

The filter is a real filter. It is doing what it was written to do. The output arrives with the value intact, because the pattern assumed a prefix the value does not have.

You set out to avoid disclosing the secret. You disclosed the secret. The step you took *specifically to prevent that* is the mechanism that produced it.

## Why it survives review

Because the guard is visible, plausible, and written by someone who was thinking about the risk. A reviewer reading the command sees a redaction step and reads it as caution. The step's presence is read as evidence of care, and the question that would defeat it — *what shape does the value actually have?* — is not asked, because a redaction pattern looks like it already answered it.

The failure is also silent in the specific way that matters: **a regex that does not match is not an error.** `sed` with a non-matching pattern is a successful no-op. It exits zero. It prints the line. There is no diagnostic, no warning, no empty result — there is the full value, formatted like an ordinary output line, in a block that everything around it says was redacted.

And it is a *dual* failure, which is what makes it worth its own entry: the masking encodes an assumption about the secret's shape, **and the reason you reached for masking was that you did not know the shape.** You are guessing at the one property the guard depends on, at the exact moment the guard becomes load-bearing.

## The general form

**A redaction step is a filter parameterized by the secret's shape, applied at the moment when the shape is the thing you do not know.**

Guard and threat are the same variable, and the guard reads as the resolution of the question rather than as a bet about it. When the bet is wrong, the guard degenerates into a pass-through and reports success.

The same shape appears anywhere a safety step is a *pattern* rather than a *predicate*:

| the guard | assumes | fails by |
|---|---|---|
| a masking regex | the value's prefix or character class | not matching, and printing in full |
| an allowlist of "safe" files | the set of files that matter | being incomplete — an omitted file is not flagged, it is *allowed* |
| a keyword denylist | the words the secret is labelled with | the label being anything else |

Every one of these is a filter that turns *"I did not check"* into *"I checked, and it passed."* That conversion is the whole cost.

## What it costs

A live credential in a transcript, and a rotation. Worse than the raw read would have cost, because the raw read would at least have been *recognized* as a risk. The masked read passes through the part of your attention that screens for risk, on the strength of the guard — and the guard is what failed.

It also costs learning. The value was not merely shown, it was shown by the mechanism meant to prevent showing it, so the incident reads as *"the masking was insufficient"* rather than *"masking was the wrong tool"* — and the next attempt is a better regex, which fails the same way on the next key.

## The defense

**Emit a count or a boolean, never the line.**

```bash
grep -c '^api_key' config.toml            # is the key present, and how many times
grep -q '^api_key' config.toml && echo present
```

You do not need to see the value to answer the questions you actually have: *is it set, how many are there, is this the field I think it is.* Those are all counts and booleans. The value is never the answer.

Three rules that close the remaining gaps:

- **Never mask — reduce.** A redaction step is a filter over content, and content is where the secret is. Move the question to the metadata layer, which cannot leak. "If you truly need to see the value's shape, the person who owns the credential reads it, not you."
- **Do not read the *neighbours* of anything you touch either.** A `cat` to check a file's format prints the whole file; a read-back that confirms your own write prints the window around it. Both are the same failure — a metadata question answered with content.
- **Chain the reduction, not the filter.** `grep -c` / `grep -q` compose safely; a masking pipeline does not, because every stage is another shape assumption that can pass everything through.

## The trigger

Any time you are about to look at a file you believe holds a secret, and your plan for looking safely involves a pattern.

The tell is that you can describe the *shape* you are masking by — and if you cannot verify that shape without looking at the value, you have already lost. Reach for a count.

**And a distinct trigger for the recurrence:** this failure recurs *after* the rule against it is written down and known, because a redaction step doesn't feel like a credential command — it feels like the careful option. Same family as the read-back: both fire in the moment of being careful, not the moment of being careless.
