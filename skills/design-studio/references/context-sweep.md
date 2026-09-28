# The context sweep: design the screen inside its app

A screen is never designed alone. Before a single variation exists, build a
picture of the app around the target and write it to `<topic>/context.md`.
Budget: ~15–25 tool calls; fan out to an Explore subagent when the app is big.

## 1. Locate the target

- Find the component/screen file(s) and the navigator that mounts them.
- Inventory what's on it today: every piece of data shown, every action, every
  state (empty, loading, error, long content). This list is the **content
  contract**: a redesign keeps all of it, or explicitly names what it drops or
  moves and where to.
- Note the behaviour the design must not break (gestures, pull-to-refresh,
  scroll-linked headers, entrance animations, test IDs).

## 2. Map the neighbourhood (the part agents skip)

Walk outward in rings, lightest touch on the outer rings:

| Ring | What | How to find it |
|---|---|---|
| Flow | Screens that navigate **to** the target and where it navigates **next** | grep the route name in `navigate(`/`push(`/`replace(`, deep links, notification taps |
| Siblings | Other screens in the same stack/tab and anything the user sees seconds before or after | the stack navigator file |
| Tab roots | Every main tab screen (Home and the other tab roots) | the tab navigator |
| Shared parts | Components the target shares with others (cards, headers, rows, charts, the mascot) | imports in the target file |
| History | Past design rounds for this area and their picks | `~/design-studio/<project>/`, the project's brain/plans notes, `TASTE.md` |

For each neighbour, capture its visual language, not its code:

- Ground and surface: background colour, card surface, radius, shadow, borders.
- Header: large title? custom header? what's in it?
- Section structure: headings style, gaps between sections, grouping.
- Type in use: which ramp sizes for hero numbers, titles, rows, captions.
- Colour roles: where the accent appears; metric/status hues.
- Components: rows, pills, rings, bars, charts, buttons, sheets, empty states.
- Density and tone: airy vs dense; playful (mascot) vs utilitarian.

**Visual truth beats code reading.** If a simulator is booted with the app, take
screenshots of the target and 3–5 neighbours (`xcrun simctl io booted screenshot
<file>.png`) and look at them. Save them into the topic dir as `ref-<screen>.png`;
the current target's screenshot doubles as the gallery's "Current" frame. If no
sim is running, don't boot one just for this; read the layout code instead and
say so in context.md.

## 3. Collect the rules

- The project's design-system docs (tokens, primitives, decision logs).
- Standing rulings about this area from the project's knowledge base and memory
  (e.g. "one mascot per screen", "no accent tint on hero cards").
- Platform constraints (tab bar count, native header, sheet detents).

A congruent variation obeys every rule. A wildcard may break a *convention*, but
never a logged ruling unless the user asked to revisit it. Say which, in its notes.

## 4. Decide the mode

Read the user's words, not your preference:

| Signals in the request | Mode | Round-1 mix of 10 |
|---|---|---|
| "clean up", "fit with", "match", "tidy", "same info better organised", "polish", nothing said | **congruent** (default) | 8 congruent + 2 labelled wildcards |
| "something new", "totally different", "fresh", "reimagine", "from scratch", "bold", "don't worry about the rest", an outside app named as the look | **explore** | 3 congruent anchors + 7 new-language |
| Both kinds of signal, or a request that names both | **mixed** | 5 + 5 |

Explore mode still keeps product truth: the same data, actions, platform, and
accessibility floor. What it drops is the app's current *look*. Every explore
variation carries a ripple note: what else in the app would change to match it.

## 5. Write context.md

Keep it to one screen of text. The gallery shows its first paragraph as the
brief; subagents rendering variations read all of it.

```markdown
# <Screen> — context

**Job:** <the one question the screen answers, and how often users come here>
**Mode:** congruent | explore | mixed — <the words that decided it>
**Flow:** arrives from <A, B>; leaves to <C, D>

## Content contract
- <every datum and action that must survive, or "dropped: X → moves to Y">

## Neighbours' language
| Screen | Surface | Header | Type (hero/row/caption) | Colour roles | Notes |
|---|---|---|---|---|---|

## Rules in force
- <ruling> (source)

## Latitude
- <what is genuinely open to change>

## Fixture
<the realistic data every variation shows: names, numbers, dates, one long string>
```

The fixture matters: identical data in every frame makes the variations
comparable, and one deliberately long value (a long product name, a 4-digit
number) catches layouts that only work with short strings.
