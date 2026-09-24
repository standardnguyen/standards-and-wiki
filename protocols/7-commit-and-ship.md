# Protocol 7: Commit, Ship & Prepare for Continuation

**This protocol means two things, and the second is not a tail step.** Commit current changes, push, create or update a pull request, update session logs — *and* leave the work in a state a brand-new session can resume from cold (§7).

Both halves run every time. "Prepare for continuation" is **part of what the words "Protocol 7" mean**, not an extra the user has to ask for.

> **Why the name carries the rule.** An earlier version of this file was titled just "Commit & Ship" while its body said continuation was implicit — so a session skimming the file read continuation as an optional last chore after the real work. The title is the part that survives a hurried read; a rule the title contradicts is a rule that erodes.
>
> **The filename stays `7-commit-and-ship.md` deliberately — do not "fix" it.** Protocols resolve by number, and cross-links, session logs, and any fork of this template already point at this path. A rename buys a tidier slug and breaks every one of them.

## Trigger

"Run Protocol 7", "Commit and ship", **"Prepare for continuation"**, or "P7".

All of these mean the same thing and run the same protocol. If the user says only *"prepare for continuation"* and there are uncommitted changes, **that is still a full Protocol 7** — shipping the work is how you make it survivable. Conversely, a clean tree does not excuse §7: a session with nothing to commit still has state worth handing forward.

## Posture: Wiki as Substrate

Before running any step below, hold this frame: **the wiki is not documentation. It is the substrate that the next Claude Code session loads as context.** Every page you touch in this protocol — `CLAUDE.md` files, wiki pages, session logs, protocols themselves — becomes the priors that future iterations reason from. Sloppy or partial edits don't just leave the page stale; they actively *poison* the next session's reasoning, because a partially-updated page reads as authoritative while quietly contradicting itself or the world.

This means:

- **Precision matters more than speed.** A change that's almost right is worse than no change, because "almost right" gets trusted. If you're unsure about a fact, mark it as unverified or empirically-checked-on-DATE rather than writing it confidently.
- **Comprehensiveness matters more than concision.** Spell out the *why*, the failure mode, the date of empirical verification, what the prior text said and why it was wrong. Future-you (and dumber models, subagents, and fresh sessions) does not have the conversation context that made the change obvious. Concision is a cost paid by the reader, not a virtue.
- **Walk the graph, not just the file.** A change to one page can silently contradict a sibling page that wasn't touched. Run Protocol 4 on cross-cutting changes — don't skip it. The contradiction you don't catch will bite a future session whose context window doesn't include this conversation.
- **Mark uncertainty explicitly.** If the wiki claimed X, your test showed not-X, but you only verified one path: say so. *"Empirically tested YYYY-MM-DD: X behaves as not-X under condition Y. Other conditions not tested — verify before relying."* Better than declaring not-X and having a future session trip on a path you didn't probe.
- **Any step you skip, you skip out loud — with an offer.** Skipping is often correct (Protocol 4 on a change with no cross-references; the propagation sweep on a log-only commit). Skipping *silently* never is — and neither does reporting a judgment call as if it were a constraint. The floor: name the step, name why it's out of scope, name what *would* have made it fire, and offer at least one lighter variant the user can opt into. Then let them pick. **Silent skip is the failure mode; explicit-skip-with-offer is the floor; user-declined-after-offer is the legitimate end state.**

  The failure this closes is subtle: a run skipped a verification step and reported it as *"this session runs under a directive not to do that"* — an **inference presented as a constraint**, which no reviewer can distinguish from a real one. It surfaced only because the user happened to ask where the directive came from. A future session cannot rely on being asked.

This posture applies to all wiki-touching steps below, not just the obvious wiki edits. **The skip rule is the exception that spans every step, wiki-touching or not.**

## Procedure

### 1. Review Changes

```bash
git status
git diff --stat
git fetch origin
git log --oneline HEAD..origin/<default-branch>   # what landed while you worked
```

