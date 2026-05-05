# Human-Readability Guidelines

The wiki should remain executable without an LLM in the loop — i.e. if Claude Code or any frontier-model assistant suddenly becomes unavailable, a human (the operator or someone they trust) should be able to read the protocols and reference pages and operate the systems unassisted.

This page captures the criteria for "human-readable enough." Validation against these criteria runs as [Protocol 9](../protocols/9-human-readability-audit.md).

## The Test

A page or protocol is **human-readable** if a competent engineer who has never used this specific system can:

1. Identify what the document is for and whether it applies to their situation.
2. Locate every prerequisite — file, credential, tool, prior protocol — it depends on.
3. Execute every step without inferring missing detail.
4. Recognize success and failure states explicitly.
5. Recover when something breaks, or know what to escalate.

If any of those fails, the document is LLM-only or LLM-assisted. That is acceptable for some surfaces (voice / persona files for the model have no human equivalent), but it is a gap whenever the system behind the document has to keep running without a model.

## Criteria

### For protocols

- **Decision criteria are explicit.** Any step that says "decide", "judge", "evaluate", "review" includes a rubric or worked example. LLMs confabulate criteria; humans don't, and shouldn't have to.
- **Commands are exact.** No "check the database" without a connection string. No "look at the logs" without a path. No "run the script" without an absolute path and arg list.
- **Harness-mediated steps have manual fallbacks.** If a step uses a subagent, a slash command, or any LLM-mediated mechanism, the underlying SSH / curl / shell equivalent is documented in the same file or a clearly-linked one.
- **Pre-reqs are stated.** "Before running this protocol, read X and Y" appears in the file. Auto-loaded context (root CLAUDE.md, project CLAUDE.md) is not assumed — call it out explicitly when it matters.
- **Error paths exist.** What does the executor do if step N fails? Where do they look? What's the escalation?
- **Worked examples for judgment calls.** At least one filled-in example for every subjective step.

### For reference pages

- **Procedure section, not just data.** A server inventory needs a "to add a new server, here's the runbook" — not just a table.
- **Schemas are documented.** If the page points at JSON, a database, or an API, every field has a type and a one-line meaning.
- **Manual fallback for service-mediated work.** Every operation routed through a wrapper script or harness tool has a curl-or-SSH equivalent stated.
- **State diagrams for multi-step workflows.** Any lifecycle a record passes through (e.g. ticket states, content-pipeline stages, build-and-deploy flow) is drawn or enumerated.
- **Break-glass section.** What happens if the automation fails? Where are the credentials? How is the system rebuilt from scratch?

### For credentials

- **Pointer, not value.** "The deploy token lives in `~/.bashrc` as `$DEPLOY_TOKEN`" is correct. Displaying the value is not.
- **Rotation procedure documented.** How is the credential regenerated, and which downstream systems need to be told?
- **Backup location stated.** If the credential is regenerable from elsewhere (a secrets manager, password manager, paper backup in a safe), that location is named.

## Audience Marker

Some surfaces are LLM-only by design and do not need to pass this audit:

- Voice / persona / register protocols — instructions for the model, no human equivalent.
- Open-ended reasoning protocols (counterfactual analysis, model self-audit) with no deterministic human procedure.
- Project CLAUDE.md files framed explicitly as agent briefs.

These are tagged at the top of the file with the marker:

```
> **audience: agent-only.** this file is an LLM brief; it has no human-execution path.
```

Files carrying this marker are skipped by Protocol 9.

## Related

- [Protocol 9: Human-Readability Audit](../protocols/9-human-readability-audit.md) — the validator that checks docs against this page.
- [Style Guide](style-guide.md) — voice, tense, tone, and formatting conventions.
