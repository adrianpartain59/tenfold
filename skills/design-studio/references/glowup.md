# Glow-up mode: how the loop changes

Glow-up turns a vibe-coded app (Lovable, v0, Bolt, Replit or Cursor output,
or an Expo app built the same way) into a designed one. The other modes
design one surface inside an app that already has a system and treat its
neighbouring screens as the authority. Glow-up inverts that: the existing
look is the thing being replaced, there is no system to inherit, and the job
is the whole app. Everything in SKILL.md holds unless this file says
otherwise.

Read with `glowup-craft.md` (what a direction contains), and
`mockup-craft.md` for an app or `web-craft.md` for a web app: glow-up is a
job on top of those frames, not a surface of its own.

## When it's on

The adapter says `mode: glowup`, or the brief says glow-up, makeover, "make
it look professional", "it looks vibe-coded" or "AI-made", "give it a real
design", "rebrand the app", or asks for themes for the whole app. Start the
topic with:

```bash
bash <SKILL_DIR>/scripts/studio.sh new <project> <topic> --glowup        # an app
bash <SKILL_DIR>/scripts/studio.sh new <project> <topic> --glowup --web  # a web app
```

It prints `MODE glowup` (and `SURFACE web`), and the round gets the theme
board gallery plus both `screen.css` and `web.css`.

## Stages

`manifest.stage` names the stage.

| Stage | What happens | User sees | Ends when |
|---|---|---|---|
| `intake` | Read the code, UI copy, README and live URL. Write `brief.md` | One confirm-or-correct question | Brief confirmed |
| `audit` | Screenshot every route; run `entropy.py` and `tells_lint.py`; pick the four key screens | Before tab | Automatic |
| `research` | 8 to 12 comparables; write `category.md` | Category tab | Automatic |
| `directions` (r1) | Ten themes, each on the same four key screens | Theme board | A pick |
| `converge` (r2+) | #1 Faithful plus refinements on the four screens | Theme board | A bare pick, or `System proof #N` |
| `system` | The pick across every route, light and dark, with empty, loading and error states | Full-app board | `Apply #N` |
| `apply` | Staged commits on `glowup/<topic>` in the user's repo | One board per stage | Each stage approved, flagged or reverted |

- Intake and audit run in one turn, so the first thing the user sees is the
  brief question.
- After the answer, research and r1 run back to back. The gallery opens with
  Before, Category and Directions together.
- A bare pick in `directions` or `converge` goes to `system`, not to apply.
  The theme isn't approved until it has been seen on every route.

## Intake

Decide the surface from `package.json`:

| Dependencies or files | Surface |
|---|---|
| `next`, `vite`, `react-router`, `tailwindcss`, shadcn's `components.json` | web |
| `expo`, `react-native`, `nativewind` | app |

Build the route inventory every later stage uses: Next `app/` or `pages/`,
react-router route definitions, expo-router's `app/`, or the navigator
files.

Write `TOPIC_DIR/brief.md`: what the product sells, who buys it, the price
tier, the category, five to eight comparable apps, and the one action the
app exists to drive. Then ask with AskUserQuestion. Question: "Is this the
right brief for the glow-up?" Options, in this order:

1. `Brief is right (Recommended)`
2. `Category is wrong`
3. `Buyer is wrong`

Typed corrections go into `brief.md` verbatim.

## Audit

Measure the app before touching it. Both outputs go in the topic dir:

```bash
python3 <SKILL_DIR>/scripts/entropy.py <repo> --out TOPIC_DIR/entropy-before.json
python3 <SKILL_DIR>/scripts/tells_lint.py <repo> --json TOPIC_DIR/tells-before.json
```

`entropy.py` prints a headline such as `ENTROPY 33 (11 colours · 5 font
sizes · 3 weights · 8 spacing values · 4 radii · 2 shadows)`, and
`tells_lint.py` ends with `TELLS 32 (...)`. Put both in the manifest's
`before.headline` and `before.summary`.

Before screenshots of every route, saved as `TOPIC_DIR/before/<id>.png`:

- web: headless Chrome at 390 and 1440 wide against the running dev server;
- app: `xcrun simctl io booted screenshot` when a simulator is booted, else
  Expo web through headless Chrome when the project supports
  react-native-web, else HTML recreations from the code, labelled as such.

Pick the four key screens by traffic and variety: the main screen
(dashboard or home), the densest list or table, the main form, and the
weakest empty or onboarding state. They are `s1` to `s4` for the whole
topic.

Write `TOPIC_DIR/context.md` with the key screens and their templates, the
content contract for each (every datum, action and state), the fixture
(including one deliberately long string), and a `## UI strings` section
listing the real strings the app shows. `check` reads each direction's voice
strings from that section.

## Category research

Follow `category-research.md`. It writes `TOPIC_DIR/category.md`, which the
manifest names as `"category": "../category.md"` and the gallery shows on
the Category tab.

## Directions and converge

