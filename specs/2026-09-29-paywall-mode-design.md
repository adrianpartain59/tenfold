# Paywall mode for design-studio

Status: design approved in chat 2026-09-29, not built.
Target release: Tenfold 1.2.0.

## Why

A paywall is an app screen, but mobile mode judges it the wrong way:

- It has one job, which is conversion, and a body of evidence about what
  moves conversion. Mobile mode's principles cover usability and
  congruence, not persuasion.
- The ideas behind paywalls fall into known **archetypes** (trial timeline,
  testimonial wall, personalised plan…). A useful round either spreads across
  archetypes or goes deep inside one of them. Mobile mode's axes don't
  describe either.
- A paywall that works with annual selected can break with monthly selected,
  or leave no room for a friend price or an exit offer. One frame hides that.
- Winners can be measured. Paywall platforms run A/B experiments, and that
  needs variants that change one variable at a time. Design rounds do the
  opposite and change two or more axes per pair.
- Real performance data exists for the paywalls already live, and nothing
  in the loop reads it.

The loop stays the same: context sweep, ten distinct variations, gallery,
Claude's pick plus a predicted pick, TASTE.md, pick then build. Paywall mode
changes the knowledge the round draws on, how rounds are staged, what each
variation contains, and what `check` enforces.

## Constraints

- Additive. Mobile and web modes keep working exactly as they do today, and
  their assets, references and `studio.sh` subcommands keep their current
  behaviour. Paywall mode adds new files and branches on a flag.
- One skill, one TASTE.md, one server. Paywall rounds are logged in the same
  taste log with `paywall` in the Project / topic column.
- No new runtime dependencies (bash, python3, Chrome for images).
- The public repo carries general paywall knowledge only. Project data,
  paywall IDs, build scripts and project rulings live in the project's
  `.design-studio/` adapter.

## How a project turns paywall mode on

1. `surface: paywall` in the adapter, or
2. the brief names a paywall, subscription screen, upgrade screen, offer
   screen or exit offer.

The adapter for a project with paywalls can give:

- `paywall-data`: a command that writes `TOPIC_DIR/performance.md` (see Live
  data below). Optional: without it the round runs on the playbook alone and
  says so in context.md.
- `proof`: where real ratings, review counts, user counts and quotes come
  from. Nothing else may appear as a claim or testimonial.
- `offer`: products, prices, trial lengths, discount states, and which states
  exist (friend, promo, exit offer, win-back).
