# Protocol 11: Wiki-RAG Maintenance

> **agent-only.** Keeps the synthetic-RAG retrieval hook accurate as the wiki grows.

## What This Maintains

The **wiki-rag hook** (`.claude/hooks/wiki-rag.py`, wired as a Claude Code `UserPromptSubmit` hook — see `.claude/settings.json.example`) is synthetic RAG: on every prompt it greps the wiki for the prompt's proper nouns and injects pointer lines to the top-matching pages, so retrieval is a harness affordance instead of something the model must remember to do (CLAUDE.md "Doing Tasks" §0, "synthetic RAG"). It's the deterministic version of the "grep first, even when you're sure" rule.

**The content side is self-fresh** — grep reads live files, so new pages and edits are searchable the instant they land. No reindex, no embedding store, no staleness.

**Two things DO drift and this protocol tends them:**

1. **`ALIASES`** — entities whose everyday word ≠ their page slug. If a monitoring hub lives at `infrastructure/monitoring/_index.md` but people call it "grafana," grepping the word alone routes to scattered logs, not the hub. The alias map is a tiny hand-curated `word → canonical page` table. New hubs whose name differs from their slug need new aliases or they're invisible to fast routing.
2. **`STOPWORDS`** — common lowercase words that look like entities in prose (`having`, `trouble`, `sweep`) and inject noise. New false-positives surface as the wiki and phrasing evolve.

(Thresholds — `MIN_SCORE`, `TOO_COMMON`, rarity weighting — are tuning knobs, not routine maintenance. Touch them only when an audit shows systematic noise or misses, and re-run the test battery below.)

## Setup (one-time, per adopter)

1. The hook ships disabled — wiring is opt-in. Copy `.claude/settings.json.example` to `.claude/settings.json` (or merge its `hooks` block into your existing settings) to register the `UserPromptSubmit` hook.
2. Ensure the hook is executable: `chmod +x .claude/hooks/wiki-rag.py`.
3. The hook auto-detects the repo root (two levels up from the script). If you run it from elsewhere, set `WIKI_RAG_ROOT`.
4. Verify: `echo '{"prompt":"run protocol 4 to harmonize"}' | python3 .claude/hooks/wiki-rag.py` should surface the relevant protocol pages.

## Mode 1: Per-Ship Alias Registration

Lightweight, runs when a commit **creates a new entity hub** — a page that is the canonical home for a named thing (a project `_index.md`, a service page, a new component) **whose name differs from its slug**.

⚠️ **That trigger alone is too narrow, and the gap is silent.** Firing only on hub *creation* means a hub that has never routed correctly will never be caught: if its slug and its title are both the technical name while everyone types a different everyday word, neither can earn a slug or title boost for the word people actually use, and nothing in the workflow ever prompts the fix. **Also run Mode 1 whenever a probe shows an existing hub failing to surface** — which means *probing*, not assuming. A hub can be months old and have never once been retrieved.

1. Ask: does the new page's everyday name appear in its path/slug or frontmatter title? If yes → grep *usually* already routes to it, **no alias needed**, done.

   > **Caveat — the name-in-slug test is not sufficient for capitalized names.** `grep_files()` shells out to `grep -rcF` — **case-sensitive** — on the *lowercased* prompt token. A page whose everyday name is normally written capitalized therefore scores only its incidental *lowercase* hits (URLs, code spans), not its real ones; the low count sorts it down, and the per-term result cap cuts it off before scoring ever sees it. A page can have a double-digit case-insensitive match count but a single-digit case-sensitive one, ranking it near the bottom and dropping it from results entirely — despite the name being both its slug *and* its title, exactly the case this step says needs no alias. **Don't reason from the rule — run step 3's check first, and alias whenever the hub doesn't actually surface**, name-in-slug notwithstanding. (The real fix is `-i` in `grep_files`, but that reshuffles ranking wiki-wide and deserves its own tested change; aliasing is the local remedy.)
   >
   > **Testing note:** `retrieve()` early-returns on very short prompts (under ~6 characters), so a bare one-word probe shorter than that returns nothing *by design* and is not evidence of a routing failure. Probe with a realistic sentence, not the bare term.
