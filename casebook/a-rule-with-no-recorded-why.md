# A rule with no recorded why

## The shape

A rule sits in the instructions, stated flatly:

> **Do not use sources from `<publisher>`.** This is a hardline preference.

Solid, unambiguous, and short — which is what rules are supposed to be. It suppresses the wrong behaviour perfectly. Then, two months later, someone needs the *scope* of it, because a related question came up that the rule never anticipated.

Nobody re-reads the rule and understands it. Nobody can. It records a prohibition and not a disqualifier, so the only way to extend it is to guess at what would make it true:

> …the publisher's content is machine-generated, so it launders confidence.

Plausible. Neatly consistent with every other rule about unverified claims. Wrong, and — this is the part worth the whole entry — **wrong in both directions at once**:

| source | invented reason ("it is machine-generated") | actual reason ("the proprietor corrupts it") |
|---|---|---|
| an honest machine-built reference | ❌ banned | ✅ permitted |
| a human-written source whose owner degrades it | ✅ permitted | ❌ banned |

The invented version is not a loose approximation of the true one. It is the *negation* of it, on both axes, and it carries the authority of the highest-read file in the repository because it was written there. A later session reading that sentence obeys it confidently and never re-examines it.

## Why it survives review

Every individual step is reasonable.

The original rule was correct when written, and short rules are the point — a procedure interrupted by three paragraphs of justification is a procedure people stop reading. The session that re-derived it was doing the right thing: it found no reason, so it supplied one. That is what a careful reader does with an underspecified instruction, and it is precisely the operation that fails.

The failure is invisible because **there is nothing to check the invention against.** With no recorded *why*, an invented rationale has no competing claim in the file to lose to. It arrives, it fits, it is written down, and the file is now more confident and less correct than it was.

There is one more reason it goes unnoticed: the invented reason usually **hooks into a rule that already exists.** "Its content is machine-generated, therefore it launders confidence" slots neatly under a section about laundering. That fit is the tell, and it reads as confirmation.

## The general form

**A rule with no recorded reason gets re-derived, and re-derived wrongly.**

The reason is not decoration. It is the only part of a rule that can be *checked*. A prohibition says what not to do; a reason says what makes a case in-scope, which is the question every future session actually has. Remove it and the rule survives only as long as nobody needs its edges.

The corollary, which is the operative rule for anyone editing an instruction file:

> **The trimmable unit is the incident, never the *because*.**

Drop the date, the names, the narrative, the cost tally — all of that can live in a linked write-up and come back as a pointer. Keep one compressed clause of reason. *"Cost a full credential rotation"* earns its bytes. *"No damage, but someone flagged it"* does not. **A rule with no recorded why gets re-derived, and re-derived wrongly** — and that is a harder failure than a wordy rule, because a wordy rule is merely skimmed while a reasonless one is actively overwritten.

Two carve-outs, both cases where the reason must stay inline whatever it costs:

- **A write-time hazard.** The session never opens the pointer at the moment it is about to make the damaging write.
- **A rule whose trigger is self-recognition** — the operator or agent *noticing* that a situation applies. You cannot look up what you do not know to look for, so the trigger has to be in the loaded surface rather than behind a link.

## What it costs

The cost is proportional to how *load-bearing* the rule was, which is exactly the variable a re-derivation doesn't preserve. A restated rule binds nothing.

There is a characteristic second-order failure: the rule was stated three times before it stuck, and each earlier statement failed for a different structural reason.

| attempt | where it landed | why it didn't hold |
|---|---|---|
| first | in the instructions, with the rule and no reason | nothing to recognize, nothing to check an invention against |
| second | in a free-form write-up of one session | **not a rule surface** — no later session loads it; it bound nothing |
| third | canonical, with the reason recorded | — |

The middle row is the sharper failure and it is a pure instance of a general hazard: **a genuine standing preference captured in the one place guaranteed not to surface it.** The information was not lost. It was filed somewhere it could never fire.

## The defense

**Record the reason at the same time you record the rule, and record the wrong reason too.**

The fix is short and it is written into the rule itself:

> The disqualifier is *adversarial editorial control* — a proprietor deliberately degrading the product for ideological ends. **Not** "it is machine-generated." That axis is wrong in both directions: a human-written source whose owner corrupts it is equally disqualified, and an honest machine-built reference is not. *(This rule was re-derived wrongly once already; the wrong axis is recorded here so the next reader recognizes it as a known mistake rather than a fresh idea.)*

Three things that paragraph does: it states the reason, it names the wrong generalization, and it makes the wrong version recognizable on sight. Only the third one prevents the repeat — a reader who has already formed the wrong rationale needs to *meet* it on the page, marked as known-wrong, or they will simply re-derive it and find nothing objecting.

Then, when trimming the file for size:

1. **Cut the incident first.** Dates, names, retellings, and cost tallies go to a linked account and come back as one clause or a link.
2. **Never cut the final *because*.** The test: could a reader, holding only this sentence, decide whether a case not mentioned in the rule is in scope? If not, the reason is still missing.
3. **Record the disqualified reasons too**, not just the correct one, when the rule has already been re-derived wrongly once.

## The trigger

You are editing an instruction or policy file and the line in front of you states a prohibition with no reason attached.

Also: you are about to *extend* a rule to a case it does not explicitly cover, and the only tool you have is inference from the rule's text. That is the moment the re-derivation happens, and it will feel like interpretation rather than invention.

And the tell that you have already done it: **your new rationale fits neatly under an existing, unrelated principle.** A reason that slots perfectly into a nearby rule feels corroborated. It has corroborated nothing.
