# The relief valve wired to the kill switch

## The shape

A long-running process can hit a wall — the context window fills, a queue backs up, a quota is consumed. So you build two things:

- **A kill switch** — a hard ceiling. Past this, stop. It exists so the failure is clean rather than catastrophic.
- **A relief valve** — an earlier, gentler trigger. Before the ceiling, do something that relieves the pressure: summarize, flush, back off, rotate.

The valve is set below the kill switch. That is the whole design: the soft limit fires first and the hard limit never has to.

```toml
# relief valve: 50% of window
trigger = ctx_max / 2      # 1,000,000 -> 500,000
# kill switch: per-turn token budget
budget  = 500_000          # a literal constant
```

Both limits read the same counter, on the same dimension, at the same number. The valve is not below the kill switch. It is the same number, and the comparison runs in that order.

## Why it survives review

Because **on the machine where it was built, the numbers were never close.**

The valve is expressed as a fraction of a per-model value; the kill switch is a fixed constant. On a small-context model the fraction lands five times below the constant, the valve fires reliably, the behavior is correct, and the design reads as sound for months.

The collision is a property of the *ratio*, and the ratio is a property of which model is in front of it. Change the model — a context window several times larger — and the fraction slides straight through the constant. Nothing in the code changed. Nothing in the config changed. The same expression that produced a comfortable gap now produces an exact tie.

And an exact tie resolves against the valve, because the kill switch's comparison runs first in the loop. The valve's turn never starts. It is not that the valve fires late; it has no ordering in which it can fire at all.

The second layer of why it survives: **there is a test pinning the claim that the two are independent.** It asserts the reassurance. It names the failure mode it denies. It passes, and it is the reason nobody looked, because it converts a design question into a settled fact.

## The general form

**A relief valve and a kill switch must be limited on different dimensions, not on different numbers along the same one.** Two limits on one axis means the stricter always preempts the looser — by definition, not by accident — and whichever one the code evaluates first is the only one that exists.

Numeric separation is not a defense. It holds only for the values it currently holds, and the values move: a window changes with a model, a budget with a config, a timeout with a network. **A gap you are not measuring will be crossed by someone else's change.**

The tell is always the same shape: two constants that are *supposed* to differ, related to each other by nothing except a remembered inequality.

Common instances, by dimension pairs that are actually independent:

- **Timeout vs. retry budget** — one is time, one is count.
- **Quota vs. backoff** — one is consumption, one is rate.
- **Context-window fraction vs. request-size absolute** — a ratio of the model's limit vs. a fixed byte count.
- **Disk watermark vs. log rotation size.**

The failure signature of the same-axis version: the valve is *never observed to fire*, and it gets read as the valve being broken. Someone investigates the valve's implementation, finds it correct — it is — and the real finding is that the valve and the kill switch are the same limit wearing two names.

There is a third cost when the two are meant to compose in a chain: the state machine behind the valve may never be reachable at all. A valve whose trigger collides with its ceiling is a valve whose downstream states are dead code.

## What it costs

The wall the valve existed to prevent, arriving exactly as designed-against.

The specific cost is that the process stops mid-task, in the state the ceiling was built to avoid — with partial work done and no relief applied, because relief was scheduled for a moment that the ceiling always gets to first.

The compounding cost is diagnostic. The stop is reported by the kill switch, which names the ceiling — a number that looks correct and a condition that looks like it fired as intended. Nothing in the output points at the valve. Time goes into the ceiling being hit: was the task too big? Is the ceiling too low? Both plausible, both wrong, because the ceiling is working and the valve is unreachable.

**And the hazard is often already written down, in a comment on the offending line, and it still fires.** A note next to a constant is read when the constant is edited and not when a different expression makes it collide. Put the hazard where the *decision* is made, not where the code is.

## The defense

**Decouple by dimension.** Not by picking better numbers.

If the valve must live on the same axis as the ceiling, the valve gets a different *kind* of measurement:

1. **Cumulative vs. per-unit.** A ceiling on a single turn's cost and a valve on the session's cumulative cost are different quantities. They cannot tie, at any window size. If no cumulative counter exists yet, building one is the fix — it is upstream of the threshold, not downstream.
2. **Rate vs. total.** A ceiling on instantaneous use and a valve on sustained rate.
3. **Ratio vs. absolute, with a floor/ceiling in the definition.** If a fraction is inherently meaningful, clamp the derived value so it cannot approach the constant — and then *measure the actual gap on every model you support*, rather than asserting it.
4. **Make the tie a test.** If the values must be compared, write a test that asserts the valve's threshold is strictly below the ceiling **for the largest configuration in use**, not for the one you happen to run. And red-confirm it: set the fraction to collide deliberately and watch it fail. A test that asserts independence without observing a collision is the reassurance, not the check.
5. **Watch it fire once.** This is the cheapest and most-skipped step. An automatic valve whose trigger you have never observed is a hypothesis. Run a session big enough to cross the valve's threshold and confirm the relief event appears *before* the ceiling, in the log, without an intervening error.

## The trigger

You are adding a soft limit in front of a hard one.

Do not ask whether the valve is below the kill switch. Ask **what dimensions they are each measuring.** If the answer is "the same one," they do not have an ordering problem to solve — they have a design problem, and tuning the numbers will appear to fix it right up until the ratio changes.

Also: any time a limit is expressed as a fraction of a value that varies by environment or configuration, and its comparison partner is a literal. That pair is a coincidence of the current configuration, and nothing holds it in place.
