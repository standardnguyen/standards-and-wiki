# Verifying your own write is a disclosure vector

## The shape

You append one line to a config file. You want to confirm it landed. So you look at the end of the file:

```bash
tail -3 ~/.profile       # confirm my line is there
```

You appended exactly one line, so the last line is your line — and the two above it are whatever happened to sit above it. In a shell rc, a `.env`, or a CI config, what sits above the end of the file is frequently a block of `export …_TOKEN=…` lines.

You wanted one line of confirmation. You printed its neighbours. The confirmation cost nothing you needed and bought you a disclosure you cannot unsee.

## Why it survives review

Because it is not a credential command. Nothing in `tail -3` says *secret* — it is the plainest diligence in the world, the read-back you do after every write. It is issued precisely in the moment you are being careful, so the part of you that screens commands for risk has already stood down.

And the failure is off by one in a way nobody models: the command's *purpose* was to inspect one line, its *effect* was to print a window. You do not think "I am about to print the region around a secret" — you think "I am about to verify my write." The window is incidental to the intent, which is why the intent-based check never fires.

The read-back is also the one step where being wrong feels most expensive. Not confirming feels careless. So the pressure runs toward *looking at more of it*, not less.

## The general form

**A read-back that verifies your write by examining a window around it prints whatever else is in the window.** The neighbours are not part of your change, so your mental model of the output does not contain them — and in exactly the file classes where you write changes (rc files, env files, config files), the neighbours are where the credentials live.

The mechanism generalizes past `tail`:

| verification | prints | discloses |
|---|---|---|
| `tail -3` after a one-line append | your line **plus two above it** | whatever sat above your line |
| `cat`/`head` to "check the format" | the whole file | everything in it |
| a count or boolean against your own line | whether your line is present | nothing |

The last row is the whole fix: **the thing you were unsure about is whether your line landed — so predicate on your line.** `tail -1` when you appended exactly one line, or a count of your exact string. Neither can print a neighbour, because neither looks outside your line.

## What it costs

A live credential in a transcript, a log, a terminal scrollback, an agent's context, or a ticket — and the response is rotation, across every system that credential touches. A rotation is not free even when it is cheap: every consumer of that secret has to be found and updated, and the ones you miss stay broken until something fails.

The disclosure also inherits whatever persistence the transcript has. An agent's context may be written to disk and synced to an archive. A terminal log may outlive the session. Removing the credential from the service does not remove it from the record.

And the class it belongs to has a shape worth naming: **the leak never comes from a command that looked like it touched a secret.** It comes from a redaction attempt, an environment render, a repository inventory, a debugging session, a deploy setup — and from the verification step, which is the one that felt most innocent of all.

## The defense

**Confirm a write with a predicate about your own line, never a window around it.**

```bash
grep -c 'the exact line I appended' ~/.profile      # 1 → it landed
tail -1 ~/.profile                                   # only if you appended exactly one line
```

The append succeeding was never the uncertain thing. Do not buy that reassurance with the neighbours.

Two rules that sit around this one and matter just as much:

- **Ask "could this command's output contain a credential?"** — not "is this a credential command?" Anything that prints a URL, an env, a config line, or a remote can. A remote listing in `scheme://user:TOKEN@host` form stores the credential in the URL, so `git remote -v` is in this class too.
- **A content-matching `grep` against a config file is the same failure wearing a research habit's clothes.** Ordinary "grep first" reconnaissance on a config file is the right instinct everywhere except there: if the matched line is `key = "value"`, the match *is* the value. Before grepping a file that might hold a credential, ask whether a hit could *be* a secret line, and if so use `-c` or `-q`. The safer form of the research habit is a habit about the file, not about the keyword: *does this file hold credentials?* If yes, count.

## The trigger

The moment after you write to a file whose neighbours you have not read — an rc file, an env file, a config file, anything under a path shaped like credentials — and you reach for a read-back to confirm it.

The specific feeling is *being careful*. That is the moment the screening step is off, and it is the moment this class of leak fires. **It does not fire when you are being reckless; it fires when you are double-checking.**
