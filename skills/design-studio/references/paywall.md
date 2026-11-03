# Paywall mode: how the loop changes

Paywall mode designs a subscription paywall: the flow of screens that leads
to the purchase screen, and the purchase screen's states. Read it with
`paywall-craft.md` (how a frame is built, the visual-first budgets, flows),
`paywall-techniques.md` (the visual techniques real paywalls use, with
examples), `paywall-playbook.md` (what converts, the rules, the rubric) and
`paywall-archetypes.md` (the concepts). Everything in SKILL.md holds unless
this file says otherwise.

Two failures this mode exists to prevent: a paywall that reads as a wall of
text (every screen leads with a visual and stays inside the word budget), and
a single crammed screen where real apps use a short flow (each concept is a
flow of 2 to 4 screens unless the brief asks for one screen).

## Build on what wins

When the project has a paywall that is measurably winning (a finished or
interim experiment in `performance.md`, or one the user names), a `concepts`
round builds on it: its mechanism stays, and the ten concepts vary how the
flow around it is staged, which techniques carry it, and what the purchase
screen looks like. Starting from a blank catalog when a winner exists throws
away the one thing the data has proven. Say in context.md which paywall is
the base and which result made it the base.

## When it's on

The adapter says `surface: paywall`, or the brief names a paywall,
subscription screen, upgrade screen, offer screen or exit offer. Start every
round with `studio.sh new <project> <topic> --paywall`.

## Adapter keys

The project's `.design-studio/adapter.md` names these for paywall mode:

- `surface: paywall`: turns paywall mode on.
- `paywall-data`: a command run with `--out <TOPIC_DIR>` that writes `performance.md`.
- `proof`: where real ratings, counts and quotes come from.
- `offer`: products, prices, trial, and which states exist.
- `buildable`: the components the build target supports, ideally as a kit name (`kit superwall`), which turns on the build-target checks in `paywall-craft.md`.
- `build`: where an approved design is built, and who publishes it.

**performance.md contract.** Per live paywall: date range, impressions
(opens), trial-start or conversion rate, revenue per user where available,
finished experiments with their result and sample size, and an Archetype
column filled in during the sweep. Rows with fewer than about 1,000
impressions, or experiments not finished, are labelled small sample and
never cited as a result.

## Stages

`manifest.stage` names the stage.

| Stage | Each variation | Count | Starts when |
|---|---|---|---|
| `concepts` | A different archetype on the same offer and fixture | 10 unless the user gives a number | A brief that names no archetype |
| `concept` | One archetype (`manifest.archetype`), executed ten ways | 10 unless the user gives a number | A brief that names one ("ten trial timeline paywalls"), or `Explore #N` |
| `converge` | #1 Faithful + refinements of the pick | 10, dropping to 4 to 6 as feedback narrows | A pick with feedback |
| `ab` | A control plus variants that each change one variable | Control + 3 to 5 | `A/B set from #N` |

A bare pick means build it, in every stage. A bare pick in `ab` builds the
whole set as an experiment.

## The pick question

The four options from SKILL.md step 6, with option 3 replaced by the stage
move:

- `concepts`: `Explore #N`: ten executions of #N's archetype.
- `concept`, `converge`: `A/B set from #N`: #N as the control plus 3 to 5 one-variable variants.
- `ab`: `Build the set as an experiment`.

A mix or the runner-up can still be typed into the answer box. The
`agentPick` reason cites the rubric line that decided it (playbook section
11) or a number from `performance.md`. The `predictedPick` reads TASTE.md's
paywall rows.

## Context sweep additions

On top of `context-sweep.md`:

1. **The offer:** products, prices, trial, and which states exist, from the adapter's `offer`.
2. **Live paywalls:** each one screenshotted or recreated, tagged with its archetype, with its numbers. When the adapter has `paywall-data`, run it with `--out <TOPIC_DIR>` and fill in the Archetype column of `performance.md`. Without it, write "No live data" in context.md.
3. **The path in:** the placements that open the paywall and what the user saw just before (onboarding answers feed a personalised paywall).
4. **Proof:** the real ratings, counts and quotes, with source and date.
5. **Rules in force:** playbook section 9 plus the adapter's rulings.

context.md holds the **offer fixture**: plans and prices, trial terms, the
longest real testimonial, and the proof list in exactly this form (`check`
reads it):

```markdown
## Proof
- P1: "The quote or figure exactly as it may appear" (source, YYYY-MM-DD)
```

## Planning a `concepts` round

