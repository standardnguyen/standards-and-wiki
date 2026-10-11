# Protocols

Protocols are numbered procedures. Invoke one by number or name ("run Protocol 7"); the agent reads the file before executing it. This index is read on demand, not loaded every session, so adding a protocol costs no context until it is used.

| Protocol | Description | File |
|----------|-------------|------|
| 0 | Setup — guided first-run onboarding; the agent interviews the user and customizes the template | [0-setup.md](0-setup.md) |
| 1 | Full harmonization pass — fix contradictions, anachronisms, tone | [1-harmonize.md](1-harmonize.md) |
| 2 | Random-sample spot-check for contradictions across file pairs | [2-spot-check.md](2-spot-check.md) |
| 3 | Verify — generate commands to check ground truth before accepting fixes | [3-verify.md](3-verify.md) |
| 4 | Recursive harmonize — apply Protocol 1 to recent changes, repeat until convergence | [4-recursive-harmonize.md](4-recursive-harmonize.md) |
| 5 | Session log setup — create session logging infrastructure for a new project | [5-session-log-setup.md](5-session-log-setup.md) |
| 6 | Homepage coverage — check that every wiki page is reachable from `home.md` | [6-homepage-coverage.md](6-homepage-coverage.md) |
| 7 | Commit, ship & prepare for continuation — commit, push, create/update PR, update session logs, hand the work forward | [7-commit-and-ship.md](7-commit-and-ship.md) |
| 8 | Design project sub-protocols — codify recurring patterns inside a project as project-scoped sub-protocols | [8-design-project-subprotocols.md](8-design-project-subprotocols.md) |
| 9 | Human-readability audit — validate that protocols and reference pages are executable without an LLM in the loop | [9-human-readability-audit.md](9-human-readability-audit.md) |
| 10 | Codify drift check — promote a recurring drift pattern into a permanent structural check at commit time | [10-codify-drift-check.md](10-codify-drift-check.md) |
| 11 | Wiki-RAG maintenance — keep the synthetic-RAG retrieval hook's alias/stopword tables accurate as the wiki grows | [11-wiki-rag-maintenance.md](11-wiki-rag-maintenance.md) |
| 12 | Park — stash a self-contained continuation so a cold future session can resume the work | [12-park.md](12-park.md) |
| 13 | Pick up — resume a parked continuation, re-grounding against live state first | [13-pickup.md](13-pickup.md) |
| 14 | UI convergence — recursive fresh-QA-agent loop over a user-facing surface until a round comes back clean | [14-ui-convergence.md](14-ui-convergence.md) |
| 15 | LLM injection scan — sweep the wiki and its rules files for prompt-injection patterns; audit only, never auto-clean | [15-llm-injection-scan.md](15-llm-injection-scan.md) |
| 16 | Fact-check — verify a page's claims against external sources, classify each, and fix only with permission | [16-fact-check.md](16-fact-check.md) |
| 17 | Conversation forensics — find the turn where a session went wrong and name the root cause | [17-conversation-forensics.md](17-conversation-forensics.md) |
| 18 | Tighten — place a unit of knowledge where the retrieval need will actually load it | [18-tighten.md](18-tighten.md) |
| 19 | Cold read — put an unprimed fresh process in front of the wiki and fix what trips it | [19-cold-read.md](19-cold-read.md) |
| 20 | Ship retrospective — after the session log in a full Protocol 7, ask three evidence-based questions of the run and make at most three proposals | [20-ship-retrospective.md](20-ship-retrospective.md) |
| 21 | Shared-checkout commit — commit safely when other sessions edit the same checkout: pathspec vs. index form, never amend, verify what shipped | [21-shared-checkout-commit.md](21-shared-checkout-commit.md) |
| 22 | Session-limit baton — at a usage or context limit, write a self-contained handoff and fix the project setup so the next session starts cheaper | [22-session-limit-baton.md](22-session-limit-baton.md) |
| 23 | Propagation sweep — when a commit changes a fact, find and fix every other page still carrying the old value: checks first, then three capped waves of finders, two-lens judging | [23-propagation-sweep.md](23-propagation-sweep.md) |

<!-- Customize: add a row for each protocol you write. Keep the number stable once published; forks may reference it. -->
