# Protocol 17: Conversation Forensics

Diagnose a past agent conversation: read the transcript of a finished run (or observe a live one), find the turn it went wrong, and explain the failure in plain language.

This is the diagnostic sibling of the template's other fresh-read workflows: [Protocol 2](2-spot-check.md) samples wiki prose for contradictions, [Protocol 14](14-ui-convergence.md) fires fresh QA agents at a running interface, and this one reads a *real* conversation that already happened. The deliverable is an explanation the user can act on — not a verdict, and not a fix.

## Trigger

"What went wrong here?", "check this conversation", "diagnose this session", "I'm confused what it got wrong" — with a transcript pasted in, a file handed over, or the session still running. The conversation can be **finished or in flight**: a post-mortem is the common shape, but "this is going sideways right now, what is it doing?" is equally valid and runs the same procedure.

## Input forms

| Shape | Looks like |
|---|---|
| **A pasted log** | Inline text in the conversation — already in your context |
| **A transcript file** | A path to a session record (`.jsonl`, `.md`, `.txt`) — read it |
| **A live session** | A process you can observe: its output, its screen, its log as it grows |

**A pasted log alone is a supported input.** Do not require a file path or a tool-specific format — text the user pasted is enough to run every step below. If the reference is ambiguous (an opaque identifier that could belong to more than one runner), **look before assuming** — list the candidate locations rather than guessing which tool produced it. For where transcripts live, why they age out, and what to archive, see [Mining Session Logs](../meta/mining-session-logs.md).

<!-- Customize: if your runner writes structured transcripts, note where they live and which
     field identifies a turn. Keep it to one line, and keep this protocol working for a
     pasted log without it. -->

## Who runs it — the one distinction that matters

**Reading a *different* conversation is genuinely external to you** — no shared blind spot, so read it directly and diagnose. This is the common case.

**Exception — it is your own current or recent session.** Then reading it yourself is self-review: the same frame that produced the confusion is the frame doing the reading. Route it to a **separate process** instead — a fresh agent instance, or a fresh session of a different tool, given the transcript cold. **A subagent is not external**; it inherits your context and your blind spots. The process boundary is what makes the read fresh, not the model name. (See [The second opinion that shares your blind spot](../casebook/the-second-opinion-that-shares-your-blind-spot.md).)

## Procedure

1. **Locate and load.** Resolve the reference, then read it. **Read *all* entry kinds — tool calls, tool results, reasoning, errors, and steps that were announced but never taken — not just the assistant's prose.** The wrong turn is usually in a tool result, a failed call, or a skipped step; the prose around it often reads as confident and correct. For a **live session**, don't fight a file still being written — take a snapshot from its output or screen, because reading a half-written record races the writer and shows you a torn state that never existed.
2. **Reconstruct the goal.** What was the agent actually asked to do? State it in one line. Half of "what went wrong" is the agent having solved a different problem from the one posed.
3. **Walk the timeline.** Turn by turn: what it read, what it called, what it concluded — noting the load-bearing decisions and the assumptions under them. The evidence tags in `CLAUDE.md` → Doing Tasks §5 (`[ran:]` / `[read:]` / `[recalled:]`) are useful vocabulary for naming which claims were checked and which were assumed.
4. **Find the divergence point.** The *specific* turn where it went wrong — the wrong assumption, the misread file, the tool that failed silently, the path that does not exist, the instruction it skipped. **Name the turn, not a vibe.** "Somewhere it got confused" is not a finding.
5. **Diagnose the root cause, not the symptom.** Classify it: **missing context** (the information was not available to it), **tooling blindness** (a tool failed, or was never reached for), **misread** (it was there and it parsed it wrong), **hallucination** (it invented something), or **posture** (it barreled past a checkpoint).
6. **Report in plain language.**
   - **What it was trying to do** — the goal, one line
   - **Where it went wrong** — the divergence turn, concretely, quoted
   - **What it got wrong** — the actual error
   - **Why** — root cause plus classification
   - **(If applicable) the fix** — a context or documentation gap, a one-off miss, or an ambiguous instruction

## Output shape

A short diagnosis, not a transcript replay. The user was confused; the win is clarity. Lead with the one-line gist and let them pull on threads. **Quote the smoking-gun turn verbatim; summarize the rest.**

**If nothing went wrong, say so.** Sometimes the conversation is correct and the user's mental model is what needs updating. Confirm a real error exists before explaining one — "nothing is broken here; the part that reads as a mistake is actually X" is a complete and valuable answer.

## Anti-patterns

- **Don't replay the whole conversation.** Diagnose, don't transcribe — a turn-by-turn dump is the thing the confused user already couldn't parse.
- **Don't diagnose your own session with yourself.** Use a separate process (see "Who runs it"); re-reading your own recent reasoning rationalizes, it does not diagnose.
- **Don't stop at the symptom.** "It got confused and gave up" is not a diagnosis. *Why* — what did it not find, misread, or assume?
- **Don't assume the agent was wrong.** Sometimes the conversation is right and the user's expectation was off.
- **Don't auto-patch on one conversation.** Forensics produces a **finding, not a fix**. One forensic read is one data point: if the root cause is a gap in the wiki or the instructions, surface it as a candidate change and let a pattern-of-three decide — don't silently edit the wiki mid-diagnosis.

## Related

- [Protocol 2: Spot-Check](2-spot-check.md) — the same fresh-eyes-beat-self-review principle, aimed at wiki prose instead of a conversation
- [Protocol 12: Park](12-park.md) / [Protocol 13: Pick Up](13-pickup.md) — when the intent is to *continue* the work from a conversation, not diagnose it
- [Protocol 10: Codify Drift Check](10-codify-drift-check.md) — where a forensic finding lands when the root cause recurs instead of being a one-off
- [Mining Session Logs](../meta/mining-session-logs.md) — the capture stack this protocol reads from
