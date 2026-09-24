#!/usr/bin/env python3
"""
Protocol 6: Exhaustive homepage reachability crawl.

Creates a temporary SQLite database, spiders from the homepage through all
internal wiki links (BFS), then reports any .md files that exist on disk but
are not reachable from the homepage through any link chain.

Usage:
    python3 protocols/scripts/homepage-crawl.py [wiki_root]

If wiki_root is omitted, defaults to the repository root (two levels up
from this script).

The SQLite database is written to /tmp and its path is printed so Claude
or the user can query it after the run.

Customization points are marked `Customize:` — the link syntaxes, asset
suffixes, and excluded directories below are defaults, not laws.
"""

import os
import re
import sqlite3
import sys
import tempfile
from collections import deque
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Absolute internal links. Matches both Wiki.js-style links (`[text](/en/path)`)
# and plain site-absolute links (`[text](/path)`). Optional anchor fragments
# are tolerated. Group 2 is the prefix, group 3 is the path body.
LINK_RE = re.compile(r'\[([^\]]*)\]\((/(?:en/)?)([^)#]+)(?:#[^)]*)?\)')

# Relative `.md` links, including parent-directory hops (`../sibling.md`).
RELATIVE_LINK_RE = re.compile(
    r'\[([^\]]*)\]\(((?:\.\./)*[A-Za-z0-9_][^)#:]*?\.md)(?:#[^)]*)?\)'
)

# Hugo relref shortcodes: {{% relref "01-foo.md" %}} / {{< relref "../_index.md" >}}.
# Targets resolve relative to the linking file's own directory, not the wiki root.
RELREF_RE = re.compile(r'\{\{[%<]\s*relref\s+"([^"]+)"\s*[%>]?\}\}')

# Extension-less relative links: `[x](sibling-page)`. These are resolved by
# ordinary relative-URL arithmetic, and are correct only from branch/section
# index pages (which publish one level shallower than their leaves). They are
# NOT rewritten by a generator's markdown render hook, which typically only
# touches `.md`-suffixed destinations. Every other page needs a form that works
# for its own type: `sibling.md` from an ordinary leaf page, `../sibling/` from
# an index-bundle page.
#
# BLIND SPOT: the pattern below requires the destination to start with
# [A-Za-z0-9_], so `](./)` is unmatchable — and from a leaf page it resolves to
# the page itself, so it returns 200 and no link checker flags it either. Grep
# for `](\./)` separately. Before widening this regex, plant a known-bad link
# and confirm the crawler reports it (see Protocol 10 on proving a check fails).
#
# Only counted when the resolved target actually exists — a bare word in parens
# is too ambiguous to report as a *broken* link.
BARE_RELATIVE_LINK_RE = re.compile(
    r'\[([^\]]*)\]\(((?:\.\./)*[A-Za-z0-9_][A-Za-z0-9_/-]*/?)(?:#[^)]*)?\)'
)

# Customize: shortcodes that auto-enumerate child pages at build time — e.g. a
# `{{< roster >}}` that renders a link to every sibling page and child section.
# Any page containing one reaches all of its children even though no literal
# link appears in the markdown, so the crawler must follow those edges or the
# children read as orphans. Leave empty if your wiki has no such shortcode.
AUTO_ENUMERATE_SHORTCODES: tuple[str, ...] = ()   # e.g. ('roster',)
AUTO_ENUMERATE_RE = (
    re.compile(r'\{\{[%<]\s*(?:' + '|'.join(AUTO_ENUMERATE_SHORTCODES) + r')\b')
    if AUTO_ENUMERATE_SHORTCODES
    else None
)

# Link targets with these suffixes are static assets, not wiki pages. Without
# this list the crawler appends `.md` to an image or PDF link and reports a
# phantom broken page that nobody ever meant to write. Extend it whenever you
# start linking a new file type.
ASSET_SUFFIXES = (
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.pdf', '.xlsx',
    '.docx', '.mp3', '.mp4', '.zip', '.epub', '.json', '.txt', '.html',
    '.csv', '.woff2', '.ttf', '.ipynb', '.py',
)

# Customize: path suffixes that are on-disk `.md` files but deliberately not
# navigable pages — machine-generated dumps, archived exports, boilerplate kept
# for reference. Listing them here keeps them out of the orphan report instead
# of accumulating there forever. Matched against the path's tail.
NON_CONTENT_PATH_SUFFIXES: tuple[str, ...] = ()   # e.g. ('raw/export.md',)

