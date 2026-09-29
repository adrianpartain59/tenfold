# Web mode for design-studio

Status: design approved in chat 2026-09-28; built on `feat/web-mode` 2026-09-28, uncommitted.
Target release: Tenfold 1.1.0.

## Why

design-studio renders ten variations of one app screen as phone mockups. A
website redesign is a different job:

- The unit is a whole page that scrolls, not one screen. A site feels premium
  or not through section rhythm, the second and third screens, and motion,
  none of which a single frame shows.
- The site is redesigned all at once. The site is made of a few templates,
  so a direction is really a design system that has to hold up on every one
  of them.
- Directions differ on type, grid and scale. App rounds share the app's
  fixed tokens; web directions each need their own.
- It has to be viewed at desktop and phone widths, with working links
  between pages.

The loop stays the same: context sweep, ten distinct directions, gallery,
Claude's pick plus a predicted pick, TASTE.md, pick then build. Web mode
changes what gets rendered, the frame it's shown in, and how rounds are
staged.

## Constraints

- Additive. Mobile mode keeps working exactly as it does today:
  `assets/gallery.html`, `assets/screen.css`, `references/mockup-craft.md` and
  the existing `studio.sh` subcommands stay byte-identical in behaviour. Web
  mode adds new files and branches on a flag.
- One skill, one TASTE.md, one server. Web rounds are logged in the same
  taste log with a `web` marker, so marketing-surface patterns carry over.
- No new runtime dependencies: bash, python3, Chrome for images. Same as
  today.

## How a project turns web mode on

1. `surface: web` in the project's `.design-studio/adapter.md`, or
2. the brief names a website, landing page, marketing site or web page.

The adapter for a web project also gives:

- `base-tokens`: how to produce the topic's `tokens.css`, meaning brand
  colours, brand art and icons. These are fixed for every direction.
- `templates`: the site's template list, as `id | label | real URL example`.
  The system stage checks every direction against this list.
- `content`: where real copy, claims and numbers come from.
- `build`: where an approved direction gets built.

## Round stages

`manifest.stage` names the stage. Stages run in this order and the user can
stop at any point.

| Stage | What each variation is | Count | Gallery |
|---|---|---|---|
| `directions` (r1) | One full-length home page (entry page only) with its own design system | 10 by default | desktop + phone frames per card |
| `converge` (r2+) | #1 Faithful (pick + feedback applied literally) + refinements of the pick, still home only | 10, or fewer as feedback narrows | same |
| `system` | The picked direction (or 2 finalists) across every template in the adapter, linked into a working site | 1 to 2 variations × N pages | page tabs per variation |

From `converge` on, the AskUserQuestion gains `System proof #N` (go to the
system stage) alongside `Build #N`. A bare pick in `converge` means system
proof, not build: the site isn't approved until its templates are seen.
A bare pick in `system` means build.

## Files

```
~/design-studio/<project>/<topic>/
  tokens.css            base brand tokens (fixed across directions)
  img/ icons.svg        as in mobile mode
  context.md            sweep + the shared content fixture
  r1/
    index.html          copy of assets/gallery-web.html
    web.css             copy of assets/web.css (reset, container, frame helpers)
    manifest.json
    v01/
      tokens.css        this direction's system: fonts, type scale, grid, spacing, radii, surfaces
      site.css          this direction's components (nav, buttons, sections)
      chrome.js         injects the shared nav + footer into every page (system stage)
      index.html        the home page
      <template>.html   system stage only, one per adapter template
    v02/ ...
```

Every page links `../../tokens.css` (brand base), `../web.css`, then its own
`tokens.css` and `site.css`. A direction may add type, scale and surface
tokens and choose among brand colours; it may not introduce a new accent
unless the variation is tagged `wildcard`.

## Manifest additions

```json
{
  "surface": "web",
  "stage": "directions",
  "templates": [{ "id": "home", "label": "Home" }],
  "variations": [
    {
      "id": "v01",
      "name": "Sky Scroll",
      "idea": "one line",
      "file": "v01/index.html",
      "pages": [{ "template": "home", "file": "v01/index.html" }],
      "tags": ["wildcard"],
      "notes": { "Type": "...", "Build cost": "..." }
    }
  ]
}
```

`pages` is optional before the system stage (defaults to `[file]`).
`templates` is only required in the system stage.

## Gallery (`assets/gallery-web.html`)

Same header, round crumbs, feedback strip, pick/fav/wildcard chips, keyboard
nav and theme toggle as the mobile gallery.

