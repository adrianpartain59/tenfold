# Apply on the web

How an approved glow-up theme reaches a React, Next or Vite codebase,
usually with Tailwind and shadcn. Four stages, one board each. Every stage
is a commit the user can review or revert on its own.

## Before you start

- Run `git status --porcelain`. If any path apply will touch has
  uncommitted changes, stop and name the files.
- `git switch -c glowup/<topic>` from the current branch, never on main.
  Record the base commit in the apply manifest as `apply.base`.
- Detect the stack:
  - Tailwind v3 (a `tailwind.config.*` file) or v4 (`@import "tailwindcss"`
    in the global stylesheet);
  - shadcn (`components.json`), and whether its `:root` variables in the
    global stylesheet are HSL triplets (`222.2 84% 4.9%`) or `oklch()`;
  - how fonts load: `next/font/google`, `@fontsource` packages, or a
    `<link>` in the document head.
- Find the scripts in `package.json` you will run after each stage:
  `build`, `typecheck` (or `tsc --noEmit`) and `lint`.

## Stage 1: theme layer

Generate from the picked direction's `theme.json`. Never hand-write values.

```bash
python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --css-vars
python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --tailwind     # Tailwind v4
python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --tailwind3    # Tailwind v3
python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --shadcn       # shadcn on oklch
python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --shadcn-hsl   # shadcn on HSL triplets
```

1. Add the `--css-vars` output to the global stylesheet. Change nothing
   else in it yet.
2. Tailwind v4: add the `--tailwind` block after it. Tailwind v3: merge the
   `theme.extend` object from `--tailwind3` into `tailwind.config.*`.
3. shadcn: replace its `:root` and `.dark` blocks with the `--shadcn` or
   `--shadcn-hsl` output, whichever matches the project's format.
4. Fonts through the project's own mechanism: `next/font/google` with the
   theme's families and weights, or the matching `@fontsource` packages.

List every file this stage touched in `apply.themeFiles`. Commit:
`style(glowup): theme layer for <direction>`.

## Stage 2: shared components

Restyle `components/ui/*` (or the project's shared components) from the
tokens. Give every interactive component the full state matrix from
`theme.json.states`:

- hover
- pressed
- a visible `focus-visible` ring of `--focus-width` at `--focus-offset`
- disabled
- loading (buttons keep their label)
- selected
- error

Apply the layout templates' density to rows and table cells. Commit.

## Stage 3: routes

Work from `entropy-before.json`: each value lists the files it appears in,
which is the to-do list for this stage. Map literals to tokens:

| Before | After |
|---|---|
| `bg-indigo-600`, `bg-blue-600` | `bg-action` |
| `text-white` on an action | `text-on-action` |
| `text-gray-500`, `text-slate-500` | `text-text-2` |
| `bg-white`, `bg-gray-50` | `bg-surface`, `bg-ground` |
| `border-gray-200` | `border-border` |
| `text-[13px]`, `text-sm` used as a heading | the ramp class for that role |
| `p-[18px]`, odd spacing | the nearest value on the scale |
| `rounded-2xl shadow-lg` on every card | the radius and elevation level for that surface role |

Then, inside each route:

- wrap the page in its layout template;
- polish the layout within the content contract (hierarchy, grouping,
  empty, loading and error states);
- rewrite copy in the theme's voice, glossary and case map;
- fix the tells that sit inside the allowed diff: labels and `htmlFor`,
  `aria-label` on icon buttons, focus rings, `tabular-nums`, input `type`,
  `autoComplete` and `inputMode`, typographic quotes and ellipses, copy.

About five routes per commit.

## Stage 4: brand surface

- `favicon.svg` and `apple-touch-icon.png` (180 × 180) from the direction's
  `brand/` images.
- A real title per route: Next `metadata` exports, or `<title>` elsewhere.
- A share image at 1200 × 630, referenced from the `og:image` meta.
- `theme-color` meta for light and dark.

## After every stage

1. Run the project's `build`, `typecheck` and `lint` scripts that exist.
2. Start the dev server or preview and screenshot each touched route at 390
   and 1440 into `ROUND_DIR/after/`.
3. Measure again:

   ```bash
   python3 <SKILL_DIR>/scripts/entropy.py <repo> --out ROUND_DIR/entropy-after.json
   python3 <SKILL_DIR>/scripts/tells_lint.py <repo> --json ROUND_DIR/tells-after.json
   bash <SKILL_DIR>/scripts/studio.sh check ROUND_DIR
   ```

4. A failing build is fixed before the board goes out. If it can't be
   fixed, `git revert` that stage's commits, set `"build": "fail"` and
   `"reverted": true`, and say so on the board.

## Hard limits

No changes to data fetching, state, routing, API calls or test IDs. No new
features, screens or navigation. The diff touches styles, render markup,
copy strings and assets. A change outside that list is a follow-up, not
part of apply.

## Follow-ups

Some tells can only be fixed by changing behaviour: validation timing,
loader delays, permission timing. Apply leaves them alone and lists each in
`apply.followUps` as one line with the rule, `file:line`, and why. The last
apply board shows them as recommended follow-ups.
