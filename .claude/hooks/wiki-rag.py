#!/usr/bin/env python3
"""Synthetic-RAG retrieval for a markdown wiki — ONE engine, shared by every harness.

Reads a prompt from stdin (Claude Code hook JSON *or* raw text), extracts
candidate proper nouns, greps the wiki's `.md` files for them, and surfaces
pointer+title lines for the top-matching pages. Makes wiki retrieval a harness
affordance instead of model discipline (CLAUDE.md "grep first" / "synthetic RAG").
This is the deterministic version of the "grep first, even when you're sure" rule.

Wire it as a Claude Code `UserPromptSubmit` command hook (see
`.claude/settings.json.example`): on every prompt it injects a short pointer
block naming the pages the prompt's entities map to, so the model reads the
right page before acting. Silent on no match — it never buries the prompt.

One engine, every caller (Protocol 11). The `retrieve()` function is shared
verbatim; only invocation + output rendering differ:
  - **text mode** (default) — prints the pointer block to stdout, which the
    Claude Code hook injects as context.
  - **`--json` mode** — emits `[{path, terms, title}]` for any other harness to
    render/inject itself. Never reimplement the engine in another language —
    shell out to this file, or you get a second copy of ALIASES/STOPWORDS to
    keep in sync (exactly the drift Protocol 11 exists to prevent).

The content side is self-fresh: grep reads live files, so new pages and edits
are searchable the instant they land — no reindex, no embedding store, no
staleness. Two small hand-curated tables (ALIASES, STOPWORDS) are the only
things that drift; Protocol 11 tends them.

Cheap (<1s, ~50-200 tokens). Pointer-only: page path + one-line title. The
model decides whether to Read the full page.
"""
import json
import os
import re
import subprocess
import sys

# Repo root is two levels up from this file (.claude/hooks/wiki-rag.py).
# Override with WIKI_RAG_ROOT if you run the hook from elsewhere.
ROOT = os.environ.get(
    "WIKI_RAG_ROOT",
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
)
MAX_PAGES = 5             # cap injected pointers
TOO_COMMON = 150          # a term hitting more files than this is a true stopword — skip
TOP_FILES_PER_TERM = 6    # only the most concentrated pages per term feed scoring
MIN_SCORE = 8             # a page must clear this to be injected (kills scattered noise)
SLUG_BOOST = 60           # term appears in the page's path/slug
TITLE_BOOST = 25          # term appears in the page's title/description
MAX_TERMS = 14            # cap grep calls per prompt
MIN_WORD_LEN = 4          # plain words shorter than this are skipped
MIN_IDENT_LEN = 3         # identifier-shaped tokens (digit/_/-/CamelCase) allowed shorter

# Common words that look like proper nouns at sentence start or when capitalized,
# plus generic tech terms that match half the wiki and carry no routing signal.
# Add new false-positives here as your phrasing surfaces them (Protocol 11 Mode 2).
STOPWORDS = {
    "the", "this", "that", "they", "them", "then", "there", "these", "those",
    "what", "when", "where", "which", "while", "with", "your", "you", "yours",
    "can", "cant", "could", "should", "would", "have", "has", "had", "are", "was",
    "and", "but", "for", "not", "all", "any", "how", "why", "who", "yes", "no",
    "okay", "ok", "well", "just", "like", "get", "got", "let", "lets", "run",
    "check", "fix", "add", "see", "look", "try", "make", "want", "need", "new",
    "i", "im", "id", "ill", "ive", "its", "it", "a", "an", "to", "of", "in", "on",
    "is", "be", "do", "we", "so", "if", "or", "as", "at", "by", "up", "out",
    # common verbs/adjectives that leak through lowercase prose as fake entities
    "having", "trouble", "doing", "please", "really", "gonna", "wanna", "instance",
    "again", "sweep", "pull", "next", "bunch", "kind", "sort", "still", "mid",
    "also", "yeah", "yep", "nope", "sure", "actually", "basically", "literally",
    "figure", "stuff", "going", "keep", "back", "over", "down", "into", "from",
    "fine", "good", "okay", "nice", "cool", "done", "yet", "now", "here",
    # too-generic wiki nouns
    "wiki", "content", "session", "protocol", "card", "file", "page",
    "code", "data", "api", "server", "container", "script", "test", "user",
    "model", "tool", "task", "work", "thing", "way", "right", "left",
}

# Entities whose canonical page name differs from the word people use for them —
# grep on the word alone routes to scattered logs, not the hub page. Paths are
# relative to the repo root. The examples below are SAMPLES — replace them with
# your own name-to-hub mappings. If a page's everyday name already appears in its
# path/slug or title, grep routes to it on its own and no alias is needed; the
# alias map is only for the name-not-equal-to-slug case (Protocol 11).
ALIASES = {
    # "grafana": "infrastructure/monitoring/_index.md",
    # "prometheus": "infrastructure/monitoring/_index.md",
}


def read_prompt() -> str:
    raw = sys.stdin.read()
    if not raw.strip():
        return ""
    try:
        return (json.loads(raw).get("prompt") or "").strip()
    except (json.JSONDecodeError, AttributeError):
        return raw.strip()  # fall back to raw text if not JSON