- `buildable`: the components the build target supports (for example the
  Superwall editor's elements), so ordinary variations stay buildable.
- `build`: where an approved design gets built, and who publishes.

## Round stages

`manifest.stage` names the stage.

| Stage | What each variation is | Count | Enters from |
|---|---|---|---|
| `concepts` | A different archetype on the same offer and fixture | 10 by default | A brief with no named archetype |
| `concept` | One archetype, executed ten different ways | 10 by default | A brief that names an archetype ("10 testimonial paywalls"), or a pick from `concepts` |
| `converge` | #1 Faithful (pick + feedback applied literally) + refinements | 10, dropping to 4 to 6 as feedback narrows | A pick with feedback from `concept` or `converge` |
| `ab` | A control plus variants that each change exactly one named variable | Control + 3 to 5 | "A/B set from #N" |

- In `concepts`, every pair differs in archetype (the persuasion mechanism)
  plus at least one other axis.
- In `concept`, every variation keeps the archetype's mechanism, and every
  pair differs on at least two within-archetype axes: proof format, hero,
  pricing module, plan picker, CTA copy and placement, density, tone. Each
  archetype entry in the catalog lists its own axes.
- In `ab`, the control is the picked design unchanged. Each variant names its
  `variable` (e.g. "CTA copy", "default plan", "proof position") and changes
  nothing else. The gallery shows the variable on each card. Variables come
  from the playbook's list of levers, ranked by expected effect.
- A bare pick means build it, in every stage, as in mobile mode. Moving to
  another stage is always an explicit option in the pick question:
  `Explore #N` (a `concept` round on that archetype) in `concepts`, and
  `A/B set from #N` in `concept` and `converge`. A bare pick in `ab` means
  build the whole set as an experiment.

## What one variation contains

A variation is a folder, `vNN/`, with one file per state:

- `main.html`: the paywall as first shown, with the default plan selected.
- `alt-plan.html`: the other plan selected, when the offer has more than one
  plan.
- Brief-dependent states, from the adapter's `offer`: `exit.html`,
  `friend.html`, `promo.html`, `winback.html`.
- Pre-paywall steps (`step-1.html` …) only when the concept needs them (for
  example "your plan is ready" before a personalised plan). `main.html` stays
  the paywall itself.

`manifest.states` lists the states this round covers. Every variation
provides every listed state. The gallery shows `main` by default and adds a
state switch that changes every card at once, so states are compared across
variations.

## Knowledge (public skill)

### `references/paywall-playbook.md`

The conversion levers, each with its source, date and evidence strength
(`benchmark` = published aggregate data, `case study` = one app's reported
result, `practice` = practitioner consensus with no published number). It is
researched when this is built, and a claim with no source can't be written
as a number. It covers at least:

- value before price, and the order a paywall's content goes in
- trial framing: trial length display, "no payment now", the reminder before
  billing, the timeline
- plan structure: single vs multiple plans, default selection, anchoring,
  per-week/per-month breakdowns, and their compliance limits
- proof: specific over generic, ratings vs quotes vs counts, placement
- risk reversal: cancel anytime, how to cancel, refund language
- CTA: one primary action, copy that names the outcome or the trial, the
  secondary purchase path
- personalisation from onboarding answers
- urgency, close-button delay and countdowns: when they help, and when they
  cross into dark patterns (FTC, App Review 3.1.2)
- the lever list for `ab` rounds, ranked by expected effect

It ends with a **scoring rubric**: the questions `agentPick` answers for
every variation (is the value clear before the price? is the billed price
the most prominent price? is there one primary action? …).

### `references/paywall-archetypes.md`

About 14 archetypes. For each: the mechanism (why it converts), anatomy (the
parts in order), where it wins and where it loses (audience, price point,
trial vs no trial), within-concept axes, compliance hazards, and reference
apps known to use it. The starting list:

1. Trial timeline (today, reminder day, billing day)
2. Testimonial wall
3. Rating hero (stars + count as the lead)
4. Feature checklist
5. Free vs Pro comparison table
6. Personalised plan (built from onboarding answers)
7. Outcome projection (the user's goal on a chart or date)
8. Coach or mascot-led
9. Video or carousel hero
10. Single-plan hero (one price, one button)
11. Plan cards (multiple plans, one pre-selected)
12. Exit ticket (a discount on dismiss)
13. Friend gift (a referral price)
14. Countdown offer (flagged: urgency ethics apply)

### `references/paywall-craft.md`

- The frame template: mobile mode's `screen.css` and phone frame, with a
  paywall layer (`paywall.css`) for pricing modules, plan pickers, trial
  timelines, proof blocks and legal footers.
- **Required elements**, each marked with a `data-pw` attribute so `check`
  can verify them structurally: `billed-price` (the amount billed, and the
  most prominent price), `renewal` (auto-renewal terms near the CTA),
  `trial-terms` when a trial exists, `restore`, `terms`, `privacy`,
  `cta` (exactly one primary).
- The states contract above.
- Buildability: a normal variation uses only the adapter's `buildable`
  components. A variation that needs anything else is tagged
  `new-primitive` and says what in `notes.build`.

## Tooling

- `studio.sh new <project> <topic> --paywall` copies `gallery-paywall.html`
  and `paywall.css` into the round.
- `check` detects `"surface": "paywall"` and runs, on top of the mobile
  checks:
  - every variation has every state in `manifest.states`
  - every `main` and `alt-plan` frame carries all required `data-pw` markers,
    with exactly one `cta`
  - every proof string (`data-pw="proof"`) matches an entry in context.md's
    proof list
  - `ab` rounds have a control and a `variable` for each variant
  - no lorem ipsum
- `sheets` writes one contact sheet per state (`sheet-main-N.png`,
  `sheet-exit-N.png` …).
- Tests: a `paywall-smoke` fixture in `tests/fixtures/` and cases in
  `tests/studio.test.sh`, covering one passing round and one round per
  failing check.

## Context sweep for a paywall

Mobile mode's sweep, with these additions:

1. **The offer:** products, prices, trial, states, from the adapter.
2. **Live paywalls:** each one rendered or screenshotted, tagged with its
   archetype, with its numbers from `performance.md`.
3. **The path in:** the screens and placements that open the paywall
   (onboarding end, feature gate, settings), and what the user has just
   seen. A personalised paywall needs onboarding's answers.
4. **Proof:** the real ratings, counts and quotes with their sources.
5. **Rules in force:** the platform's review rules (billed-price
   prominence, auto-renewal disclosure, the storefront rules for external
   purchase links) and the project's own rulings.

context.md holds an **offer fixture**: plans, prices, trial, the proof list,
and the longest real string (a long testimonial). Every variation uses it.

## Live data

The adapter's `paywall-data` command writes `TOPIC_DIR/performance.md`: for
each live paywall, the date range, impressions, trial-start rate, conversion
rate, revenue per user where available, and any finished experiment with its
result and sample size. The sweep reads it, and the round uses it three ways:

- the archetype tag on each live paywall shows which mechanisms have already
  been tried and how they did
- `agentPick`'s rationale cites the numbers when a live paywall shares the
  variation's archetype or lever
- `ab` rounds rank variables by the playbook's evidence and by what the live
  data hasn't tested yet

Small samples are labelled as such (fewer than about 1,000 impressions or no
finished experiment), and never cited as a result.

## Pick question

Same shape as mobile mode, plus:

- `agentPick`'s reason cites a rubric item or a live number.
- `predictedPick` reads the paywall rows in TASTE.md. That log already shows
  a pattern: on live revenue screens the user picks the congruent,
  least-disruptive option.
- Option 3 (the real third choice) becomes the stage option: `Explore #N`
  in `concepts`, `A/B set from #N` in `concept`/`converge`. The question
  keeps its four-option limit, and a mix or runner-up can still be typed.

## Finalise

On a build pick write `ROUND_DIR/spec.md`: the chosen design per state,
every element mapped to the adapter's `buildable` components, the copy with
its liquid/variable placeholders, the compliance checklist ticked per state,
and for `ab` the experiment definition (control, variants, the one variable
each changes, the success metric, the minimum sample). Then follow the
adapter's `build` path.

## PepAI adapter (pepai repo, not this repo)

Listed so the public design stays honest about what a real adapter needs.

- `paywall-data`: a script in `.design-studio/` that queries Superwall's
  ClickHouse per paywall ID.
- `proof`: App Store Connect ratings and reviews.
- `offer`: the live paywall IDs, products, the friend/promo/exit states.
- `buildable`: the Superwall editor's elements.
- `build`: the superwall-editor skill, edited in browser tabs, and Adrian
  publishes.
- The rulings from the 2026-09-28 compliance check: billed price first,
  auto-renewal text, web checkout US-only.

## Build order

1. Research pass for the playbook and archetype catalog (sources gathered by
   subagents, every claim cited or downgraded to `practice`).
2. `paywall-playbook.md`, `paywall-archetypes.md`, `paywall-craft.md`,
   `paywall.md` (the loop changes).
3. `paywall.css` + `gallery-paywall.html` with the state switch.
4. `studio.sh new --paywall`, `check` and `sheets` branches (`paywall_check.py`,
   `paywall_sheets.py`), fixture and tests.
5. SKILL.md: a "Paywall mode" section, description trigger words, common
   mistakes rows. `variations.md`: paywall axes. CHANGELOG, plugin.json 1.2.0.
6. PepAI adapter: `paywall-data` script, proof, offer, buildable, build.

## Out of scope

- Publishing or starting experiments. The build stops before publish, as
  with every paywall build so far.
- Web-checkout (app-to-web) pages. They're web mode's job.
- Generating paywall copy translations.