2. If the name ≠ slug/title (the grafana/monitoring case), add an entry to `ALIASES` in `.claude/hooks/wiki-rag.py`:
   ```python
   "newword": "path/to/hub/_index.md",
   ```
   Add synonyms too (point every word people use for the thing at the same hub). Keep the target the **hub**, not a log.
   ⚠️ **Do not hijack a word another section legitimately owns.** If a candidate alias is a load-bearing term elsewhere in the wiki (a topic directory, a book, a whole content type), pointing it at one entity page is a *worse* misroute than the one you are fixing — you trade a narrow miss for a broad one. Alias only unambiguous entity names, plus unambiguous multi-word phrases. When you add a phrase, check its out-of-domain hits actually share the sense you mean, and record that you checked.

   **Split an ambiguous name by what each spelling means** rather than sending every variant to the same hub. Where two related things share a base name, route each specific spelling to the page holding *its* answer, and let the bare, ambiguous form go to the hub that distinguishes them.

3. Verify: `echo '{"prompt":"... newword ..."}' | python3 .claude/hooks/wiki-rag.py` surfaces the hub.
4. Stage the hook change in the **same commit** as the new page — the page and its routing ship together (the propagation rule, CLAUDE.md "Doing Tasks" §3).

Skip entirely for leaf pages (logs, notes, recipes) — they're grep-reachable and don't need routing.

## Mode 2: Periodic Audit

A targeted health check, not a full rebuild. Run it occasionally, or when you notice the hook routing badly.

1. **Sample real prompts.** Pull ~15-20 recent prompts you've actually typed (from your shell history, recent session-log entries, or memory). Real phrasing beats synthetic.
2. **Run them through the hook** and eyeball the output:
   ```bash
   while IFS= read -r p; do
     echo "=== $p ==="
     echo "{\"prompt\":$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$p")}" \
       | python3 .claude/hooks/wiki-rag.py
   done < /tmp/sample-prompts.txt
   ```
3. **Classify each result:**
   - **Miss** (a named entity routed nowhere or to the wrong page) → usually a name≠slug entity missing from `ALIASES`. Add it.
   - **Noise** (a common word surfaced an irrelevant page as a top hit) → add the word to `STOPWORDS`.
   - **Clean** (real entities routed to hubs, generic prompts silent) → no action.
4. **Re-run a standing test battery** after any edit to confirm no regression — a handful of prompts naming real hubs (each should route to its hub) plus one bare chat line like "yeah can you do that please" (should be **silent**).
5. **Cross-check `ALIASES` against reality** — does each target page still exist at that path? Fix renamed/moved targets.
6. Ship edits per Protocol 7.

## One script, every harness

The engine is **not** reimplemented per harness — every caller shells out to the same `wiki-rag.py`. This is the whole point: one place to maintain `ALIASES`/`STOPWORDS`/scoring, zero divergence. The `retrieve(prompt)` function is shared verbatim; only invocation + output rendering differ:

| Mode | Invocation | Output |
|------|-----------|--------|
| **text** (default) | Claude Code `UserPromptSubmit` command hook | pointer block to stdout, injected as context |
| **`--json`** | any other harness pipes the prompt to `wiki-rag.py --json` | `[{path, terms, title}]` — the caller renders + injects |

The script accepts either Claude Code hook JSON (`{"prompt": …}`) or raw text on stdin, so any harness can feed it the same way. `--json` returns `[]` on no match.

**Rule: never reimplement the engine in another language.** A second copy of `ALIASES`/`STOPWORDS`/scoring is exactly the drift this protocol exists to prevent. Shell out — the non-default-harness side is just glue (pipe prompt in, parse `--json`, inject).

## Related

- `.claude/hooks/wiki-rag.py` — the hook itself
- `.claude/settings.json.example` — how to wire it as a `UserPromptSubmit` hook
- Protocol 10 (Codify Drift Check) — the broader "turn a recurring miss into a structural guardrail" discipline; an alias that keeps going stale is a candidate to codify