def candidates(prompt: str):
    """Extract distinct candidate routing terms from the prompt."""
    terms = set()
    # quoted phrases — high signal (e.g. "Waiting For", 'some_id')
    for m in re.findall(r'["“‘]([^"”’]{3,40})["”’]', prompt):
        t = m.strip()
        if t:
            terms.add(t)
    # All non-stopword tokens. Capitalization is NOT assumed to be a usable signal
    # (many users write lowercase prose), so precision comes from STOPWORDS + the
    # rarity filter (grep down-weights terms hitting many files) + multi-term
    # ranking, not caps.
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9_./-]*", prompt):
        low = tok.lower().strip("._-/")
        if not low or low in STOPWORDS:
            continue
        is_ident = (
            "_" in tok or "-" in tok
            or any(c.isdigit() for c in tok)
            or any(c.isupper() for c in tok[1:])  # interior caps (CamelCase)
        )
        min_len = MIN_IDENT_LEN if is_ident else MIN_WORD_LEN
        if len(low) >= min_len:
            terms.add(low)
    # Prefer longer / more-distinctive terms when capping grep calls.
    return sorted(terms, key=len, reverse=True)[:MAX_TERMS]


def grep_files(term: str):
    """Return (top_pages, total_files) for wiki pages matching term.

    One `grep -rcF` lists every file with its match count. total_files (how many
    pages mention the term at all) drives rarity weighting in retrieve(): a term in
    a handful of pages is specific and routes hard; one in a hundred barely counts.
    High file count is NOT a disqualifier — it's just down-weighted.
    """
    try:
        out = subprocess.run(
            ["grep", "-rcF", "--include=*.md", "--exclude-dir=.git", term, ROOT],
            capture_output=True, text=True, timeout=10,
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return [], 0
    scored = []
    for line in out.splitlines():
        path, _, cnt = line.rpartition(":")
        if not path:
            continue
        try:
            c = int(cnt)
        except ValueError:
            continue
        if c > 0:
            scored.append((path, c))
    scored.sort(key=lambda pc: -pc[1])
    return scored[:TOP_FILES_PER_TERM], len(scored)


def page_title(path: str) -> str:
    """First of: frontmatter description, frontmatter title, first heading."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            head = f.read(2000)
    except OSError:
        return ""
    for key in ("description", "title"):
        m = re.search(rf'^{key}:\s*["\']?(.+?)["\']?\s*$', head, re.MULTILINE)
        if m:
            return m.group(1).strip()
    m = re.search(r"^#\s+(.+)$", head, re.MULTILINE)
    return m.group(1).strip() if m else ""


def retrieve(prompt: str):
    """Core engine — shared verbatim by every caller (text mode, --json mode).

    Returns an ordered list of {path, terms, title} dicts (most relevant first),
    or [] on no match. Callers render/inject however they like — that's the only
    per-harness difference. Do NOT fork this logic into another language; shell
    out to this script instead (see Protocol 11).
    """
    if len(prompt) < 6:
        return []
    # path -> [score, {terms}, weight_sum]
    hits = {}
    for term in candidates(prompt):
        # Curated alias: route straight to the hub with a decisive score.
        alias = ALIASES.get(term)
        if alias:
            ap = os.path.join(ROOT, alias)
            if os.path.exists(ap):
                entry = hits.setdefault(ap, [0.0, set(), 0.0])
                entry[0] += SLUG_BOOST
                entry[1].add(term)
                entry[2] += 1.0
        files, total = grep_files(term)
        if not files:
            continue
        # Rarity weight: term in few pages → ~1.0; in many → → 0. Generic words
        # ("having", "trouble") hit hundreds of pages and contribute almost nothing.
        weight = min(1.0, 10.0 / total)
        over_common = total > TOO_COMMON
        for path, count in files:
            rel = os.path.relpath(path, ROOT).lower()
            in_slug = term in rel
            in_title = term in page_title(path).lower()
            if over_common and not (in_slug or in_title):
                continue  # too generic to route on unless it names the page
            # Cap raw count so a common word repeated in a long doc can't dominate
            # over a concentrated mention in the actually-relevant page.
            score = min(count, 8) * weight
            if in_slug:
                score += SLUG_BOOST
            elif in_title:
                score += TITLE_BOOST
            entry = hits.setdefault(path, [0.0, set(), 0.0])
            entry[0] += score
            entry[1].add(term)
            entry[2] += weight
    # Rank by summed rarity-weight of distinct terms (specific terms dominate),
    # then raw score. Inject pages clearing the score bar or carrying real weight.
    ranked = sorted(
        ((p, s, t, w) for p, (s, t, w) in hits.items() if s >= MIN_SCORE or w >= 1.2),
        key=lambda x: (-x[3], -x[1]),
    )[:MAX_PAGES]
    return [
        {"path": os.path.relpath(path, ROOT), "terms": sorted(terms), "title": page_title(path)}
        for path, _score, terms, _w in ranked
    ]


def main():
    as_json = "--json" in sys.argv[1:]
    results = retrieve(read_prompt())
    if as_json:
        # Structured output for non-Claude-Code callers (render/inject yourself).
        print(json.dumps(results))
        return
    if not results:
        return  # text mode: silent on no match
    lines = ["\U0001f50e wiki-rag — prompt terms map to these pages (consider reading before acting):"]
    for r in results:
        termstr = ", ".join(r["terms"])
        lines.append(f"  • {termstr} → {r['path']}" + (f" — {r['title']}" if r["title"] else ""))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
