# The summary compresses out the qualifier

## The shape

You get a detail right, and you get the caveat right inside it. The page says:

> reproduces the archived output byte-for-byte, apart from one intentionally stripped trailing byte

Then you write the one-line version for the index:

> regression-tested, byte-identical

Both are yours. Both are in the same commit. The second is a summary of the first, and summing up is a lossy operation — the qualifier is the highest-entropy thing in the sentence, so it is the first thing compression drops.

Months later a reader loads the index, not the page. They now hold the unqualified claim, sourced from a summary, which is a surface that *reads more authoritative than the page it summarizes* precisely because it is shorter.

## Why it survives review

Nothing here is dishonest and nothing is careless. The summary was written by someone who had just read the detail, which is exactly the person least able to see what they dropped — they still hold the caveat in working memory, so the short version *feels* complete to them.

It is also not the same artifact as the thing it summarizes. The detail page is the author's; the index row, the status line, the glossary cell, the task title, the changelog entry, the log's summary — those live elsewhere, are read by different people, and are not re-read by the person who wrote the detail. The caveat is dropped at a boundary between two documents, which is why the author never sees it happen.

And the summary is often written *first*, or written last in a hurry. Either way it is the artifact most likely to be the only one anyone reads.

## The general form

**A summary is a lossy transform, and the loss is systematically biased toward the qualifier.**

Qualifiers are long, they are conditional, and they are the part you already understood. Everything in the compression impulse points at cutting them. The result is not a wrong summary — it is an *overconfident* one, which is worse, because the reader has no signal that anything was omitted.

Three surfaces it happens on, all of which a cold reader hits before the detail:

| surface | what it does |
|---|---|
| index row / status line | compresses a caveat into a status word |
| glossary cell / shared reference | compresses a nuance into a definition, and is read by everyone |
| task title / heading | compresses into the one place a list view shows |

**The status line is the sharpest case**, because a status is a claim in the present tense that nobody re-runs. A row reading *"change pending explicit authorization"* stayed that way for eleven weeks after the change had landed — and the effect was not merely a stale fact: downstream readers concluded their own capture was behind, and looked for a gap that did not exist.

## What it costs

Everything the detail page was careful about, undone at the layer most people read.

The compounding is the expensive part. A summary is a citation for the *next* summary, and the qualifier does not survive the second hop either. A reader who only ever sees the index never learns there was a caveat to look for.

And a summary can disable a *future* check. One of these was a note claiming a fact appeared in exactly one place — false, and it would have suppressed the next sweep, which would have read the claim and skipped the files the claim said were clean. **A wrong summary does not just misinform; it can turn off the mechanism that would have caught it.**

## The defense

**Carry the qualifier into the summary, or carry nothing.**

If the short version cannot hold the caveat, the short version should not make the claim. A status word that means "verified, with a known exception" is not compressible to "verified" — write *"verified, one known exception, see detail"* and let the length of the summary signal that something is being held back.

**When a summary and its detail disagree, the detail is right and the summary is the bug.** Decide this in advance, because in the moment the summary will feel like the more considered artifact.

**And treat the summary layer as a separate deliverable of a correction, not a trailing chore.** A correction is not finished until its summaries are. Practically: enumerate the summary surfaces that mention the thing — the index, the status line, the shared reference, the heading, the log's own summary — and grep each of them for the old value. The detail page is one artifact. The summaries are usually four or five, in files the corrector was never looking at.

This is the step that gets skipped, because writing the correction *feels* like the work and the summaries feel like copying.

## The trigger

**You have just written a caveat, and now you are writing the one-line version of it.**

Also: you are writing a title, status, or summary row in the same commit that changes its body. And the inverse — you are *correcting* something and the correction lands in a new section while the summary forty lines away, the part a hurried reader acts on, still carries the superseded instruction.

The pull to compress is strongest immediately after you understand something. That is the moment to be slowest.
