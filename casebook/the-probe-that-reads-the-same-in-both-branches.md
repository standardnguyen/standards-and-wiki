# The probe that reads the same in both branches

## The shape

You want to know whether something happened. You reach for a quick measurement:

```bash
stat -c%s "$OUTPUT_PATH"     # did the job write anything?
```

It returns a number. The number looks reasonable. You proceed.

But `$OUTPUT_PATH` is a symlink, and `stat` without `-L` measures the *link*, not the target — so it returns the byte length of the path string. A job that wrote a gigabyte and a job that wrote nothing at all produce the identical reading.

## Why it survives review

Because it is not wrong in a way that produces an error. It produces a plausible number, every time, forever. There is no failing case to notice — the reading is stable, which reads as *reliable*.

And the reason nobody checks is structural: you reach for a probe precisely when you are in a hurry. A test gets scrutiny because writing tests is the activity where scrutiny lives. A probe is the thing you type to find out whether you need to be scrutinizing at all, so it gets none.

## The general form

**A probe that returns the same value in the case you are testing for and the case you are ruling out is not a measurement. It is a constant with a plausible shape.**

The question to ask before trusting any measurement is not "is this correct?" — you cannot answer that about a probe you just invented. The question is:

> **What would this read in the case we are trying to rule out?**

If the answer is "the same thing," you have learned nothing, and worse, you now believe something.

## What it costs

The specific cost is small; the general cost is that it does not fail loudly *once*. A probe that lies is not a wrong answer, it is a wrong answer you will keep consulting. Every subsequent decision inherits it, and because the reading is stable, nothing downstream ever contradicts it.

## The defense

**Control it against a known positive before you trust its negatives.**

Point the probe at a case whose answer you already know. If it cannot reproduce an answer you are certain of, it is reporting on the wrong layer — and *that* is the finding, not a nuisance to work around. Believe the control.

This is cheap. It is usually one extra invocation. It is skipped because the probe already returned something.

Two specific variants worth knowing, since both defeat a naive control:

- **Locating the subject by a property the control also has.** `rows.find(MARKER)` silently measures the *first* row carrying that marker. The moment the subject is set to the control's value, the check passes without ever examining the subject — so it degenerates exactly when you are A/B-ing the two, which is when you need it. Locate the subject by something only it has.
- **Keying a change-detector on a derived aggregate.** A length, a count, a total, a file size — these collide across the very change you built the detector to catch. Key on content.

## The trigger

The moment you write a measurement you have never run before and immediately believe its output.

Also: any time you find yourself relieved by a reading. Relief is not evidence. It is the feeling produced by both a working system and a broken instrument, and you cannot tell which from the inside.
