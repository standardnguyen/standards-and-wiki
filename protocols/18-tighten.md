# Protocol 18: Tighten

Close the retrieval loop. When a session had to *work* to find or recall a piece of information — five greps to locate a fact, a question asked whose answer was already documented, a procedure re-derived from scratch — fold it back into the wiki so the next session retrieves it automatically.

The wiki is the long-term memory, and every retrieval that cost more than it should is evidence the graph is under-tightened at that spot. The other protocols audit and repair pages that already exist; this one runs on the *finding* being expensive.

## Trigger

"Run Protocol 18", "Tighten that", "Integrate that", "Make sure future you knows this", "Write that down somewhere a future session will find it". Also invoke it proactively when you notice any of:

- You spent three or more greps or file reads locating a fact that has an obvious home.
- The user re-explained something already documented in the wiki, a `CLAUDE.md`, or a protocol.
- You asked a question whose answer was written down, but unreachable from where you were looking.
- You derived a procedure or command that worked and will recur, or a shell/API call surfaced a non-obvious gotcha — a quoting trap, a required flag, the actual cause of a 401.
- You caught yourself thinking "I'll just remember this for the rest of the session." That *is* the trigger. You won't, and the next session certainly won't.

## Procedure

### 1. Name the unit

State the information in one sentence — a fact, a procedure, a gotcha, a pointer. If it will not compress to one sentence, you have several units; handle them one at a time.

### 2. Decide the destination by kind

| Kind of unit | Destination |
|---|---|
| A rule that binds behaviour every session | root `CLAUDE.md` |
| A rule that applies only inside one project subtree | that project's `CLAUDE.md`, or its `_index.md` |
| A reference fact — an endpoint, a schema, a command, a number | the wiki page that owns that subject |
| A procedure that recurs across sessions | a protocol file under `protocols/` |
| A recurring failure mechanism, generalizable past the case that surfaced it | a casebook entry |
| A soft or situational observation, today-specific state | the nearest session log |
| A pointer to an external system | the page that already covers that system; add a one-line note if there is none |

If no row fits, ask where it belongs rather than guessing.

### 3. Check for existing coverage

Search before writing:

```bash
grep -ri "<phrase>" . --include='*.md'     # keyword search across the wiki
find . -name "_index.md"                    # section overviews: the cheapest index of where a topic lives
```

Three outcomes:

1. **Already covered, easy to find.** No write needed — the lookup pain was a one-off. Log nothing.
2. **Already covered, but you didn't find it the natural way.** The content exists; the *path* to it is weak. Don't duplicate — add a cross-link, a sentence on a more discoverable page, or a retrieval-hook alias (Protocol 11) so the next lookup lands there. **This is usually the highest-leverage fix.**
3. **Not covered.** Write the unit into the destination step 2 named.

As you write it, keep three surfaces apart, because collapsing them onto one page either dries a rich source into a flat reference or buries durable facts in a log nobody queries: the **raw record** (the command, the measured number, the quote) stays with the source, the **change record** goes in the nearest `logs/` dir, and the **durable reference** lands where a future session will load it, seeded from the source and never invented. Cross-link them both ways.

### 4. Write the minimum

- Match the voice of the file you are editing, and resist improving adjacent content — surgical changes only (root `CLAUDE.md` → "Doing Tasks" §3). A rule plus a one-line **why** is usually enough.
- Edit the existing page rather than spinning up a new file for a single fact, unless the topic genuinely lacks a home. Promote to a new protocol only if the procedure has recurred or clearly will; one-off procedures live on the relevant page.

### 5. Walk the retrieval chain

Routing by kind (§2) is necessary but not sufficient. **A unit that lands in the "right" file but on a surface that isn't loaded when the retrieval need fires is functionally invisible.** Walk the chain before committing.

| Surface | In context when | Best for |
|---|---|---|
| Root `CLAUDE.md` | Every session | Rules the agent must self-recognize |
| Retrieval-hook aliases (Protocol 11) | Every session, when the hook is wired | Routing an everyday word to its page |
| A project's `CLAUDE.md` | Only when the working directory is inside that project | In-project rules |
| Protocol files | Only when the protocol is invoked | Numbered workflows |
| Wiki pages | Only when a search finds them, or a loaded surface links to them | Reference facts, deep context |
| Session logs | Only when explicitly read, usually the newest at session start | Today-specific state, hand-off notes |
| Harness hooks and settings | The harness fires them; the agent never sees them | Mechanical enforcement, not retrieval |

