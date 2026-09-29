# A rule can be the hazard

## The shape

Your documentation contains a command. Not a description of a command — the command, character for character, meant to be pasted:

```bash
# from the runbook: "How to call the API from a shell"
source ~/.rcfile && api-client list
```

It works. It loads the credential and the call succeeds. It is also, every single time it is obeyed, printing whatever `~/.rcfile` prints — and on the day the secrets store behind that file returned an empty result, the render line inside it collapsed to a bare `export`, which in POSIX shells prints **every exported variable with its value**. The prefix dumped the entire environment to stdout.

The session was opening its own change request at the time. It was being careful, and it was being careful *by following the documented procedure* — which is the whole point.

The full output landed in a transcript: a dozen credentials across several unrelated systems.

## Why it survives review

Because documentation is reviewed for **intent** and never executed.

A reviewer of that line asks *does this correctly load the credential?* It does. Nobody asks *what else does this line print?* The output is not in the document, so it cannot be reviewed. The line's behavior is a property of a file somewhere else on the machine, and that file is not part of the diff.

Then the line *works*, which reads as verification. Extra output scrolls past as shell noise, or is piped into a `head`, or is truncated by the tool that captured it — and a directive that scrolled past unread is not distinguishable, from inside the session, from one that printed nothing.

## The general form

**An instruction is executable content. A procedure that contains a command is not advice — it is code that every obedient reader runs with their own privileges.**

That makes the instruction layer a place hazards *accumulate*, and there they are worse than the same hazard in application code, for three reasons:

1. **They are executed by careful people.** The reader is not cutting a corner. They are doing the thing they were told to do, which is the only thing they can be doing.
2. **They replicate by obedience.** One bad line in a procedure becomes one execution per reader, per session, forever — a payload with a scheduler.
3. **They misdirect the correction.** The interesting failure is fixed at the *environment*, not in the prose. Here the shell init file was made quiet at the source, and the call sites were left as-is, because their safety was always a property of the file being sourced, never of the line sourcing it.

**"I followed the instructions" is not a safety property.** It is a claim about provenance. Safety is a property of what actually ran, and an instruction can make the unsafe thing the compliant thing.

## What it costs

The first cost is the leak itself: an exposure produced *by* the control that existed to prevent bad handling.

The second is worse and less visible — **the hazard and its remedy are the same artifact.** You cannot tell a reader "don't run that" without editing the document you are telling them to read, and until you do, every session that reads it faithfully re-arms the incident. Provenance-shaped reassurance ("we have a secrets section") coexists perfectly with a rulebook that violates it.

And the fix has a direction that is easy to get backwards. If the leak comes from the environment the line touches, rewriting the call sites fixes nothing and is a lot of edits; quieting the environment fixes all of them at once.

## The defense

1. **Run the instruction once, as a command, and read the whole output — not the exit code.** Exit 0 is what a successful leak looks like too. What you are auditing is the *bytes*: everything a reader with your privileges would see printed.
2. **Ask the reviewing question differently.** Not *is this command correct?* but *if a reader pastes this exactly, what is the complete set of side effects?* If you cannot answer from the line alone, the line is not yet safe to publish.
3. **Separate loading from printing.** If the command must pull in secrets, suppress the side channel rather than the effect:

```bash
( source ~/.rcfile >/dev/null 2>&1; api-client list )
```

The parentheses matter. A bare redirect is one edit away from being nothing, and the next person editing that line will not know what it was holding back.
4. **Fix the shared upstream, then pin the invariant.** If the environment is what emits, make it emit zero bytes, and add a check that asserts exactly that — proven against a deliberately noisy stand-in first, so you know the check can fail.

## The trigger

You are writing or copying a command into anything durable: documentation, a runbook, a code comment, a ticket, a rulebook.

Second trigger: you are following an instruction and it produced output you did not expect — extra lines, an unfamiliar block, something a pipe swallowed. Stop and read it. "It worked anyway" is orthogonal to "it printed something."

Third: a safety instruction whose safety depends on the current state of some *other* file. That is a rule that will become false without anyone editing it.
