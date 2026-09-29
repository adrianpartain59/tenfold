# Changelog

## 1.1.0 · 2026-09-28

Web mode, for redesigning websites, landing pages and marketing sites.

- `studio.sh new <project> <topic> --web` starts a web round: a gallery with desktop and phone frames, a Desktop/Tablet/Phone switch, page tabs and live links.
- Each web direction carries its own design system (`vNN/tokens.css`) on top of the brand base, and real pages that scroll.
- Staged rounds: `directions` (full home pages), `converge`, then `system` (the pick across every template, linked as a site).
- `check` validates web rounds (links, direction tokens, template coverage); `sheets` writes `heroes.png`, full-length phone sheets and per-variation page strips.
- New references: `web.md`, `web-craft.md`. Mobile mode is unchanged.
- `tests/studio.test.sh` covers both modes.

## 1.0.0 — 2026-09-28

First public release as Tenfold (the skill inside is `design-studio`).

- Ten-variation design rounds on a local gallery server, with Claude's pick and a predicted pick.
- Context sweep of the surrounding app before any design, and a taste log (`~/design-studio/TASTE.md`) that learns your picks.
- Project adapters (`.design-studio/adapter.md`) for per-app rules, token exports and build steps.
- `studio.sh icons` (local Feather sprite) and `studio.sh sheets` (contact-sheet PNGs).
- Gallery server binds to localhost by default; `DESIGN_STUDIO_BIND=0.0.0.0` for phone viewing.
