# Glow-up mode for design-studio

Status: design approved in chat 2026-09-30, not built.
Target release: Tenfold 1.3.0.

## Why

App, web and paywall modes design one surface inside an app that already
has a design system. They export its tokens, match its neighbouring
screens, and check every variation against a spacing scale, a type ramp
and colour roles that someone already chose. Congruent is the default
mode, and the neighbours are the authority.

A vibe-coded app (Lovable, v0, Bolt, Replit, Cursor output, or an Expo
app built the same way) inverts that premise:

- The existing look is the thing being replaced. Matching the neighbours
  reproduces it.
- There is no system to inherit. `principles.md` says "use the spacing
  scale" and "use the app's type ramp"; a vibe-coded app has neither, so
  the rules have nothing to hold on to. The scale, ramp, neutrals, layout
  templates and component states have to be designed.
- The job is the whole app, not one screen. A theme only proves itself
  across several screens at once.
- "Professional" depends on the market. A legal tool, a kids' app and a
  fitness app earn trust with different type, colour and density. Nothing
  in the loop looks at the category.
- People who vibe-code can't apply a design by hand. Mockups without a
  codebase change are a moodboard.

Glow-up keeps the loop (ten distinct variations, the gallery, Claude's pick
plus a predicted pick, TASTE.md, pick then build) and adds what the job
needs: intake, an audit with a measured baseline, category research, a
theme system per direction, a whole-app proof, and a staged apply to the
codebase.

## Constraints

- Additive. App, web and paywall modes keep working exactly as they do
  today; their references, assets and `studio.sh` subcommands keep their
  current behaviour. Glow-up adds new files and branches on a flag.
- Glow-up is a job, not a surface. It composes with the existing frames:
  a mobile app's directions render in the phone frames from
  `mockup-craft.md` + `screen.css`; a web app's in the desktop and phone
  frames from `web-craft.md` + `web.css`. No frame code is forked.
- v1 covers web (React, Next, Vite; Tailwind and shadcn when present) and
  mobile (React Native and Expo; NativeWind or StyleSheet).
- One skill, one TASTE.md, one server. Glow-up rounds are logged in the
  same taste log with `glowup` in the Project / topic column.
- No new runtime dependencies for the gallery and checks (bash, python3,
  Chrome for images). The apply stage uses the target project's own
  toolchain (its package manager, build, typecheck, lint).
- A theme may change look, voice and layout within a screen (hierarchy,
  grouping, empty, loading and error states). It may not change
  navigation, information architecture, features or data.

## How a project turns glow-up on

1. `mode: glowup` in the adapter, or
2. the brief says glow-up, makeover, "make it look professional", "it looks
   vibe-coded / AI-made", "give it a real design", "rebrand the app", or
   asks for themes for a whole app.

`studio.sh new <project> <topic> --glowup` starts the topic. The surface
(`app` or `web`) is detected at intake from `package.json` and written to
the manifest; `--web` forces web.

## Stages

`manifest.stage` names the stage.

| Stage | What happens | User sees | Ends when |
|---|---|---|---|
| `intake` | Read the code, UI copy, README and live URL. Write `brief.md` | One confirm-or-correct question | Brief confirmed |
| `audit` | Screenshot every route; run `entropy.py`; score routes against `principles.md` and the tells; pick the four key screens | `r0` board, Before tab | Automatic |
| `research` | 8 to 12 comparables; write `category.md` | `r0` board, Category tab | Automatic |
| `directions` (r1) | Ten themes, each on the same four key screens | Theme board | A pick |
| `converge` (r2+) | #1 Faithful + refinements on the four screens | Theme board | A bare pick, or `System proof #N` |
| `system` | The pick across every route, light and dark, with empty, loading and error states | Full-app board | `Apply #N` |
| `apply` | Staged commits on `glowup/<topic>` in the user's repo | `apply-1`, `apply-2`… before/after boards | Each stage approved or a route flagged |

Intake and audit run in one turn so the first thing the user sees is the
brief question. Research and r1 run back to back after it; the gallery
opens with Before, Category and Directions together.

