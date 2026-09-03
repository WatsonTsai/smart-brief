# Changelog

## 0.2.0

Headings changed shape, and the rule they changed from was one this skill used to insist on.

**Headings are now terms, not assertions.** The previous version required an h2 to make a claim -
"Five checks overturned two of the numbers" rather than "Verification results" - on the reasoning
that a heading should carry the argument. Reading a page written both ways showed the cost: a table
of contents made of eight full sentences has to be read before it can be used, which is the opposite
of what a table of contents is for. A heading's job is to make a section findable. The argument
moves into the opening paragraph, where it has room to be made properly.

**The italic subtitle line is gone.** `.sec-goal` ("This section explains: ...") has been replaced
by `.lede`, a slightly larger opening paragraph carrying the same content as prose. One less
component to maintain, and one less thing that can quietly go stale - the change that prompted this
was a page whose standfirst still described a subtitle line that had already been deleted.

**Sections now open with background, not with the definition.** The first paragraph says where the
problem came from, so the reader knows why a thing exists in their system before being told what it
is. The test: after the opening paragraph the reader should be asking "so what is it?", not "so
what?".

**New document type: the mechanism explainer** (`D-3`). For pages whose job is to make a system
understood rather than to get a decision made - a system diagram plus one section per term, ending
in a lookup table and an evidence-strength table, with no decision section at all.

**New rule: name a term before using a pronoun for it.** Writing "it" for something the running text
has not yet named makes the reader stop and reconstruct the referent. A term appearing in the h2
does not count as naming it, because the reader is following the prose.

**New bundled script: `check_forward_refs.py`.** Lists every term by where it first appears, so you
can confirm the definition comes first. This is the one part of the check that can be mechanised,
and it needs to be: a writer re-reading their own page cannot see the problem, because they already
know what the words mean.

### Migration

Existing pages keep working - nothing here changes how the hook or the plugin loads. To bring an
older page up to date:

1. Replace each assertion h2 with the short label already sitting in that page's table of contents.
2. Turn each `.sec-goal` line into a `.lede` paragraph that opens with background.
3. Rename the `.sec-goal` CSS rule to `.lede` and drop the italics.
4. Run `check_forward_refs.py` over the result.

`examples/demo-brief.html` in this release is the same document as in 0.1.0, converted this way, so
the two versions can be diffed against each other.

## 0.1.0

Initial release: the `make-brief` skill, the Artifact-blocking `PreToolUse` hook, a plugin
marketplace entry, and a worked example page.
