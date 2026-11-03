# Building a paywall frame

Paywall frames are phone screens: everything in `mockup-craft.md` holds (the
file template, tokens, icons, images, fixture data). This file adds the
paywall layer, the markers `check` reads, and the states every variation
carries.

## Round layout

```
ROUND_DIR/
  index.html      the paywall gallery (state switch)
  screen.css      phone base
  paywall.css     pricing modules, plan pickers, timeline, proof, legal
  manifest.json
  v01/step-1.html  v01/step-2.html  v01/main.html  v01/alt-plan.html  v01/exit.html  …
```

`step-N` files are the screens before the purchase screen, in the order
`manifest.flow` (or the variation's own `flow`) lists them. `main` is always
the last screen of a flow.

A frame sits one folder deeper than a mobile frame, so its links are:

```html
<link rel="stylesheet" href="../../tokens.css">
<link rel="stylesheet" href="../screen.css">
<link rel="stylesheet" href="../paywall.css">
```

Icons are `../../icons.svg`, images `../../img/`.

## Required elements

Mark each element with `data-pw`. `check` fails a frame that lacks one.
Several markers may share an element (`data-pw="renewal trial-terms"`).

| Marker | What it holds | Rule |
|---|---|---|
| `billed-price` | The amount charged per period ("$39.99 per year") | The most prominent price on the frame. Per-week or per-month breakdowns are smaller and sit below or beside it. |
| `renewal` | Auto-renewal terms | Within one screen height of the CTA, at least 12pt, 4.5:1 contrast |
| `trial-terms` | Trial length, what is charged, when | Required when `manifest.trial` is true; beside the CTA |
| `cta` | The primary purchase button | Exactly one per frame |
| `restore` | Restore purchases | |
| `terms`, `privacy` | Links | |
| `proof` | Any rating, count, quote or claim, with `data-src="P#"` | The text must appear in context.md's `## Proof` entry P# |
| `visual` | The screen's hero visual: device or product shot, illustration, photo, chart, the note card, the timeline graphic | Every screen, steps included. Several elements may carry it; their union is what `check` measures |
| `plan` | Each plan card or the plan list | Its words don't count against the word budget |
| `legal` | The footer block (Apple row, fine print, links, utility row) | Its words don't count against the word budget |
| `note` | The body of a letter or note card | Counted on its own budget (60 words) |

Step frames (`step-N`) are exempt from everything except `proof`.

On a state whose offer has no trial, mark the line that says what is billed
today (for example "Billed today, no free trial") with `trial-terms`. Never
add trial copy to a screen that has no trial.

## Visual first

A paywall is a picture with a price under it, not a page of copy. Users give
a paywall a couple of seconds; they read the hero, the price and the button.
`studio.sh check` loads every screen in headless Chrome and measures the first
393×852 viewport:

| Screen | Visual share (min) | Words outside price, plans, CTA, legal (max) |
|---|---|---|
| `step-N` | 40% | 30 |
| `main`, `alt-plan`, `exit`, … | 25% | 40 |
| a `note` letter | counts as visual when it is a card object | 60 words in the letter body |

How to stay inside them:

- **The top 40–55% of a step screen is the visual.** A real product capture in a
  device frame, a big brand object, a photo, an illustration, a chart drawn
  with real-looking data, or a styled object (a ticket, a letter, a calendar).
  A grey box with text in it is not a visual.
- **Headline 3–7 words, at most one support line.** Benefits are 3 icon rows of
  2–5 words each, never sentences. Proof is a rating badge or one short quote
  (cut to a contiguous piece), not a wall of paragraphs.
- **Split, don't cram.** When a concept needs a timeline AND reviews AND a
  feature list, each goes on its own screen of the flow. The purchase screen
  holds the visual, the plans and the button.
- Text inside a picture (labels on a chart, values on an app capture) is part
  of the visual: give the visual element `data-pw="visual"` and those words
  still count, so keep in-visual text sparse too.

## Flows

The best-converting paywalls are multi-screen (playbook section 10, lever 1).
In paywall mode a variation is a flow by default: 2 to 4 screens, the last
one `main` (the purchase screen). Each step screen does one job and ends in
one full-width Continue button (not a purchase: steps carry no `cta` marker,
no price and no trial claim that the purchase screen would have to correct).
Common jobs, in the order apps run them (`paywall-techniques.md` has the
real-app examples):

1. **Hook:** the product or outcome as a big visual, one headline.
2. **How the trial works:** an illustrated timeline (today, mid-trial, charge
   date) when there is a trial. Only promise a reminder that really fires.
3. **Proof:** a rating badge with laurels, or one or two short real reviews.
4. **Personal:** a letter or note from the team, or a summary of the user's
   own answers when those really reach the paywall.
5. **Plans:** the purchase screen.

A step screen that mentions a trial gives its length and the price after it,
in the same element, at the same size (a later screen may not correct an
earlier one's impression). Show progress dots on step screens when the
flow has 3 or more screens. The `current` frame in the manifest can carry a
`flow` too, so today's flow sits beside the new ones.

## States

`manifest.states` lists the states this round covers. Every variation
provides every one.

- `main`: the paywall as first shown, the default plan selected.
- `alt-plan`: the other plan selected. Only plan-dependent parts change
  (price, trial terms, CTA copy, badge); nothing else moves.
- `exit`, `friend`, `promo`, `winback`: as the adapter's `offer` describes.
  Same design language as `main`; what changes is the offer.
- `step-N`: pre-paywall steps, only when the concept needs them.

Every variation uses the same fixture prices and proof.

## Pricing modules in paywall.css

| Class | Use |
|---|---|
| `.pw`, `.pw-body`, `.pw-bottom` | Frame ground, the column, a bottom-pinned CTA block |
| `.pw-close` | The dismiss button |
| `.pw-headline`, `.pw-sub` | The outcome headline and its support line |
| `.pw-quote` (+ `cite`), `.pw-rating` | Proof |
| `.pw-check` | Feature checklist |
| `.pw-plans`, `.pw-plan`, `.pw-plan.is-on`, `.pw-badge` | Plan cards and selection |
| `.pw-price`, `.pw-per` | Billed price and its breakdown |
| `.pw-trial`, `.pw-timeline` | Trial line and trial timeline (`li` holds a `.dot` and a `.line` node; no pseudo-elements) |
| `.pw-cta`, `.pw-secondary` | Primary and secondary actions |
| `.pw-fine`, `.pw-legal` | Renewal text and Restore · Terms · Privacy |
| `.pw-table` | Free vs Pro comparison |

A variation's own `<style>` may extend these. It never edits paywall.css.
paywall.css never paints the page ground; set it in the variation or the
project's paywall CSS. When the project has its own paywall stylesheet, link
it after paywall.css so its classes win where names overlap (`.pw`,
`.pw-plan`, `.pw-badge`).

## Build target (kits)

Designs that render in a browser but can't be rebuilt in the paywall tool
are wasted rounds. When the adapter's `buildable` names a kit (or the
manifest has `"kit": "<name>"`), every frame is drawn only from that kit,
`kits/<name>/KIT.md` is required reading before rendering, and `check`
enforces `kits/<name>/kit.json` in its Chrome pass:

- every drawn element carries `data-sw="<node type>"` from the kit (frame
  chrome such as the status bar is exempt), and nothing sits inside a leaf;
- no computed style the kit can't author (grid, keyframe animation,
  pseudo-element content, CSS background images, masks, …);
