# Laundered confidence

## The shape

A session reasons its way to a plausible conclusion. It is not certain — the reasoning was a mechanism, an inference, a synthesis of two things that seemed to fit. It says so out loud, hedged, in conversation:

> "if we're reading that right, it's probably X"

Then it writes the page. Pages are declarative; that is what a wiki is for. The sentence that lands on disk is:

> X.

Six weeks later, a different session needs to know about X. It greps, finds the page, and now holds a claim sourced `[read: page.md:14]` — the *strongest* evidence tier it has, stronger than anything it could derive itself. It acts on X. It writes X into a second page, cites the first. Eventually X goes into a bug report, or a vendor email, or a message to someone's doctor.

Nobody lied. Nobody was careless. The uncertainty was stated. It simply did not survive the transition from speech to storage.

## Why it survives review

Because at no single step does anything look wrong.

The hedge was real — it happened, it is in the transcript. The page is written in the house style, which is declarative, because a wiki full of "possibly" and "we think" is a wiki nobody can act on. And the later session is doing *exactly what it should*: preferring a written source over its own recollection. That is the correct instinct. It is the whole reason the wiki exists.

The failure is invisible from inside because **the page looks like evidence.** There is no visible difference between a sentence someone verified and a sentence someone inferred. Once written, they are the same bytes.

This is the systematic failure mode of any durable knowledge store maintained by the same agent that consults it. The store is supposed to be a memory; it is also, unavoidably, a laundry.

## The general form

**Writing a claim down promotes its evidence tier without adding evidence.**

Three tiers, weakest to strongest:

| tag | means | strength |
|---|---|---|
| `[recalled: …]` | we believe this | weakest — and reads as authoritative anyway |
| `[read: file:line]` | it is written here | strong |
| `[ran: <command> → <output>]` | we observed it | strongest |

The laundering is the move from tier 1 to tier 2 performed by the act of writing. No new observation occurred. The claim got stronger anyway.

**A spoken hedge does not travel with a written claim.** This is the part worth internalizing: qualifying something in conversation and then recording it flatly is *worse than not hedging at all*, because it purchases the feeling of having been careful while leaving the assertion unqualified on disk. The care went into the channel that gets discarded.

## What it costs

Proportional to how far the claim travels and how long it lives. The expensive cases share a signature: the claim leaves the system that produced it. A note-to-self can be wrong cheaply. The same sentence relayed to a vendor, a doctor, a colleague, or a court arrives carrying the full authority of a written record, and the person receiving it has no way to see that it started as a maybe.

The second cost is compounding. A laundered claim becomes a citation for the next claim, and by the third generation the original hedge is not merely lost, it is *unreachable* — there is no thread back to it.

## The defense

Three rules, in order of how much they buy you:

**1. Mark it unverified at write time.** Not in conversation — in the file. If a claim was worth hedging out loud, the hedge belongs in the artifact. An inference, a plausible mechanism, an LLM's synthesis, a workflow's output: these are hypotheses. Write them as hypotheses, or wait until you can write them as observations.

If that feels like it clutters the page, the alternative is a page that cannot be distinguished from a verified one, which is the entire problem.

**2. Re-verify before relaying outside the store.** However authoritative the page sounds. The trigger is *the claim leaving the building* — going to a vendor, a bug report, a person who will act on it. Check it against the primary source at that moment. This is usually seconds and it is the single highest-value check in this book.

**3. Carry the qualifier into the summary, or carry nothing.** The laundering is worst at the summary layer — index rows, status lines, glossary cells, changelog entries. The detail page usually gets the caveat right; the one-line summary compresses it out; and the summary is what a cold reader loads *first*. When a summary and its detail page disagree, the detail page is right and the summary is the bug.

Corollary: **a correction is not finished until its summaries are.**

## The trigger

You are about to write down something you worked out rather than something you observed.

The specific feeling to watch for is *having earned it* — you searched three times and found it on the fourth, you reasoned carefully through a mechanism, the pieces finally fit. That effort is real and it feels like verification. It is not. Effort spent reaching a conclusion is evidence about your persistence, not about the world.
