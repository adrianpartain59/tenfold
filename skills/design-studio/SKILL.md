---
name: design-studio
argument-hint: "[screen, card, flow, website or paywall to design]"
description: Use when the user wants to design, redesign, rethink, restyle, or see options, variations, directions, or mockups for an app screen, card, widget, component, sheet, or flow (mobile/iOS/React Native app UI especially), for a website, landing page or marketing site (web mode), or for a paywall, subscription screen, upgrade screen or exit offer (paywall mode), including "render an HTML doc with designs", "give me variations", "show me options for X", "ten testimonial paywalls", or picking a variation from an earlier design round to iterate on.
---

# Design Studio

Design rounds for app UI: sweep the whole app for context, render **10**
variations as phone mockups on **localhost**, send the link, ask which one
(with Claude's pick and a prediction of the user's pick), then render 10 more
of the chosen one with the user's feedback. Repeat until they say build.

`<SKILL_DIR>` below is the directory containing this file.

## The loop

1. **Set up.** Read `~/design-studio/TASTE.md` (create it with empty "Patterns"
   and "Log" sections if missing). Look for a **project adapter**: a
   `.design-studio/adapter.md` file at the project root. If it exists, read it
   now and follow it; it names the project's knowledge base, design-system
   docs, standing rulings, token/icon export commands, and build path, and it
   wins over the defaults in this skill.
   ```bash
   bash <SKILL_DIR>/scripts/studio.sh new <project> <topic>
   ```
   It prints `ROUND_DIR`, `TOPIC_DIR` and the URLs, and starts the server if
   it's down. On the first round of a topic, set up the topic's shared assets:
   - **Tokens:** the adapter's export command, or for a React Native app with
     a tokens module, `node <SKILL_DIR>/scripts/export-tokens.mjs --root .
     --entry <path/to/tokens/index.ts> --out <TOPIC_DIR>/tokens.css`. Otherwise
     write `TOPIC_DIR/tokens.css` by hand from the app's theme, using the
     `--c-*` / `--space-*` / `--radius-*` names and `.t-*` type classes
     described in `references/mockup-craft.md`.
   - **Icons:** the adapter's icon export, or `studio.sh icons <TOPIC_DIR>`
     (a local copy of the Feather sprite, MIT).
   - **Images:** link the app's image assets as `TOPIC_DIR/img`
     (`ln -sfn "$PWD/<assets dir>" <TOPIC_DIR>/img`) when it has any.

2. **Context sweep (never skip).** Follow `references/context-sweep.md`: the
   target's content contract, then the flow around it, sibling screens, every
   tab root, shared components, past rounds, and the rules in force. Decide the
   mode (congruent / explore / mixed) from the user's words. Write
   `TOPIC_DIR/context.md` with the shared data fixture. In round 2+ reuse it and
   add the new feedback. A redesign that ignores the neighbouring screens is
   the main failure this step prevents.

3. **Plan ten, as one set.** Follow `references/variations.md`: ten one-line
   theses on named axes, each pair different on at least two axes. Round 1
   diverges; round 2+ converges on the pick (#1 is always "Faithful": the pick
   with the feedback applied literally). Default count is 10 unless the user
   gives a number. Write `ROUND_DIR/manifest.json` with names, ideas, tags.

4. **Render.** Each variation is a standalone file (`references/mockup-craft.md`)
   on `../tokens.css` + `screen.css`, with real icons, real images, and the
   shared fixture. With the Agent tool available, dispatch five subagents × two
   variations in one message using the brief in `references/variations.md`;
   otherwise write them yourself. Designing one part of a screen: the rest of
   the screen comes from shared includes so every frame differs only in that
   part (mockup-craft.md). Add the current design as the `current` frame: a
   simulator screenshot, or an HTML recreation from the code when no simulator
   shows it.

5. **Check (bounded: one pass).** Run the pre-send checklist in
   `references/principles.md` against every variation, then
   `studio.sh check ROUND_DIR`. If a browser tool is available, open the URL
   and screenshot the grid once. Fix everything found in one batch, then run
   the final `check`: when the round passes, it opens the gallery in the
   user's default browser, so the round is already on their screen when the
   message arrives (`DESIGN_STUDIO_NO_OPEN=1` turns that off). If a
   file-sending tool is available (e.g. SendUserFile in the Claude desktop
   app), run `studio.sh sheets ROUND_DIR` and send the two contact-sheet
   images too, for reviewing away from the desk.

6. **Send the link, then ask.** Set `agentPick` and `predictedPick` in the
   manifest (the gallery badges them). The message **opens with the link**:

   > **Round N · <title> →** http://localhost:4545/<project>/<topic>/rN/
   >
   > 1 Name · 2 Name · 3 Name · … · 10 Name (wildcards marked)

   Add the LAN link on its own line when `studio.sh` printed one (phone
   viewing is on). Then, in the same turn, call **AskUserQuestion**. Question:
   "Which one should round N+1 build on?" Header: "Pick". Options, in this order:
   1. `#<agentPick> <Name> (Recommended)`: why it does the job best, citing a principle or the screen's job.
   2. `#<predictedPick> <Name>, your likely pick`: the TASTE.md evidence behind the prediction. If it's the same variation as #1, offer the runner-up here instead.
   3. A real third choice: the runner-up, or a mix of the two picks ("#3 top + #7 bottom").
   4. Round 2+ only, when feedback is getting small: `Build #<n>`: finalise it.

   Say one line above the question: "Type feedback in the answer box. It goes
   straight into the next round."

