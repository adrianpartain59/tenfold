# Changelog

## 1.3.0 · 2026-09-30

Glow-up mode, for turning a vibe-coded or AI-made app into a designed one.

- `studio.sh new <project> <topic> --glowup [--web]` starts a glow-up topic: a theme board gallery with Before, Category and Directions tabs and a spec card per direction.
- Stages: `intake`, `audit`, `research`, `directions`, `converge`, `system` (every route) and `apply` (staged commits on a `glowup/<topic>` branch).
- New scripts: `entropy.py` (distinct colours, sizes, weights, spacing, radii and shadows in an app), `tells_lint.py` (six families of vibe-coded tells), `theme_tokens.py` (one `theme.json` to CSS, Tailwind v3 and v4, shadcn and React Native), `glowup_check.py`, `glowup_sheets.py`.
- New references: `glowup.md`, `glowup-craft.md` (the 13-part system layer and the tells), `category-research.md`, `apply-web.md`, `apply-native.md`.
- Runs from screenshots alone (`"source": "images"`): `image_audit.py` measures the colours the screenshots use with a standard-library PNG decoder, and the topic ends with a `handoff` stage (`handoff.py`: every token format plus a paste-ready prompt for an AI builder) instead of apply.
- Mobile, web and paywall modes are unchanged by glow-up mode.

## 1.2.0 · 2026-09-29

Paywall mode, for paywalls, subscription screens and offer screens.

- `studio.sh new <project> <topic> --paywall` starts a paywall round: a gallery with a state switch (main, other plan, exit offer, friend price…) across every card.
- Stages: `concepts` (ten archetypes), `concept` (one archetype ten ways), `converge`, and `ab` (a control plus one-variable variants for an experiment).
- New references: `paywall.md`, `paywall-craft.md`, `paywall-playbook.md` (cited conversion levers, the rules, a scoring rubric), `paywall-archetypes.md` (14 archetypes).
- `check` enforces billed price, renewal terms, restore/terms/privacy, one CTA, every state, and proof that matches your real proof list; `sheets` writes one set per state.
- Adapters can add `paywall-data` so rounds read live paywall numbers.
- Mobile and web modes are unchanged by paywall mode.
- Fix: Web mode: converge rounds may hold one variation; contact sheets show pages at rest (animations off, sticky and fixed elements in flow).

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