Round 1 is ten directions: three that follow category conventions, done
well; five that stay in the category with a distinctive twist; two labelled
wildcards that break the category. The axes are in `variations.md` under
"Glow-up mode axes". Every pair differs on at least two.

Each direction is a folder `vNN/` with `theme.json`, `tokens.css` and
`s1.html` to `s4.html`. Render them with five subagents × two directions,
using the brief in `variations.md` with this "Read first":
`glowup-craft.md`, `mockup-craft.md` (app) or `web-craft.md` (web),
`principles.md`, `context.md` and `category.md`. Each subagent:

1. writes `vNN/theme.json`;
2. runs `python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --css --out vNN/tokens.css`;
3. writes the four screens on those tokens.

Each manifest entry carries `notes.market` (why it fits this market, citing
a numbered line in category.md), `notes.signature`, `notes.convention`,
`notes.different` and `notes.ripple`.

Converge rounds keep the four key screens: #1 Faithful is the pick with the
feedback applied literally, and the rest refine it.

Then one check pass and one fix batch, as in every mode:

```bash
bash <SKILL_DIR>/scripts/studio.sh check ROUND_DIR
bash <SKILL_DIR>/scripts/studio.sh sheets ROUND_DIR
```

`sheets` writes `sheet-before.png` and one `sheet-vNN.png` per direction.

## System

One or two variations, rendered on every route in the intake inventory as
`vNN/routes/<id>.html`, with the empty, loading and error states of routes
that have them, in light and dark. The direction's `theme.json` and
`tokens.css` carry over unchanged. Design the brand surface here too: the
wordmark, app icon and favicon as images in `vNN/brand/`.

## Apply

Only after `Apply #N`. Follow `apply-web.md` for a web app and
`apply-native.md` for an app. Four stages, one board each:

1. theme layer;
2. shared components;
3. routes, about five per commit;
4. brand surface.

Hard limits: no changes to data fetching, state, routing, API calls or test
IDs. The diff touches styles, render markup, copy strings and assets.

Each stage gets its own round dir with `"stage": "apply"` and an `apply`
block (see the manifest reference). It goes out with the same link and
question as any round.

## From screenshots

Glow-up runs from screenshots alone when there is no codebase: a founder
with a Lovable link, a phone screenshot, a page they can't share the repo
for. The directions are rebuilt from a content contract and a fixture
anyway, so the core of the loop is unchanged. Write `"source": "images"` in
every manifest of the topic. What changes:

- **Intake.** Ask for three or four screenshots of different screens, in
  the order of the four key screens. Accept one, and say plainly that the
  other key screens will be designed fresh. Read the product, buyer and
  category from the screens, and the surface from the shape: a portrait
  phone screenshot is an app, a wide one is web. Both go in the brief
  question.
- **Key screens.** The uploaded screens are `s1` onwards. A key screen
  with no screenshot is designed from the brief and marked
  `"invented": true` in `manifest.screens`; the gallery labels it.
- **Audit.** Copy the screenshots to `TOPIC_DIR/before/<sid>.png`, then
  measure the colours they really use:

  ```bash
  python3 <SKILL_DIR>/scripts/image_audit.py TOPIC_DIR/before/*.png --out TOPIC_DIR/image-audit.json
  ```

  It prints a headline such as `IMAGE-AUDIT 9 colours across 4 screens ·
  Tailwind gray-500, indigo-600 · cool greys`; use it as `before.headline`.
  Judge the visible tells by eye against the lists in `glowup-craft.md`
  (gradient text, uniform cards, sparkle icons, centred everything, "Oops",
  placeholder-only fields, straight quotes) and write what you find into
  context.md and `before.summary`. Spacing and type-size counts and the
  code-only tells (focus rings, reduced motion, validation timing) are out
  of reach; say so in context.md rather than guessing.
- **Content contract and UI strings.** Transcribe every datum, action and
  string visible on each screenshot into context.md. That transcription is
  the fixture and the source of the voice strings, so copy it exactly.
- **Research, directions, converge.** Unchanged.
- **System.** The uploaded screens plus their designed empty, loading and
  error states; `routes` lists them.
- **Apply.** Not available: `check` fails an apply round on an
  image-sourced topic. The topic ends at handoff.

## Handoff

The last stage for an image-sourced topic, and an option for a code topic
when the user wants the tokens without a branch. After the system pick
(`Handoff #N`), write the files into the round:

```bash
python3 <SKILL_DIR>/scripts/handoff.py <system round>/vNN/theme.json ROUND_DIR/handoff
```

It writes `tokens.css`, `theme.css`, `tailwind-v4.css`,
`tailwind.config.v3.js`, `shadcn.css`, `shadcn-hsl.css`, `theme.ts` and
`prompt.md`, a brief the user pastes into Lovable, v0, Bolt or Cursor with
those files. Then write `ROUND_DIR/handoff/screens.md` yourself: one
`## <screen label>` section per uploaded screen, naming its layout template,
what moves, what the copy becomes, and which states to add. The manifest:

