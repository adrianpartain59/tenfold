# Getting 10 variations that are actually different

Quantity only helps if the variations spread out. Ten near-twins are one design
shown ten times. Plan all ten as one set before rendering any of them.

## Round 1: diverge on named axes

Pick the axes that matter for this screen, then give each variation a distinct
position on them. Every pair of variations differs on **at least two axes**.
Differences in colour, corner radius, or font alone don't count.

| Axis | Positions (examples) |
|---|---|
| Hero (what answers the job) | one big number · a ring/gauge · a chart · the mascot's line · a next-action card · a timeline "now" marker |
| Structure | single scroll of sections · bento/grid · one dominant card + list · timeline · segmented tabs · horizontal pager · checklist |
| Density | glanceable (3–4 facts) · balanced · dense/pro (everything visible) |
| Interaction | read-only + drill-in · edit in place · sheet editor · quick actions/chips · swipe rows |
| Data form | numbers · bars · rings · sparkline/chart · text sentence ("You're 38 g short on protein") |
| Grouping | by time (morning→night) · by type (dose / food / body) · by priority (needs action first) · by goal |
| Tone | utilitarian · editorial (big type, whitespace) · mascot-led/playful · coach (instructional) |
| Disclosure | all on one screen · summary + "see all" doors · progressive (expand in place) |

Write the plan as ten one-line theses first, e.g.
"3 · Checklist: the day as tasks, each row completes in place; numbers secondary."
Read the list back and replace any thesis a user would call "the same as #N".

Names are one or two evocative words (Ledger, Rings, Chapters, Timeline,
Coach) so the user can refer to them. Number them 1–10 and keep numbers stable
within a round.

Order the set so the gallery reads well: congruent ones first, safest to
boldest, wildcards last.

### Web mode axes

In web mode (`web.md`) each direction is a design system, so the axes are
about the whole page. Every pair still differs on at least two, and
type or colour alone doesn't count.

| Axis | Positions (examples) |
|---|---|
| Hero concept | product screen hero · mascot/brand-art stage · big claim typography · live demo · proof-first (rating, results) · a transformation/before-after |
| Narrative order | problem → answer → proof · feature tour · a day in the life · audience split (who is it for) · proof early vs late |
| Grid and density | airy editorial · dense bento · alternating split rows · single centred column · full-bleed bands |
| Type personality | geometric grotesk · humanist sans · serif display + sans body · condensed display · rounded friendly |
| Art direction | device-framed screens · floating UI fragments · mascot scenes · illustration · photography (only if provided) |
| Colour field | light ground · dark ground · brand-colour bands · the app's own sky/ground |
| Motion concept | still · reveal on scroll · one hero animation · interactive demo |

### Paywall mode axes

In paywall mode (`paywall.md`) a `concepts` round spreads across the
archetype axis first; a `concept` round holds it fixed and uses the
archetype's own Axes from `paywall-archetypes.md` plus these.

| Axis | Positions (examples) |
|---|---|
| Archetype (`concepts` only) | the catalog's entries |
| Hero | outcome headline · the user's own goal or number · product screen · coach or mascot · proof as the headline · video |
| Proof | none · rating + count · one long quote · quote wall · user count · expert or press |
| Pricing module | single price · plan cards · plan list · trial toggle · comparison table |
| Trial presentation | one line · timeline · calendar · reminder promise · no trial |
| CTA | outcome copy · trial copy · price copy · sticky bottom · inline |
| Density | one screen, no scroll · scroll with a sticky CTA · multi-step |
| Tone | clinical trust · warm coach · premium editorial · playful |

### Glow-up mode axes

In glow-up mode (`glowup.md`) each direction is a whole theme
(`theme.json`), shown on the same four key screens. Every pair differs on
at least two axes; type or colour alone doesn't count.

| Axis | Positions (examples) |
|---|---|
| Category stance | conventional · conventional with a twist · category-breaking |
| Personality | clinical · warm · editorial · playful · technical · premium |
| Layout system | airy editorial column · balanced cards · dense pro grid · split panes |
| Type personality | geometric grotesk · humanist sans · serif display + sans · condensed display · rounded |
| Colour field | light warm · light cool · dark · brand-tinted ground |
| Shape | sharp · soft · pill · mixed by role |
| Depth | flat with borders · soft shadow · layered surfaces |
| Signature | a shape motif · a corner or edge treatment · an illustration style · a texture inside a bounded element · a type treatment |
| Voice | plain · warm coach · expert · playful |

Round 1 mix of ten: three conventional done well, five in-category with a
distinctive twist, two labelled wildcards that break the category.

A wildcard breaks the category, not the platform. Its world can take over the
type, shape, signature, art, voice and the ground's colour; it still ships as
a real phone app (or website): a quiet flat ground, native navigation,
44pt targets, legible text. Each wildcard writes `notes.platform`: the
platform conventions it keeps and any it breaks, with the reason. "Fits the
theme" is not a reason; a break has to make the app better to use.

