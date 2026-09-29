# When you build the instrument, its bugs arrive as good news

## The shape

There is a defect you cannot see — too fast, too subtle, spread across a whole interaction. So you build the thing that makes it visible: a demo, a benchmark, a diagnostic view, a comparison harness. It replays the fixed input through each candidate and shows you the difference side by side.

There is no baseline to compare against. You are not checking the instrument against truth; the instrument **is** how you are finding out what the truth is.

So when it reports a clean result, you have nothing to check it against. And a clean result is exactly what a broken instrument reports.

Three separate defects in one such tool, built to make a rendering artifact visible:

1. **The pane was sized to the old estimate, so the whole script fit on screen.** The scroll target stayed at zero forever, and the viewport never moved — peak motion: **zero rows, in every mode, including the unfixed baseline.**
2. **The trace window (6 s) outlived the run it measured (~4 s).** By the time anyone looked, the graph was all idle frames — the evidence had scrolled itself away.
3. **A second view handed one series the entire pane height**, re-growing the overflow that the first fix had already corrected and verified — in a different view, so the earlier verification did not cover it.

Every one of them reported a perfectly smooth baseline. None looked like a defect. All of them looked like the answer you were hoping for.

## Why it survives review

Because a measuring tool's defects are **biased toward false negatives.**

Think about what each direction of error does to the observer. An instrument that *fabricates* a real-looking defect produces output that demands explanation — you go look, you find it is spurious, you fix the tool. An instrument that *hides* a defect produces silence, and silence is indistinguishable from a correct all-clear. Only one of the two branches generates a reason to investigate.

The null result is also the branch that requires nothing to work. For the tool to show you a defect, every part of it has to be functioning: the input has to reach the display, the display has to be in frame, the window has to include the event, the view has to contain the subject. For the tool to show you nothing, *any single one* of those can be broken. **False negatives have more ways to happen, and every one of them wears the costume of success.**

And the tool is usually built last, in a hurry, by the same person who is emotionally invested in shipping the feature it was built to justify. It gets the least review of anything in the change.

## The general form

**When the artifact you built is the instrument, its failures are systematically biased toward the result you wanted, so they arrive disguised as good news.**

This is distinct from an ordinary bug. An ordinary bug produces a wrong value somewhere you were going to look. An instrument bug produces a *correct-looking absence*, precisely in the measurement you built to be confident about. The two are not the same class of hazard, and the usual testing instinct does not cover the second one.

The general shape:

- the tool reports "nothing to see"
- the reader is relieved
- relief is not evidence
- no further check happens, because a clean bill is the natural end of an investigation

## What it costs

You conclude the problem does not exist, or that your candidate is as good as the other, or that the bug is fixed.

In the case above, the cost was a decision made on an instrument that could not display the thing being decided — the difference between three candidate implementations was judged from a view that had never shown any of them moving. And a separate indicator built to catch one specific defect **had never fired once**, which meant it was a hypothesis wearing a check's uniform; when it was finally tested against a constructed case, it turned out the case it was built for only triggered by coincidence, and it had to be rebuilt around an input that provably produces the effect.

That last one is worth separating out. *A check that has never failed is not a check.* It is an untested assertion about what would happen, and it will be cited as a safeguard from the day it is written until someone tries to break it.

## The defense

**Feed the instrument a known-bad case before you trust its clean ones.**

You already have a defect you have witnessed — the whole reason you built the tool. Put *that* in front of it, first, and confirm it shows up. If the instrument cannot reproduce a failure you have personally seen, the instrument is broken, and that is the finding, not an inconvenience to work around.

This is the single highest-value ten seconds in the whole exercise, and it is skipped because the tool already produced output.

Then three structural checks, in order:

1. **Is the subject in frame?** The window long enough to contain the event, the pane small enough to force the behavior, the view that actually contains the lane. Three of the three defects above are this one check in different clothes.
2. **Can the display show the defect at all?** If the observable is a change in a value that the display clamps, rounds, or averages away, the tool is measuring its own smoothing.
3. **Has the alarm ever fired?** Watch it fire on a constructed case, deliberately. Then it is a check. Before then it is a wish.

And note the meta-lesson, because it is the one that pays: the instrument *changed the answer*. The research had produced a defensible recommendation; looking at the actual thing produced a better one, once the tool worked. Which is the argument for building it — and the reason its bugs are so expensive.

## The trigger

The moment your instrument tells you the problem isn't there.

That is the reading that deserves the most suspicion, not the least, and the feeling to watch for is **relief**. Relief is produced identically by a working system and a broken instrument, and you cannot tell which from the inside.

Also: any time you notice you are treating a diagnostic, a demo, or a benchmark as authoritative and you have never seen it report a failure. And any time you build the thing you are using to judge.
