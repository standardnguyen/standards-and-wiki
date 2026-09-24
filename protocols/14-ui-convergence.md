# Protocol 14: UI Convergence

Recursive QA-agent loop for user-facing surfaces: deploy a fresh poke-everything QA agent → triage its findings → fix → re-verify → deploy another *fresh* agent → repeat until a round comes back clean.

The single-pass sibling is the `CLAUDE.md` rule-4 directive **"frontends get driven, not just curled."** This protocol is that directive run to a fixed point. It exists because green unit tests plus endpoint round-trips repeatedly ship user-visible defects: the origin run found seven real defects — including a cross-site-scripting sink and a scroll-yank on the core use case — in a page that had already been marked "verified" on passing tests.

## Trigger

"Run Protocol 14", "QA loop this", "run it until convergence" — or offer it after shipping or substantially changing any user-facing surface (web page, web app, terminal UI).

## Prerequisites

- The surface is deployed and reachable, and the agent can drive it:
  - **Web** → a headless browser driver (Playwright, Puppeteer, Selenium). Capture console messages *and* uncaught page errors on every run. If the page holds a long-lived connection open (SSE, websocket), wait on `domcontentloaded` rather than network-idle — network-idle never fires.
  - **Terminal UI** → drive a disposable instance and capture its screen (e.g. `tmux capture-pane`).
- You know the app's API surface and its live or shared state — specifically, what an agent must **not** touch.

<!-- Customize: record your project's actual driver command and interpreter path here
     once you have one, so each round's briefing can quote it verbatim. -->

## The loop

### 1. Brief a fresh QA agent

One agent per round. This is not a bulk fan-out — get approval before ever widening it. Every section of the briefing is load-bearing:

- **App map** — what it is, its URL, the source files to read, its endpoints and views.
- **Tooling** — the exact driver invocation, where to write screenshots, and the connection-handling gotcha above.
- **HARD FENCES** — the section that makes recursion safe. Name the untouchable live state explicitly. Cap any action with a real-world cost (a message that reaches a human, a paid API call, a destructive write) at a specific small number. Point free play at zero-cost targets — a sandbox or throwaway instance. Forbid restarting processes and daemons. **Report-only: no fixes, no commits.**
- **Known-by-design list** — every deliberate quirk and deferred item, so the agent hunts *fresh* defects instead of re-litigating settled decisions. **This list is what makes the loop converge instead of oscillate**, and it is the section that grows every round.
- **Round 2 and later** — the fixes-to-verify list: *"try to break these harder."* Regression-hunting is half of a later round's value.
- **Probe menu, plus license to exceed it** — viewports (phone, narrow, landscape, desktop); content robustness (injection payloads, long unbroken strings, emoji, floods); navigation races (rapid open/close, browser-back versus in-app back, dead deep links, two tabs); input races (double-submit, whitespace-only); failure injection (intercept requests to mock hostile, 404, and empty API responses); accessibility spot-checks (contrast ratios, tap-target sizes) — plus "anything your judgment flags."
- **Report format** — defects (severity · repro steps · observed versus expected · screenshot), suggestions (rationale · effort), a **verified-fine list** so coverage is legible rather than vibes, and — from round 2 — a one-line **convergence verdict**: `CONVERGED` or `NOT CONVERGED (what blocks it)`.

### 2. Triage every finding — three bins, nothing dropped

- **Fix** — a real defect; fix it this round.
- **By-design** — intended behavior; add it to the known-by-design list so no later round re-reports it. If the agent found it confusing, ask whether the *communication* is the defect (a label or banner fix) before binning it.
- **Defer** — real but not now; write it to the project's backlog **in this round**. Per the homeless-information rule, a deferred finding that lives only in a disposable agent report is a finding you have lost.

### 3. Fix, self-verify, ship the round

Fixes follow the normal engineering rules of the repo they land in. Before deploying the next QA agent, **spot-check the riskiest fixes yourself in the real interface** — a broken fix wastes an entire agent round. Beware test-flow bugs while you do: a browser-back check needs a real history stack, not a direct deep-link load.

Tests green → deploy or reload the running instance (a stale server serves the old page, and the round will be spent re-finding fixed bugs) → commit the round as one commit.

### 4. Recurse with a fresh agent

Always a **new** agent, never a resumed one. Fresh eyes, no anchoring on its own prior report — an agent asked to re-check its own findings tends to confirm them. Its briefing grows by two sections: the fixes-to-verify list and the updated known-by-design list.

### 5. Converge or stop

- **CONVERGED** — a round reports all fix-verifications passing and no new actionable defect above cosmetic. Do a final ship: commit, update the PR, log the loop.
- **Hard cap: 4 rounds.** Not converged by then means something structural — the surface is churning underneath you, the known-by-design list is wrong, or the fixes are fighting each other. Stop, surface the pattern to the user, and don't grind.

## Cost and notes

- Each agent round is real spend. Two to three rounds is the normal shape; budget before starting.
- The QA agent's transcript is disposable; its *report* is not. Every triage bin must land somewhere durable — in code, in the known-by-design list, or in the backlog. Screenshots are session-scoped evidence, not wiki material.
- Subagents inherit the parent's full tool surface (see `CLAUDE.md` → Subagent Workflow). The fences section must re-state the prohibitions every round; a fence stated once in round 1 does not bind the round-3 agent.
- This protocol assumes a *deployed, drivable* surface. It does not replace unit tests — it is the layer above them.

## Related

- `CLAUDE.md` → Doing Tasks rule 4 ("frontends get driven, not just curled") — the single-pass directive this protocol iterates
- [Protocol 2: Spot-Check](2-spot-check.md) — the same fresh-eyes-beat-self-review principle, aimed at wiki prose instead of UI
