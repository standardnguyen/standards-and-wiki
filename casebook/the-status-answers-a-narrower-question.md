# The status answers a narrower question

## The shape

You verify a build the way you have verified it all day:

```bash
./build-site 2>&1 | tail -5
echo $?
# 0
```

Zero. The site builds. Four commits later you find it has not built since the first of them.

`$?` after a pipe is the exit status of the **last** command in the pipe. `tail` succeeded at printing five lines. The build's own failure was in those five lines, and the status you checked was tail's.

The same shape, in other clothes:

- **Exit 0 by design.** A scheduled publish script exits 0 on every path, so a failed push never wedges the schedule. That choice is defensible. It also means the failed push is recorded only as a line in the script's own log, and the public site serves days-old data while every run reports success.
- **One flag, two causes.** A merge request reports `mergeable: false`. You resolve the conflicts. It still reports `false`, because the request is marked as a draft, and a draft reports `false` however clean the merge is. A session that trusts the flag keeps re-resolving conflicts that no longer exist and reports a block that is not there.
- **Green build, wrong output.** The site generator exits 0. A table lost more than a hundred rows because a line break moved; a link points one directory too deep; a page beside a same-named directory was dropped from the site without a warning. The build's job was to finish, and it finished.
- **Merged is not deployed.** The fix is merged. You probe the fixed endpoint and it returns 200. But a handler that swallows authorization errors returns 200 with the guard present or absent, and the fix sits undeployed for days while the record says it shipped.

## Why it survives review

Because a status value is the most trustworthy-looking thing a tool emits. It is a single token, it is machine-generated, and it has a convention everyone knows: zero is good. Reading it feels like reading the verdict, and reading the output feels like reading the commentary.

But every status answers a specific, narrow question, chosen by whoever wrote the tool. *Did the last stage of this pipe succeed. Did the script reach its end. Is this request in a state where the merge button is enabled. Did the generator finish.* You asked a broader question — *is the thing I care about correct* — and accepted an answer to a narrower one because it arrived in the format of an answer.

## The general form

**A status value answers the question its author chose. Before treating it as a verdict, name that question and check it is yours.**

| status you read | question it answers | question you asked |
|---|---|---|
| `$?` after a pipe | did the last stage succeed | did the first stage succeed |
| exit 0 from a job built never to fail | did the job reach its end | did the job do its work |
| a boolean with two causes | is either cause present | is the cause I fixed present |
| a green build | did generation finish | is the output right |
| "merged" | is the change on the branch | is the change running |

## What it costs

A real failure hidden for as long as nobody looks at the artifact. The cost grows with the run of green statuses, because each one is recorded as a pass and each pass makes the next look routine. A failure behind a status check is found by a human noticing the artifact is wrong, which is the slowest detector there is.

## The defense

1. **Read the status of the command you mean.** In a pipe, use `set -o pipefail` or read `${PIPESTATUS[0]}`, or do not pipe the check at all. Run checkers unpiped and read their own exit.
2. **Check the artifact, not the status, for anything that runs unattended.** A job that must never wedge its schedule can keep exiting 0, but then something else has to watch the output: a freshness check on the published data, an alert when it goes stale.
3. **When a flag has more than one cause, read the field that names the cause.** A merge request's draft state and its conflicted-files list tell the two causes apart; the summary flag does not.
4. **After a build, check one expected output exists and is right.** One rendered row count, one link, one page that should be there. A checker for the silent-failure classes your generator has is worth building once each class recurs.
5. **Verify a deploy on the box, not on the endpoint.** Read the deployed revision, the file's modification time, or a count of the new string in the deployed file. An endpoint probe tells you the service answers, not which code answered.

## The trigger

You are about to act on one status value — an exit code, a boolean field, a green badge, the word "merged" — as if it were the diagnosis.

Especially when the status came through a pipe, from a tool built to always succeed, or from a probe on the thing you just fixed. Ask what question the status answers, and whether anything would have read differently if you were wrong.
