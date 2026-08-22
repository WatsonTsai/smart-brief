# SVG pattern library (make-brief companion)

> Four patterns lifted from a real review page and generalized.
> Copy a skeleton, swap the coordinates and the text. **Every fill / stroke must use `var(--...)`.**

---

## 0. Shared rules

```html
<figure class="dia">
  <svg viewBox="0 0 720 240" role="img" aria-label="one sentence saying what this figure compares">
    ...
  </svg>
  <figcaption>Describe it, then answer "so what" — <strong>bold the sentence that is the conclusion</strong>.</figcaption>
</figure>
```

- `viewBox` defines the coordinate system; the rendered size comes from CSS (`figure.dia svg { width:100%; height:auto }`) → never write `width`/`height`.
- Text uses **classes, not inline fill**: `.svg-title` (per-panel title) / `.svg-label` (primary annotation) / `.svg-label-s` (fine print).
  Add an inline override like `fill="var(--ok)"` only when the colour carries meaning.
- Layout: title at y≈20, body y=40–160, ground line y≈150–200, annotations y≈170–230.
  Two side-by-side panels take about 340 px each, with 60 px of gutter between them.
- **Those width budgets assume Latin text.** A CJK character is about twice as wide as a Latin
  monospace character, so a label that fits in one panel in English overflows in Chinese or Japanese
  — and `<text>` does not wrap: it runs straight out of the `viewBox` and is clipped, silently.
  So: keep labels to a few characters, put the explanation in the `figcaption` instead of on the
  canvas, and split a long label across two `<text>` lines by hand (`y` and `y+14`) rather than
  hoping it fits. Budget roughly 2 × `font-size` per CJK character when you place a label, and check
  the rendered page rather than the coordinates.

### Colour semantics (must be consistent across the whole document)

| Variable | Meaning | Typical use |
|---|---|---|
| `--flow` / `--flow-soft` | input, incoming, flow | incoming signal, data-flow arrows |
| `--accent` / `--accent-soft` | the target, the thing under attention | the obstacle, the bright line, the thing being measured |
| `--ok` | good / desired outcome | small footprint, stable, signal returns |
| `--danger` | bad / critical threshold | large footprint, the right-angle vertex, the failure point |
| `--muted` | loss, shadow, energy thrown away | specular reflection escaping, shadow region, projected position |
| `--line-strong` | neutral structural lines | ground, boundaries, outlines |

### Arrows (do not use `<marker>`)

```html
<!-- shaft -->
<line x1="60" y1="55" x2="176" y2="198" stroke="var(--flow)" stroke-width="2"/>
<!-- head: a three-point triangle whose tip coincides with the line's end point -->
<polygon points="176,198 170,188 180,186" fill="var(--flow)"/>
```

`<marker>` inherits `fill` in ways that break in dark mode; a hand-drawn polygon is the reliable option.
**Check every arrow's direction once you are done** — a finished page has mistaken an arrow's tail for its head before (see the failure modes in SKILL.md).

---

## Pattern 1 — Two-panel contrast: one phenomenon, two parameter values

**Use when**: the reader needs to see "what happens as this parameter grows or shrinks". The most general and the most effective of the four.

```html
<svg viewBox="0 0 720 240" role="img" aria-label="small parameter vs large parameter">
  <!-- left: small parameter -->
  <text class="svg-title" x="20" y="24">Parameter small (plain-language gloss)</text>
  <line x1="20" y1="190" x2="330" y2="190" stroke="var(--line-strong)" stroke-width="2"/>
  <text class="svg-label-s" x="20" y="208">baseline name</text>
  <path d="M150 40 L 165 190 L 205 190 L 180 40 Z"
        fill="var(--flow-soft)" stroke="var(--flow)" stroke-width="1.5"/>
  <line x1="165" y1="45" x2="185" y2="45" stroke="var(--flow)" stroke-width="2"/>
  <text class="svg-label" x="196" y="45">input</text>
  <line x1="165" y1="190" x2="205" y2="190" stroke="var(--ok)" stroke-width="6"/>
  <text class="svg-label" x="152" y="228" fill="var(--ok)">result: small</text>
  <text class="svg-label-s" x="152" y="172">mechanism in one line</text>

  <!-- right: large parameter (same skeleton, only the geometry and the semantic colour change) -->
  <text class="svg-title" x="390" y="24">Parameter large (plain-language gloss)</text>
  <line x1="390" y1="190" x2="700" y2="190" stroke="var(--line-strong)" stroke-width="2"/>
  <path d="M430 40 L 545 190 L 680 190 L 460 40 Z"
        fill="var(--flow-soft)" stroke="var(--flow)" stroke-width="1.5"/>
  <line x1="545" y1="190" x2="680" y2="190" stroke="var(--danger)" stroke-width="6"/>
  <text class="svg-label" x="545" y="228" fill="var(--danger)">result: much larger</text>
  <text class="svg-label-s" x="390" y="172">same input spread wider → weaker per unit</text>
</svg>
```