```json
{
  "project": "<project>", "topic": "<topic>", "title": "<App> glow-up", "round": 4,
  "mode": "glowup", "surface": "web", "source": "images", "stage": "handoff",
  "parent": { "round": 3, "id": "v01", "name": "Ledger" },
  "screens": [{ "id": "s1", "label": "Dashboard" }, { "id": "s4", "label": "Empty state", "invented": true }],
  "handoff": { "dir": "handoff", "theme": "../r3/v01/theme.json" }
}
```

`check` verifies every file exists, `tokens.css` matches the theme, and
`screens.md` has a section for every screen that wasn't invented. The
gallery's Handoff tab shows `prompt.md`, `screens.md` and download links.

## Pick question

- `directions` and `converge`: the usual four options. From `converge` on,
  option 3 becomes `System proof #N`.
- `system`: `Apply #N (Recommended)`, a converge option, and a mix. On an
  image-sourced topic, `Handoff #N (Recommended)` takes Apply's place; a
  code topic can offer it as the third option.
- Every apply board: `Approve stage (Recommended)`, `Flag a route` (typed
  route names and what's wrong), `Revert stage`.

## TASTE.md

Log glow-up rounds in the same `~/design-studio/TASTE.md` with `glowup` in
the Project / topic column. `predictedPick` reads the glow-up rows when
there are any; with none, say the prediction comes from the brief alone.

## Manifest reference

Directions (and converge, with `"stage": "converge"` and a `parent`):

```json
{
  "project": "<project>", "topic": "<topic>", "title": "<App> glow-up", "round": 1,
  "mode": "glowup", "surface": "web", "stage": "directions",
  "brief": "The job and the constraint that matters most.",
  "agentPick": "v01", "predictedPick": "v02",
  "screens": [
    { "id": "s1", "label": "Dashboard" }, { "id": "s2", "label": "Notes list" },
    { "id": "s3", "label": "New note" }, { "id": "s4", "label": "Empty state" }
  ],
  "before": {
    "s1": "../before/s1.png", "s2": "../before/s2.png", "s3": "../before/s3.png", "s4": "../before/s4.png",
    "headline": "33 values: 11 colours · 5 font sizes · 3 weights · 8 spacing values · 4 radii · 2 shadows",
    "summary": "32 tells (fingerprint 9 · forms 9 · copy 8 · a11y 4 · loading 2)"
  },
  "category": "../category.md",
  "variations": [
    { "id": "v01", "dir": "v01", "name": "Ledger", "idea": "One-line thesis.", "tags": ["conventional"],
      "notes": { "market": "Why it fits, citing category.md", "signature": "The ownable detail", "convention": "What it keeps", "different": "What it changes", "ripple": "What else changes to match" } }
  ]
}
```

System:

```json
{
  "project": "<project>", "topic": "<topic>", "title": "<App> glow-up", "round": 2,
  "mode": "glowup", "surface": "web", "stage": "system",
  "parent": { "round": 1, "id": "v01", "name": "Ledger" },
  "agentPick": "v01", "predictedPick": "v01",
  "screens": [{ "id": "s1", "label": "Dashboard" }],
  "routes": [{ "id": "home", "label": "Home" }, { "id": "settings", "label": "Settings" }],
  "variations": [{ "id": "v01", "dir": "v01", "name": "Ledger", "idea": "Ledger on every route.", "notes": { "market": "...", "signature": "..." } }]
}
```

Apply (one per stage):

```json
{
  "project": "<project>", "topic": "<topic>", "title": "<App> glow-up", "round": 3,
  "mode": "glowup", "surface": "web", "stage": "apply",
  "parent": { "round": 2, "id": "v01", "name": "Ledger" },
  "apply": {
    "stage": 3, "branch": "glowup/<topic>", "base": "<commit>",
    "themeFiles": ["src/index.css", "tailwind.config.js"],
    "entropyBefore": "../entropy-before.json", "entropyAfter": "entropy-after.json",
    "tellsBefore": "../tells-before.json", "tellsAfter": "tells-after.json",
    "build": "pass", "reverted": false,
    "headline": "Entropy 33 → 15 · tells 32 → 9",
    "routes": [{ "id": "home", "label": "Home", "before": "../before/s1.png", "after": "after/home.png" }],
    "followUps": ["<rule> in <file>:<line> changes behaviour, so apply left it alone"]
  }
}
```

What `check` reads:

- `mode` routes the round to `glowup_check.py`.
- `surface` picks the frame stylesheet each screen must link.
- `screens` must be `s1` to `s4`.
- `routes` are required in `system`.
- In `apply`:
  - `entropyBefore` and `entropyAfter` must not rise, and must fall from
    stage 3 on;
  - `tellsBefore` and `tellsAfter` must not rise;
  - every colour left in `entropyAfter` must sit in one of the
    `themeFiles`;
  - `build: "fail"` needs `reverted: true`;
  - every route needs a `before` and an `after` image.
