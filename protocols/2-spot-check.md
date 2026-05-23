# Protocol 2: Spot-Check

Detect contradictions across the wiki by comparing randomly sampled file pairs. Designed to scale to large wikis where reading every page in a single pass is impractical.

Two gears:
- **Gear 1 — Single shot.** One pass of N random pairs (default 40). Fast, suitable for inline Protocol 7 use or a one-off check.
- **Gear 2 — Marathon.** Continuous parallel sampling until convergence — keep N subagents alive, dedupe against a register, stop at 10 consecutive zero-finding runs. Use when you want to drain real cross-page drift, not just spot-check it.

## Trigger

- "Run Protocol 2" or "Spot-check" → Gear 1 (default)
- "Run Protocol 2 deep" → Gear 1 with 80 pairs
- "Run Protocol 2 marathon" or "P2 Gear 2" → Gear 2

## Gear 1: Single-Shot Spot-Check

### Procedure

1. **Inventory** — List all `.md` content files (exclude `CLAUDE.md`, `README.md`).
2. **Sample pairs** — Randomly select 40 unique pairs of files. Prefer cross-domain pairs (e.g., a containers page paired with a storage page) over same-directory pairs, since contradictions are more likely across domain boundaries.
3. **Compare each pair** — For every pair, read both files and check for:
   - **Factual contradictions** — disagreements about specs, IPs, ports, paths, identifiers, resource allocations, or current state
   - **Stale cross-references** — one page references information on the other page that has since changed
   - **Definitional drift** — the same concept described differently in each file
4. **Report** — After all pairs are compared, produce a findings summary listing:
   - Each contradiction found, citing both files and the conflicting statements
   - A confidence level (certain / likely / possible) for each finding
   - Suggested resolution (which file is probably correct, or whether both need updating)
5. **Verify** — Run Protocol 3 to generate commands that check ground truth on live systems. Present the commands to the user and wait for confirmation before applying fixes.
6. **Classify each finding before fixing.** This is the load-bearing step — see "Doc-only vs live-config" below. Findings that describe live system state can only be auto-fixed AFTER Protocol 3 has confirmed which side is wrong; until then they get queued as suggestions to the user.
7. **Fix doc-only findings.** Apply all certain and likely fixes that are confined to documentation (status banners, supersedence headers, page-internal consistency, count tables the wiki itself owns). Leave possible findings for human review, noted in the PR description.
8. **Commit, push, and create/update a PR** with findings in the PR body. Surface the suggestion queue (live-config items) in the PR body too, with the verification commands the user needs to run.

### Doc-only vs live-config: what's auto-fixable

A finding can be auto-fixed only if the wiki is the authoritative source for the fact in question. If the fact lives on a running system (env var, container image, mount path, network identity, pool membership, address-to-host mapping, file-system state, etc.), the wiki is documenting reality, not defining it — and the agent cannot tell which side of a contradiction is correct without checking the live system.

| Category | Examples | Auto-fixable? |
|---|---|---|
| **(A) Doc-only** — wiki IS the source of truth | Retirement banners, protocol prescriptions, status notes, supersedence headers, hub iteration lists | Yes |
| **(B) Wiki internally inconsistent / stale relative to another wiki page that itself records a verified migration** | Count tables where the inventory page already shows the new count; visual maps where the file's own table is authoritative; the homepage roster lagging behind a project's own `_index.md` | Yes (sync to the authoritative wiki page) |
| **(C) Wiki vs. live system state** — wiki documents a running config | Env vars, container image tags, mount paths, pool memberships, address-to-host mapping, currently-loaded model versions, reverse-proxy routes | **No — queue as suggestion.** Add a line to a manual-verify scratch file with the verify command and the proposed live-and-doc fix. Do NOT edit the wiki to match what looks correct. |

**Rule of thumb:** if applying the fix would make the wiki *lie* in the case that the live system is actually using the old value, the finding is category (C). Even if another wiki page records the migration, that record is not a live verification — migrations get planned, partially executed, or rolled back without docs catching up.

**Cross-page consistency is NOT live verification.** If `page-a.md` says service was upgraded but `page-b.md` still shows the old version, **both** could be wrong, or **either** could be wrong. Protocol 3 against the live system is what resolves it.

