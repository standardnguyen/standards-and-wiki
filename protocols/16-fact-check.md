# Protocol 16: Fact-Check

Verify the wiki's claims about the **external world** against outside sources — published figures, dates, quotes, versions, prices, attributions. Catches stale numbers, misremembered dates, and misattributed quotes before they get cited somewhere that matters.

**This is not [Protocol 3 (Verify)](3-verify.md);** the split is the axis, not the effort.

| | Protocol 3 | Protocol 16 |
|---|---|---|
| Claim is about | State of *your* systems | State of the *world* |
| Method | Generate commands; a human runs them | Fetch a source; read it |
| Ground truth | What the machine reports | What the source says |
| If unreachable | The command failed — re-run it | **Unverifiable** — not a pass |

Looking at something you control → Protocol 3. Reading something someone else published → this one.

## Trigger

"Run Protocol 16" or "Fact-check `<area>`" — after Protocols 1 or 2 flag a suspicious claim, before a PR merges, or on a schedule for high-churn pages.

## Scope

Every verifiable claim — checkable against an external source, not merely internally consistent. Extract by class: **quantities**, **dates**, **quotes and attributions**, **versions and identifiers**, **prices and dated figures**, **policy and legal specifics**, **institutional claims** (who holds which role), and **causal claims** where both terms are checkable. Weight targets by churn: frequently rewritten pages are where errors enter; sample the quieter ones so coverage accumulates across runs. Errors compound — a wrong figure on an overview page gets cited by an analysis page, which informs a decision — and the cheapest moment to catch rot is at the source page.

## Procedure

### 1. Extract

Read the target pages and pull every verifiable claim into a working list, quoted verbatim with its location so a later fix can find it.

**Do not verify from memory.** Every claim gets an external source, including the ones you are sure about. Certainty is not evidence, and it is exactly the state in which the check fails to fire.

### 2. Verify

| Claim type | Source type |
|---|---|
| Quantities, statistics | The issuing body's own release; a registry or standards document |
| Dates, deadlines | The document that set the date — the primary record, not a summary of it |
| Quotes, attributions | The original transcript or reporting; a reproduction may have drifted |
| Versions, identifiers | Changelog, release notes, or package registry — code does not paraphrase |
| Prices, dated figures | The exchange or vendor's own historical data; the date matters as much as the number |
| Legal, policy specifics | The statute, docket, or official register — not a news summary of it |
| Personnel, structure | The organization's own page, or a dated report; a source's age is part of its value |
| Causal claims | Both terms separately — two correct facts can still be falsely joined |

⚠️ **Several pages agreeing is not several sources.** Copies share an upstream, so agreement measures propagation, not truth. Find the origin, or say you could not.

A public encyclopedia API suits settled background facts and poorly suits anything recent or contested:

```bash
curl -s -L -H "User-Agent: WikiFactCheck/1.0 (contact: <you>)" \
  "https://en.wikipedia.org/w/api.php?action=query&titles=ARTICLE_TITLE&prop=extracts&explaintext=true&format=json" \
  | python3 -c "import sys,json; p=json.load(sys.stdin)['query']['pages']; print(next(iter(p.values())).get('extract',''))"
```

### 3. Classify

| Category | Meaning | Action |
|---|---|---|
| **Wrong** | Factually incorrect | Correct it |
| **Stale** | Correct when written; the fact has since changed | Update, stamped with the date you read it |
| **Unverifiable** | No external source could confirm or deny it | Mark unverified — do not remove, do not treat as confirmed |
| **Imprecise** | Roughly right but materially misleading | Correct to the precise value |
| **Correct** | Checks out against a source | None |

### 4. Report

```markdown
## Fact-Check Results — YYYY-MM-DD
**Pages checked:** [list]  •  **Claims verified:** [n]
**Errors:** [wrong + stale + imprecise]  •  **Unverifiable:** [n]

### Findings
| Page | Location | Claim (verbatim) | Category | Correct value | Source |

### Unverifiable
| Page | Claim | Source attempted | Why (unreachable / no record / no mention) |
```

A row with an empty **Source** cell is not a finding — it is a gap; it belongs in the second table.

### 5. Fix — with permission only

Do not edit target pages automatically. Present the report and wait. Typical instructions: **fix all** (Wrong + Stale + Imprecise), **fix errors only** (Wrong), **log only** (record findings, edit nothing). Fixes commit per [Protocol 7](7-commit-and-ship.md).

Two things are never retroactively edited, whatever the instruction: **append-only records** (session logs, decision histories) and **dated snapshots** (a page recording what a source said on a given day). An error in one is reported and left standing — it is evidence about what was believed then, and rewriting it destroys what a later audit would use.

## Guardrails

- **Never fabricate a correction.** An unverifiable claim stays Unverifiable. A guessed value is worse than the error it replaces, because it arrives carrying a fix's authority.
- **No source left behind.** An unreachable source, an empty result, or a source that does not contain the claim is a *reported gap*. Never mark a claim Correct because you could not check it — *nothing found* is not *nothing there*.
- **Recalculate arithmetic from the raw inputs.** Any total, rate, or derived figure gets recomputed from the numbers it claims to derive from — not merely trusted to have used them.
- **Dates are exact, not approximate.** A figure cited as one day and actually from the previous day is an error, not a rounding difference. Verify the date as carefully as the value, and record when you read the source.
- **Do not expand scope.** This checks claims that already exist; it does not add information or act on a discovery. Material discoveries go in the report; acting on them is a separate decision.
- **Write the hedge down, don't only say it.** An uncertainty voiced in conversation and then omitted from the write-up leaves the caveat in the chat and the assertion on disk.

## Related

- [Protocol 3: Verify](3-verify.md) — the live-system counterpart
- [Protocol 1: Harmonize](1-harmonize.md) and [Protocol 2: Spot-Check](2-spot-check.md) — find *suspicious* claims; this one checks whether they are true
- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md) — where fixes land
