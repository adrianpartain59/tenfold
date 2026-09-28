# Changelog

## 1.0.0 — 2026-09-28

First public release as Tenfold (the skill inside is `design-studio`).

- Ten-variation design rounds on a local gallery server, with Claude's pick and a predicted pick.
- Context sweep of the surrounding app before any design, and a taste log (`~/design-studio/TASTE.md`) that learns your picks.
- Project adapters (`.design-studio/adapter.md`) for per-app rules, token exports and build steps.
- `studio.sh icons` (local Feather sprite) and `studio.sh sheets` (contact-sheet PNGs).
- Gallery server binds to localhost by default; `DESIGN_STUDIO_BIND=0.0.0.0` for phone viewing.