**Key points**:
- The **input is identical in both panels** (same-width input line); the only difference comes from the parameter → the reader sees the causality at a glance.
- Mark the outcome with a thick `--ok` / `--danger` line; the difference in length *is* the argument.
- One `.svg-label-s` line at the bottom of each panel states the mechanism — do not push it into the caption.

---

## Pattern 2 — N panels side by side: enumerating mutually exclusive categories

**Use when**: three interaction modes, three technical routes, three data sources... every panel shares one structure, and the last panel is usually "the one we are going after".

```html
<svg viewBox="0 0 760 260" role="img" aria-label="three mechanisms">
  <!-- every panel has four fixed layers: title / scene / paths / three lines of explanation -->
  <text class="svg-title" x="10" y="20">① Category name</text>
  <line x1="10" y1="150" x2="230" y2="150" stroke="var(--line-strong)" stroke-width="3"/>
  <!-- scene objects: ellipse / rect / circle groups -->
  <!-- incoming -->
  <line x1="60" y1="55" x2="120" y2="148" stroke="var(--flow)" stroke-width="2"/>
  <polygon points="120,148 114,138 124,136" fill="var(--flow)"/>
  <!-- loss path (dashed, grey) -->
  <line x1="120" y1="148" x2="188" y2="58" stroke="var(--muted)" stroke-width="2" stroke-dasharray="4 3"/>
  <!-- return path (solid, ok/accent) -->
  <line x1="120" y1="148" x2="78" y2="88" stroke="var(--ok)" stroke-width="1.5"/>

  <text class="svg-label"   x="10" y="180">Typical instance</text>
  <text class="svg-label-s" x="10" y="200">our sample: XXX</text>
  <text class="svg-label-s" x="10" y="218" fill="var(--ink-2)">qualitative strength</text>

  <!-- second panel at x+260, third at x+520; otherwise structurally identical -->
</svg>
```

**Key points**:
- The three panels share exactly the same y coordinates (title 20 / ground 150 / explanation 180–218) — that is what makes them read as one scale rather than three drawings.
- **Use the last panel to open a gap**: let its explanation line say "← the one we are after", and the figure turns from a catalogue into an argument.
- Loss paths are always dashed + `--muted`; return paths are always solid + a semantic colour.

---

## Pattern 3 — Cross-section + plan view: physical path → what shows up in the data

**Use when**: explaining "because the physics works this way, this is what you will see in the data". The strongest explanatory figure of the four.

```html
<svg viewBox="0 0 740 300" role="img" aria-label="physical path mapped to the feature seen in the data">
  <!-- left half: cross-section (how the energy travels) -->
  <text class="svg-title" x="10" y="20">Cross-section: how the signal gets back</text>
  <line x1="10" y1="200" x2="340" y2="200" stroke="var(--line-strong)" stroke-width="3"/>
  <rect x="238" y="118" width="14" height="82" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <line x1="60" y1="55" x2="176" y2="198" stroke="var(--flow)" stroke-width="2"/>
  <polygon points="176,198 170,188 180,186" fill="var(--flow)"/>
  <line x1="176" y1="199" x2="236" y2="199" stroke="var(--accent)" stroke-width="2.5"/>
  <polygon points="236,199 228,195 228,203" fill="var(--accent)"/>
  <line x1="236" y1="160" x2="120" y2="58" stroke="var(--accent)" stroke-width="2.5"/>
  <polygon points="120,58 130,60 125,69" fill="var(--accent)"/>
  <circle cx="238" cy="200" r="7" fill="none" stroke="var(--danger)" stroke-width="2.5"/>
  <text class="svg-label-s" x="248" y="218" fill="var(--danger)">key point (90°)</text>
  <line x1="252" y1="200" x2="330" y2="200" stroke="var(--muted)" stroke-width="7" opacity=".45"/>
  <text class="svg-label-s" x="256" y="236" fill="var(--muted)">unreached = shadow</text>

  <!-- right half: the data view (what you actually see) -->
  <text class="svg-title" x="400" y="20">What you see in the data (plan view)</text>
  <rect x="400" y="36" width="320" height="230" fill="var(--surface-2)" stroke="var(--line)"/>
  <rect x="500" y="96" width="130" height="90" fill="none"
        stroke="var(--line-strong)" stroke-width="1.8" stroke-dasharray="5 3"/>
  <line x1="500" y1="186" x2="630" y2="186" stroke="var(--accent)" stroke-width="7"/>
  <text class="svg-label" x="500" y="208" fill="var(--accent)">bright line = key point</text>
  <rect x="500" y="60" width="130" height="36" fill="var(--muted)" opacity=".28"/>
  <text class="svg-label-s" x="506" y="54" fill="var(--muted)">dark area = shadow</text>
  <line x1="470" y1="248" x2="424" y2="214" stroke="var(--flow)" stroke-width="2.5"/>
  <polygon points="424,214 436,216 430,226" fill="var(--flow)"/>
  <text class="svg-label" x="440" y="262" fill="var(--flow)">sensor direction</text>
</svg>
```

