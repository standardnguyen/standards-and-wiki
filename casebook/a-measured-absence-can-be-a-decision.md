# A measured absence can be a decision

## The shape

You are bringing something back up and you find it stopped. You do the careful thing — before starting it, you check whether it is supposed to be running:

```bash
systemctl is-enabled file-service
# disabled
```

`disabled`. Against that you have a note, written the day the thing was created, that says *"enabled at boot."* Check and note disagree, and you resolve the conflict the comfortable way: **the note is stale, the world is fine.** You run `enable`, you start it, you move on.

Two hours earlier someone had stopped it and disabled it deliberately, as a containment step, because it served arbitrary file reads to the network without authentication. You have just put that back on the wire, and you will find out why in a log, not in an alarm.

## Why it survives review

Because every step is defensible on its own, and the reasoning is the reasoning you were taught.

The check is real. The value it returned is real. The note is real. Nothing in the sequence is a mistake — the mistake is a single inference, *absence implies accident*, and it is the inference that happens to be wrong.

The uncomfortable read was one command away, and the comfortable one was already half-written by the note. A conflict between what you measured and what you were told has two resolutions, and you will reach for the one that lets you proceed. That is the whole mechanism: **the resolution is chosen for its consequences, not its likelihood.**

It also survives because the check you ran answers a question about the artifact's *configuration*, and you read it as an answer about the world's *intent*. `disabled` is the same string in "nobody ever turned this on" and "someone turned this off an hour ago, on purpose." It has no room in it for *why*.

## The general form

**State is not evidence of intent, and a check that cannot see intent is not a check on it.**

Three sub-shapes, all of which read as diligence:

- **The boolean with one shape.** An enabled/disabled, present/absent, exists/missing reading collapses *never happened* and *deliberately reversed* into one value. It cannot distinguish them, by construction, and it does not say so.
- **The unexercised configuration.** "Enabled at boot" written at creation time is an intention. Until the machine has actually rebooted, nobody has observed it. It has the grammar of a fact and the status of a wish.
- **The proxy liveness check.** Liveness tested by *"is anything listening on the port"* is a check on the port. A free port looks identical to a port that is *supposed* to be free — so the check silently starts something taken down on purpose, and then, once its own process holds the port, reports the intended service healthy.

Every one of these returns a plausible, stable, correct-looking value in both branches.

## What it costs

Whatever the thing does when it runs. Here it was an unauthenticated read path to the whole filesystem, live for ten minutes.

The second cost is larger and less visible: **you have now corrected the world toward your documents.** The note said "enabled at boot," reality said otherwise, and you edited reality. The next reader finds a running service and a note that matches it, and the deliberate stop is now unrecoverable from the state of the machine — the only remaining record is a commit history you did not read.

## The defense

**A stopped thing is a decision until proven otherwise. The burden of proof runs the opposite way from where instinct puts it.**

Before starting anything you find stopped, read the history rather than the configuration: recent commits, open change requests, any note whose *date* is close to the artifact's current state. Prior intent leaves traces there and nowhere else. One `git log` answers it.

And when a measurement and a document disagree, do not resolve the conflict by choosing whichever one lets you proceed. **Name the two readings and check which is true.** "The docs are stale" and "the world is deliberate" are both hypotheses; only one of them has a test.

Fix the check where you can. An enforcement layer that refuses to start a disabled unit, rather than starting it and warning, converts a judgment call into a wall — and the judgment call is exactly what fails under time pressure.

## The trigger

You find something stopped, absent, or disabled, **and your documentation says it should be running.**

That divergence is not a discrepancy to reconcile toward the more convenient side. It is the signature of a decision someone made and did not write down where you are looking — and the tighter you are for time, the more it will look like a stale doc.
