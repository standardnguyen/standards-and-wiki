# Zero occurrences is not absence

## The shape

You need to know whether something exists. You search:

```bash
grep -rn "hyperlink" ./vendor/library/
```

Zero hits. You conclude the library cannot do this. You write it down, mark the ticket blocked, and move on.

The count is exactly right. The conclusion is false.

The search was run against the **pinned version**. The feature was added two minor versions later, in a module that did not exist in the version on disk. Your grep was correct about the tree it read, and the tree it read was a slice of the question you were actually asking.

## Why it survives review

Because a search either finds something or it does not, and "it does not" feels like data. It is the cheapest possible answer, it is unambiguous, and it is *correct* — the command did what it said. Nothing about it is sloppy. Running a grep is what careful people do.

The failure is not in the execution. It is that a negative carries an **implicit scope**, and the scope is invisible in the output. `0 hits` looks the same whether you searched the whole world or one folder. The number answers *how many did I find in the set I searched*; the conclusion you drew was *how many exist*. Those are different questions, and only one of them was asked.

There is also a specific tell that is present and routinely unread. **The searched file contained no such code at all** — not a partial match, not a variant, nothing. The right response to an entire subsystem being absent from a file that should contain it is *"then where is it?"* It is almost never *"then there is none."* An empty result in a place you expected to be full is a signal that you have the wrong place.

## The general form

**A negative result is only as wide as the search that produced it. Before writing "X does not exist", name the set you searched and ask what lies outside it.**

The recurring ways a search is narrower than it feels:

| scope error | what it hides |
|---|---|
| **The pinned version** | a capability added later — the worst case, because it converts a scheduled upgrade into a permanent blocker |
| **A code-split bundle** | everything in the chunk that is not loaded on this path |
| **A default-filtered listing** | closed items, archived rows, hidden entries — absent by default, not by fact |
| **A truncated line** | a match sitting past the display cut |
| **Case sensitivity** | a field whose casing you guessed |
| **The wrong module** | a symbol that moved out of the facade you searched — a *single* grep can be right on file A and wrong on file B within the same version |
| **Text rendered into an image or canvas** | content a DOM-text extractor silently drops |
| **A dependency's optional features** | a package listed in a lockfile but never compiled in |

The version axis deserves separate emphasis, because it is the one that **looks like architecture rather than staleness**. A missing capability in the source genuinely is a strong finding — when the source is the current one. Generalized one version forward, it becomes a false structural claim, and a false structural claim puts a task on the "impossible" pile where nobody re-examines it.

The effect compounds: the claim is written down, it reads as a finding, and a future reader gets it back as a `[read:]`-tier fact about the library's design.

## What it costs

An expensive feature gets declared impossible.

The specific cost is not the missing capability — it is the *classification*. A capability that is merely unbuilt gets built. A capability marked "cannot be done upstream" is closed, and closed honestly, and nobody reopens it. The card looks like a decision rather than a question.

The second cost is that the error survives the correction that nearly repeated it. Re-checking the newer version also returned zero hits — for an unrelated reason: the relevant structure had moved into a sub-crate in that release, so the top-level package was again the wrong thing to search. **Two zero-hit greps, both meaningless, and nothing in the output of either one said so.** An independent-looking second negative is not a second source.

## The defense

**Separate the count from the scope, and write both down.**

Before "X does not exist", complete the sentence: *"X does not exist **in <set>** as of **<point in time>**."* If you cannot fill both slots, you have a count, not a conclusion. Both qualifiers are cheap to include and neither one can be recovered later by a reader.

Then, in order:

1. **Ask what sits outside the set.** Is this a version, a chunk, a filtered view, a truncated read, a wrong package? Name it explicitly rather than assuming "the source" means "everything."
2. **Prefer source over prose — but confirm the source is the current one.** Vendor docs, changelogs, the package registry's own release list, `--help`, the actual compiled artifacts. A version bump's diff answers the version question directly.
3. **When an entire subsystem is missing from where it should be, stop searching and go higher.** Enumerate the directory. Enumerate the modules. Search the language's package registry rather than the local checkout. *"Then where is it?"* is a more productive question than *"then where isn't it?"*
4. **Beware the second negative.** Two empty searches agreeing is not corroboration when both searched the same wrong axis. Agreement tells you about the searcher, not the world.

## The trigger

Any time you are about to write **"cannot", "does not support", "not possible", "blocked upstream", or "nowhere"** — and no command in this session tested the *scope* of the claim, only its content.

Especially: a capability question about a dependency. That is where the pinned-version axis does its damage, because the answer is true of the box you searched and false of the library, and only one of those is the thing your task depends on.

And the sharpest tell of all: you searched for something in a place that seemed like it should be full of it, and found nothing. Believe the surprise.
