# A test that has never failed is a hypothesis

## The shape

You fix a bug, and you add a test so it cannot come back. The test is well written, specific, and green. You are done.

You are not done. You have written a hypothesis about whether the test can fail.

A test that has never been observed failing is not a regression pin. It is a sentence in the same language as a pin, occupying the same place in the file, providing none of the function. It will pass forever, including — and especially — in the case it was written to exclude.

Two shapes produce this, and both look green.

## Why it survives review

Because green is the only signal you have, and green is what a correct test and an inert test both return.

The test is not obviously wrong. It asserts something true. It names the right function. It reads, to any reviewer including you, as exactly the safeguard it claims to be. There is no moment at which it looks suspicious, because the quality of a test is not visible in its text — only in its behavior under a broken condition, which by construction you have not created.

**Shape 1 — the circular test.** The assertion derives its expectation from the same source it is checking:

```
// passes, and would pass with the category deleted
let all = categories();
block_every(all);
assert!(!has_any_tools_allowed());   // this helper also derives from categories()
```

Delete a category from the source of truth and **both sides move together**. The test still passes. It is checking that a function agrees with itself.

**Shape 2 — the dead sentinel.** A valuable check is nested under a condition on a string or marker that has since changed — or never matched:

```
if status_line.contains("⏎=send") {
    assert_no_deleted_inode(pane);      // never executed
}
```

The sentinel was correct when written. Later, a UI change dropped that segment from the status line. Now the guard never runs, and the surrounding script still reports success — it prints a warning where the guard would have been, and closes with a summary line that reads as confirmation. It went four days unexecuted before anyone checked by hand.

The section of the file below the guard is not obviously dead. It is well-indented and correctly formatted; nothing in the syntax says it has not run since last Tuesday.

## The general form

**A new guard's first green run is not evidence. The evidence is a red run: break the thing it guards, and watch the test fail — and check that the failure names the offender.**

Three things this buys you, and they are different things:

1. **Does it fail at all?** A test with no failing case is not a test. This is what catches the dead sentinel.
2. **Does it fail for the right reason?** A test can go red for a reason unrelated to what it claims to guard. If it fails on a parser error before reaching the assertion, the assertion is unverified and reads as verified.
3. **Is the input strong enough to isolate the mechanism?** The most expensive variant: the assertion is right, but the fixture would satisfy it *anyway*, via a different property. A test named for a prefix check that in fact passes on a downstream id parse will stay green when the prefix check is removed — and the mechanism it names was never exercised.

And the corollary that is not about tests at all: **keep a safety check independent of the readiness check beside it.** When the sentinel is also the thing that gates a warning, a stale sentinel converts a noisy warning into silence, and silence reads as health.

## What it costs

Directly: nothing. That is the problem. The cost is what the coverage claim displaces.

The test is now cited as the reason the bug cannot recur. It appears in a review, in a changelog, in the sentence "pinned by `test_…`". That citation is load-bearing — it is what stops the next person from adding the guard the test was supposed to be. So the cost is not the missing guard, it is the *decision, made on the test's authority, not to build one*.

The dead sentinel costs more, because it is a guard already in production that no longer fires. Everything downstream of it has been running unguarded for the entire period during which the report said it was guarded.

## The defense

**Mutation-check every new pin before you trust it, and red-confirm each one individually.**

One at a time. Break the guarded thing; the test must go red, and the failure output must name what broke. Restore; the test must go green. If you add three pins at once and break all three, a red result tells you nothing about which one works — and one working pin masks two dead ones.

Additional rules, in order of how much they buy:

1. **Assert against the structure directly, not through a helper that derives from the same source.** A test whose expectation and subject share an upstream is checking for internal consistency, not correctness.
2. **Prefer a compile error to a test, where you can get one.** A category that cannot be constructed cannot be forgotten at runtime. This is not always available; when it is, it is strictly stronger.
3. **Locate the subject by something only it has**, not by a shared marker or an equal value (see *the probe that finds its subject by a property the control shares*).
4. **When a guard's sentinel is a string, make the guard independent of the string.** Run it unconditionally, and let the sentinel affect only the message.

## The trigger

You have just written a test and it is green.

Particularly when: the test was added alongside the fix; the fix is in a path you cannot easily exercise; or you cannot articulate the input that would make the test fail. If you cannot say what would turn it red, you have not established that anything can.

Second trigger: a guard whose output you have never seen fire. An unexercised guard is not known-dead — it is unmeasured. Break the condition once and watch.
