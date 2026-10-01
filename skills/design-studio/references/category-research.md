# Category research

A professional look depends on the market. A legal tool, a kids' app and a
fitness app earn trust with different type, colour and density. Research
finds what signals trust in this category and what nobody in it is doing,
so every direction can say why it fits. Budget about 20 tool calls; fan out
to a subagent when the Agent tool is available.

## Choosing comparables

Start from the comparables in `brief.md`. Aim for eight to twelve:

- the direct competitors the buyer would compare against;
- two or three adjacent apps the same buyer already uses every day;
- one or two aspirational apps from outside the category, for craft only.

Skip apps that are themselves showcases or templates from an AI app builder
(Lovable, v0, Bolt galleries). They share the look you are replacing.

## Gathering screens

Web apps: open each home page and one product page with the available
browser tool. Take one desktop and one 390-wide screenshot of each and save
them as `TOPIC_DIR/category/<slug>-<n>.png`.

Mobile apps: use the public iTunes Search API, no key needed:

```bash
curl -s "https://itunes.apple.com/search?term=<name>&entity=software&limit=1" | python3 -c 'import json,sys; r=json.load(sys.stdin)["results"]; print("\n".join(r[0]["screenshotUrls"]) if r else "")'
```

Download the first three URLs into `TOPIC_DIR/category/`. Check the result's
`trackName` matches the app you meant.

No sign-ins and no paid content. When a comparable can't be reached, say so
in category.md and move on; don't describe it from memory.

## What to record

One row per comparable:

| Column | How to judge it |
|---|---|
| App | Name, and whether it is direct, adjacent or aspirational |
| Type | Display and body faces, or their kind (geometric grotesk, humanist sans, serif display) |
| Colour field | Light, dark or brand-coloured ground; where the accent appears |
| Neutral | Warm, cool or untinted greys |
| Shape | Sharp, soft, pill, or mixed by role |
| Density | Airy, balanced or dense, on the screens you saw |
| Tone | Clinical, warm, editorial, playful, technical or premium, from type and copy together |
| Signature | The one detail you'd recognise it by, or "none" |
| Source | Which screenshots or pages the row came from |

## Table stakes and white space

**Table stakes** are the conventions three or more comparables share and a
buyer would miss if they were gone: the things that make an app look like
it belongs in this category. Directions that break one must say so.

**White space** is what none of the comparables do and the brief supports:
an open type personality, a colour field nobody owns, a tone the category
lacks. This is where the distinctive directions come from.

Number both lists so direction notes can cite them ("category.md, table
stakes 2").

## Rules

- Comparable screenshots are reference only. No direction reuses a
  comparable's logo, palette or signature element.
- Every claim in category.md names the comparable it came from.
- Category research informs the market note on each direction; it never
  replaces the app's own content contract.

## category.md template

```markdown
# Category: <category>

| App | Type | Colour field | Neutral | Shape | Density | Tone | Signature | Source |
|---|---|---|---|---|---|---|---|---|
| <name> (direct) | ... | ... | ... | ... | ... | ... | ... | <pages or screenshots> |

## Table stakes
1. <convention shared by three or more comparables>

## White space
1. <what none of them do, and why the brief supports it>
```
