# Screen types: classify the screen before designing it

A main tab and an inner screen do different jobs, so they have different
targets. Classify the screen first, in `context.md`, before the inventory and
the triage. Every later rule (subtraction, the clutter rubric, the budgets)
is read through the type.

The failure this prevents: the rules for a task screen (one focal point, no
scroll, about three groups) applied to a tab root. The result looks like an
inner screen with too little on it, and no real app in the category ships a
main tab like that.

## How to classify

Answer three questions from the code and the navigator:

1. **How do users arrive?** Tab bar or launch; a tap on a card or row; a
   button, quick add or notification; a linear flow.
2. **How often do they see it?** Many times a day, daily, occasionally, once.
3. **How many areas does it cover?** One task, one metric, or several.

| Type | Arrive | Seen | Covers | Target |
|---|---|---|---|---|
| **Tab root: dashboard** | Tab bar / launch | Many times a day | Several areas | A scrolling stack of single-subject cards, 2–3 card types, a hero at the top, about 2–3 screens long |
| **Tab root: list / feed** | Tab bar | Daily | Many items | Uniform rows, an optional summary strip; detail on drill-in |
| **Detail** | Tap on a card or row | Occasionally | One metric | That metric in depth: chart with ranges, stats, history, explanation; scrolls |
| **Task screen / sheet** | Button, quick add, notification | Often, short visits | One job | One focal point, no scroll, about three groups, one primary action (Hydration) |
| **Flow step** | Linear flow | Once | One decision | One question, one illustration, Continue |
| **Settings / profile** | Tab or avatar | Rarely | Configuration | Grouped lists |

Write the answer as the first line of `context.md`: **Type:**
`<type>` · arrives from `<…>` · seen `<…>`.

## What subtraction means for each type

`subtraction.md` applies to every type, but what counts as Core and what may
leave the screen depends on the type:

| Type | Core | What leaves |
|---|---|---|
| Dashboard | One summary card for every area the tab owns | Detail-level content inside cards (range selectors, scrubbing, full history, tables, explanations, editing) moves to that card's detail screen. Duplicate cards merge. Decoration goes. **A tab's own areas never leave the tab.** |
| List / feed | The rows | Per-row actions and detail move to drill-in |
| Detail | Everything about its one metric | Other metrics and competing actions |
| Task / sheet | The input, its controls, the confirm | Everything else: relocate, make transient, cut (the Hydration example) |
| Flow step | The question | Side content, extra chrome |

## Tab-root dashboard rules

From the category research (pep-brain
`reports/screen-types-tab-root-vs-inner-2026-11-06.md`):

1. **It scrolls, ranked by attention.** The first screenful gets most of the
   attention, the first two most of the rest. The first viewport holds the
   hero plus at least two more cards; the page is about 2–3 screens.
2. **Order:** the hero (the tab's headline metric) → 2-up stat tiles →
   full-width chart cards → secondary or educational cards.
3. **Two or three card types, one anatomy:** label top left, value with a
   smaller unit, a delta or context line, a small chart, an implied tap to the
   detail. Same job, same card type.
4. **One subject per card, one card per area.** Health and fitness main tabs
   carry about 4–10 cards (Apple Health and Fitness Summary, Oura, Whoop,
   MyFitnessPal, MacroFactor, Cal AI).
5. **Every card is a door** to a detail screen. On the card: current value,
   change, a one-period mini chart, a status. On the detail: ranges, history,
   min/max/average, explanations, editing.
6. **No exploration on the tab:** no range pills, filters or scrubbing.
7. **At most one primary action** (for example Log weight on the hero card);
   logging opens a sheet.
8. **Empty states per card**, never one empty hero for the whole tab.

The clutter rubric (`principles.md` §11) still holds, at two levels: the page
(one hero card, a clear scan order down the cards, consistent card types) and
each card (one focus, label → value → context → mini chart, no label that
repeats the value, no decoration).

## Inner-screen rules

- **Task screen / sheet:** `subtraction.md` §2 in full (one starting point,
  one path, no scroll, about three groups, under about 15 words outside the
  data, interaction that removes chrome).
- **Detail:** the metric's chart or number is the hero; ranges and history are
  expected here; nothing about other metrics.
- **List / feed:** one row shape; a sticky picker or summary strip at most.
