# App design principles + the pre-send checklist

These are the floor for every variation, including the wildcards. A variation can
break the app's *conventions* in explore mode; it may not break these.

## 1. Hierarchy: one job, one hero

- Every screen answers one question first. Name it ("How am I doing today?", "What
  do I log next?"). The hero element answers it; everything else is subordinate.
- One focal point per viewport. Two heroes means none. Rank the rest in three
  tiers at most: hero, supporting, detail.
- Hierarchy comes from size, weight, and position before it comes from colour.
  Squint test: blurred, the most important thing is still the most visible.
- The first viewport (above the fold, ~700pt of content on a 393×852 screen
  with the tab bar) carries the job. What sits below it is secondary by definition.

## 2. Layout, grouping, rhythm (Gestalt)

- Proximity groups. Space *inside* a group is smaller than space *between*
  groups, every time. Use the spacing scale (4/8/12/16/20/24/32); never an
  off-scale number.
- Alignment: one left edge for the screen's text column (the screen inset,
  usually 16pt). Every element either shares an edge or is visibly centred.
- Similarity: things that behave the same look the same. Two tappable rows
  with different chrome imply different behaviour.
- Common region: a card says "these belong together". A card around a single
  line of text is noise. Don't nest cards in cards (card soup).
- Nested radii: inner radius = outer radius − the gap between them.
- Consistent rhythm down the screen: section gaps equal each other.

## 3. Typography

- Use the app's type ramp only (tokens.css `.t-*`). Four sizes on one screen is
  plenty; five is a smell.
- Numbers that matter (doses, macros, weight) are tabular, heavy, and larger
  than their labels. Units are smaller and lighter than the number.
- Line length for reading text: 35–60 characters on a phone.
- Sentence case for labels and buttons. All-caps only for tiny eyebrow labels,
  tracked out.
- Truncate deliberately (one line + ellipsis) or wrap deliberately; never let a
  long name push a layout apart. Test with the longest realistic string.

## 4. Colour

- Colour has a job: brand/action, status (good/warn/error), or data identity
  (a metric's hue). Colour with no job is decoration; use it sparingly.
- One accent. It marks what's tappable or primary, not what's pretty.
- Neutrals do 80–90% of the work: ground, surface, text tiers, hairlines.
- Contrast: body text ≥ 4.5:1, large text (≥ 18pt, or 14pt bold) and UI glyphs
  ≥ 3:1. Secondary text still clears 4.5:1 when it carries information.
- Never encode meaning in colour alone: pair it with an icon, label, or position
  (colour-blind users, glare, dark mode).
- Dark mode is a separate palette, not an inversion: lighter surfaces sit closer
  to the viewer, shadows mostly disappear, saturated hues calm down.
- The ground stays quiet: the screen's ground (and the scroller over it) is one
  flat colour. A world's pattern, scene or texture (graph paper, paper grain, a
  sky, a grid) goes inside a bounded element: a header band, a chart, a card, a
  label. A pattern behind scrolling text competes with every rule, chart line
  and letter on top of it, shimmers as it scrolls, and turns a print metaphor
  into an endless strip. The theme still owns the ground's colour; the
  pattern just moves to where it means something (a grid inside the chart reads
  as "measured").

## 5. Touch and ergonomics (iOS first)

- Tap targets ≥ 44×44pt (Android 48dp), with ≥ 8pt between adjacent targets.
- Thumb zone: the primary action lives in the lower half or bottom-right. Rare or
  destructive actions can sit up top.
- Respect the safe areas: status bar/Dynamic Island (top ~54pt), home indicator
  (bottom 34pt), floating tab bar. Content never hides under them unscrollably.
- One primary button per screen. Secondary actions are visually quieter
  (secondary/tertiary buttons, text buttons, icon buttons).
- Destructive actions are separated, labelled, and confirmed or undoable.
- Gestures are accelerators, never the only path: every swipe action also has
  a visible control.

## 6. Interaction, feedback, states

- Every tap gets feedback within 100ms (pressed state, haptic, or navigation).
- Design all states, not just "full": empty (first run), loading (skeleton, not
  a spinner in the middle of nothing), error (what happened + what to do),
  partial data, very long content, offline.
- Progressive disclosure: show what the user needs for this decision; put the
  rest one tap away. Don't hide the primary task behind a tap.
