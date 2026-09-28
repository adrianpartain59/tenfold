# Building a variation file

One variation = one standalone HTML file = one 393×852 iPhone screen (iPhone
15/16/17 logical size). The gallery frames it; opened alone on a phone it fills
the screen.

## The file template

```html
<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>07 · Chapters</title>
<link rel="stylesheet" href="../tokens.css">
<link rel="stylesheet" href="screen.css">
<script>
  document.documentElement.dataset.theme = new URLSearchParams(location.search).get("theme") || "light";
  if (window.top === window && matchMedia("(pointer: coarse)").matches) document.documentElement.classList.add("on-device");
</script>
<style>
  /* This variation only. Use tokens: var(--c-*), var(--space-*), var(--radius-*), .t-* classes. */
</style>
</head>
<body>
  <div class="status-bar"><b>9:41</b><i></i></div>
  <main class="scroll">
    <!-- the screen -->
  </main>
  <nav class="tabbar"><!-- the app's real tabs, current one .on --></nav>
  <div class="home-indicator"></div>
</body>
</html>
```

No tab bar on this screen (pushed screen, sheet, onboarding)? Add
`class="no-tabbar"` to `<body>` and drop the `<nav>`. For a sheet, render the
screen underneath, then `.scrim` + `.sheet`.

## Designing part of a screen (a card, a section, a header)

Show the part in its real screen, with the unchanged surroundings identical in
every frame, so the user judges it in place. Put the fixed parts in the topic:

- `TOPIC_DIR/shared.js`: fills `<div data-include="header|below|tabbar">` slots
  with the app's real header, the content under the section, and the tab bar.
- `TOPIC_DIR/shared.css`: their styles, plus the screen's ground (glow, etc.).
- `TOPIC_DIR/_template.html`: the template above, plus
  `<link rel="stylesheet" href="../shared.css">`, the three include slots around a
  `<section class="top">`, and `<script src="../shared.js"></script>` before
  `</body>`. Variations scope all their CSS under the section's class.

The "Current" frame uses the same includes, so the only difference between any
two frames is the part being designed.

## tokens.css (one per topic, shared by every round)

Exported by the adapter or `export-tokens.mjs`, or written by hand from the
app's theme. screen.css reads these names and falls back to neutral iOS values
for any that are missing, so a small hand-written file is fine:

```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  --c-background-root: #F4F2EE;  --c-surface: #FFFFFF;  --c-border: #E6E2DA;
  --c-text: #1B1A17;  --c-text-secondary: #6E6A62;  --c-text-tertiary: #A39E94;
  --c-accent: #FF5A1F;  --c-primary: #1B1A17;  --c-button-text: #FFFFFF;
  --c-metric-distance: #FF5A1F;  /* one hue per metric the app tracks */
  --space-xs: 4px; --space-sm: 8px; --space-md: 12px; --space-lg: 16px; --space-xl: 20px; --space-2xl: 24px;
  --radius-card: 14px; --radius-card-raised: 24px; --radius-sheet: 32px;
  --gap-screen-x: 16px;
}
[data-theme="dark"] { --c-background-root: #0E0E0D; --c-surface: #1A1A18; /* …every --c-* again */ }
.t-display { font-size: 34px; line-height: 40px; font-weight: 800; letter-spacing: -0.6px; }
.t-title   { font-size: 22px; line-height: 28px; font-weight: 700; }
.t-body    { font-size: 16px; line-height: 22px; }
.t-caption { font-size: 12px; line-height: 16px; font-weight: 600; }
```

Name colours by role (`--c-<role>`), not by hue, and copy the values from the
app's theme file rather than eyeballing them.

## What screen.css gives you

`.scroll` (safe-area-aware scroller), `.status-bar`, `.home-indicator`,
`.tabbar`, `.card` (the app's raised card surface), `.stack` / `.stack-lg` /
`.row` / `.between` / `.grow`, `.muted` / `.faint` / `.tnum` / `.ellipsis`,
`.section-title`, `.ic` (+ `.sm .lg .xl`, `.feather` for stroke icons), `.btn` (+ `.accent .secondary .sm
.block`), `.pill`, `.bar > i`, `.ring` (conic progress ring: set `--p`,
`--size`, `--stroke`, `--col`), `.scrim` + `.sheet`. Short aliases inside it:
`--bg --surface --text --text2 --text3 --line --accent --track --pad`.

Prefer these over hand-rolled equivalents. They exist so ten variations
written by five subagents still share one visual system.

## Fidelity rules

- **Tokens, not literals.** Colours, spacing, radii and type come from
  `tokens.css`. A literal hex is only acceptable in a wildcard that is
  deliberately proposing a new colour, and its notes say so.
- **Real icons.** `<svg class="ic"><use href="../icons.svg#<id>"/></svg>`, ids
  listed in `../icons.txt`. The sprite is the app's own icon set when the
  adapter exports one, otherwise the Feather sprite from `studio.sh icons`
  (Feather icons are strokes: add `.feather` to the `.ic` so screen.css sets
  `fill: none; stroke: currentColor`). The sprite must be a local file:
  browsers refuse `<use href>` pointing at another origin, so a CDN URL
  renders nothing. Never emoji as icons.
- **Real images.** The topic's `img/` links to the app's image assets (mascot
  poses, food renders, illustrations). Use them instead of drawing placeholders.
- **The shared fixture.** Every variation shows the same data from context.md.
  Include the long-string case somewhere visible.
- **Real copy** in the app's voice; the actual labels from the locale file when
  they exist.
- **Native, not web.** Large title or the app's header; iOS list rows; sheets
  with grabbers; segmented controls; switches that look like iOS switches. No
  hover-only affordances, no visible scrollbars, no `<select>` default styling.
- **Dark mode** works automatically if you only use tokens. Check it once.
- **Static by default.** One small interaction (tap to expand, segmented control
  switching) is fine when the interaction *is* the idea. No frameworks. Inline
  vanilla JS only.
- **Self-contained.** A variation never depends on another variation's file.

## Sizes to remember (points)

Screen 393×852 · status bar/Dynamic Island 54 · home indicator 34 · floating
tab bar ~62 + margin · screen inset 16 · tap target ≥ 44 · list row 44–56 ·
button 52 (compact 36) · input 48 · card padding 16 · section gap 20–24.

## Checking the round (bounded: one pass, one fix batch)

1. `bash <SKILL_DIR>/scripts/studio.sh check <ROUND_DIR>` — manifest + files.
2. If a browser tool is available, open the gallery URL and take one
   screenshot of the grid and one of dark mode.
3. Look for: blank frames, overflow, text under the tab bar, two variations
   that read as the same, anything on the principles failure list.
4. Fix everything found in one batch, reload once to confirm, and send.