7. **Next round, or build.** The answer is the pick; any typed text (the
   "Other" box or the option notes) is the feedback, recorded verbatim in the
   next manifest's `feedback`, with `parent` set to the pick. Append the round
   to TASTE.md's log (shown, both predictions, the pick, the feedback), and
   update "Patterns" when the log contradicts them. A pick with change requests
   goes to step 3. **A pick with no change requests means build it**: go to
   step 8 rather than running another converging round.

8. **Finalise.** On "build it", a `Build` pick, or a bare pick: write
   `ROUND_DIR/spec.md` (the chosen variation, the feedback trail, every element
   mapped to the project's components, any new component or variant needed,
   copy to add, and the states: empty, loading, error, long content). Then
   follow the adapter's build path, or build it in the project's existing
   components and tokens. Don't start code before this pick.

## Web mode (websites, landing pages, marketing sites)

On when the adapter says `surface: web` or the brief names a website, landing
page, marketing site or web page. Read `references/web.md` and
`references/web-craft.md` before step 1. They take the place of
mockup-craft.md and the phone-only parts of principles.md. In short:

- `studio.sh new <project> <topic> --web`: the round gets the web gallery
  (desktop + phone frames, a Desktop/Tablet/Phone switch, page tabs, live
  links) and `web.css`.
- A variation is a folder `vNN/` with its own `tokens.css` and `site.css` on
  top of the topic's brand `tokens.css`, and real pages that scroll and link.
- Rounds are staged (`manifest.stage`): `directions` (10 full home pages),
  `converge`, then `system` (the pick across every template, as a site). From
  `converge` on, the pick question offers `System proof #N`. A bare pick in
  `converge` means system proof; a bare pick in `system` means build.
- `check` and `sheets` detect `"surface": "web"` and run the web checks and
  the web contact sheets (`heroes.png`, full-length `sheet-N.png`,
  `pages-vNN.png`).
- TASTE.md is shared; log web rounds with `web` in the Project / topic column.

## Paywall mode (paywalls, subscription and offer screens)

On when the adapter says `surface: paywall` or the brief names a paywall,
subscription screen, upgrade screen, offer screen or exit offer. Read
`references/paywall.md` before step 1, and `references/paywall-craft.md`,
`references/paywall-playbook.md` and `references/paywall-archetypes.md` as
it directs. In short:

- `studio.sh new <project> <topic> --paywall`: the round gets the paywall
  gallery (a state switch across every card) and `paywall.css`.
- A variation is a folder `vNN/` with one file per state in
  `manifest.states` (`main`, `alt-plan`, `exit`, `friend`…).
- Stages: `concepts` (ten archetypes), `concept` (one archetype ten ways),
  `converge`, and `ab` (a control plus one-variable variants for an
  experiment). A bare pick still means build; `Explore #N` and
  `A/B set from #N` are explicit options.
- The playbook's rubric decides `agentPick`; the adapter's `paywall-data`
  puts live numbers in `performance.md` so the pick can cite them.
- `check` enforces the legal markers, states and real proof; `sheets` writes
  one set per state.

## Rules that hold every round

- The link goes out as soon as the round renders, as a localhost URL the user
  can click, and the round is already open in their browser (`studio.sh check`
  opens it). Not a file path or an artifact; contact-sheet images go alongside
  the link, never instead of it.
- Ten variations means ten distinct ideas. Swapping colour, radius or font
  doesn't make a new variation.
- Congruent variations use the neighbours' surfaces, headers, type roles,
  colour roles, icons and spacing. Wildcards are labelled, and they state their ripple:
  which other screens would change to match.
- Every variation passes the principles checklist, wildcards included.
- Same fixture data in every frame; one long string on purpose.
- Old rounds stay put; each round is a new `rN/` dir, so every link keeps working.

## Server notes

One Python server serves all of `~/design-studio` on port 4545
(`DESIGN_STUDIO_PORT` to change it, `DESIGN_STUDIO_ROOT` to move the folder).
It binds to 127.0.0.1, so only this computer can open it. To view rounds on a
phone on the same Wi-Fi, the user sets `DESIGN_STUDIO_BIND=0.0.0.0` (anyone on
that network can then open the mockups; only suggest it on a trusted network).
`studio.sh serve` is idempotent. If the sandbox blocks binding the port, rerun
the same command with the sandbox disabled; it only serves mockups.

## Common mistakes

| Mistake | Fix |
|---|---|
| Designing from the target file alone | The sweep's neighbour table is required input for step 3 |
| 4–6 "variations" that are one idea re-skinned | Plan theses on axes first; replace near-twins before rendering |
| Ending with a prose question or a list of letters | AskUserQuestion with both picks, every round |
| Round 2 that wanders away from the pick | #1 Faithful + nine refinements of *that* design |
| Another round after a bare pick | A pick with no change requests means build it |
| Dropping the feedback between rounds | It's quoted in the manifest and shown on the gallery |
| Mockups that look like a web page | Native patterns, real tokens, icons and images: mockup-craft.md |
| Icons linked straight from a CDN | Browsers block cross-origin `<use href>`; use the topic's local `icons.svg` |
| Endless self-QA | One check pass, one fix batch, send |
| Judging a website on a static hero | Web mode renders full-length pages; the premium feel lives below the fold |
| Ten web directions on one type system | Each direction owns its `vNN/tokens.css`; type + grid are axes, not skins |
| System-stage pages drifting from the pick | Pages build on the direction's `tokens.css`/`site.css`/`chrome.js` and never edit them |
| Ten paywalls that are one archetype re-skinned | A `concepts` round takes ten archetypes from the catalog |
| An A/B variant that changes two things | One variable per variant, named in `variable`; everything else stays the control's |
| Testimonials or ratings written for the mockup | Proof comes only from context.md's list; `check` fails anything else |
| Judging a paywall with only the default plan selected | Every state in `manifest.states`; flip the gallery's state switch |
