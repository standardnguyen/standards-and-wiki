# The probe that finds its subject by a property the control shares

## The shape

You are A/B-comparing two things and you want a measurement of each. The subject is identified by whatever distinguishes it from its surroundings:

```rust
let subject = rows.find(|r| r.glyph == MARKER);
let control = rows.find(|r| r.glyph == ASSISTANT_GLYPH);
assert_eq!(subject.col, control.col);
```

You run it. It passes. The two line up.

Now you swap the subject to the control's own value — which is the entire point of an A/B, or just an ordinary test of the new value. `MARKER` is now the same glyph as `ASSISTANT_GLYPH`.

The lookup for the subject now returns **the assistant row**, because that is the first row carrying that glyph. The assertion compares the assistant row to the assistant row, and passes. It did not examine the subject at all.

## Why it survives review

Because the failure is conditional on a change you have not made yet. In the current state — subject distinct from control — the probe works, and works correctly. It is not wrong. It is *degenerate under exactly one condition*, and that condition is the one you are about to create.

The deeper reason: **you identified the subject by the property that makes it worth naming.** A marker is a marker because of its glyph. So you search for the glyph. That is the natural, obvious, correct-feeling way to find it — and it is precisely the attribute that becomes ambiguous the moment the subject takes the control's value.

And there is no failing case to notice. The probe's output is a number, and the number is right, in both the case where the subject was found and the case where the control was found instead. Nothing in the output distinguishes them.

## The general form

**A probe that locates its subject by a property the control also has will silently measure the wrong one — and it degenerates exactly when you are A/B-ing the two, which is the one time you need the comparison to be valid.**

The failure is self-arming. The comparison exists for the case where the two are alike; the lookup collapses into a single row in that case; the assertion then compares that row to itself and passes. The more successful your A/B is at making the two equal, the less your probe is measuring.

**Locate the subject by something only it has.**

Variants, and the same test applies to each:

- **By value instead of identity.** Looking up a record by a field value that the control also carries. Use a unique key: an id, a position, a name.
- **By index instead of content.** `rows[0]` when the list is filtered, sorted, or has a default filter applied — the index names a *different* element the moment the sort changes, which is often the change under test.
- **By shared shape.** Two inputs that both parse to the same normalized form, located by that form.
- **By a container rather than the thing.** Finding the row that *contains* the marker, when the control's row also contains it as a substring.

The diagnostic question, which is the same one that catches every probe that reads the same in both branches:

> **What would this find in the case I am trying to rule out?**

If the answer is "the other one, and the assertion still passes," the probe cannot fail.

## What it costs

A passing assertion on a comparison that was never made.

The cost is proportional to what the passing signal is standing in for. In the small case, it is one unverified measurement. In the expensive case — and this is the common one, because A/B probes sit inside the change they validate — it is a *verification* that supported a decision. The swap was made on the strength of the two aligning. The alignment was never measured.

It also has a nasty property under maintenance: the probe is most likely to be fixed by someone who thinks it is fine, because in the current state it is fine. The defect is latent until the values converge, which is precisely the state a future maintainer is trying to create.

## The defense

**Identify the subject by an attribute the control does not have — and confirm the identity, not just the count.**

Four rules, in order:

1. **Find by the unique thing.** Text, id, key, position — anything that names only the subject. If the subject and the control share every attribute you can search on, add one.
2. **Assert on the identity, not only the measurement.** Capture the discriminator and include it in the assertion or its failure message, so a collapse of the lookup into the wrong row *cannot pass*. If both lookups returning the same row produces a green test, the test is missing the check that matters.
3. **Sabotage it in the degenerate state — that is the state to test in.** Don't verify the probe with distinct values; that case is the easy one. Set the subject equal to the control, run it, and confirm a wrong result *fails* and the message names the right row. This is the general rule for any check: **red-confirm it, and red-confirm it in the case that breaks it**, not the case that flatters it.
4. **Prefer a lookup that cannot be ambiguous** where the tool allows it. A handle assigned at creation beats a search every time.

The rule also applies to change-detectors generally: locate on content, never on a derived aggregate — a length, count, or total collides across the very change you built the detector to catch, and then never fires.

## The trigger

You are writing a lookup that finds one thing among several, and there is another thing nearby that could plausibly match.

Sharpen it with this: **you are about to change the subject to the control's value, or you have been asked to compare two things that are supposed to be the same.** That is the moment the probe collapses, and it is the moment you are least likely to re-check the probe, because it is passing and you have work to do.

The general trigger underneath: any assertion that could be satisfied by both the correct and the incorrect answer — with no case in which it goes red. If you cannot describe the input that would make it fail, the probe is not measuring anything, and its green result is a constant wearing a measurement's clothes.
