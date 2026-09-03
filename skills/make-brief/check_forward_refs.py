#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""check_forward_refs.py - find terms that get used before they are defined.

A writer cannot catch this by re-reading. You already know what the words mean, so your eye
slides over the first occurrence without noticing that nothing has explained it yet. The reader
does not have that luxury: they hit an undefined term, stop, and try to reconstruct it from
context. Every one of those stops is a small tax, and on a page full of new terminology the tax
compounds until the reader gives up.

This script does the one part of the check that can be mechanised: it extracts the text a reader
actually reads, finds where each term first appears, and lists the terms in that order. Deciding
whether a given spot counts as "explained" still needs a human - that requires reading.

Two things it deliberately does not treat as a definition:

  * A term in an h2. Headings help a reader find a section; they are not read as prose, and a
    reader arriving through the body text has not necessarily looked at them.
  * A term inside a diagram. Labels in an SVG are read once the reader already cares; they are
    not where a first encounter should happen. SVG contents are replaced with a marker.

Usage:
    python check_forward_refs.py <file.html>
    python check_forward_refs.py <file.html> --terms queue-time,job-mix,fail-open

Without --terms it collects candidates automatically: <code> spans, anything marked with the
.term class, and Latin-script words inside h2 headings.

Read the output top-down. The entries listed first are the dangerous ones: the page has barely
started and those words are already in play.
"""
import html
import re
import sys

STOP = {"", "-", "--", "px", "true", "false", "null", "0", "1"}


def plain_text(src):
    """The text a reader actually reads, in reading order."""
    body = src.split('<div class="wrap">', 1)[-1]
    # A table of contents is navigation, not prose: appearing there is not "being used".
    body = re.sub(r'<nav class="toc">.*?</nav>', " ", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", " ", body, flags=re.S)
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    # Diagram labels are not where a first encounter should happen.
    body = re.sub(r"<svg.*?</svg>", " [diagram] ", body, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(txt))


def collect_terms(src):
    terms = set()
    for m in re.findall(r"<code>(.*?)</code>", src, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", m)).strip()
        if 2 <= len(t) <= 28 and t not in STOP:
            terms.add(t)
    for m in re.findall(r'<span class="term">(.*?)</span>', src, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", m)).strip()
        if t:
            terms.add(t)
    for m in re.findall(r"<h2>(.*?)</h2>", src, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", " ", m))
        for w in re.findall(r"[A-Za-z_][A-Za-z0-9_\-]{3,}", t):
            terms.add(w)
    return sorted(terms)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        src = fh.read()

    if "--terms" in sys.argv:
        raw = sys.argv[sys.argv.index("--terms") + 1]
        terms = [t.strip() for t in raw.split(",") if t.strip()]
    else:
        terms = collect_terms(src)

    txt = plain_text(src)
    rows = []
    for t in terms:
        i = txt.find(t)
        if i >= 0:
            rows.append((i, t, txt[max(0, i - 44):i + 44].strip()))
    rows.sort()

    print("# Forward-reference scan: %s" % path)
    print("# %d terms, ordered by where they first appear." % len(rows))
    print("# For each row ask: at this point, does the reader know what this word means?")
    print("# A heading does not count. A diagram label does not count.")
    print()
    print("%-7s %-26s %s" % ("offset", "term", "first appearance"))
    print("-" * 108)
    for i, t, ctx in rows:
        print("%-7d %-26s ...%s..." % (i, t[:26], ctx))
    print()
    print("The rows at the top are the ones to check first: the page has barely begun and those")
    print("words are already load-bearing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