**Key points**:
- The two halves are tied together by **one shared set of semantic colours**: the `--danger` circle in the cross-section = the `--accent` bright line in the plan view;
  the `--muted` thick line in the cross-section = the `--muted` block in the plan view. The reader joins the two halves through colour, unaided.
- The plan-view panel uses a `rect` background plus a dashed outline for "where the object really is", and solid strokes for "the signal in the data" —
  that distinction is the whole point of the figure.
- Land the caption on "these two features are what we use to confirm XXX".

---

## Pattern 4 — Displacement comparison: one object's position under two parameter values

**Use when**: you need to prove a stability argument of the form "A moves, B does not".

```html
<svg viewBox="0 0 720 220" role="img" aria-label="which one moves when the parameter changes">
  <text class="svg-title" x="10" y="20">Parameter = 20°</text>
  <line x1="10" y1="160" x2="330" y2="160" stroke="var(--line-strong)" stroke-width="2.5"/>
  <rect x="200" y="98" width="12" height="62" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.5"/>
  <rect x="200" y="90" width="60" height="10" fill="var(--surface-2)" stroke="var(--line-strong)" stroke-width="1.5"/>
  <line x1="150" y1="40" x2="200" y2="94" stroke="var(--flow)" stroke-width="1.8"/>
  <polygon points="200,94 193,88 190,97" fill="var(--flow)"/>
  <!-- the thing that moves: the projected position (dashed + grey dot) -->
  <line x1="200" y1="95" x2="178" y2="158" stroke="var(--muted)" stroke-width="1.4" stroke-dasharray="3 3"/>
  <circle cx="178" cy="160" r="5" fill="var(--muted)"/>
  <text class="svg-label-s" x="120" y="182" fill="var(--muted)">moves with the parameter</text>
  <!-- the thing that does not move: the anchor (red dot) -->
  <circle cx="200" cy="160" r="5" fill="var(--danger)"/>
  <text class="svg-label-s" x="208" y="182" fill="var(--danger)">anchor</text>
  <!-- displacement scale bar -->
  <line x1="178" y1="196" x2="200" y2="196" stroke="var(--muted)" stroke-width="2"/>
  <text class="svg-label-s" x="150" y="212">small offset</text>

  <!-- right panel: parameter = 49°; the anchor's x stays put, the grey dot slides further left, the scale bar grows -->
</svg>
```

**Key points**:
- **The anchor's x coordinate must be identical in both panels** (here 200 and 580, i.e. the same offset from each panel's origin) — that is the entire argument of the figure;
  get the coordinate wrong and the figure says the opposite of what you mean.
- The difference in scale-bar length has to be visible to the naked eye (22 px vs 54 px in this example).
- Let the caption pick up the numbers: "every recommended candidate stays within 1.8–3.6 m" — the schematic makes people understand, the numbers make them believe.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Hard-coded `#333` / `#fff` | lines or text vanish in dark mode | replace all with `var(--...)`, then flip the theme and look |
| Drawing arrows with `<marker>` | arrowheads go black or disappear in dark mode | hand-draw a `<polygon>` |
| Inline `fill` on text | colour does not follow the theme | use the `.svg-label*` classes, override only for semantic colour |
| Arrow drawn backwards | the sign of the whole conclusion flips | check every start/end point after drawing; cross-check against metadata when you have it |
| Panels not aligned | it reads as several unrelated drawings | share the y coordinates of title / baseline / explanation lines across panels |
| Pretty figure, no argument | the caption can only say "...schematic" | if you cannot write the "so what" into the caption, delete the figure |
| Plotting data as hand-drawn SVG | hand-placed coordinates disagree with the real numbers | always render data to PNG (e.g. matplotlib) and bring it in with `figure.photo` |