⚠️ **For a multi-file cascade, the fetch has to happen before the *work*, not here.** This step *will* catch a diverged remote — but by then the cascade is already written, and reconciling a 20-file propagation sweep against someone else's landed changes is far more expensive than fetching first would have been. If the job is "update this fact everywhere it appears", fetch before you start enumerating.

Verify that only intended files are modified. Check for:
- Unintended files (`.env`, credentials, scratch files)
- Files that should be staged separately (different logical changes)

**Also enumerate side branches and worktrees.** If you use throwaway branches or `git worktree` for parallel work, they accumulate silently — each holding commits `dev` does not have — and nothing else in this flow ever looks at them:

```bash
git worktree list
git branch -a --no-merged dev
git rev-list --count dev..<branch>     # per candidate branch
```

If any carry unmerged commits, **offer to consolidate them into `dev` before shipping** — merge the finished ones, prune the empty ones, and leave anything dirty or checked-out alone (that is a live session's hand). Offer; don't auto-run. Merging someone else's in-flight branch out from under them is worse than a stale branch.

### 2. Update Wiki Files

**Posture: err comprehensive, not terse.** When writing or updating wiki pages, `CLAUDE.md` files, and session logs in this step (and 2a-2c below), bias toward *more* detail than you think you'll need. Spell out the obvious. Repeat context that's "already" in an adjacent file. Include the failure mode you almost left out because "of course you'd check that." The audience isn't just future-you on the same harness — it's also dumber models, subagents, and fresh sessions whose context window doesn't include the conversation that made the thing obvious. Hand-holding here is load-bearing. Concision is a cost paid by the reader, not a virtue.

Before committing, **review the full conversation** and ask:

1. **What changed in the real world?** Did infrastructure change (new service, new config, script update)? Did a project advance? Did the user learn something or make a decision? Did the state of a system change (backup failed, disk filled up, service migrated)?

2. **What wiki pages describe that part of the world?** Search for them. Read them. Check if they're still accurate.

3. **What's now wrong or incomplete?** Update pages that are stale, contradicted, or missing context from this session.

Common triggers — don't limit yourself to this list:

- New section or topic → update `home.md` links
- Changed configuration → update relevant overview pages
- New project → update project index
- New protocol or protocol change → update the protocol table in `CLAUDE.md`
- Bug diagnosed or incident resolved → update troubleshooting docs

The goal is that someone reading the wiki tomorrow sees the world as it is now, not as it was before this session. Walk through modified files and conversation decisions and ask: *"Does any other page reference this, or should any other page now link to this? Is there a page that's now wrong?"*

If anything looks off or you're unsure whether a page needs updating, **check with the user before proceeding**.

### 2a. Update Sub-CLAUDE.md Files

Any project touched during the session may have learned new patterns, gotchas, or conventions. **Read the project's `CLAUDE.md`** (if it exists) and ask:

- Did we learn a new API gotcha, workflow pattern, or classification rule?
- Did we discover how a system actually works (vs how we assumed it worked)?
- Did the user correct our approach in a way that should apply to future sessions?

Update the `CLAUDE.md` with what was learned. This is how future sessions avoid repeating mistakes.

### 2b. Wiki-Said-Not-Possible Sweep

If during the session you (or the user) **did something the wiki said couldn't be done**, the wiki is now wrong and needs updating — before the next session reads the stale claim and trips on it.

Common shape: you read a wiki page that says "X is impossible" / "X requires Y which we don't have" / "the API doesn't expose Z", then you empirically tested and X worked / Z was exposed / Y wasn't actually needed. **The wiki is stale, not the empirical result.**

Walk the conversation:

- Did you read a claim that ruled out an approach, then succeed at that approach anyway?
- Did the user push back ("I could've sworn that worked") and tested data prove the user right?
- Did a "verify" / "TBD" / "doesn't support" line in a reference page turn out to be answerable now?
- Did a guardrail or limitation prove softer than documented (e.g., a token having more permissions than the docs claimed)?

For each one, find the page that made the stale claim and fix it. Be explicit in the edit: write the new correct behavior **plus a dated note** (`"Updated YYYY-MM-DD via empirical test — prior claim that X was impossible turned out to be a documentation gap"`). The dated note matters because the next time someone reads it, they'll know it was empirically verified, not just inherited from the prior version.

If the stale claim was the headline of a section or the basis of a decision tree elsewhere in the wiki, search for downstream references and patch those too — otherwise the contradiction lingers in a less-trafficked spot and bites in three months.

This is the inverse of regular harmonization: instead of catching wiki contradictions and reconciling them to the wiki state, you catch contradictions where the *world* (or your empirical test) won and the wiki lost, and update the wiki to match.

### 2c. Harmonize with Related Pages (run Protocol 4)

The files you changed this session likely have *cross-references* — other wiki pages that name the same service, share a concept, reference the same identifier/path/script, or describe an adjacent part of the system. A change to one page can silently contradict a sibling page that wasn't touched.

**Run [Protocol 4 Recursive Harmonize](4-recursive-harmonize.md)** seeded from the files changed this session.

If the session's changes are surgical and obviously local (a one-line typo fix, a single-file session log entry with no cross-cutting facts), skip — Protocol 4 is for changes whose blast radius plausibly touches the broader graph. When in doubt, run it; the cost is grep cycles, the cost of skipping is a contradiction that bites in three months.

### 2d. Propagation Sweep

When this session **changed a fact** — a count, an address, a port, a path, a name, a date, a price, a status — every other page carrying the old value is now wrong. Summary tables, index pages, and hub descriptions are the usual survivors.

**Grep first, then scope the fix.** Run the grep *before* choosing which lines to edit — it is the scoping tool, not after-the-fact verification:

```bash
grep -rn "<old value>" . --include='*.md'
```

This is the single most common recurring drift class: a fix corrects one page and a sibling keeps the old value. When delegating fixes, **scope each worker by the grep result, never by a hand-listed set of lines** — the lines you did not list are exactly where the sibling drift survives.

**Delegate the sweep rather than hand-enumerating.** The rule above tends to fail not at the grep but at the *enumeration*: the shipping session has to list every changed fact at the exact moment its context is fullest, and under-enumeration is **silent**. So after staging (§3, before commit), hand **one read-only agent** the staged diff and this job:

1. From `git diff --cached`, extract every changed **fact** as an old→new pair. Work from the diff text only, not from conversation memory.
2. For each **old** value, grep the wiki plus `CLAUDE.md` — excluding `logs/` directories, since historical logs are never retro-edited.
3. Report every surviving carrier with `file:line`, a verbatim quote, and a same-fact-versus-coincidental-string judgment.

You verify the report, fix true stragglers **in the same commit**, and re-grep to zero. **Skip the agent only when the diff contains no factual corrections at all** — new-page-only additions, prose and formatting, log-only commits — and then the manual grep above suffices.

This matters most in **multi-pass analysis documents**, where a later section corrects a claim from an earlier one but the original text is never updated. When you write a correction, propagate it back to the original claim and to any summary page quoting it.

### 2e. Structural Drift Checks

When the diff touches a known drift-prone area, run the matching check below. A five-second grep now prevents a finding that costs far more to chase later.

**[Protocol 10](10-codify-drift-check.md) owns this table** — its procedure appends a row each time a drift pattern recurs often enough to codify. Treat the table as growing, not fixed.

| If the diff touches... | Check |
|---|---|
| Any `CLAUDE.md` | Spot-check 3 cross-references: do the paths and facts still match? |
| A new content page | Verify the parent section index (and `home.md`, if it's a new section) carries a row for it. New pages created after their index's last edit are the classic orphan source. |
| A protocol file | Verify the protocol table in `CLAUDE.md` and the list in `README.md` still match. |
<!-- Add rows here as Protocol 10 codifies recurring drift patterns for your wiki. -->

### 3. Stage and Commit

Stage specific files by name (never `git add -A` or `git add .`):

```bash
git add <file1> <file2> ...
git diff --cached --stat
```

**Run `git diff --cached --stat` as its own command — never chained into the commit with `&&`.** Chained, the file list and the commit land in one result, so you read the list *after* the commit has already shipped: the check becomes decorative, which is exactly when it will be wrong. The general shape is worth recognizing elsewhere too — **a verification step folded into the action it verifies cannot stop that action.**

⚠️ **Unchaining it is necessary but not sufficient — the index is shared mutable state, so the gap between the check and the commit is itself a race.** If another session (or a background job, or a cron task) stages something in that gap, `git diff --cached --stat` can print exactly the right file list and the commit that follows can still ship someone else's files under your message. **A racy check is worse than no check, because it reads as proof.**

**The fix is to make the commit name its own paths:**

```bash
git commit <file1> <file2> -m "..."     # commits these paths from the WORKTREE,
                                        # regardless of what else is in the index
```

🔴 **But the rule is split, and picking the wrong half silently commits the other session's work.** The pathspec form commits the **worktree**, not what you staged:

- Use **pathspec** (`git commit <paths>`) for files only *you* touched. This is the common case.
- Use **plain `git commit`** (which ships the index) for any file where you had to reconstruct a mine-only version by hand — because the pathspec form would discard your reconstruction and ship the worktree copy instead.

**When your edit shares a file with another session's uncommitted change**, don't stage the whole file. Read the file **once**, hold both versions in memory, build a mine-only copy (the committed version plus your edit), commit that, then write the both-edits version back to the worktree so their change survives uncommitted. 🔴 **Capture the original bytes BEFORE writing the mine-only copy** — if you write it first and then re-read the file to build the combined version, your base *is* the mine-only copy, and their change is silently gone. Assert both edits are present exactly once before writing, and grep for their marker afterwards. ⚠️ `git diff --cached` cannot catch this: the index is correct the whole way; the damage is in the *worktree*, which none of the staging guards look at.

**Then verify your own edit actually landed:**

```bash
git show HEAD:<file> | grep -c '<a string unique to your edit>'
```

The mirror race is real too — another session can overwrite an edit you have *not yet staged*, between your edit and your commit, and the commit message will still claim the change as done. *"The edit tool reported success"* is evidence about the past, not about `HEAD`. Use a predicate about **your own line**, never a `head`/`tail` window around it — a window prints the neighbouring lines, and neighbouring lines in config and shell-rc files are where credentials live.

Write a descriptive commit message. Use imperative mood, focus on *why* not *what*:

```bash
git commit -m "$(cat <<'EOF'
<commit message>

Co-Authored-By: Claude <current model name> <noreply@anthropic.com>
EOF
)"
```

Substitute `<current model name>` with the model actually running the session — not a name pinned into this file, which goes stale the moment you upgrade and then silently misattributes every commit.

If multiple logical changes are present, create separate commits for each.

### 4. Push

```bash
git push origin dev
```

**Do not rebase as part of this protocol.** Concurrent sessions, cron jobs, or background tools may modify the working tree, and a rebase can silently bundle unrelated work or rewrite history that's already on the remote. If `git push origin dev` is rejected non-fast-forward and a rebase is genuinely needed (e.g. `origin/dev` has fallen behind `origin/main` and `main` has commits `dev` doesn't), **stop and ask the user to run the rebase themselves**. Do not force-push without explicit user approval.

### 5. Create or Update Pull Request

Check if a PR from `dev` to `main` is already open. If one exists, pushing to `dev` already updated it. If not, create one.

<!-- Customize for your Git hosting platform:

GitHub:
  gh pr list --state open --head dev
  gh pr create --base main --head dev --title "..." --body "..."

Gitea/Forgejo:
  curl -s "https://your-git.example.com/api/v1/repos/OWNER/REPO/pulls?state=open" \
    -H "Authorization: token $TOKEN"

GitLab:
  glab mr list --source-branch dev
  glab mr create --source-branch dev --target-branch main --title "..."
-->

### 6. Session Log Check

Determine if the changes touch a project with logging requirements. Check the table below:

| Project | Logging Location | Trigger |
|---------|-----------------|---------|
<!-- Add rows as you set up session logging for projects via Protocol 5. Example:
| Infrastructure | `infrastructure/logs/` + `infrastructure/session-log.md` | Changes to `infrastructure/` |
| My Project | `projects/my-project/logs/` + `projects/my-project/session-log.md` | Changes to `projects/my-project/` |
-->

If logging is required:

1. **Create a session log file** in the appropriate logs directory:
   - Filename: `YYYY-MM-DD-HHMMSSzzz-EPOCH-<slug>.md`, stamped from the clock per Protocol 5: `date '+%Y-%m-%d-%H%M%S%Z-%s' | tr '[:upper:]' '[:lower:]'`
   - Content: date, session context, decisions made, files updated, pending items
   - Clock-stamped filenames make same-day collisions practically impossible, so there is no free suffix to race for and no remote check is needed. Legacy letter-suffixed logs keep their names — renaming breaks inbound links for no benefit.

2. **Add a row to the log index** (e.g., `projects/my-project/session-log.md`)

3. **Update relevant wiki files** if any state has changed

4. **Stage and commit** the session log files (can be a separate commit or combined)

5. **Push** the additional commit — the open PR auto-updates.

### 7. Continuation Prompt (always)

**Preparing for continuation is the default of every Protocol 7 run — you do not need to be told to do it.** After completing steps 1-6, always emit a self-contained continuation prompt that a fresh session could use to pick up where this one left off: what was accomplished, what's pending, which files and PRs were touched, and any decisions or context that would otherwise be lost when this conversation ends.

**Name what the next session must LOAD and RE-READ — with file paths, not just labels.** Spell out (a) any protocol or standing mode still in effect *and the file to re-read from disk*, and (b) the key context files: the relevant project `CLAUDE.md`, the section index, the newest session log, any reference page the work depends on. Don't write *"we were mid-Protocol 4"* and stop — write *which files to open*. The failure this closes is a continuation that drops the active protocol entirely, so the next session doesn't know it was running one.

**Render it inside a fenced code block so the user can copy it in one click** — never as prose or a blockquote. This applies to any copy-paste artifact you hand over: continuation prompts, briefings, reusable commands.

- **Resuming *later*, not next message?** When the user is stopping but wants to pick the work back up in a future session, **persist the continuation to the wiki via [Protocol 12 (Park)](12-park.md)** instead of — or in addition to — the ephemeral code block. A parked `continuations/<slug>.md` survives the end of the conversation and is triggered by name with [Protocol 13](13-pickup.md). The code block is for "resume right now"; a parked continuation is for "resume next week, cold."

## Checklist Summary

A quick scan for a session that already knows the protocol. The numbered sections above stay canonical — when a checkbox and the body disagree, the body wins.

- [ ] §1 `git status` + `git diff --stat` — every changed file intentional; side branches and worktrees enumerated, consolidation offered if any hold unmerged commits
- [ ] §2 world-model sweep — what changed in the real world, which pages describe it
- [ ] §2a project `CLAUDE.md` files updated with what was learned
- [ ] §2b wiki-said-not-possible sweep
- [ ] §2c Protocol 4 harmonize (skip only if the change is genuinely local)
- [ ] §2d propagation sweep — grep every changed fact, delegate the enumeration
- [ ] §2e structural drift checks matching the diff
- [ ] §3 stage exact paths (never `-A` or `.`), `git diff --cached --stat` as its **own** command, commit with the current model's co-author line
- [ ] §4 push `dev` — **no rebase** without explicit user permission
- [ ] §5 PR pre-check → update the existing PR or create a new one
- [ ] §6 session log filed (clock-stamped filename) + index row
- [ ] §7 continuation prompt in a fenced code block, naming files to re-read — or a Protocol 12 park
- [ ] **every skipped step announced out loud with an offer** (Posture) — and no judgment call reported as a constraint

## Notes

- This protocol is meant to be run at the end of a work session, not mid-stream.
- If there are no changes to commit (`git status` shows clean), **skip §1-§6 — but still run §7.** A clean tree means there is nothing to ship; it does not mean there is nothing to hand forward. The session still knows what was decided, what was ruled out, what's mid-flight, and what the next session must re-read — and the end of the conversation drops all of it either way.
- The session log step is the safety net against wiki drift.
