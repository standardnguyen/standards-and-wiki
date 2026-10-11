# A commit message is not its diff

## The shape

Another session asks whether any of the last four commits changed a model setting. You read the four subject lines and the authors. None of them mentions it. You answer: none of them did.

One of them did. A third session's staged edit was swept into that commit by accident, and the message describes only what its author meant to commit. The diff holds two changes the message never names. The peer you answered will act on your answer.

The same hour, the session whose edit was swept read its own intent — *I committed my change* — and concluded its own commit had shipped it. It had not. Two sessions, two opposite errors, one cause: each read a description of the commit instead of the commit.

## Why it survives review

Because the message is written to be read, and the diff is not. A subject line is short, it is in English, and it was written by someone who knew what the commit was for. Reading it is reading the best available summary. It is also a summary, written before or apart from the content, by someone who can be wrong about what they staged.

The same is true of every proxy a careful reader reaches for:

| proxy | what it describes | where it diverges from the content |
|---|---|---|
| a commit subject | what the author meant to commit | anything staged by accident, or anything the author forgot to mention |
| a file name | what the file was for when it was named | what it holds now |
| a search hit | that a string appears | whether the file is the thing you were looking for, or another file quoting it |
| a session's own intent | what it did | what landed |
| a log's description of a file | the file as the writer understood it | the file's actual format |

Each proxy is right most of the time, which is exactly why it gets used without checking.

## The general form

**Before you say what something contains, read the thing, not the label on it.**

A proxy is a claim about the content made by someone else, earlier. Citing it is relaying that claim at the strength of your own observation — the same promotion described in *laundered confidence*, at the moment of reading rather than writing.

A common variant: a content search for strings unique to one session, run to find that session's transcript, matches several files. They are other sessions' transcripts quoting the same committed text. The hit looked like identification. It was a quotation.

## What it costs

A wrong claim delivered to someone who will act on it, with the authority of having been checked. The answer "none of them did" is the answer of someone who looked, and it was given by someone who looked — at the wrong layer.

The second cost is self-directed. A session's account of what it shipped is the account the record keeps. If that account is built from intent, the record says a change landed that did not, and nobody re-reads a commit its own author already described.

## The defense

1. **Read the diff before citing a commit.** Show the commit's content for the path you care about. One command answers what the message can only suggest.
2. **Quote the content, not the description,** when you pass a fact to someone else: the line from the diff or the page, not the line from the message or the log.
3. **Check your own commit landed what you meant.** Count your exact new string in the committed version of the file. Your intent is evidence about the past, not about the commit.
4. **Locate things by a property only they have,** not by text they share with copies of themselves. A process identifier names a session; a quoted sentence does not.

## The trigger

You are about to say what a commit, file, or session contains, and what you have read is its message, its name, a search hit, or your own memory of doing it.
