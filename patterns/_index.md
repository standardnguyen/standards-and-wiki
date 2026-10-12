# Patterns

Patterns are named, reusable design shapes. They sit beside [protocols](../protocols/_index.md) as the same kind of support, but they are a different kind of thing:

- **A protocol is a process with an end state.** It has ordered steps and is followed as written. You check it by asking whether the steps were followed.
- **A pattern is a shape you reach for in the middle of a protocol, when a judgment call needs scaffolding.** It has no ordered steps and no exit state. You adapt it rather than execute it, and you check it by asking whether the shape was the right one for the situation, not whether every line was obeyed.

The split exists so an agent never has to guess how closely to follow what it just read. Anything under `protocols/` is followed as written; anything under `patterns/` is adapted. (Not to be confused with [Protocol 8](../protocols/8-design-project-subprotocols.md), which turns a recurring project workflow into a sub-protocol; a pattern stays a shape you adapt.)

## Invoking a pattern

Invoke a pattern by number and name: "use pattern 00001, mario-and-luigi", or just "run this as a Mario and Luigi pair". When a pattern is invoked, the agent reads its `_index.md` before acting, the same rule as for protocols, so what runs is the current text and not a remembered copy.

## Structure

A pattern is a directory, not a single page:

```
patterns/<NNNNN>-<slug>/
├── _index.md          # the invariant: what the shape is, when to reach for it, when not to
└── examples/          # the variant archive: one file per shipped implementation
    └── YYYY-MM-DD-<what-it-decided>.md
```

**Why the examples are load-bearing.** No two implementations of a pattern are the same. They differ in tooling, in scripts, in what the situation forced. That variance is the knowledge you need when you adapt the shape next time, and it is lost if only the invariant survives. So:

- When you implement a pattern and ship the work, store your variant under `examples/`: what it decided, what it did differently from the invariant, and where its scripts or instruments live.
- If your variant changes, contradicts or qualifies how the invariant says something is done, fix the invariant in the same commit. Agents run the `_index.md`, not the examples, so a lesson filed only as an example is one nobody runs.
- Before building a new instance, read two or three examples.

<!-- Customize: if you use Protocol 7 to ship, consider adding a step there that treats a missing example as an unfiled fact. -->

## Adding a pattern

A pattern earns its number by being instantiated at least twice. Patterns shipped with this template earned theirs in the wiki they were ported from; your own new patterns need two instances of yours. The shape must have recurred, not just been invented, and it must be something a future session would otherwise re-derive from scratch. Number patterns with five digits, sequentially from `00001`. The slug is the handle; the number is the address. Keep a number stable once published, since forks may reference it.

## Index

| # | Pattern | Description | Directory |
|---|---------|-------------|-----------|
| 00001 | **mario-and-luigi** | Two long-lived sessions run one job that outlives a context window. One drives the work; the other navigates, watches the driver's context and progress, and compacts the driver at a clean boundary so the work never pays for a fresh boot. Two sessions, never three. | [`00001-mario-and-luigi/`](00001-mario-and-luigi/_index.md) |

<!-- Customize: add a row for each pattern you name. -->
