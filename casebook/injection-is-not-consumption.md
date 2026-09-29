# Injection is not consumption

## The shape

A session is asked how long it has been working. It answers with a number shaped from narrative feel — "about three and a half hours" — and moves on.

The exact current time had been stamped into **every single turn** of that session, including the first one. The value was in context, adjacent to the answer, refreshed continuously, and free. Nothing consulted it.

Delivery: perfect. Consumption: zero. Actual duration: under two hours.

## Why it survives review

Because "it was in context" and "it was used" are recorded the same way in the transcript.

Any system that injects context — a retrieval hook, a status stamp, a system-prompt section, a tool's mounted route, a loaded rules file — can demonstrate *arrival*. It cannot demonstrate *consultation*. So the pipeline is green by construction, and the failure happens one layer downstream in a place with no instrumentation at all.

And the failure state is self-concealing. **Confabulation does not feel like guessing.** An invented number arrives with the same texture as a retrieved one, so the internal check that would fire on "I don't know" never fires — there is no felt gap to notice, and noticing a gap is the only thing that triggers a lookup. Data present, lookup never fired, no alarm anywhere.

The same shape appears whenever a capability is assumed live. One session reasoned about its own tool routes — "they're mounted in my list, so they work" — and wrote around a broken connection. A mounted route is not a live connection. A loaded rule is not an applied rule.

## The general form

**Handed-to-you context only helps when you notice you are missing something — and the states where you most need it are the states where you don't notice.**

Delivery and consumption are separate axes, and every system that tests only the first will report success through every instance of the second. The sharper version: **the presence of injected context can suppress the search it was meant to replace**, because "I already have that" and "I just used that" feel identical from inside.

Two consequences:

- **More injection does not fix it.** A larger context window makes arrival cheaper and does nothing for consultation; it can make it worse by making arrival feel like coverage.
- **An answer that is confidently wrong and an answer that is confidently right are indistinguishable at generation time.** No amount of care in *how* you answer substitutes for the lookup you did not perform.

## What it costs

A number, a capability claim, or a date enters the record with the full confidence of a looked-up value and none of the substance. It is then load-bearing: someone schedules against it, plans on it, or cites it later as a fact about what happened.

The second cost is on the pipeline's side. Because the instrumentation measures arrival, every incident reads as *the injection failed*. Long stretches get spent debugging a delivery path that was never broken, while the actual defect — nothing reads what is delivered — sits in no test at all. From outside, "the injection didn't fire" and "the injection fired and was ignored" look identical.

## The defense

1. **Make the value load-bearing and unmentioned.** If you are testing whether injected context lands, never name the mechanism in the prompt. Naming it is the tell that invalidates the test — an agent asked to consult something will consult it. The pass condition is reaching for it *unprompted*.
2. **Ask rather than assert.** Reading the clock is a decision to consult; being asked the time is a decision to look. Any harness that is *asked* will look. The failure case is that nothing asked.
3. **Treat the absence of a lookup as the default for every number you did not run a command for.** The gate cannot be "do I feel uncertain" — certainty is exactly the state where the check does not fire. Run it unconditionally, or tag the claim as recalled.
4. **Separate the axes when you verify anything: did it arrive, and did it change anything.** Arrival has cheap, binary, externally checkable proofs. Consumption does not, which is why it is the one that gets skipped. Grade consumption from what the agent *did*, not from what it says it knows.

## The trigger

You are about to state a fact you did not look up: a duration, a count, a date, whether a feature works, whether a service is up.

Watch especially for a claim that feels *recalled*. That feeling is the unreliable instrument. And watch for the specific internal sentence *"I already have that"* — it is what a missing lookup feels like from the inside.
