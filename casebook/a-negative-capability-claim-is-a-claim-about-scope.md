# A negative capability claim is a claim about scope

## The shape

You need a feature the current dependency does not appear to offer. You search its source:

```bash
grep -rn "cell_link\|hyperlink" ./vendor/ui-lib/
```

Zero hits. Nothing in the type holding a cell's contents has a field for it. You write it down: *the library cannot do this.* The ticket is marked blocked upstream. It does not resurface for a day.

The next release of that library shipped exactly this, with tests named after the feature.

Your search was correct about the code it read. The code it read was the version pinned in your lockfile — a slice of the question you were actually asking. You searched a snapshot and reported a property of the world.

## Why it survives review

Because a negative *feels* like a finding, and it is the cheapest one available.

`0 hits` is unambiguous, reproducible, and obtained by doing the diligent thing. It has the grammar of evidence. And a negative carries an **implicit scope that is invisible in the output** — the same `0 hits` appears whether you searched a folder, a version, or everything. The command answered *how many are in the set I searched*; the sentence you wrote claimed *how many exist*. Only one of those was asked.

It is worse when the claim is written down, because writing launders it. A reader now receives *"X cannot do Y"* at the strongest evidence tier available to them, indistinguishable from a verified structural fact about the library's design.

## The general form

**"X cannot do Y" is never a fact about X. It is a fact about the breadth of your search, restated as a fact about X.**

The recurring ways a search is narrower than it feels:

| scope error | what it hides |
|---|---|
| **The pinned version** | a capability added later — the worst case, since it converts a scheduled upgrade into a permanent blocker |
| **A default-filtered listing** | closed items, archived rows, hidden entries — absent by default, not by fact |
| **A code-split bundle** | everything in the chunk not loaded on this path |
| **The wrong module** | a symbol that moved into a subpackage — one grep can be right on the facade and wrong in the same version |
| **A truncated output** | a match the display cut removed |
| **Case and naming** | a field whose spelling you guessed |

The version axis is the one to internalize, because it **looks like architecture rather than staleness.** A missing capability in the current source is a genuinely strong finding. Generalize it one release forward and it becomes a false structural claim — and a false structural claim puts work on the impossible pile, where nobody re-examines it.

There is also a tell that is present, unread, and diagnostic: **the file you searched contained no such code at all** — not a variant, not a partial, nothing. When an entire subsystem is absent from where it obviously belongs, the right question is *"then where is it?"* It is almost never *"then there is none."*

## What it costs

The feature is not merely unbuilt. It is **classified** — as impossible, and therefore as decided. An unbuilt capability gets built. One marked "cannot be done upstream" gets closed honestly, and closing it is what prevents anyone revisiting it.

The second cost is that the classification propagates into planning language: a roadmap that drops a dependency of the work, a card that says "blocked, no path," a decision record that makes the absence structural. By the time someone re-checks, the claim is a premise.

And the failure is durable in a specific way: it is exactly the kind of statement that gets written into a rule. Never persist *"this tool doesn't do X"* — an environment-specific or version-specific refusal hardens into a capability claim the agent then cites against itself long after the fix.

## The defense

1. **Complete the sentence before you write it.** *"X cannot do Y **in \<set\>** as of **\<point in time\>**."* If either slot is empty you have a count, not a conclusion — and neither qualifier is recoverable later by a reader.
2. **Name what sits outside the set, explicitly.** A version, a chunk, a filtered view, a truncated read, a wrong package. "The source" does not mean "everything"; it means the tree you happened to have.
3. **When a whole subsystem is missing from where it should be, stop and go higher.** Enumerate the directory, enumerate the modules, query the package index rather than the local checkout. *Where is it* beats *where isn't it*.
4. **Beware the second negative.** Two empty searches agreeing is not corroboration when both searched the same wrong axis — and re-checking an upgrade can return zero hits for an unrelated reason, the code having moved into a subpackage. Agreement tells you about the searcher, not the world.
5. **Probe instead of asserting, wherever the claim is one command from being testable.** The API you declared absent may answer on the first call — an assertion that cost one invocation to test went untested for weeks and was wrong.

## The trigger

Any time the next sentence you are about to write contains **"cannot," "does not support," "not possible," "blocked upstream,"** or **"there is no way to"** — and no command in this session tested the *scope* of the claim, only its content.

Especially: a capability question about a dependency, where the answer is true of the version on disk and false of the library.

And the sharpest tell: you searched somewhere that should have been full of the thing and found nothing. Believe the surprise, not the emptiness.
