# Glow-up craft: the system a vibe-coded app never had

`principles.md` assumes the app already has a system (a spacing scale, a type
ramp, tuned neutrals, component states) and checks that each screen follows
it. A vibe-coded app has none of that, which is most of why it looks
generated. Glow-up designs the system first, as `theme.json`, and builds
every screen from it. A direction is a whole system, not a skin.

## theme.json

One file per direction, `vNN/theme.json`. The worked example is
`tests/fixtures/glowup-smoke/r1/v01/theme.json` in the Tenfold repo; copy its
shape. `glowup_check.py` runs `validate_theme` on it and fails the round on
any of these:

| Key | Holds | Rule |
|---|---|---|
| `name` | The direction's name | Required |
| `type.display`, `type.body` (`type.mono` optional) | `family` (a Google Fonts family), `weights`, optional `fallback` stack | Weights are 100 to 900 in steps of 100 |
| `type.pairing` | One line on why these faces belong together in this market | Required |
| `type.ramp` | `display h1 h2 h3 lede body small caption eyebrow`, each with `face`, `size`, `line`, `weight`, `track` (em), optional `upper` | Every ramp weight is loaded by its face |
| `color.primitives` | Named ramps of 12 steps (`"1"` to `"12"`), hex or `oklch()` | Every step parses |
| `color.light`, `color.dark` | The 15 roles: `ground surface surface-2 border text text-2 text-3 action on-action accent on-accent good warn error focus` | Each is a colour or a reference like `neutral.11` |
| `layout` | `space` (increasing), `templates` (3 or 4: `id`, `label`, `columns`, `max`, `gutter`, `margin`, `density`), `keylines` | See the system layer |
| `shape.radius` | Named radii, `full: 999` for pills | At least two distinct values below 999 |
| `elevation` | `style` (`border`, `shadow` or `layered`) and at least three named `levels` | |
| `icons` | `set`, `license`, `stroke`, `sizes` | |
| `motion` | `fast`, `base`, `slow` in ms, `easing.out`, `easing.in-out`, optional `spring` | |
| `states` | `hover`, `pressed`, `disabled` as opacities, `focus.width`, `focus.offset` | |
| `signature` | `what`, `where` (two or more of `s1` to `s4`), `never`, `uses` | See the human rules |
| `voice` | Three `adjectives`, five `strings` (`before`, `after`), `case` for `button`, `title`, `label`, a `glossary` | `before` strings exist in context.md |
| `brand` | `wordmark` and `icon` concepts | |
| `reasons` | One line per framework default the theme keeps on purpose, keyed by path | See the human rules |

Generate the direction's tokens from it, every time it changes:

```bash
python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --css --out vNN/tokens.css
```

Never hand-edit `tokens.css`. `check` fails a tokens file that doesn't match
the theme byte for byte.

## The system layer

These are the thirteen parts a vibe-coded app is missing. A direction fills
in every one; the first six live in `theme.json` and three of them are also
direction axes.

### 1. Layout system

Give the theme a spacing scale and three or four named layout templates (a
reading column, sidebar plus content, a dashboard grid, and on mobile a
margin and keyline scheme). Every screen declares exactly one template with
`data-template`, and data views run denser than reading views. The tell it
replaces: each screen with its own padding, its own max width, and headers
that don't line up with the content under them.

### 2. Brand surface

A wordmark treatment, an app icon, a favicon, a splash screen, page titles
and share images. Write the concepts in `brand` now; design them in the
`system` stage and apply them in apply stage 4. The tell: the Vite favicon,
"React App" in the tab, the default Expo icon.

### 3. Colour construction

Build ramps in OKLCH so the steps look even, tint the neutrals toward the
brand hue, and keep three tiers: primitive ramps, semantic roles, and the
component roles apply maps them to. The tell: Tailwind `gray-500` with
`indigo-600`, colours picked one at a time.

### 4. Component state matrix

Specify every interactive component in default, hover, pressed, focus,
disabled, loading, selected and error, from `states`. Loading buttons keep
their label. The tell: buttons with no pressed or disabled look, inputs with
no error state, the browser's default focus ring.

### 5. Type construction

A modular scale; tracking tighter on display sizes and looser on small text;
line height falling as size rises; a deliberate weight ladder; tabular
figures for numbers. Write the reason for the pairing. The tell: one face at
default tracking and sizes picked by feel.

