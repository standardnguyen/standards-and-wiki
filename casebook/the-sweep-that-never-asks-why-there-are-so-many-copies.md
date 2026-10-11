# The sweep that never asks why there are so many copies

## The shape

You change a fact — a count, an address, a default. You know the fact lives on more than one page, so you sweep: search for the old value, update every hit, and send reviewers after the copies your search missed. In one maintainer's own cycle (a single measurement, not a general rate), six rounds reported 157 stale copies.

There were never 157 problems. About 60% of the findings were numbers or counts written into prose. One fact typically lived on four to nine pages. Over a third of all findings were the same dozen facts found again in a later round. The sweep was propagating each fact to all its copies and never asking whether the fact should have that many copies.

So every sweep left the wiki more consistent and exactly as duplicated, and the next change to any of those dozen facts paid the same bill again.

A second version of the same mechanism lives in single words. A cleanup script gains a flag that limits it to one environment; before, it acted on all of them. The phrase *"cleans everything"* now describes it wrongly, and that phrase sits in the script's header, two help screens, a remedy section and a protocol step. Round after round finds a few more of them, because each round searches for the phrasing its author remembers. The count of known copies rises while the correcting sentence is being written.

## Why it survives review

Because each round is doing its job. It finds stale copies and fixes them, and each fix is right. A sweep is measured by what it finds, and a sweep that finds a lot looks productive.

The question that would end it — *why does this fact live in nine places?* — is not a question the sweep is built to ask. The sweep's frame is propagation: given a change, carry it everywhere. Reducing the number of places is a different task, and nothing in the sweep's procedure points at it.

Scope words make it worse because they do not look like facts. *Every*, *all*, *the whole*, *verified*, *covered*, *resolved* — these read as description, not as a value that can go stale. They go stale the moment the thing they describe grows a tier, a flag, or a filter.

## The general form

**Propagating a fact to its copies fixes the instance. Reducing the copies fixes the cause. A sweep that only propagates will be repeated forever at the same cost.**

The signals that you are fixing instances, not the cause:

1. You are updating the same fact on its third page.
2. Three or more findings in one round share one mechanism.
3. You are sweeping prose for a fact that a file or command already defines.
4. The same fact turns up again in a later round of the same sweep.

## What it costs

The full cost of every future change to that fact, multiplied by the number of copies, for as long as the copies exist. Plus the copies the sweep misses, which disagree with the ones it fixed — and one page disagreeing with eight is worse than nine pages agreeing on a stale value, because now the wiki contradicts itself.

## The defense

1. **Give each fact one home.** Other pages link to it instead of restating it. A link cannot go stale when the fact changes.
2. **Where a file or command already defines the fact, point at that** rather than copying the value into prose. Better: let a check script compare the prose against the source and fail on mismatch. A deterministic check catches this class in seconds, where reviewers cost far more and still miss copies worded differently.
3. **Replace a summarizing word with the facts it summarizes.** *"Backed up off-site"* is one claim that can be partly true. Four separate statements — what, where, how often, last verified — can each be checked.
4. **When three findings share one mechanism, stop fixing findings.** Fix the mechanism once: consolidate the copies, or write the one check keyed on the words that make the claim.

## The trigger

You are about to update the same fact on a third page, or you have just found the third stale copy of one phrase, or you are writing *every*, *all*, or a summarizing word like *verified* about something that has, or could grow, a tier, flag or filter.
