# The correct check and the wrong outcome

## The shape

You learned not to chain the check to the action. So you separate them:

```bash
git add <paths>
git commit -m "..."            # step 2, minutes later
```

```bash
git diff --cached --stat       # step 1 — its own command, own result block
```

Step 1 runs. It is a genuinely separate invocation, and you read its output before step 2 exists. It reports exactly the two files you meant to commit. You verify the staged content directly — a content predicate, not a status line — and it is correct. Then you commit.
The commit contains eight files, all of them someone else's, under your message.

## Why it survives review

Every part of this is right, and each fix from the previous lesson is fully applied. The check is unchained. It is read in its own result block, so the file list is confirmed *before* the action, not after. The content predicate is the hardened form. By every rule you have, the check was performed correctly.

The unstated assumption is that the gap between the check and the action is **empty** — that the state the check read is the state the action will act on. On a shared system that assumption is false, and the window between them is exactly where a concurrent actor operates.

And there is nothing to notice. You cannot see the other actor's write. The check's output was correct when printed; the commit's contents are wrong when shipped; both are true, and no single observation contains the contradiction.

The second-order detail is the one that makes it structural: **the failure cuts both ways in the same window.** The other session's commit took your file at the same time yours took eight of theirs. Two independent actors, both running the discipline, each correctly and each mis-shipping. A shared resource does not care which of you is being careful.

## The general form

**A check reads state; the action re-reads it. If the state is shared and mutable, and any time passes between them, the check is only as good as that assumption — and that assumption holds only because you never wrote it down.**

The same shape, wherever two steps share mutable state:

- A lock file inspected and then acquired — the lock is gone by acquisition.
- A "slot is free" probe, then a write into the slot.
- A row count checked, then a delete by predicate.
- A balance read, then a transfer sized from it.

In each, the check and the action take separate snapshots of the same mutable thing, and correctness requires an atomicity nobody supplied.

## What it costs

The wrong action, plus the credibility of the right check. That second part is worse than in the chained version, because an unchained check *reads as proof* — a check read separately and correctly is exactly the shape you were taught to trust. Downstream, the record still says the work shipped: your message, your log entry, your report. The mislabeled artifact is out there under a subject line that describes an entirely different set of files.

The cleanup is asymmetric too. What your commit picked **up** is bounded by naming paths. What another actor picks **off** between your write and your commit is not bounded by anything you did.

## The defense

**Make the action name its own inputs, so it can no longer be steered by shared state.**

Instead of acting on "whatever is currently staged," name the targets in the action itself:

```bash
git commit path/one.md path/two.md -m "..."
```

The check then confirms *what you are about to do* rather than *what a shared resource happens to hold* at an instant you do not control.

This bounds one direction only. It stops your action from absorbing someone else's state; it does not stop someone else's action from absorbing yours. Accept that — the exposing property is that your work is reachable by another actor between write and commit, and the mitigation is timing, not syntax:

- Keep the window short. Write, verify, commit — no detours.
- Verify the *result*, not the intent. Read the action's own output summary, which reports what it actually did, rather than trusting the subject line you wrote.
- Content-verify your own contribution afterward, as a predicate about your line: is it present at the destination? "The tool reported success" is evidence about the past, not about the destination.

## The trigger

Any two-step sequence where step 1 reads a piece of state and step 2 acts on it, where the state is not exclusively yours:

- Anything on a shared filesystem, index, database, queue, or lock.
- Any check-then-act across a network boundary.
- Anywhere between your check and your action there could be another actor — a person, a process, a peer session, a scheduled job.

The specific feeling to catch: **the relief of an unchained check.** Separating the commands produces exactly the reassurance that the job is done, and that reassurance is the thing standing between you and asking whether the state is yours alone.
