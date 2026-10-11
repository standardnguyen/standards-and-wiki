# Protocol 21: Shared-Checkout Commit

How to commit when several agent sessions, background jobs, or scheduled tasks share **one git checkout** and stage and edit files while you work. [Protocol 7](7-commit-and-ship.md) §3 carries the short form at every commit; this page is canonical for the commit forms and for the mine-only reconstruction.

The underlying fact: **the index and the worktree are shared mutable state.** Anything you check about them can change before the commit that relies on the check. Every step below either removes a window or verifies what actually shipped.

Read this file from disk when you run it; a remembered copy predates the latest fix.

## Trigger

Any commit on a checkout that another live session or background job can touch. Run §2 whenever a file you must commit also holds another session's uncommitted edit — a shared index file such as a session-log index is the usual case.

<!-- Customize: if your repo only ever has one session at a time and no background jobs write to the tree, Protocol 7 §3 is enough and this protocol is optional. -->

## Procedure

### 1. Pick the commit form

Pick the form by where the bytes you mean to ship live: the worktree or the index.

1. **A file only you touched: commit by pathspec**, `git commit <path1> <path2> -m "..."`, never `git add` followed by a bare `git commit`. Pathspec commits those paths from the worktree regardless of what else is in the index, so a peer re-staging between your check and your commit cannot add their files to yours. ([The correct check and the wrong outcome](../casebook/the-correct-check-and-the-wrong-outcome.md).)
2. **`git add` every new file first.** Pathspec matches only tracked paths, so one untracked path aborts the whole commit: `error: pathspec '<path>' did not match any file(s) known to git`.
3. **Before a pathspec commit, run `git diff --numstat HEAD -- <paths>` and account for every deletion.** Pathspec ships the worktree. If a peer committed from the index without restoring the worktree, yours lags HEAD, and your commit silently reverts theirs. Read `--numstat`, not a grep over the diff text: a deleted markdown bullet renders as `-- item`, and a pattern like `^-[^-]` skips it.
4. **Read the diff of every path you name, against what will ship.** Before a pathspec commit that is `git diff HEAD -- <path>` (the worktree against HEAD); before an index-form commit it is `git diff --cached -- <path>`. A bare `git diff <path>` compares the worktree with the *index*, so a hunk a peer has already staged does not appear in it. `git status` prints `M <file>` whether or not another session's hunk is in it, so it cannot tell you the file is all yours. On a file with very long lines, read it as `git diff -U0 --word-diff=plain -- <path>`.
5. **A file you reconstructed mine-only (§2) ships from the index: commit it with plain `git commit`.** Pathspec would commit the worktree copy, which holds the other session's change, under your message. When one commit would span both kinds of file, split it into two commits rather than choosing one form for the pair.
6. **Before a plain `git commit`, assert on the whole index, in the same command**, aborting if it lists any path that is not yours. A path-scoped `--cached` check cannot see what another session staged, so it reads clean either way. An example, where `mine.txt` lists your repo-relative paths one per line:

   ```bash
   [ -s mine.txt ] || exit 1                       # no list: abort, never fail open
   foreign=$(git diff --cached --name-only | grep -vxF -f mine.txt); rc=$?
   [ "$rc" -eq 1 ] || { echo "abort: ${foreign:-grep error}" >&2; exit 1; }   # 1 = nothing foreign
   git commit -m "..."
   ```

   A plain `... | grep ... && exit 1` fails open when the list file is missing (grep exits 2) and aborts every clean commit if chained. If the assertion aborts, unstage the foreign path with `git restore --staged <path>` and rerun.
7. **A check you read runs in its own command; only an assertion that aborts may chain into the commit.** A chained check is read after the commit has shipped. ([The check that cannot stop the action](../casebook/the-check-that-cannot-stop-the-action.md).)
8. **Never `--amend`; make a second commit.** An amend rewrites whatever HEAD is now, so a peer's commit that landed after yours ships under your message.

