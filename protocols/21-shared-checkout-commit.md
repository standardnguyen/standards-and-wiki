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
   rc=0; foreign=$(git diff --cached --name-only -z --no-renames | grep -zvxF -f "$list" | tr '\0' '\n'; exit "${PIPESTATUS[1]}") || rc=$?
   [ "$rc" -eq 1 ] || { echo "abort: ${foreign:-grep error}" >&2; exit 1; }    # 1 = nothing foreign
   [ "$(git rev-parse HEAD)" = "$base" ] || { echo "abort: HEAD moved; rebuild" >&2; exit 1; }
   git commit -m "..."
   ```

   `-z` and `--no-renames` matter: without `-z`, git quotes non-ASCII paths and a clean commit aborts; without `--no-renames`, a peer's staged deletion that resembles your new file prints as one rename and slips through. Write the assignment as `rc=0; foreign=$(...) || rc=$?`: grep exits 1 when it finds nothing foreign, which is the success case, and under `set -e` a bare assignment would abort the script right there (found by running it). A plain `... | grep ... && exit 1` fails open when the list is missing (grep exits 2) and aborts every clean commit if chained. If the assertion aborts, unstage the foreign path with `git restore --staged <path>` and rebuild.
7. **A check you read runs in its own command; only an assertion that aborts may chain into the commit.** A chained check is read after the commit has shipped. ([The check that cannot stop the action](../casebook/the-check-that-cannot-stop-the-action.md).)
8. **Never `--amend`; make a second commit.** An amend rewrites whatever HEAD is now, so a peer's commit that landed after yours ships under your message.

Tested in a throwaway repo: with index = base + your row and worktree = base + your row + their row, `git commit f.md` commits their row; plain `git commit` commits only yours and leaves theirs uncommitted in the worktree.

### 2. Mine-only reconstruction

Use it when a file you must commit also holds another session's uncommitted edit; a shared index file such as a session-log index is the usual case.
The one model, stated the same way in Protocol 7 §3: make your edit first, then run the script below, which stages the mine-only copy (the file at HEAD plus your edit) straight into the index and commits it in one invocation; nothing rewrites the worktree.
Because the write-back form it replaced (write the mine-only copy into the worktree, stage it, write the both-edits copy back) overwrote any peer write in between, and its restore step lost a peer's row unseen.

1. Save the script as a file, fill in its six values, and run it with `bash` from the repo root.
   Because it builds, stages, asserts and commits in one invocation, and any pause between staging and committing is a window another session can commit through.
2. `OLD` is the text your edit replaced and `NEW` what it made of it; every value goes in single quotes, with `'` written as `'\''`, and never into the Python.
   Because a Python bytes literal rejects an em dash and reads `\n` as a newline, and a failed build without `pipefail` stages and commits an empty file.
3. `MINE` and `THEIRS` are strings that only your edit and only theirs add; on a log index use the whole row, never the log id.
   Because the id sits in both the ID column and the row's URL, so a count of 1 fails on correct data.
4. Before staging it aborts if anything is staged, `OLD` is not exactly once at HEAD, `NEW` lacks `MINE` or holds `THEIRS`, or `NEW` adds a line the worktree lacks.
   Because that last check is a subset of lines, which catches a mangled `NEW` (a stray indent, a lost `\r`) at any placement, where a count does not.
5. After staging it aborts if anything else is staged, HEAD moved, or the index entry is no longer yours, and its exit trap then unstages your copy.
   Because a stale base reverts a peer's commit, two sessions staging one file ship each other's rows, and a copy left staged ships under the next plain commit's message.
6. After the commit it stops if HEAD is not your blob on the recorded base, or their edit has left the worktree.
   Because a peer can still stage in the instant before `git commit`, and no index or HEAD check sees the worktree.
7. After an abort, clear its cause and rerun: commit any staged file of yours by pathspec (§1) first; if it says `THEIRS` is at HEAD, their edit has shipped and §1 applies to yours too; if it warns that your copy is still staged, unstage it once git is free.
   Because the pre-check refuses any staged path, whoever staged it, and the trap cannot unstage while another git process holds the index lock.
8. When you change the script, run it in a throwaway repo through every abort branch and on the real file's shape before you rely on it, and when two runs disagree, find the hidden variable before writing either up.
   Because each defect in its history surfaced only when it was run, and a predicate passes where its author ran it.

```bash
set -euo pipefail
f='<file>'                           # repo-relative, no ./
OLD='<the text your edit replaced>'  # exactly once at HEAD
NEW='<what your edit made of it>'
MINE='<a string only your edit adds>'
THEIRS='<a string only their edit adds>'
msg='<commit message>'
export f OLD NEW MINE THEIRS
base=$(git rev-parse HEAD)
[ -z "$(git diff --cached --name-only)" ] || { echo "abort: something is already staged" >&2; exit 1; }
mode=$(git ls-tree "$base" -- "$f" | cut -d' ' -f1)
[ -n "$mode" ] || { echo "abort: $f is not tracked at HEAD" >&2; exit 1; }
blob=$(git show "$base:$f" | python3 -I -c 'if 1:
    import os, sys
    e, b = os.environb, sys.stdin.buffer.read()
    w = open(e[b"f"], "rb").read()
    if e[b"THEIRS"] in b or e[b"THEIRS"] not in w: sys.exit("abort: THEIRS must be in the worktree and not at HEAD")
    if b.count(e[b"OLD"]) != 1: sys.exit("abort: OLD is not exactly once at HEAD")
    n = b.replace(e[b"OLD"], e[b"NEW"], 1)
    if n.count(e[b"MINE"]) != 1 or e[b"THEIRS"] in n: sys.exit("abort: NEW must add MINE once and THEIRS never")
    if not set(n.split(b"\n")) - set(b.split(b"\n")) <= set(w.split(b"\n")): sys.exit("abort: NEW adds a line the worktree lacks")
    sys.stdout.buffer.write(n)' | git hash-object -w --stdin)
undo() { if [ "$(git rev-parse -q --verify ":$f")" = "$blob" ] && [ "$(git rev-parse -q --verify "HEAD:$f")" != "$blob" ]; then git restore --staged -- "$f" || echo "WARN: $f is still staged as $blob; unstage it" >&2; fi; }
trap undo EXIT
git update-index --cacheinfo "$mode,$blob,$f"
[ "$(git diff --cached --name-only -z --no-renames | tr '\0' '\n')" = "$f" ] || { echo "abort: something else got staged" >&2; exit 1; }
[ "$(git rev-parse HEAD)" = "$base" ] || { echo "abort: HEAD moved; rerun" >&2; exit 1; }
[ "$(git rev-parse ":$f")" = "$blob" ] || { echo "abort: the index entry is not yours" >&2; exit 1; }
git commit -q -m "$msg"
c=$(git rev-parse HEAD)
[ "$(git rev-parse "$c^") $(git rev-parse "$c:$f")" = "$base $blob" ] || { echo "STOP: HEAD is not your blob on $base; read git log -2 --stat" >&2; exit 1; }
/usr/bin/grep -qF -- "$THEIRS" "$f" || { echo "STOP: their edit is gone from the worktree" >&2; exit 1; }
echo "committed $c"
```

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
