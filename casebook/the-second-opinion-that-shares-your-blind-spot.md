# The second opinion that shares your blind spot

## The shape

You have finished something and you want it checked. So you ask for a review — a second agent, a second instance, a fresh session — and you hand it what you have: the conversation, the framing, the summary of what the change is and why.

It agrees. Or it flags something small, inside the frame you handed it. Either way the box is ticked: the work was reviewed.

The reviewer was a label. The isolation never existed.

| what you varied | isolated? |
|---|---|
| the agent's name | no |
| the model behind it | no |
| a new conversation in the same process, inheriting the parent's context and tool state | no |
| a separate process, loading the artifact cold from disk, with no access to the conversation that produced it | yes |

Independence is a property of the information that crossed the boundary — not the model name, not the agent label, not the fact that a second entity said something. A reviewer that receives your context, your summary, or your conclusion *before* it forms its own has been handed your answer and asked whether your answer is right.

## Why it survives review

Because a review did happen. There is a second voice, a delivered verdict, and often a recorded transcript of it. Nothing about that exchange looks defective. It looks like diligence, and the diligence is genuine — the failure is in what the second entity was given, and giving it more context feels like *helping*, not like contaminating the test.

The deeper reason it is invisible: the blind spot is shared, so neither party can see it. A same-frame reviewer does not agree at random. It agrees exactly where your frame is wrong and pushes back exactly where your frame pushes back — that is the whole content of a shared frame. The agreement is structured, which makes it read as confirmation rather than as an echo.

And the check that would catch it is *awkward*. Real isolation costs something: a separate process, a cold load, re-explaining a goal that you already understand. Every shortcut that avoids that cost is presented to you as an efficiency.

## The general form

**Independence is a property of information flow, not of naming. And what a genuinely independent reviewer contributes is not a second pair of eyes — it is a second vocabulary.**

Two distinct failure modes, and they are easy to confuse:

- **Shared context.** The reviewer inherits your conclusion. It can no longer reach a different answer, because it never saw the input — it saw your description of the input. The test is one question: *could this reviewer have concluded otherwise about this artifact?* If it cannot see the artifact, no.
- **Shared vocabulary.** Even a reviewer with the full artifact and none of your context still searches with words. You can only look for the phrasing *you* used. So a reviewer working from the same lane, the same idiom, the same naming instincts will check for the carriers you already know about and miss the ones worded differently — and a same-lane author is the worst possible checker of their own lane. **What survives a sweep is what is worded in somebody else's words**, because those are the instances the author's own search never matched.

The second one is the subtler finding, because it survives even good isolation. You can hand someone a cold artifact with a clean process boundary and still get a review that could only ever find your mistakes *as you would have described them*.

## What it costs

You ship with the confidence of a review. The defects that go through are precisely the class the review existed to catch — the ones inside the frame — so the more you needed the review, the better it is at telling you that you didn't.

The record compounds it. "Reviewed" goes into the log, the commit message, the summary. A later reader sees that the work was checked and has no way to see that the checker shared the frame. That is ordinary laundered confidence: the review tier got promoted, and no review was added.

The second cost is the invisible one. Every carrier worded in your own phrasing gets found; every carrier worded in someone else's survives. You never learn which ones those were, because the search that would have found them is the search you didn't have.

## The defense

**Make the isolation a process boundary.** A separate process, a fresh context, loading the artifact from disk cold — nothing from the conversation that produced the change. Two things to be honest about when you set it up:

- A separate process buys you the isolation. It does **not** buy you a different lineage. A second instance of the same harness shares that harness's blind spots, which is fine when the question is *"does this read correctly"* and insufficient when the question is *"would a different reader misread this."*
- Hand over the **artifact and the goal**, not your framing of them. A summary you write is the contamination you were trying to avoid, and it arrives looking like a courtesy.

**Then treat the reviewer's output as a claim, not a verdict.** A differently-framed reviewer is wrong in *its* direction. Verify its correction, and **check the reverse** — the thing it asserted in passing, on its way to the correction. In one exchange between two sessions with genuinely different frames, each one caught a real error in the other, and neither error was visible from inside the session that made it. That is the value. It is also why a second opinion is not an oracle: it is a second position from which to look, and its output needs the same checking you would give your own.

## The trigger

The moment you say *"let me get a second opinion"* and then reach for the context to paste in. The paste is the instinct to be helpful, and it is the exact move that dissolves the independence you were buying.

Also: any time you are relieved by an agreeing review. Relief is what both a real check and an echo produce, and you cannot tell them apart from the inside.

And: whenever you want the review to be *independent* while also sparing it the cost of loading the context cold. Both of those can be true, and choosing the second one is choosing to keep the blind spot.
