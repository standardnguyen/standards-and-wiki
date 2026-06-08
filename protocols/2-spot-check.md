# Protocol 2: Spot-Check

Detect contradictions across the wiki by comparing randomly sampled file pairs. Designed to scale to large wikis where reading every page in a single pass is impractical.

Three gears:
- **Gear 1 — Single shot.** One pass of N random pairs (default 40). Fast, suitable for inline Protocol 7 use or a one-off check.
- **Gear 2 — Marathon.** Continuous parallel sampling until convergence — keep N subagents alive, dedupe against a register, stop at 10 consecutive zero-finding runs. Use when you want to drain real cross-page drift, not just spot-check it.
- **Gear 3 — Ultramarathon.** Higher concurrency plus targeted domain sweeps alongside random sampling — a larger fleet split between random samplers, spider samplers, and domain sweepers, converging at 30 consecutive zero-finding runs. Use when you want to drain drift from a large wiki exhaustively, not just sample it.

## Trigger

- "Run Protocol 2" or "Spot-check" → Gear 1 (default)
- "Run Protocol 2 deep" → Gear 1 with 80 pairs
- "Run Protocol 2 marathon" or "P2 Gear 2" → Gear 2
- "Run Protocol 2 ultramarathon" or "P2 Gear 3" → Gear 3

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
7. **Fix doc-only findings — with user review, not mass auto-apply.** ⚠️ **Don't rubber-stamp a bulk fix batch.** Even category (A)/(B) findings carry nuance the agent doesn't have: a "stale" table row might describe a secondary use case the agent doesn't know about; a page's pre-edit body text might be intentionally preserved as historical context; a count mismatch might reflect a different counting convention, not a propagation failure.
   - **Present fixes as a categorized list for user review**, not a pre-applied diff. Group by: (1) mechanical fixes the user can approve in bulk (dead links, link-prefix normalizations, obvious count corrections), (2) judgment-required fixes where the agent proposes a change and the user confirms the direction, (3) findings the agent isn't confident enough to propose a fix for.
   - **Purely mechanical, no-judgment patterns** (a site-wide dead-link or link-prefix fix, for instance) are the one safe bulk fix — script them and apply. Everything that touches meaning goes through the review list. Leave possible findings for human review, noted in the PR description.
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

## Agent types

Three sampling strategies, used in different ratios by Gear 2 and Gear 3:

### Random samplers
The original P2 method. Randomly select N cross-domain file pairs and compare for contradictions. Good at surfacing drift between unrelated pages that happen to reference the same fact. Converges fast — after 3-4 waves the same known findings dominate and new discoveries drop to near-zero.

### Spider samplers
Start from a high-connectivity hub page (a section index, the root `CLAUDE.md`, the homepage, a busy project hub) and follow its cross-references outward for 2 hops. At each hop, check: does the linked page agree with the hub on shared facts? Do the linked pages agree with *each other*? This catches drift that hides in reference chains — where A→B is fine and B→C is fine but A contradicts C. Spiders are more expensive per agent (they read more files) but find chain-of-reference drift that random pairs miss because random rarely lands on both ends of a 2-hop chain.

### Domain sweepers (targeted)
Full cross-join within a specific topic cluster (e.g., all pages in one section, all protocol files). Exhaustive within their domain but blind to cross-domain drift. Best in early waves to drain intra-domain rot; diminishing returns after the first pass through each cluster.

## Gear 2: Marathon (Continuous Parallel Loop)

The marathon runs many Gear-1 spot-checks back-to-back in parallel, deduping against a persistent findings register, until the wiki actually stops surfacing new contradictions. Use when you suspect real drift, not when you just want a sanity check.

### Setup

- Keep **8 P2 subagents running in parallel** at all times.
- **Wave 1 default mix:** 4 random samplers + 2 spider samplers + 2 domain sweepers (see "Agent types" above).
- **Adaptive reweighting (wave 2+):** Same yield-tracking rule as Gear 3 — shift slots toward agent types that find things, away from types that return empty. Minimum 1 slot per type. If random samplers dry up, replace them with spiders or targeted sweeps.
- Spider hub selection: pick high-connectivity pages that cross domain boundaries (section indexes, the root `CLAUDE.md`, the homepage, busy project hubs). Rotate through them — don't repeat a hub until all have been spidered. **Re-spider productive hubs** with refreshed skip lists.
- Subagent model: **mid-tier** is the default for marathon work (best findings/cost ratio — on Claude that means sonnet-class). Frontier models (Opus-class) are more conservative on random samples; haiku-class is unfit — it tends to rubber-stamp the register instead of doing the work.

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
- **Practical convergence:** If the yield rate across all types drops below 0.5 findings/agent for 2 consecutive waves, that's convergence even without hitting the streak threshold. The point is draining drift, not padding zeros.

### Main-thread responsibilities

- Maintain a findings register at `.scratch/p2-marathon-findings.md` (gitignored) with: HARD section (numbered F1, F2, …), SOFT section, open questions for the user, and a streak ledger.
- After each subagent completes: read its result, classify findings as new vs already-logged, update the register, log the score and streak, immediately launch a replacement subagent to keep 8 active.
- **Classify each finding A / B / C per Gear-1 step 6.** (A) and (B) → safe to auto-fix in the post-converge batch. (C) → append to the manual-verify scratch file under "Live verification queue" with the verify command. Do not auto-fix (C) items, even if "the right answer looks obvious from another wiki page." Cross-page consistency is not live verification.
- After the marathon converges (or you pause it): apply Gear 1 step 7 (user-reviewed fix list, not mass auto-apply), commit per Protocol 7, and hand the (C) queue back to the user. The user decides whether to live-verify in-session or defer. **The step 7 warning about user review applies here identically** — marathon scale amplifies the false-positive risk, it doesn't reduce it.