A bare pick in `directions` or `converge` goes to `system`, not to apply.
The theme isn't approved until it's been seen on every route.

## Intake

- Stack: `package.json` decides web (next, vite, react-router, tailwind,
  shadcn's `components.json`) or mobile (expo, react-native, nativewind).
- Routes: Next `app/` or `pages/`, react-router definitions, expo-router's
  `app/`, or the navigator files. This list is the route inventory every
  later stage uses.
- `brief.md`: what it sells, who buys, price tier, category, five to eight
  comparable apps, and the one action the app exists to drive.
- The confirm question: "Brief is right (Recommended)", "Category is
  wrong", "Buyer is wrong". Typed corrections go into `brief.md`
  verbatim.

## Audit

- Before screenshots of every route. Web: headless Chrome at 390 and 1440.
  Mobile: the booted simulator; else Expo web when the project supports
  react-native-web; else HTML recreations from the code, labelled as such.
- `entropy.py` counts the distinct values the codebase uses: colours (hex,
  rgb, hsl, oklch, Tailwind colour classes, RN literals), font sizes,
  font weights, spacing values, radii, shadows. Output is
  `TOPIC_DIR/entropy.json` and a one-line headline ("31 colours · 14 font
  sizes · 22 paddings · 7 radii · 9 shadows"). The same script runs after
  every apply stage.
- Each route gets a score against `principles.md` and the tells in
  `glowup-craft.md`, and a list of what fails.
- Key screens: four, chosen by traffic and variety. The main screen
  (dashboard or home), the densest list or table, the main form, and the
  weakest empty or onboarding state. Written into `context.md`; fixed for
  the whole topic.
- The content contract per route (every datum, action and state) goes into
  `context.md`. A direction may regroup or reorder it, never drop it.

## Category research

`references/category-research.md` runs it.

- Comparables come from `brief.md`. Web: their home page and public product
  screenshots through a browser tool. Mobile: App Store screenshots from the
  public iTunes Search API (`screenshotUrls`).
- Per comparable, `category.md` records type, colour field, neutral
  temperature, shape, density, tone and signature element, with the source.
- It ends with two lists: **table stakes** (what signals trust in this
  category) and **white space** (what nobody in the category is doing).
- Comparable screenshots stay in `TOPIC_DIR/category/` as reference only.
  No direction reuses a competitor's logo, palette or signature element.

## What one direction contains

A folder `vNN/`:

| File | What it is |
|---|---|
| `theme.json` | The direction's system, platform-neutral (schema below) |
| `tokens.css` | Generated from `theme.json` by `theme_tokens.py --css` |
| `s1.html` … `s4.html` | The four key screens on `tokens.css` + the surface's frame CSS |

`theme.json` holds:

- `type`: display and body faces (Google Fonts, which map to
  `@expo-google-fonts` for native), the scale, and per-size tracking and
  line height, the weight ladder, the pairing reason.
- `color`: primitive ramps (built in OKLCH), semantic roles, component
  roles; light and dark. Brand, one accent, a tinted neutral ramp, status.
- `layout`: the spacing scale, three or four named layout templates, and
  keylines (see the system layer).
- `shape`: radius scale and the nested-radius rule.
- `elevation`: named depth levels and the border-or-shadow choice.
- `icons`: an open-licensed set, size grid, stroke weight.
- `motion`: duration and easing tokens, springs for native.
- `states`: how every component shows hover, pressed, focus, disabled,
  loading, selected and error.
- `signature`: the one ownable recurring detail, where it appears, where it
  never appears.
- `voice`: three adjectives and five real strings from the app rewritten.
- `brand`: wordmark treatment and app icon / favicon concept.
- `reasons`: one line for every value that equals a framework default.

The manifest note for each direction carries its thesis, its "why it fits
this market" (citing a line in `category.md`), what it takes from category
convention, what it does differently, and its ripple in plain words.

## The system layer

`references/glowup-craft.md` teaches how to build each part. These are the
parts a vibe-coded app never has, and they're what principles.md assumes.

1. **Layout system.** A spacing scale; three or four named layout templates
   (for example a single reading column, sidebar + content, a dashboard
   grid, and on mobile a margin + keyline scheme); every screen declares
   one template. On web, the container and column grid from web-craft.md
   become per-direction values.
2. **Brand surface.** Wordmark, app icon, favicon, splash screen, page
   titles, share (OG) images. Designed in `system`, applied in apply
   stage 4.
3. **Colour construction.** Ramps built in OKLCH so steps look even;
   neutrals tinted toward the brand hue; three token tiers (primitive,
   semantic, component) so apply can map them to Tailwind, shadcn variables
   or a `theme.ts`.
4. **Component state matrix.** Every shared component specified in all its
   states, shown on the spec card.
5. **Type construction.** A modular scale; tracking tighter on display and
   looser on small text; line height falling as size rises; a deliberate
   weight ladder; tabular figures for numbers.
6. **Signature element.** One recurring, ownable detail. A system that is
   only correct still reads as generated.
7. **Content and voice system.** A glossary of the app's terms, one
   capitalisation style per element type, buttons as verbs, one step-label
   set per flow (for example Get Started / Continue / Done), errors that
   say what is wrong and how to fix it, with numbers. No "Oops", no
   "invalid", no over-apologising.
8. **Loading policy.** No loader under about 1 s. A loader appears after a
   150 to 300 ms delay and stays at least 300 to 500 ms. Skeletons for
   full-page loads, mirroring the loaded layout exactly; a spinner for one
   module; a progress bar past 10 s. Loading buttons keep their label.
9. **Form system.** Labels above fields, never placeholder-only. Optional
   fields marked "(optional)", no asterisks. Inputs sized to their content.
   Validate on blur, clear on the fixing keystroke, never disable submit
   pre-emptively, focus the first error. `autocomplete`, `type` and
   `inputmode` set. Mobile inputs 16 px or larger.
10. **Numbers and tables.** Numbers right-aligned with tabular figures, text
    left-aligned, headers aligned with their data, one precision per column,
    the unit once, light horizontal rules, locale-aware formatting through
    `Intl`, en dashes in ranges.
11. **Feedback hierarchy and haptics.** Feedback as loud as the information
    is important: status inline, alerts only for critical and actionable
    things, undo over confirm dialogs. On native, haptics only in their
    documented meanings (notification, impact, selection), short and synced
    to the visual.
12. **Responsive components and navigation.** Components change form with
    the window, not just shrink: a bottom bar of 3 to 5 destinations becomes
    a rail at medium widths (Material breakpoints 600 / 840 / 1200 dp);
    below 768 px dialogs become sheets, and dialogs with inputs go
    full-screen. Tab bars navigate, never act, and never hide tabs. On web,
    navigation is links and view state lives in the URL.
13. **Density.** A density setting per layout template: data views run
    denser than reading views (Carbon row heights 24 / 32 / 40 / 48 / 64 px).

Construction details `glowup-craft.md` carries from the research:

- Colour ramps follow Radix's 12-step roles: steps 1 to 2 backgrounds, 3 to
  5 component states, 6 to 8 borders, 9 to 10 solid fills, 11 to 12 text.
  Borders, shadows and text on a coloured ground are tinted toward its hue;
  never grey text on colour.
- State-layer opacities from Material (hover .08, focus and pressed .10,
  disabled .38 content / .12 container), marked `practice` until re-checked
  against the live page.
- Shadows have at least two layers (ambient + direct), paired with a
  semi-transparent border.
- Motion tokens from Material (50 / 100 / 150 ms short, 250 / 300 ms medium;
  emphasised-decelerate entering). Never `transition: all`; animate only
  transform and opacity; input can interrupt any animation.
- A shape scale (Material's 0 / 4 / 8 / 12 / 16 / 20 / 28 / 32 / 48 / full
  as the reference), from which each direction picks a subset.
- Empty states: an optional image, a positive title naming the start, a
  body naming the next action, one call to action.
- Icons: one family, consistent size, detail, stroke and perspective; stroke
  weight matched to adjacent text weight; filled icons in tab bars.

Layout system, type construction and signature element are also direction
axes (below). Items 7 to 13 are shared rules every direction follows, not
axes; each direction's `theme.json` fills in its values (its glossary,
density per template, motion tokens).

## The human rules

1. **Defaults need a reason.** `glowup_check.py` flags any token equal to a
   framework default (Tailwind's gray and indigo ramps, shadcn's slate base
   and 0.5rem radius, Lucide at a 2px stroke, system Inter at default
   tracking) unless `theme.json.reasons` gives one line for it.
2. **Every direction names its signature element**, and it appears on at
   least two of the four screens.
3. **Voice rewrites real strings.** The five voice strings are lines that
   exist in the app today, rewritten.
4. **The failure lists** in principles.md and web-craft.md apply, plus the
   tells list in glowup-craft.md, which has two tiers:
   - First-order tells: Inter as the only face, gradient headline text
     (`bg-clip-text`), the same `rounded-2xl shadow-lg` on everything, the
     untouched shadcn palette, one fade-up on every section, count-up
     stats, the sparkle icon for AI, arrows welded onto every CTA.
   - Second-order "tasteful" tells, the ones a glow-up drifts into when
     it only avoids the first tier: cream + terracotta, near-black + one
     acid accent, all-caps mono chrome, 01 / 02 / 03 section numbering,
     fake window dots, one accented word in the headline.
   A direction may use a second-order pattern only as its named signature
   element, with the reason in its notes.
5. **Zero entropy is a tell too.** The same radius and padding on every
   surface (the untouched shadcn Card) reads as generated. A direction's
   layout templates and shape scale must give different surface roles
   different values.

Glow-up's tells list overrides web-craft.md's allowance of "a number
counting up once" inside glow-up rounds only; web mode is unchanged.

## Direction axes

Every pair differs on at least two axes. Type or colour alone doesn't count.

| Axis | Positions (examples) |
|---|---|
| Category stance | conventional · conventional with a twist · category-breaking |
| Personality | clinical · warm · editorial · playful · technical · premium |
| Layout system | airy editorial column · balanced cards · dense pro grid · split panes |
| Type personality | geometric grotesk · humanist sans · serif display + sans · condensed display · rounded |
| Colour field | light warm · light cool · dark · brand-tinted ground |
| Shape | sharp · soft · pill · mixed by role |
| Depth | flat with borders · soft shadow · layered surfaces |
| Signature | a shape motif · a corner or edge treatment · an illustration style · a texture · a type treatment |
| Voice | plain · warm coach · expert · playful |

Round 1 mix of ten: three conventional done well, five in-category with a
distinctive twist, two labelled wildcards that break the category.

## The theme board

`assets/gallery-glowup.html`:

- Tabs: Before · Category · Directions (then System and Apply boards in
  later rounds).
- Directions: rows are directions, columns are the four key screens,
  the Before row pinned on top, a light/dark switch.
- Clicking a row opens its spec card: type specimen, swatches with
  contrast, layout templates drawn as wireframes, the state matrix for
  button and input, icon sample, the signature element, voice strings, and
  the market note.
- The Before tab shows the audit scores and the entropy headline. Apply
  boards show before/after per route and the entropy delta.

## Apply

On `Apply #N`. Runs in the user's app repo, on a new branch
`glowup/<topic>` cut from their current branch, never on main. Refuses to
start with uncommitted changes in the paths it will touch.

| Stage | Commit |
|---|---|
| 1. Theme layer | `theme_tokens.py` writes the stack's native form. Web: Tailwind config or v4 `@theme`, shadcn variables in `globals.css`, fonts through `next/font` or `@fontsource`. Mobile: `theme.ts`, the NativeWind config when present, `@expo-google-fonts` |
| 2. Shared components | `components/ui/*` (shadcn) or the RN shared components restyled, with the full state matrix |
| 3. Routes, about five per commit | Literals swapped for tokens, each screen on its layout template, layout polish within the content contract, copy in the new voice |
| 4. Brand surface | App icon, favicon, splash, page titles, OG images |

Hard limits: no changes to data fetching, state, routing, API calls or test
IDs. The diff touches styles, render markup, copy strings and assets.

After every stage: the project's own build, typecheck and lint when they
exist; screenshots of the touched routes; `entropy.py` again. A stage that
fails its build is fixed before the board goes out, or reverted, and the
board says which. `references/apply-web.md` and `references/apply-native.md`
hold the stack-specific playbooks (where tokens live, how shadcn and
NativeWind consume them, how fonts load, how to find literals).

## From screenshots (`source: images`)

Added 2026-09-30 after the first build. Glow-up also runs from screenshots
alone, with no codebase. The directions are rebuilt from a content
contract and a fixture anyway, and Claude reads both from a screenshot
about as reliably as from source, so the core of the loop is unchanged.
What changes is at the two ends.

| Stage | From screenshots |
|---|---|
| Intake | Product, buyer and category read from the screens; surface from the aspect ratio (portrait phone means app, wide means web), confirmed in the brief question. Ask for three or four screenshots; accept one with a warning |
| Audit | `image_audit.py` measures the colours the screenshots really use (a stdlib PNG decoder, clustering in OKLab, Tailwind-default matches, neutral temperature). The visible tells are judged by eye against the tells list and written into context.md. Spacing and type counts and the code-only tells drop out |
| Key screens | The uploaded screens, in order. When fewer than four are uploaded, the rest are designed fresh and marked `"invented": true` in `manifest.screens`; the gallery labels them |
| Research, directions, converge | Unchanged |
| System | The uploaded screens plus their designed empty, loading and error states. `routes` lists them |
| Apply | Not available. `check` fails an apply round on an image-sourced topic |
| Handoff (new final stage) | `handoff.py` writes the picked theme in every token format plus `prompt.md`, a paste-ready brief for an AI builder (Lovable, v0, Bolt, Cursor). The agent adds `screens.md`, one section per screen. `check` verifies the files, that the tokens aren't stale, and that every uploaded screen has a section |

The topic records `"source": "images"` in every manifest. The handoff stage
also exists for code topics where the user wants the tokens without a
branch.

## Tooling

| Script | Does |
|---|---|
| `scripts/entropy.py <repo> [--out file]` | Counts distinct colours, sizes, weights, spacing, radii, shadows in web and RN source |
| `scripts/theme_tokens.py <theme.json> --css \| --tailwind \| --shadcn \| --rn` | One theme, every output format |
| `scripts/glowup_check.py <ROUND_DIR>` | Directions: valid `theme.json`, four screens, signature on two screens, voice strings, market note, defaults-need-a-reason, tokens not literals, each screen declares a layout template. Apply: entropy fell, no literal colours outside the theme files |
| `scripts/tells_lint.py <repo> [--out file]` | Scans app source for the five lint families below. Runs in the audit (its count joins the Before headline) and after every apply stage |

`tells_lint.py` families, all static checks over web and RN source:

1. **Default fingerprint:** untouched shadcn variables, Inter as the only
   face, `from-purple|indigo-* to-blue-*`, `bg-clip-text text-transparent`,
   the share of `rounded-2xl shadow-lg`, the `Sparkles` icon, the same
   entrance animation on every section, the second-order palettes.
2. **Forms:** inputs with no label, `disabled={!isValid}` on submit,
   asterisk markers, missing `autocomplete` / `type` / `inputMode`, input
   font size under 16 px, validation on `onChange` before the field is
   touched.
3. **Copy and numbers** over JSX strings: "Oops", "Something went wrong",
   "Submit", "Click here", "...", straight quotes, mixed capitalisation
   within one element type, `toFixed` / `toLocaleString()` without explicit
   options, ISO dates rendered as text, numeric text without `tabular-nums`.
4. **Accessibility and interaction:** `outline-none` with no `focus-visible`
   replacement, `user-scalable=no` / `maximum-scale=1`, `<div onClick>`,
   icon-only buttons with no `aria-label`, `transition-all`, no
   reduced-motion handling.
5. **Loading and first run:** a full-screen spinner as a page state,
   loaders with no show-delay, permission requests at the app root or on
   mount, a launch screen containing a logo or text.

Findings inside apply's allowed diff (markup, styles, copy, assets: labels,
`aria-label`, focus rings, `tabular-nums`, input types, punctuation, copy)
are fixed in apply stage 3. Findings that would change behaviour
(validation timing, loader delays, permission timing) are listed on the
final apply board as recommended follow-ups, not changed.

