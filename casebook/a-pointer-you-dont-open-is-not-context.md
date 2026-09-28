# A pointer you don't open is not context

## The shape

Retrieval runs and surfaces the right document — the one that is load-bearing for the task at hand. It arrives as a path, a title, and a one-line description:

```
◆ search · operations/tooling-notes.md — Tooling notes · prepared scripts, list IDs, do-not-delete rules
```

The agent sees it. It reads the title. It then greps that same file for the one concrete value it needs — a list ID — never opens the section holding the prepared tool that would have done the entire job, and builds the tool from scratch.

Twice. And the second build is the exact approach the surfaced document explicitly forbids.

Delivery was perfect. Consumption was zero.

## Why it survives review

Because **delivery is instrumented and consumption is not.** A retrieval layer can prove it returned a pointer: the pointer is right there in the transcript. Nothing in the harness can prove the pointer changed what happened. So the one measurement that exists is green by construction, and it measures the half that isn't failing.

From the inside, naming a file does not feel like absence — it feels like *having handled it*. A filename is a strong enough cue that naming it can substitute for opening it, and it also suppresses the search you would otherwise have run. The failure is invisible precisely because it produces the sensation of success.

There is a readable tell, and it is usually unread: **the document was named in the output and no sentence from it appears anywhere in your reasoning.** You can cite the path; you cannot quote the page.

## The general form

**A pointer is a promise of context, not context.** The exchange rate is not one to one. Value is realized only at the moment something is opened, and the presence of a pointer is not evidence that an opening happened.

Three corollaries worth carrying:

- **A specific question is what makes a pointer go unopened.** When you know exactly what you need, a surfaced document becomes a *lookup* — grep it for the keyword and leave. But a document's most valuable content is exactly what you cannot grep for, because you do not know it is there. You only find it by reading.
- **An index is not its contents, and a *growing* index is worse than a short one.** More pointers means more retrievals that resolve to nothing while registering as successful. An index can also be confidently wrong about what exists — a location table that has drifted makes a reader conclude the thing is absent when it is merely unfiled.
- **The moment of risk is not the moment of reading.** A pointer is consumed long before the action it governs. By the time someone is about to do the damaging thing, they are not re-reading.

## What it costs

The exact work the document existed to prevent, redone — and redone in the forbidden shape, because the prohibitions live in the part that was not read. A pointer that lands and is not opened converts a solved problem into a reinvented one, and the reinvention inherits the failure the document was written to record.

The second cost is a corrupted feedback loop. Retrieval appears to be working — it keeps surfacing things — so the intervention is judged successful while the behavior it was built to change is unchanged. That is worse than no retrieval, because it closes the question.

## The defense

1. **Make the pointer cost one command to consume — or don't ship pointers.** "Open it" fails as advice; it has been tried. Inlining the top hit's best-matching section *does* work, because the knowledge lands whether or not anything gets read. If you control the retrieval layer, the fix lives there, not in a rule telling readers to follow links.
2. **Treat a surfaced path as an obligation, not a notification.** If you noticed a file and did not open it, you have not had the context. Open it before the first write that the file governs — and scope the obligation by *touching the system*, not by editing files in its directory. The dangerous case is the document that governs a system you can operate without ever writing inside its folder.
3. **Verify consumption, not delivery.** One question, after the fact: can you quote a sentence from the document? If not, it did not land. Delivery assertions are always green; they cannot answer this.
4. **When you write a pointer, put the part that must not be missed inline, at the site where the mistake would be made.** A warning that has to be followed is a warning that will be skipped at exactly the moment it matters.

## The trigger

You are about to do something, and you can name the document that covers it without having read it.

Or: a search result, an injected block, or a teammate's message named a file, and your next action is a targeted grep of that file rather than reading it.

And the meta-trigger: your retrieval is working — things keep being surfaced. Ask what landed. Delivery metrics do not go red for this failure; they go green.
