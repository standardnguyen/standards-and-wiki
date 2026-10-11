# Personal Wiki Template

A reference implementation of an agent-maintained wiki — a Git repository of markdown files, kept coherent by Claude Code and a set of structured protocols.

Based on a production wiki that manages 100+ interconnected pages across infrastructure documentation, project tracking, and personal knowledge management.

Two things live here, and they answer different questions. The **protocols** are the skeleton: procedures you run. The **[casebook](casebook/_index.md)** is the material: the specific ways careful work fails while looking correct — each entry a mechanism rather than an anecdote, stripped of the setting it was found in. The skeleton tells you what to do; the casebook is why the steps are shaped the way they are, and what happens when a step gets dropped because nobody remembered why it existed.

## What You Get

- **`CLAUDE.md`** — Project instructions that Claude Code loads automatically. Defines conventions, Git workflow, domain context, and protocol index.
- **Casebook** — Failure mechanisms from a wiki that's been running for hundreds of sessions, each written as a transferable shape with a recognizable trigger. This is the part that doesn't survive a rules-only sync: it's where the *why* lives.
- **Style guide** — Adapted from Wikipedia's Manual of Style for a personal technical wiki. Covers voice, tense, page types, words to avoid.
- **24 protocols** — Structured maintenance workflows invoked by saying "run Protocol N":
  0. **Setup** — Guided first-run onboarding: your agent interviews you and customizes the template (start here)
  1. **Harmonize** — Full editorial pass to fix contradictions, anachronisms, tone
  2. **Spot-Check** — Random-sample contradiction detection across page pairs
  3. **Verify** — Generate commands to check wiki claims against live systems
  4. **Recursive Harmonize** — Iterative harmonization until convergence
  5. **Session Log Setup** — Create logging infrastructure for a new project
  6. **Homepage Coverage** — Ensure every wiki page is reachable from the homepage
  7. **Commit, Ship & Prepare for Continuation** — Stage, commit, push, create PR, update session logs, and hand the work forward
  8. **Design Project Sub-Protocols** — Codify recurring patterns inside a project as sub-protocols
  9. **Human-Readability Audit** — Validate that protocols and reference pages are executable without an LLM in the loop
  10. **Codify Drift Check** — Promote a recurring drift pattern into a permanent structural check at commit time
  11. **Wiki-RAG Maintenance** — Keep the synthetic-RAG retrieval hook's alias/stopword tables accurate as the wiki grows
  12. **Park** — Stash a self-contained continuation so a cold future session can resume the work
  13. **Pick Up** — Resume a parked continuation, re-grounding against live state before acting
  14. **UI Convergence** — Recursive fresh-QA-agent loop over a user-facing surface until a round comes back clean
  15. **LLM Injection Scan** — Sweep the wiki and its rules files for prompt-injection patterns; audit only
  16. **Fact-Check** — Verify a page's claims against external sources, classify, fix with permission
  17. **Conversation Forensics** — Find the turn where a session went wrong and name the root cause
  18. **Tighten** — Place a unit of knowledge where the retrieval need will actually load it
  19. **Cold Read** — Put an unprimed fresh process in front of the wiki and fix what trips it
  20. **Ship Retrospective** — After the session log in a full Protocol 7, ask what the run itself taught and make at most three proposals
  21. **Shared-Checkout Commit** — Commit safely when other sessions edit the same checkout
  22. **Session-Limit Baton** — At a usage or context limit, write a self-contained handoff and fix the project setup
  23. **Propagation Sweep** — When a commit changes a fact, find and fix every other page still carrying the old value
- **Synthetic-RAG hook** — Optional `UserPromptSubmit` hook that greps the wiki on every prompt and injects pointers to the relevant pages (the deterministic version of "grep first"). Off by default; wire via `.claude/settings.json.example`.
- **Homepage crawl script** — Python BFS crawler that finds orphaned pages and broken links
- **Session logging pattern** — Append-only decision logs that prevent wiki drift across sessions
- **Session-log mining guide** — Your agent's session history is a queryable memory (decision archaeology, performance self-reviews, incident lookups); `meta/mining-session-logs.md` covers the grep-first capture stack and when RAG earns its keep
- **Example pages** — Starter homepage, infrastructure overview, and style guide

