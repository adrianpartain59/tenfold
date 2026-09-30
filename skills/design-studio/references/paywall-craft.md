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
  v01/main.html  v01/alt-plan.html  v01/exit.html  …
```

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

Step frames (`step-N`) are exempt from everything except `proof`.

On a state whose offer has no trial, mark the line that says what is billed
today (for example "Billed today, no free trial") with `trial-terms`. Never
add trial copy to a screen that has no trial.

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
| `.pw-trial`, `.pw-timeline` | Trial line and trial timeline |
| `.pw-cta`, `.pw-secondary` | Primary and secondary actions |
| `.pw-fine`, `.pw-legal` | Renewal text and Restore · Terms · Privacy |
| `.pw-table` | Free vs Pro comparison |

A variation's own `<style>` may extend these. It never edits paywall.css.

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
- [ ] The close button is visible, or the variation is flagged per playbook section 8.
- [ ] Every rating, count and quote has a `data-src` from the proof list.
