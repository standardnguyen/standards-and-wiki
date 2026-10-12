# Pattern 00001: Mario and Luigi

**Class:** a pattern, not a protocol. There are no ordered steps and no exit state. Adapt the shape to your harness and your job; see [the patterns index](../_index.md) for the difference.

## The invariant

**Two long-lived agent sessions run one standing job as a pair.**

- **Mario drives.** He holds the queue, does the work, and is the only session with work in flight: the only scheduled tick, the only running subagents.
- **Luigi navigates.** He does no queue work. He watches Mario's context size and progress and does the things a session cannot do for itself.

Luigi's two duties:

- **Compaction.** When Mario's context crosses the bar and he reaches a clean boundary, Luigi compacts him, using whatever your harness offers for one session to compact another. Mario keeps going from the compacted state instead of being replaced by a fresh session.
- **Model guard.** If your harness lets a session's model drift or be switched, make the check step 0 of the driver's tick: each half reads the other's model and puts it back if it changed. Luigi has no tick of his own, so with fixed seats decide per run which half runs the guard, and test that it still does; a guard nobody is scheduled to run quietly stops running.

The seats can be **fixed** (Luigi compacts Mario in place, and Mario compacts Luigi when Luigi asks) or they can **swap**: at the bar, Mario hands off to Luigi with a message naming the state of record, the roles swap, and the new driver compacts the old one. Either way, a handoff is a message, not a spawn.

The pair loops until the job is done: the queue is empty, or, for open-ended improvement work, a round produces no new idea worth doing.

**The state of record is files on disk, not either session's memory.** Before Mario is compacted, he commits what he has done and decided since the last compaction (a dated entry in the job's session log is enough), somewhere that outlives the job's scratch space. Before compacting, Luigi checks the commit, not Mario's report of it: the entry's last commit must be later than Mario's last compaction. A transcript is not the state of record.

<!-- Customize: name where your pair keeps its state of record (a continuation file, a queue log, the project's session log). -->

## The shape

1. **Two, never three.** A third session turns the pair back into a chain, which is what this replaces.
2. **Compact the partner; never stop it.** Stopping a session kills whatever it is running. Compaction rewrites what the model reads and leaves its process alone.
3. **Nothing in flight on either side.** Do not compact a session that is hosting a live subagent, or one whose delegated job has not yet written its result. A clean boundary means the last batch of work has landed, its results are written down, and nothing is pending. This binds whichever half holds the work, including the navigator.
4. **Write the state before the switch, not after.** Whatever the next driver, or the compacted driver, needs has to be in the files when the handoff message is sent or the compaction starts, including a line naming every in-flight background job and which session will receive its completion notice. A queue written beforehand costs the successor one file read; a queue written afterwards costs it a full reconstruction.
5. **Resume light.** After compaction, the session reads its state-of-record files and only the parts of other documents the next step actually needs. A full re-read of everything is the boot cost this pattern exists to avoid.
6. **The bar is soft, and the task in hand outranks it.** At the bar, stop *starting* new work; finish what is in hand, then compact or hand off. Never interrupt a task just to honor the number. Have something tell the driver it is approaching the bar a little before it gets there, because a clean boundary you have to wait for is one you need to see coming. A warning that fires only at turn boundaries misses a long turn, and if it computes a percentage, print the raw used and window figures so a wrong window size is visible.
7. **Look before typing into the partner.** If Luigi reaches Mario by typing into his input, he checks first that the input is empty. Unsent text there may be the operator's draft, so leave it alone. Tell a real draft apart from any placeholder or suggestion text the harness shows. Then confirm the compaction actually ran (the harness's compaction prompt or summary record appears): a command delivered as plain text can be sent as chat and look like a compaction that never happened.
8. **Clean up the tools you used to reach the partner.** Any client, terminal or connection opened to compact or check the partner is closed when that step ends. A leftover one outlives the work that opened it and goes unnoticed until it gets in the way.
9. **Address the partner by name.** A cached handle (a socket, a process id) belongs to one process and goes stale when that process restarts.
10. **The pair shares one concurrency limit.** If you cap how many subagents run at once, count both halves' agents against the cap.
11. **If the operator talks to both halves, mirror and reconcile.** Each half logs every operator message it receives and passes it to the other half in the same turn. Before a handoff, both lists are merged into the state of record. The half holding the queue is the operator's primary contact; the other half points the operator there. Approval given to one half is not approval for the other: relaying it would be passing on consent the other half never received. If the operator insists the non-holding half act, it tells the holder before touching anything.

<!-- Customize: set your bar (a share of the context window) and the earlier warning point, and say what delivers the warning in your harness. -->

## When to reach for it

- A standing job that will outlive one context window: a long queue of changes, an overnight run, a supervisor that watches other sessions.
- The job holds state a fresh session would have to re-read before it could do anything useful.
- The operator is away and cannot arbitrate each turnover.

## When not to use it

- **The job fits in one context window.** The second session is pure overhead.
- **The operator has not agreed to two sessions.** Two sessions on one job spend two shares of the operator's quota.
- **Your harness gives one session no way to compact another.** Without that, the navigator has nothing to do that the driver could not do for itself, and you are better off with a plain handoff between sessions.

## What it costs

- A second session's idle context, held for the whole job. In the runs this pattern was written from, that was on the order of 100K tokens after compaction.
- A few minutes for each compaction, during which the driver does no work.
- Discipline in writing state down before every switch, which costs tokens each time.

What it saves: the driver never pays a fresh boot. In a chain, where each session spawns a successor and stops, every turnover costs a full re-read of the job, and that boot is the binding cost, not the work.

## Known gap: a pair can die silently

Nothing in the shape notices when one half has stopped. A note that says "my partner is X" reads the same whether X is alive or not, and a script that checks the driver's state can read a vanished session as an idle one. If the job matters, add a liveness check of your own, and test it against a session you know is dead.

## How it is audited

As with any pattern, by whether the shape was right, not whether every line was followed:

- **Did every compaction and handoff happen at a clean boundary, after the state was written down?** One taken mid-task, or with the driver's state only in its own context, is the shape misapplied even if nothing visibly broke.
- **Did anything in flight die?** A killed batch, an orphaned subagent, or a partner that was stopped instead of compacted is the failure this pattern exists to prevent.

## Related

- [Protocol 22 (Session-Limit Baton)](../../protocols/22-session-limit-baton.md): the single-session handoff at a forced stop. This pattern avoids reaching that stop.
- [Protocol 12 (Park)](../../protocols/12-park.md): stopping on purpose for days. A pair is for work that keeps running.
- [Protocol 21 (Shared-Checkout Commit)](../../protocols/21-shared-checkout-commit.md): both halves commit to one checkout, so commit by pathspec.

## Examples

This template ships the invariant only. There are no stored examples yet, because a real example records what one actual run did and decided, and this template has none of its own runs to record.

When you run a pair and ship the work, store your variant in `examples/` as `YYYY-MM-DD-<what-it-decided>.md`, recording what it decided, what it did differently from the invariant, and where its scripts live. A variant might read: *"Seats stayed fixed; the navigator compacted the driver in place at <your bar>% and refused while the driver's background job was running; scripts in `tools/pair/`."* (Hypothetical, to show the shape of an entry.)
