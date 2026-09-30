# Web mode: how the loop changes

Web mode designs a website, not a screen. Read this with `web-craft.md` (how
a page is built). Everything in SKILL.md holds unless this file says otherwise.

## When it's on

The adapter says `surface: web`, or the brief names a website, landing page,
marketing site or web page. Start every round with
`studio.sh new <project> <topic> --web`.

## Stages

A website is redesigned whole, but judging ten whole sites is slow and they
end up judged on their home page anyway. So rounds are staged, and
`manifest.stage` names the stage.

| Stage | Each variation | Count | Ends when |
|---|---|---|---|
| `directions` (r1) | One full-length home page with its own design system (`vNN/tokens.css`) | 10 unless the user gives a number | The user picks (with or without feedback) |
| `converge` (r2+) | #1 Faithful + refinements of the pick, home only | 10, dropping to 4 to 6 as feedback narrows | A bare pick, or `System proof #N` |
| `system` | The pick (or two finalists) across every template in the adapter, linked into a working site | 1 to 2 | A bare pick = build |

The pick question adds these options. From `converge` on:
`System proof #N`: "see #N across every page before building". In `system`:
`Build #N`. A bare pick in `directions` or `converge` goes to the next stage,
not to build. The site isn't approved until its templates have been seen
together.

## Context sweep for a site

Replace the neighbour table with a site map:

1. **Every template** the adapter lists, with one real URL each. Open the live
   ones and note what content each must hold (the content contract).
2. **The conversion path:** the one action the site exists to drive, and
   every place it appears.
3. **The nav and footer** as they are today: items, legal links, store
   badges.
4. **Invariants:** URLs, SEO headings and schema, legal text, claims that
   need a source. A direction may restyle these but never change them.
5. **The app** (when the site sells an app): its tokens, art, mascot and
   screens. The adapter's `base-tokens` command exports them into
   `TOPIC_DIR/tokens.css`. This file is the brand base every direction shares.
6. **Proof:** real ratings, review counts, user counts and quotes, with where
   each came from. Nothing else may appear as a claim.

Write `TOPIC_DIR/context.md` with a **content fixture** instead of a data
fixture: the hero line candidates, the section list with real copy, proof
numbers with sources, the store links, and the longest real string
(a long guide title or FAQ question). Every direction uses the same fixture.

## Rendering in parallel

- `directions` / `converge`: five subagents × two directions, using the
  brief from `variations.md`. Change the brief's "Read first" to `web.md`,
  `web-craft.md`, `principles.md` (web checklist), and `context.md`. Each
  subagent writes `vNN/tokens.css`, `vNN/site.css` and `vNN/index.html` for
  its two directions.
- `system`: first, one subagent writes the direction's system: `tokens.css`,
  `site.css` and `chrome.js` (nav + footer) taken from the picked home page.
  Then three or four page subagents, each given 3 to 5 templates, write pages
  on that system and never edit it. If a page needs a new component, it is
  added to its own `<style>` block and reported back. The main agent then
  promotes shared ones into `site.css` in the one fix batch.

## manifest.json (web)

```json
{
  "project": "acme", "topic": "website", "title": "acme.com redesign", "round": 1,
  "surface": "web", "stage": "directions",
  "brief": "The job and the constraint that matters most.",
  "agentPick": "v04", "predictedPick": "v09",
  "current": { "file": "../current/index.html", "label": "Today" },
  "templates": [{ "id": "home", "label": "Home" }, { "id": "guide", "label": "Guide article" }],
  "variations": [
    {
      "id": "v01", "file": "v01/index.html", "name": "Sky Scroll",
      "idea": "One-line thesis.",
      "tags": ["congruent"],
      "pages": [{ "template": "home", "file": "v01/index.html" }],
      "notes": { "type": "Display and body faces, scale", "story": "Section order", "art": "How the product and brand art appear", "build": "What it needs that the site doesn't have" }
    }
  ]
}
```

`current` is optional: a saved copy of today's page (`file`) or a full-page
screenshot (`image`). `templates` and multi-entry `pages` are only needed in
the `system` stage.

## Check, sheets, send

`studio.sh check ROUND_DIR` runs the web checks when the manifest says
`"surface": "web"`: pages exist, every page links its direction's
`tokens.css`, local links resolve (including those in `chrome.js`), no lorem
ipsum, and in `system` every template is covered. `studio.sh sheets
ROUND_DIR` writes `heroes.png` (every first screen at desktop),
`sheet-N.png` (five directions as full-length phone pages), and in `system`
`pages-vNN.png`. Phone pages are drawn as a stack of 844 px screens, so `vh`
units look the way they do on a real phone. Send heroes and sheets with the
link.

## Finalise

On `Build #N` write `ROUND_DIR/spec.md`. It covers:

- the direction's tokens as a table
- the nav/footer
- each template mapped to the project's real component or route
- new components
- copy to add
- states (long titles, empty lists, 404)
- the build order: tokens, then nav/footer, then home, then the rest

Then follow the adapter's `build` path.

## Taste log

Web rounds go in the same `~/design-studio/TASTE.md`, with `web` in the
Project / topic column (`acme / web home`), so marketing-surface patterns
from app rounds inform the prediction.
