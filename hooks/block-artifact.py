#!/usr/bin/env python
"""PreToolUse hook - block the Artifact tool, force local HTML + the make-brief skill.

Artifacts are hosted off-machine and can't be pulled back into git, so this
project keeps briefs as local HTML files under version control.

The only call that is allowed through is action="list" (a read-only query that
produces no externally hosted content). Everything else is denied, and the
message on stderr tells Claude what to do instead.

Exit code contract:
  0 = allow
  2 = block; stderr is fed back to Claude
"""
import json
import sys


GUIDANCE = """\
[blocked by hook] The Artifact tool is disabled in this environment.

Artifacts are hosted off-machine and can't be pulled back into git, so this
project keeps briefs as local HTML files under version control.

Use this flow instead:

1. Load the make-brief skill -- /smart-brief:make-brief if it is installed as
   a plugin, otherwise ~/.claude/skills/make-brief/SKILL.md.
   It is the house process for "an HTML page a human can read and decide
   from": motivation-first section structure, inline SVG cause-and-effect
   diagrams, explicit self-correction and evidence-strength markers.
   Start by copying the starter.html that sits next to that SKILL.md and
   rewriting it; do not hand-roll the CSS again.

2. Write a local .html file with the Write tool
   -- default location: <project>/docs/reports/<topic>_YYYY-MM-DD.html
      (use the scratchpad only for genuinely throwaway pages)
   -- the file must carry a full skeleton of its own (<!doctype html> /
      <html lang="..."> / <meta charset="utf-8"> / viewport / CSS reset),
      otherwise non-ASCII text renders as mojibake.
   -- do not write the file through a shell redirect or a shell's
      write-file cmdlet; encoding and BOM handling are not reliable there.

3. Open it in the browser:
   -- Windows:      Start-Process "<absolute path>"
   -- macOS:        open "<absolute path>"
   -- Linux:        xdg-open "<absolute path>"

4. Print the full local path in the conversation, plus a separate summary
   (claim + evidence + what the reader has to decide). Handing over a path
   alone does not count as delivering the work.

Note: a local file has none of the Artifact CSP restrictions, but still do not
link to external resources -- the page has to open offline. Inline all CSS/JS.
"""


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # If the input can't be read, don't block -- never break a normal flow
        return 0

    if payload.get("tool_name") != "Artifact":
        return 0

    tool_input = payload.get("tool_input") or {}
    # Read-only query is allowed: it produces no externally hosted content
    if tool_input.get("action") == "list":
        return 0

    sys.stderr.write(GUIDANCE)
    return 2


if __name__ == "__main__":
    sys.exit(main())