- prices and dates are bound, not typed: a text node showing one carries
  `data-liquid="{{ … }}"` with the expression the build will use;
- every purchase control carries the kit's `data-action` (purchase,
  select-product, navigate-page, restore).

Illustrations (an envelope, laurels, a seal, a device frame) are one image
or svg node each, listed in `notes.build` as assets to export; never CSS
shapes and pseudo-elements. Tenfold ships `kits/superwall/`. A project on
another tool adds its own kit with the same two files.

## Buildability

The adapter's `buildable` list names what the build target supports (a
paywall editor's elements, or the app's components). A normal variation uses
only those. A variation that needs anything else is tagged `new-primitive`
and says what in `notes.build`.

## Pre-send checklist (with principles.md)

- [ ] The playbook's rubric (section 11) is run; any "no" is a deliberate choice named in `notes.changes`.
- [ ] The billed price is the most prominent price in every state.
- [ ] `alt-plan` changes only plan-dependent parts.
- [ ] The longest real testimonial in the fixture renders without breaking the layout.
- [ ] The first viewport holds headline, value or proof, price and CTA.
- [ ] Every screen has a `visual`, and `studio.sh check` passes the visual share and word budgets.
- [ ] Each step screen does one job; no step promises what the purchase screen doesn't show.
- [ ] The close button is visible, or the variation is flagged per playbook section 8.
- [ ] Every rating, count and quote has a `data-src` from the proof list.
