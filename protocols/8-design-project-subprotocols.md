# Protocol 8: Design Project Sub-Protocols

Survey a project's recurring operations and propose a set of project-scoped sub-protocols that codify them. Run when a project's been alive long enough to have repeated patterns but young enough that those patterns aren't yet documented.

## Trigger

"Run Protocol 8", "Design subprotocols for this project", "What sub-protocols would help here?", "Codify the patterns we keep doing".

## When this is the right protocol

Run P8 when ALL of these are true:

- The project has been worked on across ≥3 sessions
- You can name ≥2 patterns that have repeated (e.g., "the cleanup pass we keep doing", "the file-identification dance")
- Future-Claude would benefit from a concrete procedure rather than re-deriving each time

Don't run P8 when:

- The project is new — patterns haven't emerged yet; just track work in the project's session log
- Only one pattern exists — it's a single sub-protocol, not a system; just write it inline in the project's CLAUDE.md
- The project is wrapping up — codifying patterns for a dying project is wasted effort

## Procedure

### 1. Read the project state

Bring yourself up to speed:

- The project hub (`projects/<project>/_index.md` or equivalent)
- The project's existing CLAUDE.md (if any)
- The project's session log + last 3-5 individual log entries
- Any task tracker, kanban board, or issue list the project uses
- Any reusable scripts the project has accumulated

The patterns you'll codify live in those places. You're looking for: things that keep happening, names that keep appearing, scripts that keep getting written.

### 2. List recurring operations

Enumerate every operation that has happened ≥2 times. For each, name it concretely:

| Pattern shape | Example |
|---|---|
| Cleanup / audit pass | "we keep finding records with missing fields and have to backfill" |
| Identification / disambiguation | "we keep getting downloads with hash filenames and have to figure out what they are" |
| Cross-link maintenance | "we keep finding orphaned pages or unlinked references" |
| External enrichment | "we keep doing API lookups for items where we know one field but not the rest" |
| Bulk ingestion | "we keep dropping batches of N files and needing to generate companion records" |
| Flag handling | "we keep flagging things AMBIGUOUS and never coming back to them" |
| Sprawl consolidation | "we keep finding clusters that should be one umbrella" |
| Disambiguation between layers | "we keep deciding what goes in layer A vs layer B" |
| Periodic review | "we keep wanting to look at items that haven't been touched in N days" |

Don't force categories. If a project has unique patterns, name them.

### 3. Filter to "worth codifying"

A pattern is worth a sub-protocol if:

- It has ≥3 non-obvious procedural steps, OR
- It involves ≥2 layers of state (e.g. database + index + filesystem), OR
- Forgetting one step causes a real problem (data loss, wrong API call, misleading metadata), OR
- It involves API discovery / shape that's expensive to re-derive

A pattern is NOT worth a sub-protocol if:

- It's a one-liner shell command
- It's covered by an existing root protocol
- It's a one-time migration (the migration itself is a session log, not a protocol)

Aim for **4-7 sub-protocols** per project. More is over-engineering; fewer is fine if the project genuinely has fewer patterns.

### 4. Surface the candidate set to the user

Present the list with: name, trigger phrase, brief scope (1-2 sentences), why it matters (1 sentence). Format:

```
SP-N: <Name> — <trigger phrase>
  Scope: <what it does>
  Why: <pain it relieves>
```

Ask the user to approve the set, drop any that feel forced, add any you missed. The user knows the project's pain better than the surface signals show.

### 5. Choose the storage layout

Default: `projects/<project>/subprotocols/<N>-<slug>.md` for each, `projects/<project>/subprotocols/_index.md` as the registry, `projects/<project>/CLAUDE.md` registers them in a top-level Sub-Protocols table.

Numbering starts at 0 within the project namespace (per the sub-protocol numbering convention in the prime CLAUDE.md). Filename matches `N-<slug>.md`.

If the project has only 2-3 sub-protocols, inlining them into `CLAUDE.md` as `## Sub-Protocol N: <Name>` headers is also valid. The dir-with-files pattern is for projects with substantive procedures.

### 6. Write each sub-protocol

Each file follows the root protocol shape:

```markdown
# <Project Code> Sub-Protocol N: <Name>

<One-paragraph description.>

## Trigger

"<Project> Sub-Protocol N", "<casual phrasing 1>", "<casual phrasing 2>". Run when:
- <bullet list of conditions>

## Procedure

### 1. <First step>

<details>

### 2. <Next step>

...

## Notes

- <gotcha>
- <preserve-this>

## Related

- <SP-N> — <when this protocol hands off to another>
- <root protocol> — <for adjacent flows>
- Tooling: <reusable script>
- Reference run: <session log>
```

The "Tooling" and "Reference run" lines matter — they pin the protocol to concrete artifacts that prove it works.

### 7. Write the registry / CLAUDE.md updates

`<project>/subprotocols/_index.md` is the navigation page — table of all sub-protocols with one-line descriptions.

`<project>/CLAUDE.md` gets a `## Sub-Protocols` section that:
- Lists all sub-protocols in a table
- Names the conventions (numbering, naming, where they live)
- Lists the reusable scripts the protocols reference (Tooling table)

### 8. Cross-reference from the project hub

Update `<project>/_index.md` to mention sub-protocols exist + link to the registry. Doesn't need to be prominent — a Related-section link is enough.

### 9. Commit

One commit. The diff is large (one file per sub-protocol + registry + CLAUDE.md + hub edit) but the scope is coherent — "design + register sub-protocols for project X."

Commit message names the count + lists the sub-protocols by name.

## Notes

- **Sub-protocols can chain.** SP-0 (cleanup) often surfaces work that SP-1 / SP-2 / SP-3 handle. Document the hand-offs explicitly in the Related sections.
- **Reference reruns prove the procedure works.** When a sub-protocol describes a pattern that just played out in a session, link the session log + commit hash that exemplifies it. This is the best documentation: "here's the protocol; here's what it looked like when we actually did it."
- **Don't over-spec.** Sub-protocols capture *intent + structure*, not exhaustive command sequences. The right level of detail: "run the audit script (template at <path>); bucket findings; apply per-record patches" — not "here are 47 lines of shell." The script lives in the tooling references; the protocol is the playbook.
- **Watch for protocol bloat.** If a project has 8+ sub-protocols, some probably should be merged or demoted to inline notes in the CLAUDE.md. The number is a signal, not a limit, but it's worth checking when you cross 7.
- **Re-run P8 periodically.** As a project grows, new patterns emerge. Re-running P8 every ~6 months can surface new candidates and retire stale ones. Don't delete retired sub-protocols; mark them deprecated in the registry and link to what replaced them.

## Related

- Prime `CLAUDE.md` → "Protocols" section — sub-protocol numbering convention
