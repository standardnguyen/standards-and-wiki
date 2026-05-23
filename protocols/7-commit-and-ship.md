# Protocol 7: Commit & Ship

Commit current changes, push to remote, create or update a pull request, and update session logs if the work touches a project with logging requirements.

## Trigger

"Run Protocol 7" or "Commit and ship"

## Posture: Wiki as Substrate

Before running any step below, hold this frame: **the wiki is not documentation. It is the substrate that the next Claude Code session loads as context.** Every page you touch in this protocol — `CLAUDE.md` files, wiki pages, session logs, protocols themselves — becomes the priors that future iterations reason from. Sloppy or partial edits don't just leave the page stale; they actively *poison* the next session's reasoning, because a partially-updated page reads as authoritative while quietly contradicting itself or the world.

This means:

- **Precision matters more than speed.** A change that's almost right is worse than no change, because "almost right" gets trusted. If you're unsure about a fact, mark it as unverified or empirically-checked-on-DATE rather than writing it confidently.
- **Comprehensiveness matters more than concision.** Spell out the *why*, the failure mode, the date of empirical verification, what the prior text said and why it was wrong. Future-you (and dumber models, subagents, and fresh sessions) does not have the conversation context that made the change obvious. Concision is a cost paid by the reader, not a virtue.
- **Walk the graph, not just the file.** A change to one page can silently contradict a sibling page that wasn't touched. Run Protocol 4 on cross-cutting changes — don't skip it. The contradiction you don't catch will bite a future session whose context window doesn't include this conversation.
- **Mark uncertainty explicitly.** If the wiki claimed X, your test showed not-X, but you only verified one path: say so. *"Empirically tested YYYY-MM-DD: X behaves as not-X under condition Y. Other conditions not tested — verify before relying."* Better than declaring not-X and having a future session trip on a path you didn't probe.

This posture applies to all wiki-touching steps below, not just the obvious wiki edits.

## Procedure

### 1. Review Changes

```bash
git status
git diff --stat
```

Verify that only intended files are modified. Check for:
- Unintended files (`.env`, credentials, scratch files)
- Files that should be staged separately (different logical changes)

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

### 3. Stage and Commit

Stage specific files by name (never `git add -A` or `git add .`):

```bash
git add <file1> <file2> ...
```

Write a descriptive commit message. Use imperative mood, focus on *why* not *what*:

```bash
git commit -m "$(cat <<'EOF'
<commit message>

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

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
   - Filename: `YYYY-MM-DD-<slug>.md` (letter suffix if multiple logs on same day)
   - Content: date, session context, decisions made, files updated, pending items

2. **Add a row to the log index** (e.g., `projects/my-project/session-log.md`)

3. **Update relevant wiki files** if any state has changed

4. **Stage and commit** the session log files (can be a separate commit or combined)

5. **Push** the additional commit — the open PR auto-updates.

## Notes

- This protocol is meant to be run at the end of a work session, not mid-stream.
- If there are no changes to commit (`git status` shows clean), do nothing.
- The session log step is the safety net against wiki drift.
