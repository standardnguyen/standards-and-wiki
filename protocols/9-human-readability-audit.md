# Protocol 9: Human-Readability Audit

Validate that a protocol or reference page can be executed by a human without LLM assistance, against the criteria in [meta/human-readability.md](../meta/human-readability.md). Use deliberately weakened reader agents — frontier LLMs are too good at filling gaps a human couldn't.

## Trigger

"Run Protocol 9" or "Human-readability audit" — optionally scoped:

- "Run Protocol 9 on Protocol 4" — single target.
- "Run Protocol 9 on `projects/<project>/`" — directory scope.
- "Run Protocol 9 full sweep" — every `.md` under `protocols/` and every `_index.md` (or section overview) under the wiki root.

## Pre-reqs

- Read `meta/human-readability.md` for the criteria the validator scores against.
- Confirm an Anthropic API key is available if running validators via direct API call rather than subagent.
- Create a scratch directory for outputs (gitignored). Default suggestion: `.scratch/human-readability-audit/<date>/`.

## Procedure

### 1. Resolve the scope

Build the target list:

```bash
# Single protocol
ls protocols/4-*.md

# All protocols
ls protocols/[0-9]*.md

# All section overviews (adjust to match your overview filename convention)
find . -name "_index.md" -not -path "./protocols/*"
find . -name "overview.md" -not -path "./protocols/*"
```

Filter out files carrying the `audience: agent-only` marker:

```bash
for f in <target list>; do
  grep -l "audience: agent-only" "$f" >/dev/null || echo "$f"
done
```

### 2. Pick a tier

Default Tier 1 unless the file gates critical infrastructure (disaster recovery, credential rotation, vulnerability response — those get Tier 3) or Tier 1 reported clean and the operator suspects gaps remain (escalate to Tier 2).

### 3. Run the validator

One agent per target, batched in parallel — up to 6 at a time to keep output reviewable. Use a small / fast model for cost (e.g. Haiku via subagent). Each agent writes its output to `<scratch-dir>/<target-name>.md`.

Tier prompts are below; substitute `<file_path>` for each target.

#### Tier 1 — Junior reader (default)

```
You are a junior engineer who has just been handed the file at <file_path> and
asked to execute it. You have access to a Linux terminal and to the files
explicitly referenced in the file. You do NOT have web access. You do NOT have
access to other systems unless the file says how to reach them. You do NOT have
prior knowledge of how this organization normally works.

Read the file. Walk through it step by step. At every step, note what you would
actually run, what you would expect to see, and whether the file gives you
enough to proceed. Flag every place you would have to guess.

Output format:
- One section per step or sub-section.
- For each, a `verdict:` line — `clear` / `ambiguous` / `blocked`.
- For ambiguous/blocked, a `gap:` line stating what's missing.
- End with a one-line `overall:` verdict — `executable` / `executable-with-gaps`
  / `not-executable`.

Do not propose fixes. The audit lists gaps; the operator decides what to fix.
```

#### Tier 2 — Strict no-inference reader

Add to the Tier 1 prompt:

```
Do not infer. If the file says "review the changes" without saying what
"review" means in this context, flag it. If it says "run the script" without
giving the path, flag it. Treat any missing detail as a blocker, not as
something to fill in from common sense.
```

#### Tier 3 — Hostile-environment roleplay

```
You are the operator, three years from now. The Anthropic API has been shut
down, Claude Code is gone. You have a terminal and the wiki at <file_path>.
Your job is to execute this protocol right now. Walk through it. At every
step, narrate what you would do. If you would be unable to proceed, stop and
report — do not improvise past the gap.

Output format same as Tier 1.
```

### 4. Synthesize

After all per-target outputs land in the scratch dir, write a summary at `<scratch-dir>/SUMMARY.md`:

- Verdict count (executable / with-gaps / not-executable / agent-only-skipped).
- Cross-cutting patterns — gaps that recur across multiple targets.
- Highest-value fixes — the 5–8 specific edits that resolve the most gaps with the least churn.
- Files where the validator output looks spurious — operator judgment, not a fix.

### 5. Promote findings

For each target with `executable-with-gaps` or `not-executable`:

- Open the source file.
- Apply the fix where it's small and uncontroversial.
- For larger rewrites, file a follow-up task with the validator output attached.
- Targets that the operator judges should be agent-only get the marker added at the top.

### 6. Re-run on fixed targets

Confirm convergence. A target that flips from `executable-with-gaps` to `executable` is done.

## Output

- Per-target validator transcripts in the scratch directory.
- `SUMMARY.md` in the same directory.
- A bullet list, in the calling session, of the protocols/pages with the highest-impact gaps and the proposed fixes.
- A row added to an audit log at `meta/human-readability-audit-log.md` with date, scope, tier, and verdict counts. (Create the file on first run.)

## When to Run

- On any new protocol before its first commit.
- After substantial edits to an existing protocol — added or rewritten steps, not typo fixes.
- Yearly full sweep, optionally as a sub-step of Protocol 1 (harmonize).
- After any incident where a human had to step in without a model and couldn't proceed — re-validate the failing protocol after fixes.

## Notes

- The validator is not authoritative. It is a probe. The operator's judgment overrides any flag the validator raises.
- Per-run decisions to record: which model version was used, whether subagents or direct API calls were used, and any prompt tweaks. These go in the audit log row so future runs are comparable.
- Implementing a standalone Python validator that calls the API directly is a sensible follow-up once the prompts have settled. Until then, run via subagents in-session.