**Chain check.** Name the trigger that creates the retrieval need — "when the user says X" / "when the agent is about to do Y" / "when working in subtree Z". Which surfaces above are loaded at that moment? If your destination is one of them, you are done. If not, add a one-line breadcrumb from a loaded surface to the destination. **Self-recognition is the strict case:** if the trigger is the *agent* noticing a situation on its own rather than a user-typed invocation, the rule must sit on an always-loaded surface — root `CLAUDE.md`, or a hook alias reachable by breadcrumb from one — because wiki pages and session logs are not self-discoverable.

**Common patterns:**

- *Fact belongs on a page, but the need fires at session start, before any search* → register an alias so the retrieval hook routes the term to the page, and check the page is linked from its section's `_index.md`.
- *A procedure the agent should run automatically on a recognized trigger* → root `CLAUDE.md`; one that only recurs on explicit invocation can live in a protocol file.
- *A rule that must fire even if the agent forgets* → not retrieval but enforcement: wire it into a hook, and keep the procedure itself in the wiki rather than in harness config (root `CLAUDE.md` → "Subagent Workflow").
- *Buried in a session log's hand-off note* → fine as supporting evidence, but the load-bearing rule belongs on an always-loaded surface; logs decay in attention as they age.

If the answer is "only if the next session greps for the exact phrase I just used", the chain is broken. One extra cross-link is cheap; re-discovering the fact next session is what triggered this protocol.

### 6. If you cut text, run the balance check

A trim that deletes the *opening* half of a parenthetical leaves a rule grammatical enough to read past and no longer saying what it meant. One line finds them:

```bash
awk 'NR>1{o=gsub(/\(/,"(");c=gsub(/\)/,")"); if(o!=c) print NR": open="o" close="c}' <file>
```

Blank output means balanced. Run it after any cutting pass, and check the same way for orphaned backticks and half-deleted markdown links. ⚠️ It cannot tell a *quoted* paren from an unbalanced one, so a file that itself quotes a literal close-paren inside a code span always reports that line — **diff against `HEAD` before chasing a hit**, since a line flagged in both is pre-existing, not yours. Backtick parity works the same way: only the *delta* proves anything. And **diff the rendered sentence, not just the byte count**.

### 7. Does the page still read?

Every check above is about correctness; this one asks whether the result is usable, because a page can be entirely true and still fail as substrate. Run it on any page an editing pass touched more than about three times. Three questions, cheapest first:

1. **Where does the point arrive?** If it arrives 80% of the way down, behind preamble and caveats, move it up — a buried point has failed regardless of accuracy.
2. **What share is apparatus?** The correction notes, the "an earlier version said…" lines, the provenance hedging, the narration of the session's own process. Past about a third, move the archaeology to the session log and keep the rules on the page — a log is exempt, since a log is *supposed* to be archaeology.
3. **Does it argue with itself?** Resolve two callouts giving opposite instructions, a struck item whose replacement contradicts the strike, a header promising two things that introduces three. Surgical edits produce these constantly and no correctness check sees them.

Don't defer this as editorial polish — bad organisation manufactures defects, and a judgement left unresolved on a page becomes a false statement someone acts on.

### 8. Ship it

Tightenings are commits worth shipping immediately; don't leave them unstaged where the next session loses them. Ship per [Protocol 7](7-commit-and-ship.md) — stage exactly the paths you touched, never `git add .`, verify the staged list, then commit with a short subject: `tighten: <one-line description of what was integrated>`.

## Notes

- **The unit of tightening is small.** One fact, one rule, one cross-link. Don't refactor a whole section; if you want to, that is a separate task — surface it.
- **Watch for the duplicate-fact smell.** If what you are about to write *feels* like it already exists, it probably does — find the existing entry and strengthen it, or its discoverability, rather than creating a parallel one.
- **Don't over-tighten.** Not every retrieval needs encoding — only the ones that cost more than they should have, or that the user has now answered more than once. Over-tightening adds noise to the files read every session.

## Related

- [Protocol 1: Harmonize](1-harmonize.md) — the broad editorial pass; this is its narrow, in-the-moment counterpart
- [Protocol 6: Homepage Coverage](6-homepage-coverage.md) — when the weak path is reachability rather than phrasing
- [Protocol 7: Commit, Ship & Prepare for Continuation](7-commit-and-ship.md) — staging and shipping the tightening
- [Protocol 10: Codify Drift Check](10-codify-drift-check.md) — when a retrieval miss keeps recurring, promote it to a structural check
- [Protocol 11: Wiki-RAG Maintenance](11-wiki-rag-maintenance.md) — registering an alias so an everyday word routes to its page