### 6. Signature element

One recurring, ownable detail: a shape motif, a corner or edge treatment, an
illustration style, a texture, a type treatment. Say where it appears and
where it never does. A system that is only correct still reads as
generated; the signature is what makes it feel made by someone.

### 7. Content and voice system

A glossary of the app's terms, one capitalisation style per element type,
buttons as verbs, one step-label set per flow (for example Get Started,
Continue, Done), and errors that say what is wrong and how to fix it, with
numbers. No "Oops", no "invalid", no over-apologising. The tell: "Oops!
Something went wrong", "Submit" everywhere, mixed Title Case and sentence
case.

### 8. Loading policy

No loader under about 1 s. A loader appears after a 150 to 300 ms delay and
stays at least 300 to 500 ms. Skeletons for full-page loads, mirroring the
loaded layout exactly; a spinner for one module; a progress bar past 10 s.
The tell: a full-screen centred spinner that flashes for a split second.

### 9. Form system

Labels above fields, never placeholder-only. Optional fields marked
"(optional)", no asterisks. Inputs sized to their content. Validate on blur,
clear the error on the keystroke that fixes it, never disable submit ahead
of time, focus the first error on submit. Set `autocomplete`, `type` and
`inputmode`. Mobile inputs are 16 px or larger. The tell: red errors the
moment a field gets focus, a greyed-out submit, every input full width.

### 10. Numbers and tables

Numbers right-aligned with tabular figures, text left-aligned, headers
aligned with their data, one precision per column, the unit once, light
horizontal rules, locale-aware formatting through `Intl`, en dashes in
ranges. The tell: `$1234.5`, ISO timestamps in the UI, centred number
columns.

### 11. Feedback and haptics

Feedback as loud as the information is important: status inline, alerts
only for critical and actionable things, undo over confirm dialogs. On
native, haptics only in their documented meanings (notification, impact,
selection), short and synced to the visual. The tell: a toast on every
action, a confirm dialog for everything.

### 12. Responsive components and navigation

Components change form with the window, they don't just shrink. A bottom
bar of 3 to 5 destinations becomes a rail at medium widths (Material
breakpoints 600, 840 and 1200 dp); below 768 px dialogs become sheets, and
dialogs with inputs go full-screen. Tab bars navigate, never act, and never
hide tabs. On web, navigation is links and view state lives in the URL. The
tell: a desktop modal shrunk onto a phone, filters lost on reload.

### 13. Density

A density per layout template: data views denser than reading views (Carbon
row heights run 24, 32, 40, 48 and 64 px). The tell: one airy density for
everything, including tables.

## Construction details

- Colour ramps follow Radix's 12-step roles: steps 1 to 2 backgrounds, 3 to
  5 component states, 6 to 8 borders, 9 to 10 solid fills, 11 to 12 text.
  Borders, shadows and text on a coloured ground are tinted toward its hue;
  never grey text on colour.
- State-layer opacities from Material: hover .08, focus and pressed .10,
  disabled .38 on content and .12 on the container (`practice`, not
  re-checked against the live page).
- Shadows have at least two layers, ambient and direct, paired with a
  semi-transparent border.
- Motion tokens from Material: 50, 100 and 150 ms short, 250 and 300 ms
  medium, an emphasised decelerate curve for entering. Never
  `transition: all`; animate only transform and opacity; input can
  interrupt any animation.
- A shape scale, with Material's 0, 4, 8, 12, 16, 20, 28, 32, 48 and full as
  the reference; each direction picks a subset.
- Empty states: an optional image, a positive title naming the start, a body
  naming the next action, one call to action.
- Icons: one family, consistent size, detail, stroke and perspective; stroke
  weight matched to the adjacent text weight; filled icons in tab bars.

## The human rules

