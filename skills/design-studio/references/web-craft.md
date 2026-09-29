# Building a web variation

One variation = one folder `vNN/` = a design system plus real pages. Pages are
real HTML that scrolls, works from 390 to 1440 px wide, and links to its
sibling pages.

## Files

| File | What it holds |
|---|---|
| `vNN/tokens.css` | The direction's system: `--f-display`, `--f-body`, the type ramp as `.t-display .t-h1 .t-h2 .t-h3 .t-lede .t-body .t-small .t-eyebrow`, `--container`, `--gutter`, `--section-y`, `--radius-*`, `--surface-*`, `--shadow-*`. It picks from the brand colours in `../../tokens.css` and adds no new accent unless the direction is a wildcard. |
| `vNN/site.css` | Components: nav, footer, buttons, store badges, section layouts, cards, device frames. |
| `vNN/chrome.js` | `system` stage: the shared nav and footer as template strings, injected into `[data-chrome="nav"]` and `[data-chrome="footer"]`. Links are relative (`index.html`, `guide.html`). |
| `vNN/index.html` | Home. In `system`, one more file per template: `vNN/<template id>.html`. |

## Page template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>04 · Sky Scroll · Home</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;700;800&family=Inter:wght@400;600&display=swap">
<link rel="stylesheet" href="../../tokens.css">
<link rel="stylesheet" href="../web.css">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="site.css">
<script src="chrome.js" defer></script>
</head>
<body>
  <header data-chrome="nav"></header>
  <main>
    <section class="section">...</section>
  </main>
  <footer data-chrome="footer"></footer>
</body>
</html>
```

In `directions` and `converge`, the nav and footer can live inline in
`index.html`, since there's only one page. `web.css` provides `.wrap` (the
content column), `.section` (vertical rhythm), `.device-phone` (an app
screenshot in a phone frame) and `.visually-hidden`.

## Rules

- **One job per viewport.** The first screen says what it is and shows the
  one primary action at 390 and at 1440. Later sections each earn their place
  by answering one objection or showing one capability.
- **Nav:** logo left, three to five links, the primary action as the only
  filled button. On a phone, the links collapse behind a menu button and the
  action stays visible.
- **Footer:** product links, legal links (privacy, terms, and any required
  health-data notice), contact, store badges, copyright.
- **Grid:** a container of 1120 to 1280 px with a 12-column grid inside it,
  and a gutter of 20 px on phones and 32 px or more on desktop. Full-bleed
  bands are allowed, but text stays in the container.
- **Type:** fluid sizes with `clamp()`. The display face is used for
  headlines only. Body text is 16 to 18 px with a line length of 45 to 80
  characters. Keep it to four or five sizes per page.
- **Breakpoints:** design at 390, 834 and 1440. There is no horizontal scroll
  at 390, ever. Tablet is a width to check, not a separate design.
- **Imagery:** real product screens in `.device-phone` frames (from the
  topic's `img/`), the brand's own art and mascot, and real photography only
  when the adapter provides it. No stock people, no made-up logos, and no
  "as seen in" rows without a source.
- **Store badges:** use the adapter's official badge files. With no files,
  use a black button with the store's logo glyph and the store's exact
  wording ("Download on the App Store").
- **Proof:** ratings, counts and quotes come from the content fixture only,
  shown with their source ("4.9 on the App Store, 12,400 ratings").
- **Motion:** CSS only, explaining something (a screen sliding into a
  device, a number counting up once). Respect `prefers-reduced-motion`
  (`web.css` does this globally). No scroll-jacking. A wildcard may break
  this if its notes say so.
- **States:** hover and visible focus on every link and button. Targets are
  44 px or larger on phones.
- **Performance and portability:** Google Fonts or local fonts, inline SVG
  icons from the topic's `icons.svg`, and no JS frameworks. The only JS is
  `chrome.js` and small progressive touches.

## The web failure list (reject on sight)

- A centred hero over a purple or blue gradient blob.
- Three identical feature cards with an icon, a title and two lines.
- Glassmorphism, glows or noise used as decoration.
- Stock photos of smiling people, or a fake logo wall.
- Emoji as icons.
- Every section the same height and layout (no rhythm).
- A hero with two competing buttons of equal weight.
- Tiny grey body text, or text over an image without contrast.
- A direction that differs from another only in font or colour.