## Two Ways To Use This

**Adopt it.** Fork or clone, run Protocol 0, let your agent interview you and set it up. This is the intended path, and the Quick Start below walks it.

**Read it.** If you already maintain a wiki with an agent — or you're deciding whether to — the casebook is the part worth an hour on its own. It's the accumulated record of how agent-maintained knowledge stores go wrong: checks that can't fail, probes that report the answer you hoped for, claims that get stronger by being written down. None of it depends on adopting the protocol set.

## Quick Start

**The short version:** fork or clone this repo, start your agent in the repo directory, and say **"run protocol 0"** — it interviews you and does all of the setup below itself. The numbered steps are the manual path if you'd rather drive.

btw if you ever get confused just say "can you hold my hand through this bb" and i'll say yes.

1. **Fork or clone this repo.** Rename it to whatever you want.

2. **Edit `CLAUDE.md`.** This is the most important file. Customize:
   - The "What This Is" section to describe your wiki's purpose
   - The "Repository Structure" section to match your directory layout
   - The "Workflow" section for your Git hosting (GitHub, Gitea, Forgejo, etc.)
   - The "Key Domain Context" section with facts Claude Code needs to know
   - Add session logging sections as you create new projects

3. **Edit `home.md`.** Replace the example sections with your own. This is your wiki's front door.

4. **Start Claude Code** in the repo directory:
   ```bash
   cd ~/your-wiki
   claude
   ```
   Claude Code auto-loads `CLAUDE.md` and knows the project context. Just describe what you want.

5. **Add content.** Tell Claude Code what to document:
   ```
   "document my home network setup"
   "add a page about the NAS"
   "I moved the database to a new server. Update the wiki."
   ```

6. **Run protocols** to maintain quality:
   ```
   "protocol 4"   — recursive harmonize after changes
   "protocol 2"   — spot-check for contradictions
   "protocol 6"   — check that all pages are reachable from the homepage
   ```

## Keeping the Wiki Consistent (Protocol 7)

When you change one fact, the pages that still carry the old value are now wrong, and nothing tells you which ones. Protocol 7 is the pass that finds them. Run it at the end of a work session, once the change is done.

**How to trigger it.** Start your agent in the repo and say any of:

```
"run protocol 7"
"commit and ship"
"prepare for continuation"
"P7"
```

All four mean the same thing. The agent reads `protocols/7-commit-and-ship.md` and works through it.

**What it does.**
1. Reviews what changed in the working tree.
2. Updates the wiki pages and project `CLAUDE.md` files that describe the change.
3. Harmonizes related pages (Protocol 4), so a sibling page doesn't contradict the one you edited.
4. Commits the change. When it corrects a fact (a count, an address, a name, a date, a status) or changes how a mechanism works, it then runs the propagation sweep (Protocol 23) on that commit: check scripts first, then up to three waves of read-only finder agents that extract the changed facts from the diff and grep for each old value, with fixes landing as their own commits.
5. Pushes `dev`, and creates or updates the pull request.
6. Files the session log, runs a short retrospective on the run (Protocol 20), and leaves a continuation prompt so a cold future session can pick up where this one stopped.

If a step doesn't apply, the agent says which step it's skipping and why, and offers a lighter version. It doesn't skip silently.

**If you only want the consistency work without the full close-out** (no session log or continuation prompt), run the pieces on their own: `"protocol 4"` harmonizes recent changes, `"protocol 2"` spot-checks random page pairs for contradictions, and `"protocol 23"` sweeps named commits. Each of these still commits its own fixes, so ask for a report only if you want no commit.

## Why Don't We Have Skills?

Because we needed a name that didn't collide with what existing harnesses already mean by "skill", and because we wanted control over invocation that a skill doesn't give.

In Claude Code and on claude.ai, a skill's name and description are loaded into context by design, so the model can decide when to use it; only the body waits for a trigger. That has two costs. The always-loaded part grows with every skill you add, and when a skill fires depends on the model matching a description, which you can't fully control.

A protocol is a plain markdown file that nothing loads until you name it ("run Protocol 7") or a step points at it. So:

