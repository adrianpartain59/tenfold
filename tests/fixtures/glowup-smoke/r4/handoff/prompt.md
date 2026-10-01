# Apply the Ledger design system

Paste this into your AI builder (Lovable, v0, Bolt or Cursor) together with the files in this folder. It restyles the app. It does not change what the app does.

## Files

- `tokens.css`: every colour, spacing, radius, shadow, motion and state value as CSS variables. Add it to the global stylesheet.
- `tailwind-v4.css` or `tailwind.config.v3.js`: maps Tailwind utilities to those variables. Use the one that matches the project.
- `shadcn.css` (OKLCH) or `shadcn-hsl.css` (HSL triplets): replaces shadcn/ui's `:root` and `.dark` blocks.
- `theme.ts`: the same theme for React Native and Expo.
- `theme.css`: the full stylesheet the mockups were built on, including type and layout classes, for reference.

## Fonts

- Display: Fraunces (600, 700)
- Body: Inter Tight (400, 500, 600)

Why this pairing: A soft serif for headings gives a notes tool a written, considered feel; a tight grotesk keeps dense lists legible.

## Colours

Use these roles, never raw colour values. `tokens.css` defines each one as `--c-<role>`.

| Role | Light | Dark |
|---|---|---|
| ground | #fcfcfd | #111113 |
| surface | #ffffff | #18191b |
| surface-2 | #f0f0f3 | #212225 |
| border | #d9d9e0 | #363a3f |
| text | #1c2024 | #edeef0 |
| text-2 | #60646c | #b0b4ba |
| text-3 | #8b8d98 | #696e77 |
| action | #3e63dd | #3e63dd |
| on-action | #ffffff | #ffffff |
| accent | #ffc53d | #ffc53d |
| on-accent | #4f3422 | #4f3422 |
| good | #218358 | #3dd68c |
| warn | #ab6400 | #ffca16 |
| error | #ce2c31 | #ff9592 |
| focus | #8da4ef | #5472e4 |

## Type

| Style | Face | Size / line | Weight | Tracking |
|---|---|---|---|---|
| display | Fraunces | 40 / 44 px | 700 | -0.02 em |
| h1 | Fraunces | 32 / 38 px | 700 | -0.015 em |
| h2 | Fraunces | 24 / 30 px | 600 | -0.01 em |
| h3 | Inter Tight | 18 / 24 px | 600 | -0.005 em |
| lede | Inter Tight | 18 / 28 px | 400 | 0 em |
| body | Inter Tight | 16 / 24 px | 400 | 0 em |
| small | Inter Tight | 14 / 20 px | 400 | 0.005 em |
| caption | Inter Tight | 12 / 16 px | 500 | 0.01 em |
| eyebrow | Inter Tight | 12 / 16 px | 600 | 0.08 em, all caps |

Numbers use tabular figures.

## Spacing and layout

Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64 px. Use only these values.

Every screen uses exactly one of these layouts:

- Reading column: 1 column, max 680 px, 24 px gutter, 24 px margin, spacious
- Sidebar and content: 12 columns, max 1200 px, 24 px gutter, 32 px margin, comfortable
- Dashboard grid: 12 columns, max 1280 px, 16 px gutter, 24 px margin, compact

## Shape and depth

Radii: sm 4 px, md 10 px, lg 16 px, full 999 px.
Elevation style: layered. Levels:

- 0: `none`
- 1: `0 1px 2px rgba(17, 17, 19, 0.06), 0 1px 1px rgba(17, 17, 19, 0.04)`
- 2: `0 4px 12px rgba(17, 17, 19, 0.08), 0 1px 2px rgba(17, 17, 19, 0.06)`
- 3: `0 12px 32px rgba(17, 17, 19, 0.12), 0 2px 6px rgba(17, 17, 19, 0.08)`

## States

Every button, input and link has a hover overlay at 0.06, a pressed overlay at 0.1, 0.4 opacity when disabled, and a 2 px focus ring in the focus colour at 2 px offset. Loading buttons keep their label. Inputs have an error state.

## Signature

A ruled ledger line under every section heading, in the action colour. It appears on the screens `screens.md` marks as signature screens. Never on buttons, inputs or list rows.

## Voice

Plain, exact and calm. Buttons say what happens. Use sentence case for buttons, titles and labels.

Rewrite these strings:

- “Welcome to your dashboard” → “Your notes”
- “Oops! Something went wrong” → “That didn’t save. Check your connection and try again.”
- “Get Started” → “Start a note”
- “Submit” → “Save note”
- “No notes yet” → “No notes yet. Your first one takes ten seconds.”

Glossary:

- note: note (never memo or entry)
- space: space (never workspace)

## Design decisions

Why the design is the way it is. Keep these when you change anything.

- Composition: Dashboard-first: this week's count leads, like the category's calm tools (category.md, table stakes 1).
- Interaction: Notes open in a reading column and are edited in place; no modal editor.
- Navigation: A quiet top bar with three items; routes unchanged.
- Anatomy: Home is the signed-in app: the count, recent notes and one action, no marketing sections.
- Art: None on purpose: the ruled line is the only ornament.
- Icons: Feather at 1.5 px to match the light serif.
- Mark: Lowercase ledger wordmark with the ruled line under it.
- Motion: The ruled line draws in under a heading on first view, 200 ms ease-out; nothing loops.
- Mobile: Single column; the top bar becomes a bottom bar of three items.

## Screen by screen

Follow `screens.md` in this folder: one section per screen, naming its layout and what to change.

## Do not change

- Data, logic, API calls, routing, navigation and features.
- Test IDs and analytics events.

Change styles, markup, copy and assets only.
