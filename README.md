# smart-brief

A Claude Code skill and hook that replace the built-in Artifact tool with local, version-controlled HTML briefs.

English · [繁體中文](README.zh-TW.md)

Claude Code can publish a page as a hosted Artifact. This repo does the opposite. A `PreToolUse` hook blocks that tool, and the `make-brief` skill writes the page into your own repository instead: one self-contained HTML file under `docs/reports/`, tracked in git, readable offline, years later, on a machine with no network.

## Install

The repo is its own plugin marketplace, so two lines inside Claude Code install the skill and the hook together:

```
/plugin marketplace add WatsonTsai/smart-brief
/plugin install smart-brief@smart-brief
```

Read the install summary: if it says `Run /reload-plugins to activate.`, run that. Then ask Claude to publish something as an artifact. It should be blocked, and reach for the skill instead, which is namespaced as `/smart-brief:make-brief`.

The hook runs `python`. If `python` on your PATH is missing or is Python 2, change the `command` field in `hooks/hooks.json` to `python3` or to an absolute interpreter path.

<details>
<summary><b>Manual install (fallback)</b> — for a Claude Code without the <code>/plugin</code> command</summary>

<br>

1. Copy `skills/make-brief/` into `~/.claude/skills/`, and `hooks/block-artifact.py` into `~/.claude/hooks/`.
2. Merge `examples/settings.snippet.windows.json` (or `settings.snippet.unix.json`) into `~/.claude/settings.json`, replacing `YOUR_USERNAME` with the real absolute path.
3. Restart Claude Code and ask it to publish something as an artifact. It should be blocked, and reach for the skill instead.

The `python` note above applies here too, in the snippet's `command` field.

</details>

## What comes out

![The top of a brief: the headline names the subject, the standfirst says what was built and how to read the page, a warning box marks the sample as invented, and the table of contents is a list of short topics.](docs/demo-brief.png)

Diagrams are inline SVG drawn from CSS variables, so they recolor in dark mode, and the caption states the consequence rather than naming the picture:

![A two-panel contrast diagram. Both panels show the same 24.6-minute wait split between queue time and build time in opposite proportions, with a green segment showing what a faster build would save in each case.](docs/demo-diagram.png)

That page ships with the repo as `examples/demo-brief.html` — open it locally to read the whole thing, flip it to dark mode, and print it. Its numbers are invented; it exists to show the format.

## Why block Artifacts

**What stays on your machine is a fragment, not the page.** Claude Code does write the file into your project before publishing it, so nothing is lost — but that source file carries no `<!doctype html>`, no `<head>`, and no charset declaration. The host injects that skeleton at publish time. Open the local copy on its own and you get something other than what your readers saw, and non-ASCII text can come out as mojibake. Meanwhile a full copy sits on Anthropic-hosted storage, and there is no ordinary unpublish; deletion runs through a compliance API.

**A hosted page is styled to look finished.** This template is built for the opposite job: motivation before results, inline SVG at the causal steps, and explicit marks on evidence strength and on the places the author changed their mind. A page you can argue with beats a page that looks settled.

**Switching the feature off is not the same as redirecting it.** Claude Code already ships three official ways to disable artifacts — `"disableArtifact": true` in settings, `CLAUDE_CODE_DISABLE_ARTIFACT=1`, or `Artifact` in `permissions.deny`. Use one of those if all you want is the capability gone. The hook is for the other half of the problem: with the feature merely disabled, Claude falls back to writing a bare, unstyled file, whereas the hook's rejection message hands it this skill, the section structure, and the landing path. The block is not absolute — `action: "list"` is read-only and publishes nothing, so it passes.

## What the skill enforces

- **Motivation first.** Every prerequisite the reader is missing becomes an earlier section. The 30-second self-check is run on the outline, not on the finished draft.
- **Headings are terms, and the argument lives in the paragraph.** "Queue time", not "Separating the two waits needed three timestamps per job". A table of contents made of full sentences has to be read before it can be used, which defeats the point of a table of contents. Each section then opens with background — where the problem came from — before any definition, and closes with a one-line takeaway.
- **Terms are defined before they are used.** A bundled scan (`check_forward_refs.py`) lists every term by where it first appears, because a writer re-reading their own page cannot see this: you already know what the words mean. A term in a heading does not count as defined.
- **Diagrams answer a specific "why".** Inline SVG only, every fill and stroke from a CSS variable so dark mode recolors, arrows hand-drawn as `line` + `polygon`, and a caption that states the consequence rather than describing the picture.
- **Honesty has a fixed shape.** A self-correction carries all three parts: what was originally said, why it was wrong, what to believe now. Numbers are marked as measured, inferred, or not quotable. Any metric used for ranking gets a confounder check first. Every decision item carries a recommendation and its reasoning.
- **Updates are rewrites.** Patching an existing page a third time turns its section order into a history of the author's mistakes. The skill makes you rewrite and keep the superseded file with a banner instead.
- **A sentence-level pass** for buried verbs, unresolvable pronouns, comparatives with no baseline, and ungrounded abstract nouns.
- **The page is never the delivery.** The claim, the evidence, and the decision still get written in the conversation; the HTML is the layer to descend into.

## When not to use this

- **Three paragraphs in the conversation would cover it.** Then write the three paragraphs. A page that exists to look thorough costs the reader more than it gives them.
- **The material is going to be presented out loud.** Build slides.
- **The output is a durable conclusion for agents or future sessions to read.** A plain `docs/reports/*.md` is enough; it does not need layout.
- **The point is comparing magnitudes and nothing else.** That is a table. The skill will tell you to draw fewer diagrams, not more.
- **You want a URL you can send to someone outside your repository.** That is what the built-in artifact is for, and it does it well. This plugin exists for the case where the page belongs next to the code, not on the web.

## Files

```
.claude-plugin/
  plugin.json       plugin manifest: name, version, author, license
  marketplace.json  marketplace catalog, so the repo can install itself
skills/make-brief/
  SKILL.md          the skill itself
  starter.html      full skeleton: tokens, reset, both themes, theme toggle, all components
  svg_patterns.md   four reusable schematic patterns + the colour-meaning table
hooks/
  hooks.json        registers the hook for the plugin install, via ${CLAUDE_PLUGIN_ROOT}
  block-artifact.py PreToolUse hook: exit 2 on the Artifact tool, allow action="list"
examples/
  settings.snippet.windows.json   manual install only
  settings.snippet.unix.json      manual install only
  demo-brief.html   a full brief produced by the skill (invented data)
docs/
  demo-brief.png    screenshot of the above
  demo-diagram.png  close-up of one of its diagrams
```

## Notes

- Built and used on Windows. The hook and the skill are platform-neutral and the skill prints all three open commands, but the Unix install snippet has not been run on macOS or Linux.
- `"matcher": "Artifact"` matches the built-in tool by its documented identifier, the same string `permissions.deny` takes. If a future version renames the tool, the matcher needs updating with it.
- `starter.html` is `lang="en"` and keeps a CJK font as the last fallback in its stack. Change either to suit what you write.

## License

MIT