Tested in a throwaway repo: with index = base + your row and worktree = base + your row + their row, `git commit f.md` commits their row; plain `git commit` commits only yours and leaves theirs uncommitted in the worktree.

### 2. Mine-only reconstruction

Use this when a file you must commit also holds another session's uncommitted edit. Do not stage the whole file.

The model: make your edit first, in the worktree, as usual. The worktree file is then the **both-edits copy** (their change + yours), and you never need to rewrite it. The **mine-only copy** is `git show HEAD:<file>` + your edit, applied by string replacement. You put the mine-only copy into the **index** directly, so the worktree is never touched and a peer's late write to it cannot be overwritten.

1. **Build the mine-only text in memory** from `git show HEAD:<file>` plus your edit, by exact-once string replacement. Assert that your marker appears exactly once in it and theirs not at all. Assert on a string that is unique per edit, such as a whole table row. Pick their marker as one line of the other session's edit that your own edit does not contain. An identifier that appears twice per row (in a column and in a link) fails the count on correct data.
2. **Stage it without touching the worktree:**

   ```bash
   mode=$(git ls-files -s -- <file> | cut -d' ' -f1)       # keep the file's mode (100644 or 100755)
   blob=$(printf '%s' "$MINE_ONLY_TEXT" | git hash-object -w --stdin)
   git update-index --cacheinfo "$mode,$blob,<file>"
   ```

   Pass the text through a variable or a temporary file made with `mktemp`; never a fixed path such as `/tmp/x`, which another session's run can overwrite.
3. **Assert on the whole index and commit in one invocation** (§1 step 6), with plain `git commit`. Any pause between staging and committing is a window another session can commit through, and this procedure necessarily leaves the index populated.
4. **Confirm what happened.** `git show HEAD:<file>` holds your marker once and theirs not at all, and the worktree file still holds both: `grep -c '<their marker>' <file>` prints 1. If it prints 0, their edit was lost by something other than this procedure; stop and tell the user.

Because the worktree is never rewritten, there is no restore step and no window in which a peer's edit can be clobbered. (An older form of this procedure wrote the mine-only copy into the worktree and restored the both-edits copy afterwards; any peer write inside that window was silently overwritten.)

### 3. Verify and cite what shipped

1. **Verify every commit with `git show --stat --format='%h %s' HEAD`**, not by its subject line. The message is the one part guaranteed to say what you intended.
2. **Per edited file, run `git show HEAD:<file> | grep -c '<your exact string>'`.** Another session can overwrite an edit you had not yet staged, so `--stat` lists the file while your content is gone. Print a count, never a window of lines: the lines around yours can hold credentials. ([Verifying your own write is a disclosure vector](../casebook/verifying-your-own-write-is-a-disclosure-vector.md).)
3. **After an index-form commit, run `git log --oneline -S'<a string unique to your edit>' -- <file>`** to see which commit introduced your edit. The HEAD content check passes whether your commit or a peer's shipped it. ([The probe that reads the same in both branches](../casebook/the-probe-that-reads-the-same-in-both-branches.md).)
4. **Before citing what a commit did, read `git show <sha> -- <path>`.** Its subject line, its author, and your memory of what you staged are intent, not content; on a shared checkout a commit can carry a peer's staged edits that its message never mentions.

## Notes

- **Never bulk-stage** (`git add .`, `-A`, `-u`) and never rebase without the user's permission; see `CLAUDE.md` → Workflow. If a rebase is needed, stop and ask the user to run it themselves; if they ask you to run it, check `git status` first and leave unstaged changes you did not make alone.
- **Coordinate live when you can.** If two sessions want to write the same file at once, having one wait a minute is cheaper than any reconstruction.
- **Commit small and commit quickly.** Every minute an edit sits uncommitted is a minute another session can overwrite it.

## Related

- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md) — §3 carries the short form of these rules at every commit
- [The correct check and the wrong outcome](../casebook/the-correct-check-and-the-wrong-outcome.md) — why a separated check still races
- [The check that cannot stop the action](../casebook/the-check-that-cannot-stop-the-action.md) — why checks run in their own command
