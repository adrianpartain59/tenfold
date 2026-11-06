# Subtraction: decide what the screen is for before drawing it

The most common way an AI redesign fails is not ugliness. It is a screen that
keeps everything the old one had, rearranges it, and decorates the hero. The
result is one more cluttered screen: no starting point, no flow for the eye,
too much text, every part fighting for attention.

Good screens are made mostly by taking things away. Do that on purpose, before
round 1, and show the user what was taken away and where it went.

## 1. Triage: every element earns its place or leaves

List every element on the screen today (data, actions, labels, headings,
containers, decorations, states). Give each one a verdict:

| Verdict | Test | Where it goes |
|---|---|---|
| **Core** | The user acts on it, or needs it to act, *at the moment they open this screen* | Stays, and gets the space |
| **Relocate** | It's real, but it's for reviewing, comparing or managing, not for the moment of use | The screen where people already review that kind of thing (history into the existing history/log screen, weekly summaries onto Home's summary area, unit settings into the screen's settings) |
| **Transient** | It only matters right after an action | Feedback that appears and leaves: a toast with Undo, a brief confirmation, an animation |
| **Merge** | It says what another element already says | Fold it into that element (a "Goal reached" line is the filled gauge; a "Quick add" heading is the tiles themselves) |
| **Cut** | Nothing breaks without it | Gone. Say so |

Rules:

- Name the destination for every Relocate. "Moved off-screen" without a home
  is a Cut and must be labelled as one.
- A label, heading or container that restates what the content already shows
  is Merge or Cut. Headings over a single group, cards around a single row,
  boxes around icons, and captions under self-explanatory visuals all go.
- Decoration (glare, gradients, texture, extra outlines) is Cut unless it
  carries information.
- Write the triage table into `context.md` under `## Triage`. Tell the user the
  Relocates and Cuts in the round message, in one line each, so they can veto
  any of them.
- The user can always restore an item. Assuming it must stay is the failure
  this step prevents.

## 2. The target: one screen, one focus, one path

After triage, the screen holds only the Core items. Design toward:

- **One starting point.** A single hero, the biggest thing on the screen,
  that answers the screen's job. Prefer a visual (a gauge, an object that
  fills, a big number with a picture) over a sentence. A hero smaller than
  about a third of the first viewport reads as a header, not a hero.
- **One path for the eye.** Top to bottom, in one column: the number, then the
  visual, then the actions in the thumb zone. Write the path as 1 → 2 → 3 for
  every variation. If you can't, the layout has no path.
- **Fits without scrolling** for daily tools (logging, checking, quick
  actions). If the Core doesn't fit on the smallest supported phone, triage
  again before shrinking things.
- **Pictures over words.** Action tiles carry an image and a short label;
  feedback is a toast or an animation, not a line of text that stays.
- **The same thing looks the same.** Reuse the app's existing parts exactly:
  its rows, its edit fields, its sheets, its buttons. A second look for the
  same job reads as inconsistency even when each one is nice.

## 3. Interaction removes chrome too

Many visible controls exist only because the interaction is clumsy. Fix the
interaction and the control disappears:

- Edit in place: tap the number, type, see the gauge move live, tap away to
  save. No Save button, no Cancel, no edit sheet.
- Undo instead of confirm: act at once and offer Undo in the toast.
- A custom amount opens a small sheet with an X, one number field (unit
  inside it) and Done. Nothing else.
- Motion explains changes so text doesn't have to: digits roll, the fill
  rises, a pressed tile scales down.

## 4. Assets the design needs: make them

When the design wants an image or a shape the app doesn't have, make it
instead of falling back to an icon, emoji or text. This is permitted, not
required: do it when a custom asset would clearly carry the screen better,
and say in the variation's notes that it's new and how it was made.

- **Illustrations and object pictures** (vessels, foods, products, empty-state
  art): generate them with an image model when one is configured (for example
  Gemini's image model with the key from the project's secrets). Ask for one
  consistent style across the set ("drawn like an iOS emoji, plain object, no
  text or logos, centred, white background"), key the white to transparent,
  and export at the sizes the app uses (@1x/2x/3x). Keep the prompt script in
  the round dir so the set can be regenerated or extended.
- **Hero shapes and gauges** (a bottle, a glass, a ring with a custom
  silhouette): draw them as SVG paths. Keep the geometry in one place
  (viewBox, the fill range) so it can be tuned in small steps ("rounder
  corners", "a bit taller", "ribs flush with the edge") without redrawing.
- Match the style to its neighbours: one family of pictures per screen, the
  app's outline weight and colours on drawn shapes.
- When the user sends a reference picture, copy its proportions and details
  exactly first, then propose changes.

## 5. Worked example: a water-logging screen

Before (a vibe-coded first pass, all of it kept by a 20-frame round):

> amount + pencil · "of 100 oz" · tapered cup · % · "Quick Add" heading ·
> four tiles · "+ Custom" card · "Goal reached" line · Today's Log (rows with
> trash buttons) · This Week (paginator in boxes + bar chart in a card) ·
> Apple Health button · oz/mL switch

Triage the user arrived at, one change at a time, after the round:

| Item | Verdict |
|---|---|
| Amount, goal, %, the vessel, four quick adds, Custom | Core |
| Today's Log | Relocate: into the day's meal history, where food logs already live |
| This Week | Relocate: Home's weekly summary carousel |
| oz/mL switch | Relocate: the screen's settings pop-up |
| Log rows after a quick add | Transient: a toast ("+8 oz", the vessel picture, Undo) for 3 s |
| "Quick Add" heading, "Goal reached", card behind Custom, boxes around chevrons | Merge or Cut |
| Glare on the bottle, black outline | Cut (decoration) |
| Apple Health button | Cut from this screen |
| Edit sheet with Save/Clear | Replaced by inline editing with a live preview |

After: amount (rolling digits, edited inline) · "of 100 oz" · a large bottle
drawn as SVG that fills smoothly · % · four tiles with generated pictures ·
"+ Add Custom". One screen, no scroll, the bottle about 40% of the height. Then
the hero was made bigger three times. Every step was a deletion, a move or an
enlargement; nothing was added except motion and the two custom assets.

A round that had started from this triage would have spent its ten frames on
how to present the Core, not on how to decorate a glass above a log list.
