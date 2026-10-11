# Protocol 22: Session-Limit Baton

You are at, or close to, a usage or context limit. Do two things before you stop: hand the task to the next session in a prompt it can act on cold, and fix the project setup so the next session does not spend the same tokens reloading the same context.

Works on two kinds of surface:

- **An agent working in a repo** — the setup is the root `CLAUDE.md`, any project `CLAUDE.md`, and the wiki pages they point to.
- **A chat surface with a project workspace** — the setup is the workspace's standing instructions plus the reference files uploaded to it.

<!-- Customize: name your own surfaces here, e.g. the agent harness and chat app you actually use. -->

## Trigger

- "Run Protocol 22", "you're about to hit the limit", "hand off, you're out of room".
- The user pastes a usage-limit or quota warning.
- You notice it yourself: the context window is nearly full, the host has warned about quota, or your answers are getting worse.

## When to use which

Three protocols hand work forward. They are for different situations, and they can be combined (Protocol 7 §7 lets you park in addition to the continuation prompt):

| Situation | Use |
|---|---|
| Normal end of a session; work resumes now or in the next message | [Protocol 7](7-commit-and-ship.md) §7 — continuation prompt in a code block |
| Stopping on purpose; work resumes days later, cold | [Protocol 12 (Park)](12-park.md), resumed with [Protocol 13 (Pick Up)](13-pickup.md) |
| **Forced stop: the session is out of budget mid-task** | **This protocol** |

What this one adds: it assumes there is no budget left for a full close-out, a park, or an interactive handoff, so the prompt alone has to carry the task. And it treats the limit as evidence that the project setup is too expensive to load, and fixes that. If budget remains to park the work properly, park it instead.

## Why

Two losses compound when a session hits its limit mid-task:

1. **The task loses momentum.** Without a baton, the user has to re-explain, and the next session re-derives conclusions this one already reached.
2. **The setup stays expensive.** Whatever made this session costly — long pasted context, scattered references, a missing or thin `CLAUDE.md`, no project workspace at all — will make the next one costly too.

## Procedure

Two tasks, in order.

### 1. Write the baton prompt

A self-contained prompt the user can paste into a fresh session. It must let that session start without the user re-explaining.

```markdown
## Baton: <task name>

### What we're doing
<1-3 sentences: the goal, not the history>

### Where we left off
<what exists now, what works, what's broken, what was just decided>

### Next concrete step
<the single next action the incoming session should take>

### Context the next session won't have
<decisions, gotchas, dead ends already ruled out, anything that would otherwise be re-argued>

### What to read first
<ordered list: file paths, or the workspace's reference files>
```

Delivery:

- **Repo agent:** write the baton to a scratch file (e.g. `scratch/baton-<slug>.md`) and tell the user the path and the command to start the next session in the same directory.
- **Chat surface:** output the baton in a fenced code block the user can copy into a new chat in the same workspace. If there is no workspace (see task 2, case A), the baton has to be more self-contained, because it cannot point at reference files.

Keep it tight. The next session loads the baton as input, so every token of it counts against that session's budget too.

### 2. Fix the setup

If you hit a limit, the setup is probably part of why. Decide which case you are in.

**Case A — there is no project workspace, or no relevant `CLAUDE.md`.**

Tell the user plainly that context carried turn by turn in this conversation should live in a project setup, and give them:

1. A proposed project name.
2. The standing instructions (`CLAUDE.md` content, or the workspace's instructions) — drafted, ready to paste, not just described.
3. The files or pages worth loading as reference, each with one line on why it belongs.

The goal: the next session loads this context once at the start, not piece by piece through the conversation.

**Case B — there is a workspace or `CLAUDE.md`, but it did not pay its keep.**

Name what made this session expensive that the setup should have absorbed. Common causes:

1. The user re-explained something more than once — it belongs in the standing instructions.
2. You re-read the same file more than twice — it belongs in the reference set, or the instructions should point to it earlier.
3. A decision was made that later sessions would otherwise re-argue — record it as a durable rule.
4. A gotcha turned up (an API quirk, a path that does not exist, a flag that broke things) — record it as a durable note.
5. The reference set holds stale or oversized files — recommend trimming them.

Then act:

1. **If you can edit the setup yourself**, do it — surgically, one edit per real finding, and as its own reviewable commit (by exact path, per Protocol 7 §3) rather than a silent change. At a forced stop, say in the baton whether it is pushed, and that the Protocol 7 §2d/Protocol 23 sweep of that edit is deferred to the next session. [Protocol 18 (Tighten)](18-tighten.md) covers where each kind of fact belongs.
2. **If you cannot**, output the exact text for the user to paste and the files to add or remove. "Add this line under the existing `## Writing Conventions` section" beats "consider updating your instructions."

After the setup edits, re-check the baton. Anything the next session will now load from the setup does not need to be in the baton too.

### 3. Report and stop

End the turn with a short summary:

1. **Baton location** — the file path, or "above in this message."
2. **Setup changes** — what you edited, or what you are asking the user to edit.
3. **How to resume** — the exact command or steps to start the next session.
4. **First move** — one sentence, matching the baton's "next concrete step."

Then stop.

## Notes

- **Don't keep working on the task.** This protocol fires because the budget is gone. Spending the last of it on "one more fix" instead of the handoff is the failure it exists to prevent.
- **Don't bloat the setup to look thorough.** The standing instructions are read every session, so every line has an ongoing cost. One real durable rule beats five speculative ones.
- **The next session cannot read this conversation.** Everything load-bearing goes in the baton or in the setup you just edited.
- **Say why you are stopping.** "I'm wrapping up because I'm at the session limit" is fine; don't give a different reason.
- **No credentials in the baton or the setup.** Name the path or command that provides a secret, never its value.

## Related

- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md) — the normal close-out and its continuation prompt
- [Protocol 12: Park](12-park.md) — the deliberate, wiki-persisted handoff for resuming later, including the live interactive handoff when a second session can be started now
- [Protocol 13: Pick Up](13-pickup.md) — resuming a parked continuation
- [Protocol 18: Tighten](18-tighten.md) — placing a fact on the surface that will actually be loaded