- **Invocation is exactly when you say.** No description match decides it.
- **The count doesn't matter.** You can write as many as you like without watching your context. A protocol that falls out of use costs nothing and doesn't need maintaining; it just sits there. (`CLAUDE.md` tells the agent to read a protocol's file before running it, so what runs is the current text, not a remembered copy.)
- **It works in any harness.** There is no skills directory to port.

What you give up: nothing volunteers a protocol you didn't think to ask for. The protocol table in `CLAUDE.md` is the mitigation. A one-line row each is the only always-loaded cost, and a protocol you rarely run doesn't need a row. If you like skills anyway, nothing stops you from adding one whose body says "run Protocol N"; keep the procedure in the protocol so the skill can't go stale.

# Why Pay Tokens Up Front: The Propagation Problem

A fact in a wiki, or in an agent's memory, is rarely written once. A count sits in a summary table, an index row, a hub description and a status line. When the fact changes and one copy is fixed, every other copy is now a contradiction, and nothing tells the next session which pages they are. That is the propagation problem, and it is one of the ways an agent-maintained knowledge store goes quietly wrong.

**What the other systems document.** This is a description of what each system says it does, not a benchmark. For Hermes it comes from the source and bundled docs of a `main` checkout at commit 175054c (its `pyproject.toml` says 0.20.5; 2026-08-23), read in October 2026; for Claude it comes from Anthropic's own docs read the same month. These products move quickly, so check the current versions before relying on any line.

- **Hermes Agent** keeps two small capped memory files. Replacing or removing an entry edits one entry found by a substring, and a substring that matches several different entries is an error, not a set to update. At the size cap it tells the model to consolidate or remove stale entries itself. The whole built-in store is injected into the system prompt each session (about 1,300 tokens), so the model sees every copy without searching, which only works because the store is tiny. Its background review prompt prefers patching skills loaded in the session. Its curator archives skills by time since last use, and its merge-by-topic pass is off by default. In the built-in memory and skill stores, nothing searches for other copies of a changed fact. Its optional external memory providers advertise related features (Holographic has an on-demand `contradict` action that returns conflicting pairs, Mem0 advertises deduplication, Honcho has a query-time pass that reconciles its own earlier reasoning); we did not test what any of those do to a stale copy.
- **Claude's memory** saves topics as you chat, and you correct them by hand or by asking. The docs do not describe how a contradiction between two saved topics is resolved. Claude Code's auto memory tells the model to "merge or drop stale entries" when the index nears its size cap (and returns an error asking it to rewrite the index when it is over), and its prompt audit reports contradictions between instruction files with proposed edits that you apply on request. The closest thing to a store-wide fix is Anthropic's Dreams for Managed Agents: an asynchronous research-preview job that reads a memory store and up to 100 session transcripts and, by default, writes a separate output store, never modifying the input, in which duplicates are merged and stale or contradicted entries are replaced with the latest value, for you to review.

**What this template does.** It treats propagation as a procedure with a bounded cost. [Protocol 7](protocols/7-commit-and-ship.md) ships a change. When the change corrects a fact, [Protocol 23](protocols/23-propagation-sweep.md) runs on the commit: your check scripts first, then at most three waves of read-only finder agents handed the commit SHAs (so they extract the changed facts themselves and grep for the old values), then two judging lenses that must both agree a line is stale before it is edited. Disagreements are logged, not edited. Where a fact has many carriers, the fix is to pick one canonical home and make the rest pointers, and to delete counts of mutable sets instead of updating them. [Protocol 20](protocols/20-ship-retrospective.md) then asks what the run itself taught, so the procedure improves.

**The cost, stated plainly.** This spends tokens, every time a ship changes a fact, before anything has gone wrong. The finders and judges are real agent calls, and the maintenance pass is a real share of a session's cost. The sweep is capped at three waves because, in the one cycle the maintainer audited, the few later-wave findings audited (six) were not real (n = 1 and confounded with how those waves were scoped; most later-wave findings in that cycle were errors the sweep's own fixes had introduced, so treat it as a reason to measure your own, not a law). It runs on commit SHAs because a sweep that depends on the shipping session listing the changed facts from memory fails silently when that list is incomplete.

**Why it is worth paying.** The alternative is to pay later and invisibly, as a store that looks complete and contradicts itself. The bet behind this template is that paying the maintenance cost up front, in a bounded sweep, keeps the store closer to true than paying it later and invisibly. The [casebook](casebook/_index.md) records the ways this kind of maintenance fails.