# The homepage. `home.md` is this template's default; `_index.md` is the Hugo
# section-index convention. The first one that exists is used as the crawl seed.
SEED_NAMES = ['home.md', '_index.md']

# Files that are not wiki pages (exact relative paths from wiki root)
EXCLUDE_FILES = {
    'CLAUDE.md',
    'README.md',
    'LICENSE.md',
}

# Repo-facing (non-page) basenames, skipped at any depth. `AGENTS.md` is
# commonly a symlink or twin of the sibling `CLAUDE.md` so that non-Claude
# harnesses load the same project instructions; one per project directory adds
# up fast, and every one of them reads as an orphan until excluded here.
NON_PAGE_BASENAMES = {'CLAUDE.md', 'README.md', 'AGENTS.md'}

# Top-level directories that are not wiki content.
#
# <!-- Customize -->  AUDIT THIS LIST; DO NOT INHERIT IT. An exclusion added
# when a directory genuinely held no wiki pages survives after that directory
# fills up with real, tracked, linked pages — and from then on the orphan check
# reports a clean result on a published section it never looks at. It cannot
# report a page that lost its homepage link, because it never sees the page.
# That is a detector going blind, which is the failure this script exists to
# prevent. Before trusting a green run, list what each entry currently hides.
EXCLUDE_DIRS = {
    'scratch',
    '.claude',
    '.git',
    '.github',
}

# Directory names skipped wholesale at any depth. `__pycache__` is Python build
# output beside the protocol scripts; some site generators auto-create an
# `_index.md` inside it during a migration.
EXCLUDE_BASENAMES_ANYWHERE = {
    '__pycache__',
}


def is_non_content_artifact(rel_path: str) -> bool:
    """True for on-disk `.md` files that are deliberately not navigable pages."""
    return bool(NON_CONTENT_PATH_SUFFIXES) and rel_path.endswith(NON_CONTENT_PATH_SUFFIXES)


def is_log_dir_placeholder(rel_path: str) -> bool:
    """True for `logs/_index.md` stubs.

    Static-site generators want an index file in every directory, so `logs/`
    dirs pick up an empty `_index.md` that exists only to satisfy the build.
    The meaningful index is the parent's `session-log.md`, which links each
    log file individually — so treat the stub as non-content rather than
    reporting it as an orphan forever.
    """
    parts = rel_path.split('/')
    return (
        len(parts) >= 2
        and parts[-2] == 'logs'
        and parts[-1] == '_index.md'
    )

# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def wiki_root_default() -> Path:
    """Derive wiki root from script location: protocols/scripts/ -> root."""
    return Path(__file__).resolve().parents[2]


def link_path_to_files(link_path: str, wiki_root: Path) -> list[str]:
    """Convert an absolute wiki link path to candidate relative .md file paths.

    A link can address either an explicit page (`/foo/bar` -> `foo/bar.md`) or
    a section directory (`/foo` -> `foo/_index.md`). Try each and return
    whichever exists; if none exists, return one canonical spelling so the
    caller can record the broken reference.
    """
    base = link_path.rstrip('/')
    if base.lower().endswith(ASSET_SUFFIXES):
        return []  # static asset link, not a page reference
    if base.rsplit('/', 1)[-1] in NON_PAGE_BASENAMES:
        return []  # repo-facing file, deliberately outside the page set
    if base.endswith('.md'):
        # The link already names the file — appending `.md` again produced
        # phantom `.md.md` entries in the broken-link report.
        return [base]
    # `/index.md` is the leaf-bundle spelling (a page that renders at its
    # directory's URL and keeps its assets beside it).
    candidates = [base + '.md', base + '/_index.md', base + '/index.md']
    existing = [c for c in candidates if (wiki_root / c).exists()]
    # When broken, report ONE canonical spelling rather than every candidate —
    # reporting all of them inflates the broken-link count several-fold.
    return existing if existing else [candidates[0]]


