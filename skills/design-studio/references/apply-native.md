# Apply on React Native and Expo

How an approved glow-up theme reaches a React Native or Expo codebase,
usually with StyleSheet literals and sometimes NativeWind. Four stages, one
board each. Every stage is a commit the user can review or revert on its
own.

## Before you start

- Run `git status --porcelain`. If any path apply will touch has
  uncommitted changes, stop and name the files.
- `git switch -c glowup/<topic>` from the current branch, never on main.
  Record the base commit in the apply manifest as `apply.base`.
- Detect the stack:
  - navigation: expo-router (an `app/` directory) or react-navigation;
  - styling: NativeWind (v4 reads CSS variables from `global.css`; earlier
    versions need literal values) or plain StyleSheet;
  - an existing theme module (`theme.ts`, `colors.ts`, `constants/Colors.ts`)
    that the new one replaces.

## Stage 1: theme layer

Generate the theme module from the picked direction's `theme.json`:

```bash
python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --rn --out <theme dir>/theme.ts
```

It exports `theme` (hex colours for `light` and `dark`, `space`,
`keylines`, `radius`, `type` with `@expo-google-fonts` family names,
`elevation` as shadow props, `motion`, `states`) and `fonts`, the list of
font names to load.

- Add a `useTheme()` hook on `useColorScheme()` that returns `theme.light`
  or `theme.dark` with the shared scales.
- Fonts: `npx expo install @expo-google-fonts/<family>` for each family,
  then `useFonts(...)` at the root with the names in `fonts`, holding the
  splash screen until they load.
- NativeWind v4: also write `--css-vars` into `global.css` and merge the
  `--tailwind3` output's `theme.extend` into `tailwind.config.js`.

Replace the old theme module's exports or re-export from the new one, so
imports keep working. List every file touched in `apply.themeFiles`.
Commit: `style(glowup): theme layer for <direction>`.

## Stage 2: shared components

Restyle buttons, inputs, cards, list rows, sheets and headers from the
theme. Pressed states use `Pressable` with `states.pressed`; disabled uses
`states.disabled`; inputs get a focus border at `states.focus.width`.
Haptics through `expo-haptics` only in their documented meanings: selection
for pickers, impact for a confirmed action, notification for success,
warning and error. Commit.

## Stage 3: screens

Work from `entropy-before.json`: each value lists the files it appears in.

- Replace StyleSheet literals with theme references: colours from
  `useTheme()`, spacing from `space`, radii from `radius`, text styles from
  `type`.
- Wrap each screen in its layout template: the template's margin is the
  screen inset, and dense screens use the compact template.
- Polish the layout within the content contract, then rewrite copy in the
  theme's voice, glossary and case map.
- Fix the tells inside the allowed diff:
  - `accessibilityLabel` on icon-only buttons and placeholder-only inputs
  - `textContentType` and `autoComplete` on inputs browsers and password
    managers can fill
  - input text at 16 or larger
  - typographic quotes, copy

About five screens per commit.

## Stage 4: brand surface

- `icon` (1024 × 1024) and `android.adaptiveIcon` in `app.json`, from the
  direction's `brand/` images.
- A splash that matches the first screen's ground colour, with no logo and
  no text (Apple's guidance: the launch screen should look like the app's
  first screen).

## After every stage

1. `npx tsc --noEmit` and the lint script when configured. When the project
   has no other build script, `npx expo export --platform ios` is the build
   check.
2. Screenshots into `ROUND_DIR/after/<id>.png`:
   - `xcrun simctl io booted screenshot ROUND_DIR/after/<id>.png` when a
     simulator is booted;
   - else Expo web through headless Chrome when the project supports
     react-native-web;
   - else HTML recreations, labelled "not from the device" on the board.
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

No changes to data fetching, state, navigation structure, API calls or test
IDs. No new features or screens. The diff touches styles, render markup,
copy strings and assets. A change outside that list is a follow-up, not
part of apply.

## Follow-ups

Permission timing (`L-permission-on-mount`), loader delays and validation
timing change behaviour, so apply leaves them alone. List each in
`apply.followUps` as one line with the rule, `file:line`, and why. The last
apply board shows them as recommended follow-ups.