- Card: a browser frame (a 1440 × 900 viewport scaled down, with a thin
  chrome bar showing the page's path) with a 390 × 844 phone frame
  overlapping its lower right. Thumbnails don't take input and show the top
  of the page.
- Size toggle: S / M / L scales the cards, as today.
- Focus view (click a card): one full-size, scrollable iframe with a width
  switch `Desktop 1440 · Tablet 834 · Phone 390`. The iframe is laid out at
  the true width and scaled to fit the window, so scrolling and hover work.
  Page tabs across the top when the variation has more than one page, and
  links inside the iframe work too. "Open live ↗" opens the entry page in a
  new tab as a real site.
- ←/→ and number keys step through variations; `[` and `]` step through
  pages.

## Server script (`studio.sh`)

- `new <project> <topic> --web`: same as `new`, but copies
  `gallery-web.html` and `web.css` instead of `gallery.html` and
  `screen.css`.
- `check <round-dir>`: when `manifest.surface == "web"`, the checks are:
  every `pages[].file` exists; every page links a `tokens.css`; every local
  `href` to a `.html` resolves; no lorem ipsum; unique names; in `system`,
  every `templates[].id` is covered by every variation's `pages`. Warn when
  `agentPick`/`predictedPick` are missing. Mobile checks are unchanged.
- `sheets <round-dir>`: in web mode it writes two kinds of image.
  - `heroes.png`: every variation's desktop first screen (1440 × 900) in a
    2 × 5 grid, for scanning.
  - `sheet-N.png`: five variations side by side as full-length phone pages
    (390 wide), each drawn as a stack of 844 px slices so `vh` units keep a
    real phone's viewport (one page-tall iframe stretched them; found in the
    Task 5 visual check). Page height is measured in a first headless pass: a wrapper
    page on the same origin reads each iframe's `scrollHeight` and prints it,
    and `--dump-dom` captures it. Heights are capped at 9000 px.
  - `system` stage: `pages-vNN.png`, every template of a variation at phone
    width, side by side.

## References

- `references/web.md` (new): what web mode changes in the loop. It covers
  stage rules, what the context sweep reads for a site (every template, the
  nav, the footer, the conversion path, SEO URL invariants, real
  claims and numbers), how the content fixture is written, and how the
  system stage is split across subagents: one subagent writes the
  direction's `tokens.css`, `site.css` and `chrome.js` first, then page
  subagents build on them.
- `references/web-craft.md` (new; the web counterpart of mockup-craft.md):
  it covers
  - nav and footer anatomy
  - one primary CTA per viewport
  - container widths and a 12-column grid
  - fluid type with `clamp()`
  - breakpoints at 390, 834 and 1440 with no horizontal scroll
  - section rhythm
  - real product imagery: app screens in device frames, brand art, official
    store badges
  - CSS-only motion that respects `prefers-reduced-motion`
  - fonts from Google Fonts or local files, and no JS frameworks
  - light/dark only when the brand has both
- `references/variations.md`: gets a "Web axes" section. The axes are hero
  concept, narrative order, grid/density, type personality, art direction
  (how the product and brand art appear), colour field, and motion concept.
  Every pair must still differ on two or more axes. Type or colour alone
  doesn't make a new direction.
- `references/principles.md`: gets a short web checklist block. It checks
  that the CTA is visible in the first viewport at 390 and 1440, that text is
  readable on every image, that there is no horizontal overflow at 390, and
  that proof claims come from the content fixture.

## SKILL.md

The description adds websites, landing pages and marketing sites. A new
"Web mode" section says when web mode applies, to read `references/web.md`
and `references/web-craft.md`, to use `new --web`, and that the stage table
replaces steps 3 to 8 where the two differ. The Common mistakes table gains
three web rows:

- judging a static hero
- ten directions sharing one type system
- system-stage pages that drift from the direction's `tokens.css`

## Testing

1. Mobile regression: run a mobile round on the Tempo demo topic. Mobile
   assets must match what 1.0.0 produced, and `check` output must be
   unchanged.
2. Web smoke round: a fictional site ("Tempo" marketing site), 3 directions
   at the `directions` stage, then 1 at `system` with 4 templates. Then:
   - `check` passes, and fails on a deliberately broken link and on a
     missing template
   - the gallery loads in a browser, the width switch reflows the page, page
     tabs and `[ ]` work, and links inside the iframe work
   - `sheets` produces heroes.png and full-length phone sheets, and the
     images are checked by eye
3. Phone check: the gallery at 390 wide (the focus overlay once swallowed
   touch on a phone; see TASTE log 2026-09-27).

## Delivery

Version 1.1.0 in `plugin.json`, `marketplace.json` and CHANGELOG. The
installed copy (`~/.claude/plugins/cache/tenfold/tenfold/1.0.0`) is
currently identical to the repo, so the new version only takes effect after
it is published and the plugin is updated, or after the local plugin is
pointed at this checkout. Which of the two happens is decided at release
time, not here.

## Not in scope

- Exporting a chosen direction into a production codebase automatically. The
  adapter's `build` path does that, template by template.
- Tablet-specific design passes. Tablet is a width to check, not a separate
  design.
- Animation beyond CSS: no scroll-jacking and no WebGL in web mode's
  defaults. A wildcard may break this if it says so.