Rendered hit-target size (under 24 px on web, 44 pt on mobile) and skeleton
mismatch need screenshots, so they run in `glowup_check.py` against the
apply boards rather than in the static lint.

`studio.sh check` and `sheets` detect `"mode": "glowup"` and route to these.

## Pick question

- `directions` / `converge`: the usual four options; option 3 becomes
  `System proof #N` from `converge` on.
- `system`: `Apply #N (Recommended)`, a converge option, and a mix.
- `apply` boards: "Approve stage (Recommended)", "Flag a route" (typed
  route names and what's wrong), "Revert stage".
- `predictedPick` reads the `glowup` rows in TASTE.md when there are any;
  with none, it says the prediction is from the brief alone.

## Testing

- `tests/fixtures/glowup-web/`: a small Vite + Tailwind + shadcn app with
  deliberate entropy (scattered hex values, mixed paddings, default slate).
- `tests/fixtures/glowup-native/`: a small Expo app with StyleSheet
  literals.
- `tests/studio.test.sh` runs `entropy.py` (expected counts),
  `tells_lint.py` (expected findings per family, including a zero-entropy
  case),
  `theme_tokens.py` (every format, golden files), and `glowup_check.py`
  (a passing round and a failing one) against both.
- `refs_lint.py` covers the new reference files.
- Existing mode tests stay unchanged and pass.

## Build order

1. `glowup-craft.md` (system layer, human rules, tells), `category-research.md`.
2. `entropy.py`, `theme_tokens.py` and `tells_lint.py`, with fixtures and
   tests.
3. `glowup.md` (the loop), `gallery-glowup.html`, `glowup_check.py`,
   `studio.sh new --glowup` and the check/sheets routing.
4. `apply-web.md`, `apply-native.md`.
5. SKILL.md: a "Glow-up mode" section, description trigger words, common
   mistakes rows. `variations.md`: glow-up axes. CHANGELOG, plugin.json 1.3.0.
6. A hand run on three public vibe-coded repos (two web, one Expo),
   recording entropy before/after, tokens used, and wall-clock time.

## Out of scope

- Navigation, information architecture, new features or new screens.
- Logo design beyond a wordmark treatment.
- Generated illustration or photography; art comes from open-licensed sets
  or the app's own assets.
- Flutter, SwiftUI, Vue, Svelte.
- Right-to-left readiness (logical properties, mirrored icons). Worth a lint
  family later; not a v1 glow-up concern.
- Changing behaviour the tells lint finds (validation timing, loader delays,
  permission timing). Reported as follow-ups only.
- The hosted SaaS (repo connection, cloud sandboxes, hosted galleries,
  billing). It gets its own spec; this mode is its engine.

## Sources

Gathered by a research pass on 2026-09-30. Rules marked `practice` in the
references are widely held but not taken from a fetched page.

- Apple HIG: writing, feedback, playing haptics, launching, onboarding,
  privacy, tab bars, accessibility, icons, dark mode, right to left.
- Material 3: applying layout, navigation bar, density, states, motion
  tokens, corner radius scale.
- Radix Colors: understanding the scale.
- Shopify Polaris: error messages (from search snippets; the page did not
  load), localized currency formatting.
- GitHub Primer: dialog guidelines.
- IBM Carbon: data table style, empty states pattern.
- GOV.UK Design System: text input, question pages.
- Vercel design guidelines.
- Nielsen Norman Group: skeleton screens, response time limits, form
  placeholders. Baymard: inline form validation.
- WCAG 2.2.
- Refactoring UI (Wathan, Schoger).
- On AI-design tells: github.com/funboy322/avoid-ai-design and
  925studios.co/blog/ai-slop-web-design-guide (practitioner sources, used
  for the tells list only).
