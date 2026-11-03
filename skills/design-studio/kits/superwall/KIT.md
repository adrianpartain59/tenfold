# Build kit: Superwall paywall editor

A mockup for a Superwall paywall is drawn only from what the Superwall
editor can author, so the approved design can be rebuilt node for node.
`kit.json` is the machine-checked part; this file is how to draw with it.
Researched 2026-11 from Superwall's docs and the editor's own tool
definitions; anything marked **[unverified]** stays out of mockups.

## The renderer

Editor paywalls are HTML/CSS shown in a web view on the device (WebKit on
iOS, Chromium on Android), not native views. The limit is what the editor
lets you **author**: its property panels, a per-element Custom CSS field
(single properties, never rules), and the `write_html` importer. So: no
stylesheets, no `@keyframes`, no `:hover`/`::before`/`::after`, no media
queries, no JavaScript, flexbox only.

## Node types (`data-sw` on every drawn element)

| `data-sw` | Editor node | Notes |
|---|---|---|
| `stack` | Stack | Flexbox; axis vertical, horizontal or **layered** (children on top of each other). Scroll: none, normal, paging, infinite. |
| `text` | Text | One style per node. Liquid allowed. A leaf: no children. |
| `image` | Image | Uploaded asset or remote URL. PNG, JPG, GIF. A leaf. |
| `svg` | SVG | Static inline SVG, stored as an asset. A leaf. |
| `icon` | Icon | 1,000+ built-in icons, weight and colour editable. A leaf. |
| `video` | Video | Always fills like `object-fit: cover`; autoplay forces muted. A leaf. |
| `lottie` | Lottie | The only way to animate on its own. Network-loaded. A leaf. |
| `carousel` | Carousel | Auto-advancing pager (a paging stack). |
| `slides` | Slides | Swipe pager with built-in dots. |
| `autoscroll` | Autoscroll | Marquee (infinite-scroll stack). |
| `indicator` | Indicator | Dots, segments, progress bar. |
| `multiple-choice` | Multiple Choice | Single/multi select from one item template. |
| `drawer` | Drawer | Bottom sheet with detents and a dimming view. |
| `navigation`, `page` | Navigation + pages | The multi-screen flow; each `step-N` and the purchase screen are pages. |
| `input`, `picker`, `slider` | Input, Picker, Slider | Rare on paywalls. |

Leaves (`text`, `image`, `svg`, `icon`, `video`, `lottie`, `input`,
`picker`) hold no children. Text over a photo is a **sibling** in a layered
stack, never a child of the image.

## Styling you can use

Radius (each corner), borders (solid, dashed), box-shadow (Effects → Shadow,
outer or inner), opacity, background colour, blur and background blur
(frosted glass), **rotate, scale, move X/Y** (Effects), overflow hidden,
aspect-ratio, position normal/relative/absolute/fixed/sticky with z-index,
min/max sizes, units px % vw vh dvh rem em, letter-spacing, line-height,
text-transform, text-shadow, text-align, underline/strikethrough. Gradients
are likely (Layer → Fill, or Custom CSS `background`) **[unverified]**: use
them only as a flat-to-flat backdrop that would still look right as a solid
colour.

**Not buildable:** CSS grid (nest stacks), `@keyframes` and animate-on-appear
(use a Lottie, GIF or video), pseudo-elements (make the tape strip, fold or
notch a real node or part of an image), CSS `background-image: url()` (use an
image node at the bottom of a layered stack), clip-path and masks (circle =
radius 50% + overflow hidden), gradient text, blend modes, filters other than
blur, line-clamp, `flex-grow` (the editor's stacks ignore it: size with px,
% or the stack's distribution).

## Text rules

- **One style per text node.** A bold word, a coloured price or a struck
  price mid-sentence becomes its own text node, and separate nodes don't
  wrap together like a paragraph. Draw emphasis as its own line or chip.
- **Fonts:** System Font by default (it differs between iOS and Android);
  any Google Font or an uploaded TTF/OTF/WOFF file per weight. Each extra
  family is a download at paywall load and falls back to the system font if
  it fails, so use at most one non-system family, for display only.
- **Prices and dates are Liquid, never typed** (`data-liquid` on the node,
  holding the expression; the fixture value is the visible text):
  - billed price `{{ products.selected.price }}` / `{{ products.primary.price }}`
  - period `{{ products.primary.period }}`, `{{ products.primary.periodly }}`
  - breakdown `{{ products.primary.monthlyPrice }}`, `weeklyPrice`, `dailyPrice`
  - trial `{{ products.primary.trialPeriodText }}`, `trialPeriodDays`, `trialPeriodPrice`
  - charge date `{{ products.primary.trialPeriodEndDate }}`; other dates with
    the `date_add` / `date_subtract` / `date` filters
- Trial wording sits behind `products.hasIntroductoryOffer` (and, where the
  project requires it, `products.selected.trialPeriodDays > 0`): every
  trial line in a mockup is something the build shows or hides with that
  condition.

## Images

- Every picture is an image node (uploaded asset). Keep a paywall under ~20
  images; video 3–10 s, 2–5 MB.
- Rotated, overlapping, layered photos are fine (rotate + absolute/layered +
  z-index). A collage of 3 tilted captures = 3 image nodes, or one exported
  image when it never changes.
- **Illustrations** (an envelope, a wax seal, laurels, doodles, a device
  frame) are one SVG or PNG each, drawn in the mockup as an `svg` or `image`
  node, never assembled from CSS shapes and pseudo-elements. Name each one in
  `notes.build` as an asset to export.
- A device frame around a capture: either one exported PNG (frame +
  capture), or a stack with radius, border and overflow hidden holding the
  capture image.

## Purchase controls (`data-action`)

| Element | `data-action` | Editor tap behaviour |
|---|---|---|
| The CTA (`data-pw="cta"`) | `purchase` | Purchase → Selected product |
| Each plan card (`data-pw="plan"`) | `select-product` | Select Product; selected styling from `products.selectedIndex` |
| A step's Continue | `navigate-page` | Navigate Page → next |
| Restore | `restore` | Restore |
| Terms / Privacy | `open-url` | Open URL |
| Close | `close` | Close |

## Recipes

- **Plan selector:** a horizontal or vertical stack of plan stacks, each
  `data-sw="stack" data-pw="plan" data-action="select-product"`; inside, text
  nodes for name, Liquid price and breakdown; a check icon whose opacity
  follows `products.selectedIndex`.
- **Trial timeline:** a vertical stack of rows; each row a horizontal stack of
  an icon (or a small stack as the node dot), a thin stack as the connector,
  and two text nodes; the charge row's date and price in Liquid.
- **Rating badge with laurels:** an image (the laurel pair as one SVG/PNG)
  in a layered stack with the number and star icons as sibling nodes.
- **Note card:** a stack (white, radius, shadow, optional rotate) holding
  text nodes; a team photo is an image node with radius + overflow; tape or
  a seal is an image placed with absolute position and rotate.
- **Review carousel:** `carousel` (auto) or `slides` (swipe) of review stacks.
- **Sticky CTA:** a stack with position sticky/fixed at the bottom.

## Building it (editor MCP)

- Delete existing nodes with `delete_nodes`, never with `write_html` mode
  "replace": replaced children disappear from the editor but Save merges them
  back from the server copy, so they ship. Verify each save by fetching the
  paywall's `paywall_url` and searching it for the removed copy.
- Rotation, absolute position and z-index from `write_html` import as native
  properties; Liquid text imports with liquid rendering.