### How to file a (C) finding

Append to a manual-verify scratch file (e.g. `.scratch/p2-needs-manual.md`, gitignored) under "Live verification queue":

```
N. **<one-line description>**
   - Wiki currently says: <quote>
   - Reason for doubt: <which other wiki page or finding triggered this>
   - Verify: `<exact shell command>`
   - Suggested action: if live is X, change live to Y and update doc; if live is Z, fix doc only.
```

The next P2 cycle (or a dedicated fix session) picks this up. The marathon does not block on these — they're a backlog, not a gate.

### Tuning (Gear 1)

- The default is 40 pairs. If invoked as "Protocol 2 deep", use 80 pairs.
- If invoked with a topic (e.g., "Protocol 2: storage"), restrict the inventory to files matching that topic and compare every file against every other (full cross-join instead of random sampling).
- Inside Protocol 7, P2 samples across the **full tree** every cycle (not narrowed to the cycle's diff). High finding counts on a narrow diff are evidence the surrounding tree has unmeasured rot — random sampling is how that rot gets surfaced.

## Gear 2: Marathon (Continuous Parallel Loop)

The marathon runs many Gear-1 spot-checks back-to-back in parallel, deduping against a persistent findings register, until the wiki actually stops surfacing new contradictions. Use when you suspect real drift, not when you just want a sanity check.

### Setup

- Keep **8 P2 subagents running in parallel** at all times. Each runs the standard Gear-1 40-pair sample with its own random seed.
- Subagent model: **mid-tier** is the default for marathon work (best findings/cost ratio on Claude that means sonnet-class). Frontier models (Opus-class) are more conservative on random samples; haiku-class is unfit — it tends to rubber-stamp the register instead of doing the work.

### Reporting (per subagent)

Each subagent must end its message with two lines:
- `HARD: <N>` — count of mutually-exclusive cross-page facts (different addresses/ports/identifiers/dates/statuses for the same thing)
- `SOFT: <N>` — count of stale pages, intra-file inconsistencies, single-page errors, hub-vs-roster mismatches

Subagents must read the active register first and only report findings NOT already in it. Subagents do steps 1-4 only — do not let them run Protocol 3, fix, or commit.

### Scoring

- Hard finding = 1.0, soft finding = 0.5.
- **Already-logged findings don't count** — only NEW unique findings contribute to the score.
- Run score = sum of unique-finding weights for that subagent.

### Streak + stop condition

- Streak = consecutive runs with `score = 0`.
- Reset to 0 on any non-zero run.
- **Stop when streak reaches 10.**

### Main-thread responsibilities

- Maintain a findings register at `.scratch/p2-marathon-findings.md` (gitignored) with: HARD section (numbered F1, F2, …), SOFT section, open questions for the user, and a streak ledger.
- After each subagent completes: read its result, classify findings as new vs already-logged, update the register, log the score and streak, immediately launch a replacement subagent to keep 8 active.
- **Classify each finding A / B / C per Gear-1 step 6.** (A) and (B) → safe to auto-fix in the post-converge batch. (C) → append to the manual-verify scratch file under "Live verification queue" with the verify command. Do not auto-fix (C) items, even if "the right answer looks obvious from another wiki page." Cross-page consistency is not live verification.
- After the marathon converges (or you pause it): batch-fix only the (A) and (B) findings (Gear 1 step 7), commit per Protocol 7, and hand the (C) queue back to the user. The user decides whether to live-verify in-session or defer.

### Tips

- Skip-list grows naturally. Every 8-10 runs, refresh the per-subagent prompt's "skip categories" list with the recently-logged finding patterns so subagents don't waste their context re-flagging things you've already captured.
- Historical session logs are not retroactively edited per repo style guide — exclude them from "stale page" findings unless the agent is sure.
- Wiki-wide patterns (e.g. stale "Last Updated" stamps on idea pages, empty `_index.md` stubs in active log dirs) are patterns, not per-page bugs — collect once, don't re-flag each instance.
- The marathon may not converge on a drift-heavy wiki within a single session. That's fine — the register is the artifact. Pause, fix, resume next session.