def extract_links(filepath: Path, wiki_root: Path) -> list[tuple[str, str]]:
    """Return [(link_text, relative_md_path), ...] from a markdown file."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return []

    # HTML comments and inline code spans hold examples, not navigation.
    content = re.sub(r'<!--.*?-->', '', content, flags=re.S)

    results = []
    in_code_block = False
    for line in content.splitlines():
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            # Links inside fenced examples are illustrations, not navigation.
            continue
        line = re.sub(r'`[^`]*`', '', line)

        for m in LINK_RE.finditer(line):
            link_text = m.group(1)
            wiki_path = m.group(3)   # group 2 is the "/" or "/en/" prefix
            for candidate in link_path_to_files(wiki_path, wiki_root):
                results.append((link_text, candidate))

        for m in RELATIVE_LINK_RE.finditer(line):
            sibling = m.group(2)
            if sibling.startswith('/'):
                continue
            if sibling.lower().endswith(ASSET_SUFFIXES):
                continue
            sibling_path = (filepath.parent / sibling).resolve()
            try:
                rel = sibling_path.relative_to(wiki_root.resolve())
            except ValueError:
                continue
            results.append((m.group(1), str(rel)))

        for m in RELREF_RE.finditer(line):
            target = m.group(1).split('#')[0]
            if not target:
                continue
            if not target.endswith('.md'):
                target = target.rstrip('/') + '.md'
            target_path = (filepath.parent / target).resolve()
            try:
                rel = target_path.relative_to(wiki_root.resolve())
            except ValueError:
                continue
            results.append(('relref', str(rel)))

        for m in BARE_RELATIVE_LINK_RE.finditer(line):
            target = m.group(2).rstrip('/')
            for candidate in (target + '.md', target + '/_index.md',
                              target + '/index.md'):
                cand_path = (filepath.parent / candidate).resolve()
                if not cand_path.exists():
                    continue
                try:
                    rel = cand_path.relative_to(wiki_root.resolve())
                except ValueError:
                    continue
                results.append((m.group(1), str(rel)))

    if AUTO_ENUMERATE_RE and AUTO_ENUMERATE_RE.search(content):
        # The shortcode renders a link to every child page at build time.
        for sibling in sorted(filepath.parent.glob('*.md')):
            if sibling == filepath:
                continue
            try:
                rel = sibling.relative_to(wiki_root.resolve())
            except ValueError:
                continue
            results.append(('auto-enumerate', str(rel)))
        for sub in sorted(filepath.parent.iterdir()):
            # Child sections are enumerated too, via their own index file.
            sub_index = sub / '_index.md'
            if sub.is_dir() and sub_index.exists():
                try:
                    rel = sub_index.relative_to(wiki_root.resolve())
                except ValueError:
                    continue
                results.append(('auto-enumerate', str(rel)))
    return results


def gather_all_md_files(wiki_root: Path) -> set[str]:
    """Return the set of all .md relative paths that count as wiki pages."""
    pages = set()
    for md in wiki_root.rglob('*.md'):
        rel = md.relative_to(wiki_root)
        rel_str = str(rel)

        # Skip excluded exact files and any repo-facing basename in subdirs
        if rel_str in EXCLUDE_FILES or rel.name in NON_PAGE_BASENAMES:
            continue

        if is_non_content_artifact(rel_str):
            continue

        # Skip excluded top-level directories
        if rel.parts[0] in EXCLUDE_DIRS:
            continue

        # Skip directories named in EXCLUDE_BASENAMES_ANYWHERE at any depth
        if any(part in EXCLUDE_BASENAMES_ANYWHERE for part in rel.parts):
            continue

        # Skip placeholder `logs/_index.md` files
        if is_log_dir_placeholder(rel_str):
            continue

        pages.add(rel_str)
    return pages


def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.executescript('''
        CREATE TABLE pages (
            path        TEXT PRIMARY KEY,
            parent      TEXT,
            depth       INTEGER NOT NULL,
            on_disk     INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE links (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            source      TEXT NOT NULL,
            target      TEXT NOT NULL,
            link_text   TEXT,
            target_exists INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE orphans (
            path TEXT PRIMARY KEY
        );
    ''')
    conn.commit()
    return conn


def crawl(wiki_root: Path, conn: sqlite3.Connection,
          seed: str) -> tuple[set[str], set[str]]:
    """BFS from the seed homepage file. Returns (reachable, orphans)."""
    visited: set[str] = set()
    queue: deque[tuple[str, str | None, int]] = deque()

    queue.append((seed, None, 0))
    visited.add(seed)
    conn.execute(
        'INSERT INTO pages (path, parent, depth, on_disk) VALUES (?,?,?,?)',
        (seed, None, 0, int((wiki_root / seed).exists())),
    )

    while queue:
        current, _parent, depth = queue.popleft()
        current_file = wiki_root / current

        if not current_file.exists():
            continue

        for link_text, target_path in extract_links(current_file, wiki_root):
            target_exists = (wiki_root / target_path).exists()

            conn.execute(
                'INSERT INTO links (source, target, link_text, target_exists) '
                'VALUES (?,?,?,?)',
                (current, target_path, link_text, int(target_exists)),
            )

            if target_path not in visited:
                visited.add(target_path)
                conn.execute(
                    'INSERT INTO pages (path, parent, depth, on_disk) VALUES (?,?,?,?)',
                    (target_path, current, depth + 1, int(target_exists)),
                )
                if target_exists:
                    queue.append((target_path, current, depth + 1))

    conn.commit()

    # Compare against all files on disk
    all_pages = gather_all_md_files(wiki_root)
    orphans = all_pages - visited

    for orphan in sorted(orphans):
        conn.execute('INSERT INTO orphans (path) VALUES (?)', (orphan,))
    conn.commit()

    return all_pages, orphans


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(conn: sqlite3.Connection, all_pages: set[str],
                 orphans: set[str], db_path: str) -> None:
    total_links = conn.execute('SELECT COUNT(*) FROM links').fetchone()[0]
    broken_links = conn.execute(
        'SELECT COUNT(*) FROM links WHERE target_exists = 0'
    ).fetchone()[0]
    reachable_on_disk = conn.execute(
        'SELECT COUNT(*) FROM pages WHERE on_disk = 1'
    ).fetchone()[0]

    print('=' * 64)
    print('  PROTOCOL 6 — HOMEPAGE REACHABILITY CRAWL')
    print('=' * 64)
    print()
    print(f'  Database: {db_path}')
    print()
    print('  STATS')
    print('  ' + '-' * 60)
    print(f'  Wiki pages on disk (excl. scratch/CLAUDE.md): {len(all_pages):>4}')
    print(f'  Pages reachable from the homepage:            {reachable_on_disk:>4}')
    print(f'  Internal links found:                         {total_links:>4}')
    print(f'  Broken links (target missing on disk):        {broken_links:>4}')
    print(f'  Orphaned pages (on disk, unreachable):        {len(orphans):>4}')
    print()

    # Broken links
    if broken_links:
        print('  BROKEN LINKS')
        print('  ' + '-' * 60)
        rows = conn.execute(
            'SELECT source, target, link_text FROM links '
            'WHERE target_exists = 0 ORDER BY source, target'
        ).fetchall()
        for source, target, text in rows:
            print(f'  {source}')
            print(f'    -> {target}  ("{text}")')
        print()

    # Orphans
    if orphans:
        print('  ORPHANED PAGES')
        print('  ' + '-' * 60)
        for orphan in sorted(orphans):
            print(f'  {orphan}')
        print()
    else:
        print('  No orphaned pages. Every wiki page is reachable from the homepage.')
        print()

    # Depth distribution
    print('  DEPTH DISTRIBUTION')
    print('  ' + '-' * 60)
    for depth, count in conn.execute(
        'SELECT depth, COUNT(*) FROM pages WHERE on_disk = 1 '
        'GROUP BY depth ORDER BY depth'
    ):
        label = 'homepage' if depth == 0 else f'depth {depth}'
        bar = '#' * count
        print(f'  {label:>10}: {count:>3}  {bar}')
    print()

    # Deepest pages
    max_depth = conn.execute(
        'SELECT MAX(depth) FROM pages WHERE on_disk = 1'
    ).fetchone()[0]
    if max_depth and max_depth >= 3:
        print('  DEEPEST PAGES (depth >= 3)')
        print('  ' + '-' * 60)
        for path, parent, depth in conn.execute(
            'SELECT path, parent, depth FROM pages '
            'WHERE depth >= 3 AND on_disk = 1 ORDER BY depth DESC, path'
        ):
            print(f'  [depth {depth}] {path}')
            print(f'            via {parent}')
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    wiki_root = Path(sys.argv[1]) if len(sys.argv) > 1 else wiki_root_default()
    wiki_root = wiki_root.resolve()

    seed = next((s for s in SEED_NAMES if (wiki_root / s).exists()), None)
    if seed is None:
        print(
            f'ERROR: no homepage file found under {wiki_root} '
            f'(looked for: {", ".join(SEED_NAMES)})',
            file=sys.stderr,
        )
        return 2

    db_fd, db_path = tempfile.mkstemp(suffix='.db', prefix='p6_')
    os.close(db_fd)

    print(f'Crawling from {wiki_root / seed} ...')
    print()

    conn = init_db(db_path)
    all_pages, orphans = crawl(wiki_root, conn, seed)
    print_report(conn, all_pages, orphans, db_path)
    broken = conn.execute(
        'SELECT COUNT(*) FROM links WHERE target_exists = 0'
    ).fetchone()[0]
    conn.close()

    return 1 if orphans or broken else 0


if __name__ == '__main__':
    raise SystemExit(main())
