# Personal Wiki

This wiki is a source of truth for many things in my life — infrastructure, projects, knowledge, procedures, and decisions. If it's not documented here, it doesn't exist.

---

## Sections

### Infrastructure
Everything about the homelab, network, and self-hosted services.

- [Infrastructure Overview](/en/infrastructure/overview) — Hardware, architecture, and design decisions

### Projects

Active projects and ongoing work.

<!-- Add project links here as you create pages. Example:
- [Project Name](/en/projects/project-name/overview) — Short description
-->

### Ideas

Half-baked projects that might become real, or might just live here forever.

<!-- Add idea links here. Example:
- [Idea Name](/en/ideas/idea-name) — What it is and why it's interesting
-->

### Meta

How this wiki is managed and maintained.

- [Style Guide](/en/meta/style-guide) — Voice, tense, tone, and formatting conventions
- [AI-Managed Wiki](/en/meta/ai-managed-wiki) — How Claude Code maintains this wiki
- [Human Readability](/en/meta/human-readability) — Criteria for docs that stay executable without an LLM
- [Mining Session Logs](/en/meta/mining-session-logs) — Using agent session history as queryable memory
- [Parked Continuations](/en/continuations) — Resumable task briefings (park with Protocol 12, pick up with Protocol 13)

### The Casebook

What goes wrong — and the reasons the protocols are shaped the way they are. One entry per failure mechanism, each stripped of the setting it was found in.

- [The Casebook](/en/casebook) — Index: six chapters, the entry format, and why a casebook rather than more rules
- [Laundered confidence](/en/casebook/laundered-confidence) — Writing a claim down strengthens it without adding evidence
- [The check that cannot stop the action](/en/casebook/the-check-that-cannot-stop-the-action) — A guard folded into the same call it guards
- [The probe that reads the same in both branches](/en/casebook/the-probe-that-reads-the-same-in-both-branches) — A constant with a plausible shape
- [A test that has never failed is a hypothesis](/en/casebook/a-test-that-has-never-failed-is-a-hypothesis) — A green test that has never been red proves nothing
- [The relief valve wired to the kill switch](/en/casebook/the-relief-valve-wired-to-the-kill-switch) — Two limits on one axis, so the softer one can never fire
- [A pointer you don't open is not context](/en/casebook/a-pointer-you-dont-open-is-not-context) — Retrieval that returns a path has returned nothing yet
- [N agreeing sources are not N sources](/en/casebook/n-agreeing-sources-are-not-n-sources) — Agreement among copies measures propagation, not truth
- [A rule with no recorded why](/en/casebook/a-rule-with-no-recorded-why) — The reason is the part that keeps a rule from being re-derived wrongly
- [Verifying your own write is a disclosure vector](/en/casebook/verifying-your-own-write-is-a-disclosure-vector) — Reading back your line prints its neighbours

<!-- Customize: the full set lives in the casebook index — link a few here, or swap these for the ones that hit you hardest; the situation should do the reminding. -->

### Protocols

Structured workflows for wiki maintenance, invoked via Claude Code.

<!-- Customize: keep this list complete, or replace it with a link to the protocols index. A hand-maintained partial list on the homepage reads as a roster and silently becomes a stale one — nothing fires when a protocol is added. If you would rather not maintain it, say so explicitly here and point at the index instead. -->

- [Protocol 0: Setup](/en/protocols/0-setup) — Guided first-run onboarding; your agent interviews you and sets everything up
- [Protocol 1: Harmonize](/en/protocols/1-harmonize) — Full pass to fix contradictions, anachronisms, and tone
- [Protocol 2: Spot-Check](/en/protocols/2-spot-check) — Random-sample cross-domain contradiction detection
- [Protocol 3: Verify](/en/protocols/3-verify) — Generate commands to check ground truth on live systems
- [Protocol 4: Recursive Harmonize](/en/protocols/4-recursive-harmonize) — Iterative harmonization until convergence
- [Protocol 5: Session Log Setup](/en/protocols/5-session-log-setup) — Create session logging for a new project
- [Protocol 6: Homepage Coverage](/en/protocols/6-homepage-coverage) — Check that every page is reachable from the homepage
- [Protocol 7: Commit, Ship & Prepare for Continuation](/en/protocols/7-commit-and-ship) — Commit, push, create PR, update session logs, hand the work forward
- [Protocol 8: Design Project Sub-Protocols](/en/protocols/8-design-project-subprotocols) — Codify recurring project patterns
- [Protocol 9: Human-Readability Audit](/en/protocols/9-human-readability-audit) — Validate docs are executable without an LLM
- [Protocol 10: Codify Drift Check](/en/protocols/10-codify-drift-check) — Promote recurring drift into a commit-time check
- [Protocol 11: Wiki-RAG Maintenance](/en/protocols/11-wiki-rag-maintenance) — Tend the retrieval hook's alias/stopword tables
- [Protocol 12: Park](/en/protocols/12-park) — Stash a continuation a cold future session can resume
- [Protocol 13: Pick Up](/en/protocols/13-pickup) — Resume a parked continuation, re-grounding first
- [Protocol 14: UI Convergence](/en/protocols/14-ui-convergence) — Recursive fresh-QA-agent loop until a round comes back clean
- [Protocol 15: LLM Injection Scan](/en/protocols/15-llm-injection-scan) — Sweep the wiki and its own rules for injected instructions
- [Protocol 16: Fact-Check](/en/protocols/16-fact-check) — Verify a page's claims against external sources, classify, fix with permission
- [Protocol 17: Conversation Forensics](/en/protocols/17-conversation-forensics) — Find the turn where a session went wrong, and name why
- [Protocol 18: Tighten](/en/protocols/18-tighten) — Place a unit of knowledge where the retrieval need will actually load it
- [Protocol 19: Cold Read](/en/protocols/19-cold-read) — Put an unprimed reader in front of the wiki and fix what trips it

---

## Quick Reference

<!-- Add your own quick-reference table here. Example:

| Resource | URL | Access |
|----------|-----|--------|
| Git Hosting | https://github.com/you/wiki | Web + SSH |
| Wiki UI | https://wiki.example.com | Web |
| NAS | https://nas.local | LAN only |
-->
