# The check that cannot stop the action

## The shape

You write a verification step, and then you chain it to the thing it verifies:

```bash
git diff --cached --stat && git commit -m "..."
```

The check runs. Its output is correct. The commit happens anyway.

## Why it survives review

Because the check *is* real, and its output *is* right. Nothing about the line is wrong except its position in time.

`&&` means "run the second thing if the first one exits zero." `git diff --cached --stat` exits zero when it successfully prints a diff — including when the diff it prints is the wrong one. The exit code answers *did the command work*, not *did you like the answer*. There is no version of a human-read check that can gate a `&&`, because the gate is evaluated by the shell in microseconds and the human reads the output afterward.

And afterward is the problem. Both outputs land in the same result. You scroll up, read the file list, and confirm it was correct — after the commit that used it has already shipped.

The check has become documentation of what you did, not a decision about whether to do it.

## The general form

**A verification step folded into the same atomic action it verifies cannot prevent that action.**

It generalizes past shells. Any place where the confirming read and the committing write happen inside one indivisible step has this shape: a dry-run flag that prints its plan and then executes it in the same invocation; a preview pane rendered by the same call that publishes; a "confirm?" that is logged rather than awaited; an assertion inside the function whose side effects have already fired above it.

The tell is not the `&&`. The tell is that **there is no point in time at which a human or a caller could have said no.**

## What it costs

Whatever the action costs, plus the false confidence. The second part is worse. An unchecked action is a known risk. An action with a decorative check attached is a risk you have already decided is handled — you will not re-examine it, and neither will your reviewer, because the guard is right there in the diff.

## The defense

**Separate the commands.** Run the check. Read it. Then run the action, as its own invocation, after you have decided.

That is necessary and not sufficient, because a check separated in time is still a check against *shared mutable state* — see *the correct check and the wrong outcome* in this book's chapter on checks for the race that defeats even a correctly-separated check.

The stronger fix, where the tool allows it: **make the action name its own targets.** Instead of checking what happens to be staged and then committing whatever is staged, name the paths in the commit itself. Then the check is confirming *what you are about to do* rather than *what state currently holds*, and the two cannot drift apart between the reading and the doing.

## The trigger

Any time you catch yourself writing a safety step and an action on the same line, or in the same call. The impulse that produces it is a good one — you are trying to be careful and also trying not to be slow — which is exactly why it is worth naming. **Carefulness that costs nothing usually isn't.**

If separating the check makes the workflow feel more tedious, that tedium is the check actually existing.