Each variation is a different archetype from the catalog. A new archetype is
allowed as a wildcard, with its mechanism stated. Pairs differ in archetype
plus at least one axis of the paywall table in `variations.md`. Leave out
archetypes whose "Loses when" fits this offer, and name them in context.md.

When the round builds on a winning paywall (above), the archetype axis is
replaced by the winner's mechanism combined with a second archetype or a
technique from `paywall-techniques.md` (a note + a trial timeline, a note +
a laurel rating, a note on a device shot…), so ten concepts still differ.

Plan each concept as its flow: list the screens and the one job of each
(`"flow": ["step-1", "step-2", "main"]`) before anything is drawn, and name
the technique that carries each screen's visual.

## Planning a `concept` round

All ten keep the archetype's mechanism. Vary the entry's **Axes**; each pair
differs on at least two. #1 is the catalog's anatomy done well, as the
round's control.

## Planning an `ab` set

The control is the pick unchanged (`"control": true`). Each variant changes
exactly one lever from playbook section 10 and names it in `variable`.
Prefer levers `performance.md` shows no finished experiment for. Variants
look alike on purpose; the gallery labels what changed. Every variant still
provides every state.

## Rendering

The subagent brief from `variations.md`, with "Read first" changed to
`paywall-craft.md` (all of it, especially "Visual first" and "Flows"),
`paywall-techniques.md`, the kit's `KIT.md` when the round has a kit, playbook sections 9 and 11, the archetype's catalog
entry, and `context.md`. Each subagent writes `vNN/step-N.html` for every
step of the variation's flow and `vNN/<state>.html` for every state in
`manifest.states`, for its two variations, then runs `studio.sh check` on the
round and fixes every visual-share and word-budget failure on its own two
before replying. The brief gives each subagent its variations' flows screen
by screen (job + technique), not only a thesis.

## manifest.json (paywall)

```json
{
  "project": "acme", "topic": "paywall", "title": "Main paywall", "round": 1,
  "surface": "paywall", "stage": "concepts",
  "archetype": "trial-timeline",
  "states": ["main", "alt-plan", "exit"],
  "flow": ["step-1", "step-2", "main"],
  "kit": "superwall",
  "trial": true,
  "brief": "The job and the constraint that matters most.",
  "agentPick": "v04", "predictedPick": "v07",
  "current": { "label": "Today", "states": { "main": { "image": "../ref-main.png" } } },
  "variations": [
    {
      "id": "v01", "dir": "v01", "name": "Three Days",
      "idea": "One-line thesis.",
      "tags": ["congruent"],
      "archetype": "trial-timeline",
      "flow": ["step-1", "main"],
      "screens": { "step-1": "Hook: device shot of the app's main screen", "main": "Plans under a laurel rating" },
      "notes": { "changes": "…", "keeps": "…", "build": "…", "levers": "Playbook levers this pulls" }
    }
  ]
}
```

`archetype` at the top is for `concept`, `converge` and `ab` rounds; in
`concepts` each variation names its own. In `ab`, one variation has
`"control": true` and the rest have `"variable"`.

`flow` (round level, or per variation to override it) lists the screens in
order and ends with `main`. `screens` names each screen's job and technique;
the gallery doesn't show it, it is for the build spec. The gallery opens on
a **Flow** view (each variation as a row of its screens) and keeps the state
switch for the purchase screen.

## Check, sheets, send

`check` runs the paywall checks when the manifest says `"surface":
"paywall"`: every flow screen and state file exists, every screen has a
`visual`, the required `data-pw` markers are present with exactly one CTA,
proof matches the proof list, an `ab` round has one control and a variable
per variant, and (one headless Chrome pass) every screen meets the visual
share and word budgets in `paywall-craft.md`. `sheets` writes
`sheet-flow-<k>.png` (four flows per sheet) and `sheet-<state>-<k>.png`.
Send every `sheet-flow-*`, then `sheet-main-*`, with the link.

## Finalise

On a build pick, write `ROUND_DIR/spec.md`:

- the chosen design per state
- every element mapped to the adapter's `buildable` components
- the copy with its variable placeholders
- playbook section 9 ticked per state
- for `ab`, the experiment: control, variants, the one variable each changes, the success metric (trial starts or paid conversion per open), and the minimum sample

Then follow the adapter's `build` path. Never publish a paywall or start an
experiment; that stays the user's call.

## Taste log

Log paywall rounds in TASTE.md with `paywall` in the Project / topic column
(`acme / paywall main`), plus the stage, and the variables for `ab` rounds.