## Round 2+: converge on the pick

The user picked #N (possibly with feedback, possibly "N's top with M's bottom").
The next ten are all versions of that pick. The pick's identity (its hero,
structure, tone) stays; what varies is how well it's executed.

- **#1 Faithful:** the pick with the feedback applied literally, nothing else
  changed. This is the control for the round.
- **#2–#10:** each takes the pick + feedback and pushes one refinement
  dimension further than #1, e.g.:
  - hierarchy: a different element promoted/demoted
  - density: tighter / airier
  - component treatment: ring ↔ bar ↔ number; chips ↔ rows
  - the feedback pushed further than asked (if they said "bigger", go much bigger)
  - the feedback solved a different way than literally asked
  - a quieter version (fewer colours, less chrome)
  - a bolder version (stronger type contrast, more colour or mascot)
  - an interaction change (edit in place vs sheet)
  - a layout rearrangement of the same parts
  - a merge with the runner-up from the previous round
- Feedback beats the pick: if the pick contradicts the feedback, the feedback wins.
- If the user says "none of these", treat it as a new round 1 with their words
  as the brief, not as a refinement.
- If the answer is feedback with no pick (a new requirement, a priority, a
  constraint they forgot), don't re-ask. Add it to context.md, then run the next
  round as a **re-brief**: re-run the strongest directions from the last round
  with the requirement built into each (name the source variation in each idea,
  "From r1 #4: …"), and replace the ones the requirement rules out.
- Converging: when feedback is getting small ("a bit more spacing"), the round
  can drop to 4–6 variations. Say so in the message. Never drop below 10 in a
  diverging round to save effort.

## Mixes

"#3's header with #7's list" is a valid pick. The next round's #1 Faithful is the
literal mix; the rest vary the seam between the two parts as well as the parts.

## Predicting the user's pick

Before sending, name two variations:

- **agentPick:** the one you'd ship, judged on the principles and the job.
- **predictedPick:** the one you think the user will pick, judged on TASTE.md
  (past picks, stated reasons, the direction feedback has been moving). Cite
  the evidence in the question, e.g. "you've picked the ring-led option in 2 of
  3 past rounds".

They are allowed to differ, and that's more useful than when they agree. If
they are the same, say so and offer the runner-up as the second option.

## manifest.json (the gallery reads this)

```json
{
  "project": "my-app",
  "topic": "home-screen",
  "title": "Home screen",
  "round": 2,
  "mode": "congruent",
  "brief": "First paragraph of context.md: the job and the constraint that matters most.",
  "feedback": "The user's words that this round answers (omit in round 1).",
  "parent": { "round": 1, "id": "v07", "n": 7, "name": "Chapters" },
  "agentPick": "v03",
  "predictedPick": "v07",
  "current": { "image": "../ref-home.png", "label": "Today" },
  "variations": [
    {
      "id": "v01",
      "file": "v01.html",
      "name": "Faithful",
      "idea": "One-line thesis: what this variation bets on.",
      "tags": ["congruent"],
      "notes": {
        "changes": "What moved, grew, shrank or went away versus today.",
        "keeps": "What deliberately stays the same.",
        "build": "Which existing primitives it uses; any new primitive or variant it needs.",
        "ripple": "Wildcards only: which other screens would change to match."
      }
    }
  ]
}
```

Tags: `congruent`, `wildcard`, and optionally `new-primitive` when building it
needs something the design system doesn't have yet. `current` is optional: use
`image` for a sim screenshot or `file` for an HTML recreation.

## Parallel rendering with subagents

For ten variations, the main agent plans (context.md, fixture, the ten theses,
manifest) and subagents render. Five subagents × two variations each is the
default split. Each subagent gets a self-contained brief:

```text
Render two variations for the design round in <ROUND_DIR>.
Read first: <TOPIC_DIR>/context.md (job, content contract, neighbours, rules,
fixture), <SKILL_DIR>/references/mockup-craft.md (file template and rules),
<SKILL_DIR>/references/principles.md (run the pre-send checklist on your two).
Tokens: ../tokens.css. Base: screen.css. Icons: ../icons.svg (ids in ../icons.txt).
Images: ../img/.

Variation <id-a> "<Name>": <thesis>. Tag: <congruent|wildcard>.
Variation <id-b> "<Name>": <thesis>. Tag: <congruent|wildcard>.
Every other variation in this round, so you stay distinct from them: <list of the other 8 theses>.

Write <id-a>.html and <id-b>.html in <ROUND_DIR>. Do not touch manifest.json or
any other file. Reply with, for each: name, one-line idea, notes.changes,
notes.keeps, notes.build, notes.ripple (wildcards), and any checklist item it
fails and why.
```

The main agent then merges the replies into manifest.json, looks at the whole
gallery once, fixes anything broken or too similar, and sends the link.