- Hick's law: fewer, clearer choices beat more choices. Group, default, or
  defer the rest.
- Fitts's law: frequent targets are big and close to the thumb.
- Recognition over recall: show the options, the last value, the current state.
- Edit in place when the value is small and frequent; use a sheet when editing
  needs room or confirmation; push a screen when it's a new context.
- Sheets and modals: the backdrop fades, it never slides with the sheet.

## 7. Content and copy

- Real content, real lengths, the app's voice. No lorem ipsum, no "Title here".
- Labels say what things are; buttons say what happens ("Log dose", not "OK").
- Numbers get units and context ("82 of 120 g" beats "82g"; "3 days left" beats a
  date the user has to compute).
- Cut every word that doesn't change what the user does.
- The project's own copy rules (from the adapter or the style guide) apply too.

## 8. Platform fit

- It must look like it belongs on iOS: native navigation (large titles or the
  app's header), native sheets, system font, SF-style symbols/icons, standard
  gestures (back swipe, pull to refresh). A web page in a phone frame is a fail.
- No web-isms: hover states as the only affordance, visible scrollbars, desktop
  dropdowns, tiny link text, cursor-dependent UI.
- Motion explains change (where did this come from / go to). 200–350ms, ease-out
  in, ease-in out. Never motion just to decorate.
- Accessibility: Dynamic Type grows text without breaking layout; VoiceOver has a
  sensible order; nothing relies on colour or motion alone; reduce-motion honoured.

## 9. Consistency (the whole-app view)

- Same thing, same look, same place, across screens. A card surface, a section
  heading, a metric's colour, a back affordance: pick the app's existing one.
- A new pattern must earn its place: it solves something the existing pattern
  can't. Name what it solves.
- If a variation introduces a new pattern, say which other screens would need to
  adopt it for the app to stay coherent (the "ripple").

## 10. The AI-mockup failure list (reject on sight)

- Everything centred; a centred stack of cards with no hierarchy.
- Gradient backgrounds, glows, glassmorphism or neon used as decoration.
- A pattern or texture painted on the whole ground (graph paper, grain, grid)
  instead of inside a bounded element.
- Emoji as icons. Mixed icon families on one screen.
- Card soup: every element in its own card, cards in cards.
- Five font sizes, three font weights for the same role.
- Uniform grid of identical tiles when the data has an obvious hero.
- Fake precision or filler stats nobody asked for.
- Tiny grey text carrying important information.
- A variation that differs from another only by colour or corner radius.

## Pre-send checklist (run on every variation before the link goes out)

1. Can I say in one sentence what this screen's hero answers? Is it the biggest
   thing in the first viewport?
2. Squint: does the hierarchy survive blur?
3. Every spacing value on the scale; inner group gaps < between-group gaps.
4. Only ramp type sizes; ≤ 4 sizes; numbers tabular with smaller units.
5. Accent used only for action/primary; metric hues match the app's metric hues.
6. Every tap target ≥ 44pt; primary action reachable by thumb; one primary button.
7. Safe areas respected; nothing hides under the tab bar or status bar.
8. Real data, the shared fixture, longest-string case doesn't break it.
9. Congruent variations: surfaces, headers, radii, icons match the neighbours in
   context.md. Wildcards: the ripple is written in the notes, and so is the
   platform line: a wildcard breaks the category's conventions, never the
   platform's (ground, navigation, tap targets, system type sizes, legibility).
10. Nothing from the failure list above.
11. It is visibly different from every other variation in the round on ≥ 2 axes.

## Web pre-send checklist (web mode)

In web mode, sections 5 and 8 above (touch ergonomics and iOS platform fit)
give way to `web-craft.md`. Run these in place of items 6 and 7 of the
checklist above:

1. The primary action is visible in the first viewport at 390 and at 1440.
2. No horizontal scroll at 390; nothing clipped or overlapping at 834.
3. Text over images passes contrast at every width.
4. Every proof claim (rating, counts, quotes) comes from context.md's content fixture, with its source.
5. Body text is 16 px or larger, with a 45 to 80 character line length on desktop.
6. Every link and button has a hover and a visible focus state; targets are 44 px or larger on phones.
7. The direction's `tokens.css` drives every page; no page redefines the type ramp in its own `<style>`.
8. Nothing from the web failure list in `web-craft.md`.
