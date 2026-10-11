# Protocol 21: Shared-Checkout Commit

How to commit when several agent sessions, background jobs, or scheduled tasks share **one git checkout** and stage and edit files while you work. [Protocol 7](7-commit-and-ship.md) §3 carries the short form at every commit; this page is canonical for the commit forms and for the mine-only reconstruction.

The underlying fact: **the index and the worktree are shared mutable state.** Anything you check about them can change before the commit that relies on the check. Every step below either narrows a window (to the milliseconds between your last assertion and the commit; a fully atomic commit would need a compare-and-swap on `HEAD`) or verifies what actually shipped.

Read this file from disk when you run it; a remembered copy predates the latest fix.

## Trigger

Any commit on a checkout that another live session or background job can touch. Run §2 whenever a file you must commit also holds another session's uncommitted edit — a shared index file such as a session-log index is the usual case.

<!-- Customize: if your repo only ever has one session at a time and no background jobs write to the tree, Protocol 7 §3 is enough and this protocol is optional. -->

## Procedure

### 1. Pick the commit form

Pick the form by where the bytes you mean to ship live: the worktree or the index.

1. **A file only you touched: commit by pathspec**, `git commit <path1> <path2> -m "..."`, never `git add` followed by a bare `git commit`. Name files, never a directory or a glob (a directory pathspec commits every tracked change under it, peers' included, and a path containing `[ ] * ?` is a glob). Pathspec commits those paths from the worktree regardless of what else is in the index, so a peer re-staging between your check and your commit cannot add their files to yours. It also rewrites the index entries for those paths, replacing any index-only version a peer had staged. ([The correct check and the wrong outcome](../casebook/the-correct-check-and-the-wrong-outcome.md).)
2. **`git add` every new file first.** Pathspec matches only tracked paths, so one untracked path aborts the whole commit: `error: pathspec '<path>' did not match any file(s) known to git`.
3. **Before a pathspec commit, record `base=$(git rev-parse HEAD)` and run `git diff --numstat "$base" -- <paths>`, and account for every deletion.** Pathspec ships the worktree. If a peer committed from the index without restoring the worktree, yours lags HEAD, and your commit silently reverts theirs. Read `--numstat`, not a grep over the diff text: a deleted markdown bullet renders as `-- item`, and a pattern like `^-[^-]` skips it. A deletion count cannot tell your own replaced lines from a reverted peer line, so classify each one with the diff in step 4. Then commit in the same command as a check that HEAD has not moved: `[ "$(git rev-parse HEAD)" = "$base" ] || exit 1; git commit <paths> -m "..."`. After it, `git diff --numstat HEAD^ HEAD -- <paths>` must match what you read before.
4. **Read the diff of every path you name, against what will ship.** Before a pathspec commit that is `git diff HEAD -- <path>` (the worktree against HEAD); before an index-form commit it is `git diff --cached -- <path>`. A bare `git diff <path>` compares the worktree with the *index*, so a hunk a peer has already staged does not appear in it. `git status` prints `M <file>` whether or not another session's hunk is in it, so it cannot tell you the file is all yours. On a file with very long lines, read it as `git diff -U0 --word-diff=plain -- <path>`.
5. **A file you reconstructed mine-only (§2) ships from the index: commit it with plain `git commit`.** Pathspec would commit the worktree copy, which holds the other session's change, under your message. When one commit would span both kinds of file, split it into two commits rather than choosing one form for the pair.
6. **Before a plain `git commit`, assert on the whole index, in the same command**, aborting if it lists any path that is not yours, or if `HEAD` moved. A path-scoped `--cached` check cannot see what another session staged, so it reads clean either way. An example for bash, run as a script or inside `( ... )` (a bare `exit` closes an interactive shell). `$list` is a private temporary file listing your repo-relative paths, one per line; never a fixed name such as `mine.txt`, which a peer's run can overwrite and so whitelist their own paths:

   ```bash
   base=$(git rev-parse HEAD)                       # recorded when you built what you will commit
   list=$(mktemp); printf '%s\n' path/one path/two > "$list"
   [ -s "$list" ] || exit 1                         # no list: abort, never fail open
   foreign=$(git diff --cached --name-only -z --no-renames | grep -zvxF -f "$list" | tr '\0' '\n'; exit "${PIPESTATUS[1]}"); rc=$?
   [ "$rc" -eq 1 ] || { echo "abort: ${foreign:-grep error}" >&2; exit 1; }    # 1 = nothing foreign
   [ "$(git rev-parse HEAD)" = "$base" ] || { echo "abort: HEAD moved; rebuild" >&2; exit 1; }
   git commit -m "..."
   ```

   `-z` and `--no-renames` matter: without `-z`, git quotes non-ASCII paths and a clean commit aborts; without `--no-renames`, a peer's staged deletion that resembles your new file prints as one rename and slips through. A plain `... | grep ... && exit 1` fails open when the list is missing (grep exits 2) and aborts every clean commit if chained. If the assertion aborts, unstage the foreign path with `git restore --staged <path>` and rebuild.
7. **A check you read runs in its own command; only an assertion that aborts may chain into the commit.** A chained check is read after the commit has shipped. ([The check that cannot stop the action](../casebook/the-check-that-cannot-stop-the-action.md).)
8. **Never `--amend`; make a second commit.** An amend rewrites whatever HEAD is now, so a peer's commit that landed after yours ships under your message.

Tested in a throwaway repo: with index = base + your row and worktree = base + your row + their row, `git commit f.md` commits their row; plain `git commit` commits only yours and leaves theirs uncommitted in the worktree.

### 2. Mine-only reconstruction

Use this when a file you must commit also holds another session's uncommitted edit, and the file is already tracked. It does not apply to a new file. Do not stage the whole file.

The model: make your edit first, in the worktree, as usual. The worktree file is then the **both-edits copy** (their change + yours), and you never need to rewrite it. The **mine-only copy** is the file at a recorded `HEAD` plus your edit, applied by exact-once replacement on bytes. You put the mine-only copy into the **index** directly, so the worktree is never touched and a peer's late write to it cannot be overwritten.

1. **Record the base and refuse the cases this does not cover.** If the file is not in `HEAD`, or someone has already staged it, stop.
2. **Build the mine-only bytes from that base, byte-exact, and stage them without touching the worktree:**

   ```bash
   base=$(git rev-parse HEAD)
   git cat-file -e "$base:<file>" || { echo "abort: <file> is not in HEAD; this section does not apply" >&2; exit 1; }
   [ -z "$(git diff --cached --name-only -- <file>)" ] || { echo "abort: <file> is already staged by someone" >&2; exit 1; }
   mode=$(git ls-files -s -- <file> | cut -d' ' -f1)          # keeps 100644 / 100755
   blob=$(git show "$base:<file>" | python3 -I -c '
   import sys
   b = sys.stdin.buffer.read()
   old = b"<a line that appears exactly once>"
   new = b"<that line>\n<your edit>"
   assert b.count(old) == 1, "anchor must appear exactly once"
   sys.stdout.buffer.write(b.replace(old, new, 1))
   ' | git hash-object -w --stdin)
   git update-index --cacheinfo "$mode,$blob,<file>"
   ```

   Build the bytes in a script like this, never in a shell variable: command substitution strips trailing newlines, so a variable passed to `printf '%s'` drops the file's final newline (and leaves a stray `\r` on a CRLF file), and the next appended row glues onto the last one. Never pipe a `$(...)` result straight into `hash-object`. If you must stay in shell, append a sentinel (`X=$(...; printf x); X=${X%x}`).
3. **Assert and commit in one invocation** (§1 step 6, with `base` from step 2), and add one more assertion before the commit: `[ "$(git rev-parse :<file>)" = "$blob" ] || { echo "abort: index entry is not mine" >&2; exit 1; }`. Without the first, a peer who commits to the same file between your build and your commit has their edit reverted by yours. Without the second, two sessions running this at once overwrite each other's staged entry and each ships the other's row under its own message. Any pause between staging and committing is a window another session can commit through, and this procedure necessarily leaves the index populated.
4. **Confirm what happened, by content.** `git rev-parse HEAD^` equals `$base`. `git diff --numstat HEAD^ HEAD -- <file>` shows only your additions; any deletion you did not make means you reverted someone. `git show HEAD:<file> | grep -cF '<your marker>'` prints 1 and `... '<their marker>'` prints 0. The worktree file still holds both: `grep -cF '<their marker>' <file>` prints 1. If your marker is 0 in HEAD, or theirs is present in HEAD, or theirs is gone from the worktree, stop and tell the user. Use `grep -cF` (a fixed string); a marker with `*`, `[` or `.` in it is otherwise read as a pattern and gives false alarms and false passes.

Pick a marker as a whole line of the edit that appears nowhere else in the file: for your edit, a line of yours; for theirs, a line of the other session's edit that your own edit does not contain. An identifier that appears twice per row (in a column and in a link) fails the count on correct data.

Because the worktree is never rewritten, this procedure cannot overwrite a peer's late edit to it. (An older form wrote the mine-only copy into the worktree and restored the both-edits copy afterwards; any peer write inside that window was silently overwritten.)

### 3. Verify and cite what shipped

1. **Verify every commit with `git show --stat --format='%h %s' HEAD`**, not by its subject line. The message is the one part guaranteed to say what you intended.
2. **Per edited file, run `git show HEAD:<file> | grep -cF '<your exact string>'`.** Another session can overwrite an edit you had not yet staged, so `--stat` lists the file while your content is gone. Print a count, never a window of lines: the lines around yours can hold credentials. ([Verifying your own write is a disclosure vector](../casebook/verifying-your-own-write-is-a-disclosure-vector.md).)
3. **After an index-form commit, run `git log --oneline -S'<a string unique to your edit>' -- <file>`** to see which commit introduced your edit. The HEAD content check passes whether your commit or a peer's shipped it. ([The probe that reads the same in both branches](../casebook/the-probe-that-reads-the-same-in-both-branches.md).)
4. **Before citing what a commit did, read `git show <sha> -- <path>`.** Its subject line, its author, and your memory of what you staged are intent, not content; on a shared checkout a commit can carry a peer's staged edits that its message never mentions.

## Notes

- **Never bulk-stage** (`git add .`, `-A`, `-u`) and never rebase without the user's permission; see `AGENTS.md` → Workflow. If a rebase is needed, stop and ask the user to run it themselves; if they ask you to run it, check `git status` first and leave unstaged changes you did not make alone.
- **Coordinate live when you can.** If two sessions want to write the same file at once, having one wait a minute is cheaper than any reconstruction.
- **Commit small and commit quickly.** Every minute an edit sits uncommitted is a minute another session can overwrite it.

## Related

- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md) — §3 carries the short form of these rules at every commit
- [The correct check and the wrong outcome](../casebook/the-correct-check-and-the-wrong-outcome.md) — why a separated check still races
- [The check that cannot stop the action](../casebook/the-check-that-cannot-stop-the-action.md) — why checks run in their own command