1. **Defaults need a reason.** `check` flags any value equal to a framework
   default (Tailwind's gray and indigo ramps, an untinted grey neutral ramp,
   shadcn's 0.5rem radius, Lucide at a 2px stroke, Inter as the only face)
   unless `reasons` has a line for its path. Inter can be a good choice; it
   has to be a choice.
2. **Every direction names its signature element**, and it appears on at
   least two of the four screens.
3. **Voice rewrites real strings.** The five `before` strings are lines the
   app shows today, listed in context.md under `## UI strings`.
4. **The failure lists** in principles.md and web-craft.md apply, plus the
   tells below.
5. **Zero entropy is a tell too.** The same radius and padding on every
   surface reads as generated. Give different surface roles different
   values.

Inside glow-up rounds the tells list overrides web-craft.md's allowance of
"a number counting up once": no count-up stats. Web mode is unchanged.

## The tells

First-order tells, the obvious generated look. The ids are `tells_lint.py`
rules, which `check` runs on every screen:

- Inter as the only face (`F-inter-only`)
- gradient headline text (`F-gradient-text`) and purple-to-blue gradients
  (`F-gradient-purple`)
- the same `rounded-2xl shadow-lg` card everywhere (`F-uniform-card`)
- the untouched shadcn palette (`F-shadcn-untouched`) and Tailwind's default
  hex values (`F-tailwind-hex`)
- one fade-up on every section (`F-entrance-everywhere`)
- count-up stats (`F-count-up`)
- the sparkle icon for AI (`F-sparkles`)
- an arrow welded onto every call to action (`F-arrow-cta`)

Second-order tells, the "tasteful" defaults a glow-up drifts into once it
only avoids the first list:

- a cream ground with a terracotta accent (`cream-terracotta`)
- a near-black ground with one acid accent (`black-acid`)
- all-caps mono eyebrows and chrome (`mono-chrome`)
- 01 / 02 / 03 section numbering (`S-numbered-sections`)
- fake window dots (`S-window-dots`)
- one accented word in the headline (`S-accent-word`)

A direction may use a second-order pattern only as its named signature: put
the id in `signature.uses` and say why in the direction's notes. Anything
else fails `check`.

## Layout templates on each surface

- **App surface:** put the template class on the scroller,
  `<div class="scroll tpl-column">`. The template's margin is the screen
  inset, so it replaces screen.css's padding rather than adding to it.
- **Web surface:** put the template class on `<main>`. The template's `max`
  and `gutter` are the container and gutter, and full-bleed bands sit
  outside it.

`tokens.css` defines `.tpl-<id>` for every template, plus `.span-all` for a
child that spans the grid and `.tnum` for tabular figures.

## Screens

Each `vNN/s1.html` to `s4.html`:

- links `../screen.css` (app) or `../web.css` (web), then `tokens.css`
- puts `data-template="<template id>"` on `<body>`, naming a template from
  the theme
- marks the signature element with `data-signature` on every screen listed
  in `signature.where`
- uses only tokens: no hex, `rgb()`, `hsl()` or `oklch()` literals
- shows the shared fixture from context.md, including the long string
- keeps the content contract: it may regroup or reorder, never drop a datum
  or an action
- writes copy in the direction's voice, with typographic quotes and `…`

The mockup rules in `mockup-craft.md` (app) or `web-craft.md` (web) hold
too: real icons from the topic's sprite, real images, native patterns.

## Pre-send checklist

1. `theme_tokens.py --css` ran after the last edit to `theme.json`.
2. Every screen declares a template from the theme.
3. The signature shows on the screens in `signature.where`.
4. The voice strings are real lines from context.md.
5. Every framework default the theme keeps has a line in `reasons`.
6. No second-order pattern unless its id is in `signature.uses`.
7. It differs from every other direction on at least two axes; type or
   colour alone doesn't count.
8. Contrast passes in light and dark (`check` tests the main pairs).
9. The principles.md checklist passes: the mobile items for an app, the web
   items for a website.

## Sources

Gathered by a research pass on 2026-09-30. Rules marked `practice` are
widely held but not taken from a fetched page.

- Apple Human Interface Guidelines: writing, feedback, playing haptics,
  launching, onboarding, privacy, tab bars, accessibility, icons, dark mode.
- Material 3: applying layout, navigation bar, density, states, motion
  tokens, corner radius scale.
- Radix Colors: understanding the scale.
- Shopify Polaris: error messages, localized currency formatting.
- GitHub Primer: dialog guidelines.
- IBM Carbon: data table style, empty states pattern.
- GOV.UK Design System: text input, question pages.
- Vercel design guidelines.
- Nielsen Norman Group: skeleton screens, response time limits, form
  placeholders. Baymard Institute: inline form validation.
- WCAG 2.2.
- Refactoring UI (Wathan, Schoger).
- On AI-design tells: github.com/funboy322/avoid-ai-design and
  925studios.co/blog/ai-slop-web-design-guide (practitioner sources, used
  for the tells list only).
