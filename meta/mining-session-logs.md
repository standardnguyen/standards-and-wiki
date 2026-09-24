# Mining Your Agent Session Logs

Every session your agent runs produces two artifacts: the **work** (edits, commits) and the **record of how it got there** (the transcript, and — if you keep the discipline this template ships — a distilled session log). Most people keep the first and let the second evaporate. That's leaving value on the table: your session history is a queryable memory of every decision, dead end, and fix you and your agent have ever made together.

This page is the template's answer to "how do I actually use that history." It's deliberately low-tech — the expensive version of this idea is a vector database over embedded session summaries; the version here is markdown and grep, and it covers most of the same ground for free.

## The three layers

**1. Session logs — the distilled layer (this template's pattern).** Append-only markdown logs of what each working session decided and why, one row per session in an index, one file per session for the narrative (Protocol 5 sets this up per project). This is the layer worth the most per byte, because it's *written to be retrieved*: decisions, rejected alternatives, and gotchas, in prose, with dates. Grepping "why did we pick X" against session logs works because a past session wrote a sentence answering it.

**2. Raw transcripts — the complete layer.** Your agent runner keeps full transcripts somewhere (Claude Code: `~/.claude/projects/<project>/*.jsonl`) — but usually with a **retention window**, after which they're deleted. If you want the complete record, archive them before the runner ages them out. The dumbest thing that works: a cron job that `rsync`s the transcript directory into a git repo **without `--delete`**, so the archive only ever grows — when the runner deletes an old transcript, the archive keeps its copy. Now "what did we discuss about X months ago" is one `grep -r` away, forever.

**3. Retrieval — grep first, RAG optional.** Naive grep over layers 1–2 answers most questions: performance self-reviews ("what did I actually ship this year"), decision archaeology ("when did we change the backup strategy and what did we reject"), incident lookups ("have we seen this error before"), onboarding a new machine or teammate. If your history outgrows grep, the same corpus is exactly what you'd feed a RAG pipeline — vectorize the session *summaries* (layer 1), not the raw transcripts, since summaries are already the high-signal distillation. This template's synthetic-RAG hook (Protocol 11) applies the same philosophy to the wiki itself: deterministic grep-based retrieval, injected automatically, no embeddings required.

## Why the wiki layer beats transcripts alone

A transcript records what happened; a wiki page records what's *true now*. The pipeline this template encourages — work in sessions → distill decisions into session logs → promote stable facts into wiki pages — means each layer is more retrievable than the one below it. When someone says "if it's not captured, it didn't happen," this is the capture stack: transcripts catch everything, session logs catch what mattered, the wiki catches what's still true.

## Practical starters

- Adopt the session-log pattern from day one (Protocol 5). It costs a paragraph per session.
- Set up the no-delete transcript archive *before* your runner's retention window eats history you'll want later. You can't backfill what's already gone.
- Once a quarter, try to answer a real question purely from your logs ("what did we decide about X?"). If you can't, the gap tells you what your session logs should start recording.