### Pattern codification (Protocol 10 integration)

When a drift pattern recurs 2+ times across different agents or waves, it's a candidate for **[Protocol 10 (Codify Drift Check)](10-codify-drift-check.md)** — promotion to a permanent structural check at commit time. The main thread should:

1. Add a skip-category note in the register: *"Pattern identified — Protocol 10 candidate."*
2. Surface to the user: *"[pattern] has recurred [N] times. Recommend Protocol 10 to codify it."*
3. Execute Protocol 10 if the user approves (it's fast — just adding a conditional check).

This is how the marathon pays forward: findings that would otherwise be rediscovered next run become grep-checkable guards that fire at commit time.

### Tips

- Skip-list grows naturally. Every 8-10 runs, refresh the per-subagent prompt's "skip categories" list with the recently-logged finding patterns so subagents don't waste their context re-flagging things you've already captured.
- Historical session logs are not retroactively edited per repo style guide — exclude them from "stale page" findings unless the agent is sure.
- Wiki-wide patterns (e.g. stale "Last Updated" stamps on idea pages, empty `_index.md` stubs in active log dirs) are patterns, not per-page bugs — collect once, don't re-flag each instance.
- The marathon may not converge on a drift-heavy wiki within a single session. That's fine — the register is the artifact. Pause, fix, resume next session.

## Gear 3: Ultramarathon (High-Concurrency Domain-Targeted Loop)

The ultramarathon roughly doubles the marathon's concurrency and adds targeted domain sweeps alongside random sampling. Where Gear 2 relies mostly on random pairs to surface drift, Gear 3 splits the fleet: some agents do random cross-domain sampling, some spider reference chains, and some do full cross-joins within specific topic clusters where contradictions are most likely to hide.

### Setup

- Keep **16 P2 subagents running in parallel** at all times.
- **Wave 1 default mix:** 6 random samplers + 4 spider samplers + 6 domain sweepers.
- **Adaptive reweighting (wave 2+):** After each wave, compute the **yield rate** (findings per agent) for each agent type (random, spider, sweeper). For the next wave, shift slots toward the highest-yield type and away from the lowest-yield type. The principle: **maximize discovery rate, not streak count.** Agents that find things get more slots; agents that return empty get fewer.
  - Minimum floor: 2 slots per type (so no type goes to zero — even a low-yield type occasionally surfaces propagation failures a targeted agent wouldn't hit).
  - If a type's yield drops to zero for 2 consecutive waves, reduce it to the floor (2) and redistribute.
  - If a type's yield is 3×+ another type's, it gets the freed slots.
  - **Targeted grep-based sweeps** (propagation checks, dead-link scans, frontmatter audits) count as sweepers for yield tracking but are especially high-value in mid-to-late waves — prefer them over re-sweeps of already-clean domains.
- Spider hub selection: same as Gear 2 but with more hubs to cover. After exhausting the primary list, use section `_index.md` files, project `CLAUDE.md` files, and other high-fanout pages as hubs. **Re-spider hubs that were productive** — a 2nd or 3rd pass with a refreshed skip list often finds chain drift the first pass missed.
- Subagent model: **mid-tier** (same rationale as Gear 2).
- Convergence threshold: **30 consecutive zero-finding runs** (vs Gear 2's 10). But see the adaptive note — the point is draining drift, not padding zeros. If the yield rate across all types drops below 0.5 findings/agent for 2 consecutive waves, that's practical convergence even if the formal streak hasn't hit 30.

### Topic clusters for targeted agents

Targeted agents rotate through domain clusters, doing full cross-joins (every file against every other) within their assigned cluster. Define clusters that match your wiki's top-level sections — the goal is that each cluster is small enough to cross-join exhaustively but large enough to contain related facts that drift apart.

<!-- Customize: replace the rows below with your wiki's actual sections. The pattern is one row per topic cluster, with the file glob and the kinds of contradiction most likely within it. -->

| Cluster | Scope | What to look for |
|---------|-------|-----------------|
| (section A) | `section-a/**/*.md` + its `_index.md` | identifier/address conflicts, version drift, status mismatches, count tables |
| (section B) | `section-b/**/*.md` cross-referenced against related pages | assignment conflicts, range overlaps, naming drift |
| protocols | `protocols/*.md` + cross-refs to `CLAUDE.md` files | index-vs-file drift, cross-protocol references, trigger collisions, step numbering |
| projects | `projects/**/_index.md` + sub-pages | status conflicts, cross-references, date conflicts |
| cross-domain | two or more sections combined | references in one section that name facts owned by another |

After exhausting all clusters, rotate back through them — drift introduced by fixes in earlier waves can create new findings in domains already swept.

### Scoring + convergence

Same as Gear 2, except:
- **Stop when streak reaches 30** (not 10).

### Main-thread responsibilities

Same as Gear 2, plus:
- Track which topic clusters have been assigned and rotate through them. Don't assign the same cluster to two concurrent targeted agents.
- Track which spider hubs have been used. Don't repeat a hub until all primary hubs have been spidered at least once; then rotate through secondary hubs (section indexes, project `CLAUDE.md` files).
- After every wave completes, refresh the skip-categories list for subsequent agents with recently-logged finding patterns.
- The (A)/(B)/(C) classification and fix rules from Gear 1 step 6 apply identically.