## Design Principles

- **If it's not documented here, it doesn't exist.** The wiki is the source of truth.
- **Git provides the safety net.** Every change is a commit. Every change goes through a PR. Humans review diffs before merging.
- **Protocols formalize what's normally ad-hoc.** "Check if the wiki is consistent" becomes a repeatable, invocable workflow.
- **Verification closes the loop.** Protocol 3 generates commands to prove the wiki matches reality.
- **Session logs prevent drift.** Append-only decision records ensure continuity across Claude Code sessions.
- **`CLAUDE.md` prevents cold starts.** Conventions survive across sessions because they're codified, not remembered.

## Adapting for Your Use Case

### Infrastructure / Homelab Wiki
The template was originally built for this. Document servers, containers, network topology, services, and operational procedures. Protocol 3 (Verify) is especially valuable here — it generates commands to check that your documentation matches what's actually deployed.

### Project Knowledge Base
Track projects with overview pages, session logs, and decision records. The session logging pattern (Protocol 5) is the key differentiator — it prevents the gap between what was decided in conversation and what the wiki reflects.

### Personal Knowledge Management
Organize notes, research, reading lists, and ideas. The homepage coverage check (Protocol 6) ensures nothing gets orphaned as the wiki grows.

### Team Documentation
The protocol system works for teams too. Protocol 1 (Harmonize) catches contradictions that creep in when multiple people update docs. Protocol 2 (Spot-Check) scales to large wikis where reading every page isn't practical.

## File Layout

```
your-wiki/
├── CLAUDE.md                  <- Project instructions (edit this first)
├── README.md                  <- You are here
├── home.md                    <- Wiki homepage (edit this second)
├── casebook/                  <- Failure mechanisms — why the protocols are shaped this way
│   ├── _index.md              <- Six chapters + the entry format (start here)
│   └── *.md                   <- One entry per mechanism, grouped by chapter in the index
├── .claude/
│   ├── hooks/
│   │   └── wiki-rag.py        <- Optional synthetic-RAG retrieval hook (Protocol 11)
│   └── settings.json.example  <- How to wire the hook (copy to settings.json)
├── meta/
│   ├── style-guide.md         <- Writing conventions
│   ├── mining-session-logs.md <- Using agent session history as queryable memory
│   ├── ai-managed-wiki.md     <- How this wiki works
│   └── human-readability.md   <- Criteria for human-executable docs (Protocol 9)
├── protocols/
│   ├── 0-setup.md             <- Guided first-run onboarding (start here)
│   ├── 1-harmonize.md
│   ├── 2-spot-check.md
│   ├── 3-verify.md
│   ├── 4-recursive-harmonize.md
│   ├── 5-session-log-setup.md
│   ├── 6-homepage-coverage.md
│   ├── 7-commit-and-ship.md
│   ├── 8-design-project-subprotocols.md
│   ├── 9-human-readability-audit.md
│   ├── 10-codify-drift-check.md
│   ├── 11-wiki-rag-maintenance.md
│   ├── 12-park.md
│   ├── 13-pickup.md
│   ├── 14-ui-convergence.md
│   ├── 15-llm-injection-scan.md
│   ├── 16-fact-check.md
│   ├── 17-conversation-forensics.md
│   ├── 18-tighten.md
│   ├── 19-cold-read.md
│   ├── 20-ship-retrospective.md
│   ├── 21-shared-checkout-commit.md
│   ├── 22-session-limit-baton.md
│   ├── 23-propagation-sweep.md
│   └── scripts/
│       └── homepage-crawl.py
├── continuations/             <- Parked task briefings (Protocols 12/13)
│   └── _index.md
├── infrastructure/            <- Example section (rename/replace)
│   └── overview.md
├── projects/                  <- Project tracking (add as needed)
└── ideas/                     <- Half-baked ideas (add as needed)
```

## Prerequisites

- [Claude Code](https://claude.ai/code) CLI installed
- A Git repository (any hosting: GitHub, Gitea, Forgejo, GitLab, etc.)
- Optional: a wiki renderer like Wiki.js, Gollum, or MkDocs that syncs from Git
