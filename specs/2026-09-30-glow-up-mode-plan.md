# Glow-up Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add glow-up mode to the `design-studio` skill: turn a vibe-coded web or React Native app into a designed one through intake, a measured audit, category research, ten theme directions on four key screens, a whole-app system proof, and a staged apply to the codebase.

**Architecture:** Glow-up is a job flag (`"mode": "glowup"` in the manifest) that composes with the existing app and web frames, not a new surface. Five new stdlib-only Python scripts do the mechanical work (`theme_core.py` shared maths and validation, `theme_tokens.py` one theme to every output format, `entropy.py` and `tells_lint.py` measure an app's source, `glowup_check.py` gates every round, `glowup_sheets.py` contact sheets). A new gallery (`gallery-glowup.html`) shows directions as rows across the four key screens. Five new references teach the loop, the system layer, category research and the two apply playbooks.

**Tech Stack:** bash, python3 (stdlib only), vanilla HTML/CSS/JS for the gallery, headless Chrome for contact sheets and DOM tests.

**Spec:** `specs/2026-09-30-glow-up-mode-design.md`. Read it before starting any task.

## Global Constraints

- Additive. App, web and paywall modes keep their current behaviour; every existing assertion in `tests/studio.test.sh` keeps passing. The only existing assertion that changes is the version check (`1.2.0` to `1.3.0`) in Task 10.
- No new runtime dependencies: bash, python3 stdlib, Chrome or Chromium for images only.
- Python scripts follow `skills/design-studio/scripts/web_check.py`: `#!/usr/bin/env python3`, a module docstring with the usage line, `FAIL ...` / `WARN ...` lines, then one `OK|FAIL <summary>` line, exit 1 on any FAIL.
- No em dashes in any shipped file (references, SKILL.md, README, CHANGELOG, gallery, scripts). Rewrite the sentence; don't swap in a hyphen.
- The public repo carries general knowledge only. No project-specific names, data or rulings.
- Target version: `1.3.0`.
- Glow-up manifests carry `"mode": "glowup"` plus `"surface": "app"` or `"web"`. `studio.sh` routes on `mode` before `surface`.
- A theme may change look, voice and layout within a screen. Apply may not change navigation, information architecture, features, data fetching, state, routing, API calls or test IDs.
- Run every python unit test with `python3 tests/glowup_test.py -v` and the full suite with `bash tests/studio.test.sh`.

## File map

| File | Responsibility |
|---|---|
| `skills/design-studio/scripts/theme_core.py` | Colour maths (hex, OKLCH, HSL, WCAG contrast), `theme.json` load/validate, framework-default and second-order checks, the default-palette constants |
| `skills/design-studio/scripts/theme_tokens.py` | `theme.json` to `--css`, `--css-vars`, `--tailwind`, `--tailwind3`, `--shadcn`, `--shadcn-hsl`, `--rn` |
| `skills/design-studio/scripts/entropy.py` | Walk app source; count distinct colours, font sizes, weights, spacing, radii, shadows; `walk()` shared with the lint |
| `skills/design-studio/scripts/tells_lint.py` | Six lint families over app source or one mockup file (`scan`, `scan_text`) |
| `skills/design-studio/scripts/glowup_check.py` | Gate for directions, converge, system and apply rounds |
| `skills/design-studio/scripts/glowup_sheets.py` | Contact-sheet wrapper pages for a glow-up round |
| `skills/design-studio/scripts/studio.sh` | `new --glowup [--web]`, and `check`/`sheets` routing on `mode` |
| `skills/design-studio/assets/gallery-glowup.html` | Theme board: Before, Category, Directions/System/Apply tabs, spec card |
| `skills/design-studio/references/glowup.md` | The loop: stages, intake, audit, manifests, pick question |
| `skills/design-studio/references/glowup-craft.md` | `theme.json`, the 13-part system layer, human rules, tells, screen rules, checklist |
| `skills/design-studio/references/category-research.md` | Choosing and recording comparables |
| `skills/design-studio/references/apply-web.md` | Apply playbook for React/Next/Vite with Tailwind and shadcn |
| `skills/design-studio/references/apply-native.md` | Apply playbook for React Native and Expo |
| `tests/glowup_test.py` | Python unit tests for the five scripts |
| `tests/fixtures/glowup-web/` | A small vibe-coded Vite + Tailwind + shadcn app with known entropy and tells |
| `tests/fixtures/glowup-native/` | A small Expo app with StyleSheet literals |
| `tests/fixtures/glowup-smoke/` | A glow-up topic: context, before images, r1 directions, r2 system, r3 apply |
| `tests/studio.test.sh` | New glow-up sections; version assertion moves to 1.3.0 |
| `SKILL.md`, `references/variations.md`, `CHANGELOG.md`, `README.md`, `.claude-plugin/*.json` | Docs, triggers, axes, release |

---

### Task 1: `theme_core.py` and the reference theme

**Files:**
- Create: `skills/design-studio/scripts/theme_core.py`
- Create: `tests/fixtures/glowup-smoke/r1/v01/theme.json`
- Create: `tests/glowup_test.py`

**Interfaces:**
- Produces: constants `ROLES`, `RAMP`, `SCREENS`, `STEPS`, `WEIGHT_NAMES`, `TAILWIND_HEX`, `SHADCN_HSL`, `SHADCN_OKLCH`; functions `parse(c) -> (r, g, b)` floats 0..1, `to_hex(rgb) -> "#rrggbb"`, `to_oklch_str(rgb) -> "oklch(L C H)"`, `to_hsl_triplet(rgb) -> "H S% L%"`, `srgb_to_oklch(rgb) -> (L, C, H)`, `contrast(c1, c2) -> float`, `load_theme(path) -> dict`, `resolve(theme, mode, role) -> str`, `validate_theme(t) -> list[str]`, `contrast_errors(t) -> list[str]`, `default_hits(t) -> list[(path, why)]`, `second_order_hits(t) -> list[(id, why)]`.

- [ ] **Step 1: Write the reference theme**

`tests/fixtures/glowup-smoke/r1/v01/theme.json` (this is also the worked example the references point to):

```json
{
  "name": "Ledger",
  "type": {
    "display": { "family": "Fraunces", "weights": [600, 700], "fallback": "Georgia, serif" },
    "body": { "family": "Inter Tight", "weights": [400, 500, 600] },
    "pairing": "A soft serif for headings gives a notes tool a written, considered feel; a tight grotesk keeps dense lists legible.",
    "ramp": {
      "display": { "face": "display", "size": 40, "line": 44, "weight": 700, "track": -0.02 },
      "h1": { "face": "display", "size": 32, "line": 38, "weight": 700, "track": -0.015 },
      "h2": { "face": "display", "size": 24, "line": 30, "weight": 600, "track": -0.01 },
      "h3": { "face": "body", "size": 18, "line": 24, "weight": 600, "track": -0.005 },
      "lede": { "face": "body", "size": 18, "line": 28, "weight": 400, "track": 0 },
      "body": { "face": "body", "size": 16, "line": 24, "weight": 400, "track": 0 },
      "small": { "face": "body", "size": 14, "line": 20, "weight": 400, "track": 0.005 },
      "caption": { "face": "body", "size": 12, "line": 16, "weight": 500, "track": 0.01 },
      "eyebrow": { "face": "body", "size": 12, "line": 16, "weight": 600, "track": 0.08, "upper": true }
    }
  },
  "color": {
    "primitives": {
      "neutral": { "1": "#fcfcfd", "2": "#f9f9fb", "3": "#f0f0f3", "4": "#e8e8ec", "5": "#e0e1e6", "6": "#d9d9e0", "7": "#cdced6", "8": "#b9bbc6", "9": "#8b8d98", "10": "#80838d", "11": "#60646c", "12": "#1c2024" },
      "neutral-dark": { "1": "#111113", "2": "#18191b", "3": "#212225", "4": "#272a2d", "5": "#2e3135", "6": "#363a3f", "7": "#43484e", "8": "#5a6169", "9": "#696e77", "10": "#777b84", "11": "#b0b4ba", "12": "#edeef0" },
      "brand": { "1": "#fdfdfe", "2": "#f7f9ff", "3": "#edf2fe", "4": "#e1e9ff", "5": "#d2deff", "6": "#c1d0ff", "7": "#abbdf9", "8": "#8da4ef", "9": "#3e63dd", "10": "#3358d4", "11": "#3a5bc7", "12": "#1f2d5c" },
      "brand-dark": { "1": "#11131f", "2": "#141726", "3": "#182449", "4": "#1d2e62", "5": "#253974", "6": "#304384", "7": "#3a4f97", "8": "#435db1", "9": "#3e63dd", "10": "#5472e4", "11": "#9eb1ff", "12": "#d6e1ff" }
    },
    "light": {
      "ground": "neutral.1", "surface": "#ffffff", "surface-2": "neutral.3", "border": "neutral.6",
      "text": "neutral.12", "text-2": "neutral.11", "text-3": "neutral.9",
      "action": "brand.9", "on-action": "#ffffff", "accent": "#ffc53d", "on-accent": "#4f3422",
      "good": "#218358", "warn": "#ab6400", "error": "#ce2c31", "focus": "brand.8"
    },
    "dark": {
      "ground": "neutral-dark.1", "surface": "neutral-dark.2", "surface-2": "neutral-dark.3", "border": "neutral-dark.6",
      "text": "neutral-dark.12", "text-2": "neutral-dark.11", "text-3": "neutral-dark.9",
      "action": "brand-dark.9", "on-action": "#ffffff", "accent": "#ffc53d", "on-accent": "#4f3422",
      "good": "#3dd68c", "warn": "#ffca16", "error": "#ff9592", "focus": "brand-dark.10"
    }
  },
  "layout": {
    "space": [4, 8, 12, 16, 24, 32, 48, 64],
    "templates": [
      { "id": "column", "label": "Reading column", "columns": 1, "max": 680, "gutter": 24, "margin": 24, "density": "spacious" },
      { "id": "split", "label": "Sidebar and content", "columns": 12, "max": 1200, "gutter": 24, "margin": 32, "density": "comfortable" },
      { "id": "dashboard", "label": "Dashboard grid", "columns": 12, "max": 1280, "gutter": 16, "margin": 24, "density": "compact" }
    ],
    "keylines": [24, 72]
  },
  "shape": { "radius": { "sm": 4, "md": 10, "lg": 16, "full": 999 } },
  "elevation": {
    "style": "layered",
    "levels": {
      "0": "none",
      "1": "0 1px 2px rgba(17, 17, 19, 0.06), 0 1px 1px rgba(17, 17, 19, 0.04)",
      "2": "0 4px 12px rgba(17, 17, 19, 0.08), 0 1px 2px rgba(17, 17, 19, 0.06)",
      "3": "0 12px 32px rgba(17, 17, 19, 0.12), 0 2px 6px rgba(17, 17, 19, 0.08)"
    }
  },
  "icons": { "set": "phosphor", "license": "MIT", "stroke": 1.5, "sizes": [16, 20, 24] },
  "motion": {
    "fast": 120, "base": 200, "slow": 320,
    "easing": { "out": "cubic-bezier(0.2, 0.8, 0.2, 1)", "in-out": "cubic-bezier(0.6, 0, 0.2, 1)" },
    "spring": { "damping": 20, "stiffness": 240 }
  },
  "states": { "hover": 0.06, "pressed": 0.1, "disabled": 0.4, "focus": { "width": 2, "offset": 2 } },
  "signature": {
    "what": "A ruled ledger line under every section heading, in the action colour",
    "where": ["s1", "s2"],
    "never": "Never on buttons, inputs or list rows",
    "uses": []
  },
  "voice": {
    "adjectives": ["plain", "exact", "calm"],
    "strings": [
      { "before": "Welcome to your dashboard", "after": "Your notes" },
      { "before": "Oops! Something went wrong", "after": "That didn’t save. Check your connection and try again." },
      { "before": "Get Started", "after": "Start a note" },
      { "before": "Submit", "after": "Save note" },
      { "before": "No notes yet", "after": "No notes yet. Your first one takes ten seconds." }
    ],
    "case": { "button": "sentence", "title": "sentence", "label": "sentence" },
    "glossary": { "note": "note (never memo or entry)", "space": "space (never workspace)" }
  },
  "brand": {
    "wordmark": "Lowercase “ledger” in Fraunces 700 with the ruled line under it",
    "icon": "A single ruled line on an action-colour square"
  },
  "reasons": {}
}
```

- [ ] **Step 2: Write the failing tests**

`tests/glowup_test.py`:

```python
#!/usr/bin/env python3
"""Unit tests for glow-up's python scripts. Run: python3 tests/glowup_test.py -v"""
import copy, json, os, subprocess, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPTS = os.path.join(REPO, "skills", "design-studio", "scripts")
FIX = os.path.join(HERE, "fixtures")
THEME = os.path.join(FIX, "glowup-smoke", "r1", "v01", "theme.json")
sys.path.insert(0, SCRIPTS)

import theme_core as tc


def theme():
    return copy.deepcopy(tc.load_theme(THEME))


class ThemeCoreTest(unittest.TestCase):
    def test_hex_round_trip(self):
        self.assertEqual(tc.to_hex(tc.parse("#3E63DD")), "#3e63dd")
        self.assertEqual(tc.to_hex(tc.parse("#fff")), "#ffffff")

    def test_oklch_round_trip_within_one_step(self):
        back = tc.parse(tc.to_oklch_str(tc.parse("#3e63dd")))
        for a, b in zip(back, tc.parse("#3e63dd")):
            self.assertLessEqual(abs(round(a * 255) - round(b * 255)), 1)

    def test_white_in_oklch(self):
        self.assertEqual(tc.to_oklch_str(tc.parse("#ffffff")), "oklch(1.000 0.000 0.0)")

    def test_hsl_triplet(self):
        self.assertEqual(tc.to_hsl_triplet(tc.parse("#fcfcfd")), "240.0 20.0% 99.0%")

    def test_contrast(self):
        self.assertAlmostEqual(tc.contrast("#ffffff", "#000000"), 21.0, places=2)

    def test_resolve(self):
        t = theme()
        self.assertEqual(tc.resolve(t, "light", "action"), "#3e63dd")
        self.assertEqual(tc.resolve(t, "light", "surface"), "#ffffff")
        self.assertEqual(tc.resolve(t, "dark", "text"), "#edeef0")

    def test_reference_theme_is_clean(self):
        t = theme()
        self.assertEqual(tc.validate_theme(t), [])
        self.assertEqual(tc.contrast_errors(t), [])
        self.assertEqual(tc.default_hits(t), [])
        self.assertEqual(tc.second_order_hits(t), [])

    def test_validate_reports_missing_parts(self):
        t = theme()
        del t["color"]["dark"]["text-2"]
        t["layout"]["templates"] = t["layout"]["templates"][:2]
        t["signature"]["where"] = ["s1"]
        errs = tc.validate_theme(t)
        self.assertIn("color.dark.text-2 missing", errs)
        self.assertIn("layout.templates needs 3 or 4 templates (has 2)", errs)
        self.assertIn("signature.where needs at least two of s1, s2, s3, s4", errs)

    def test_one_radius_everywhere_is_rejected(self):
        t = theme()
        t["shape"]["radius"] = {"md": 12, "full": 999}
        self.assertIn("shape.radius needs at least two distinct values below 999 (one radius everywhere reads as generated)", tc.validate_theme(t))

    def test_ramp_weight_must_be_loaded(self):
        t = theme()
        t["type"]["ramp"]["h1"]["weight"] = 800
        self.assertIn("type.ramp.h1 weight 800 is not in type.display.weights", tc.validate_theme(t))

    def test_contrast_failure(self):
        t = theme()
        t["color"]["light"]["text-2"] = "#b9bbc6"
        self.assertTrue(any(e.startswith("light: text-2 on ground") for e in tc.contrast_errors(t)), tc.contrast_errors(t))

    def test_default_hits(self):
        t = theme()
        t["shape"]["radius"]["md"] = 8
        t["type"]["display"] = {"family": "Inter", "weights": [600, 700]}
        t["type"]["body"]["family"] = "Inter"
        t["icons"] = {"set": "lucide", "license": "ISC", "stroke": 2, "sizes": [16, 20, 24]}
        t["color"]["primitives"]["brand"]["9"] = "#4f46e5"
        hits = dict(tc.default_hits(t))
        self.assertEqual(hits["shape.radius.md"], "shadcn's 0.5rem radius")
        self.assertEqual(hits["type.body.family"], "Inter as the only face")
        self.assertEqual(hits["icons.stroke"], "Lucide at its default 2px stroke")
        self.assertEqual(hits["color.primitives.brand"], "Tailwind default indigo-600")

    def test_untinted_neutral_ramp(self):
        t = theme()
        greys = ["#fcfcfc", "#f9f9f9", "#f0f0f0", "#e8e8e8", "#e0e0e0", "#d9d9d9", "#cecece", "#bbbbbb", "#8d8d8d", "#838383", "#646464", "#202020"]
        t["color"]["primitives"]["neutral"] = dict(zip(tc.STEPS, greys))
        self.assertIn(("color.primitives.neutral", "an untinted grey ramp"), tc.default_hits(t))

    def test_second_order_cream_terracotta(self):
        t = {"type": {}, "color": {"light": {"ground": "oklch(0.96 0.02 80)", "action": "oklch(0.6 0.13 40)", "accent": "#ffc53d"}, "dark": {}}}
        self.assertIn("cream-terracotta", [i for i, _ in tc.second_order_hits(t)])

    def test_second_order_black_acid(self):
        t = {"type": {}, "color": {"light": {"ground": "#0b0b0c", "action": "#a3e635", "accent": "#ffffff"}, "dark": {}}}
        self.assertIn("black-acid", [i for i, _ in tc.second_order_hits(t)])

    def test_second_order_mono_chrome(self):
        t = theme()
        t["type"]["mono"] = {"family": "JetBrains Mono", "weights": [500]}
        t["type"]["ramp"]["eyebrow"].update({"face": "mono", "weight": 500})
        self.assertIn("mono-chrome", [i for i, _ in tc.second_order_hits(t)])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 tests/glowup_test.py -v`
Expected: `ModuleNotFoundError: No module named 'theme_core'`.

- [ ] **Step 4: Write `theme_core.py`**

```python
#!/usr/bin/env python3
"""Glow-up core: colour maths, theme.json loading and validation, and the
framework-default and second-order checks. Imported by theme_tokens.py,
tells_lint.py and glowup_check.py; not run directly."""
import json, math, re

ROLES = ("ground", "surface", "surface-2", "border", "text", "text-2", "text-3",
         "action", "on-action", "accent", "on-accent", "good", "warn", "error", "focus")
RAMP = ("display", "h1", "h2", "h3", "lede", "body", "small", "caption", "eyebrow")
SCREENS = ("s1", "s2", "s3", "s4")
STEPS = tuple(str(i) for i in range(1, 13))
DENSITIES = ("compact", "comfortable", "spacious")
ELEVATION_STYLES = ("border", "shadow", "layered")
CASES = ("sentence", "title", "upper")
FACES = ("display", "body", "mono")
WEIGHT_NAMES = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium",
                600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"}

# Framework defaults that read as generated when nobody chose them.
TAILWIND_HEX = {
    "#f9fafb": "gray-50", "#e5e7eb": "gray-200", "#6b7280": "gray-500", "#111827": "gray-900",
    "#f8fafc": "slate-50", "#e2e8f0": "slate-200", "#64748b": "slate-500", "#0f172a": "slate-900",
    "#71717a": "zinc-500", "#18181b": "zinc-900",
    "#6366f1": "indigo-500", "#4f46e5": "indigo-600", "#3b82f6": "blue-500", "#2563eb": "blue-600",
    "#8b5cf6": "violet-500", "#7c3aed": "violet-600", "#a855f7": "purple-500", "#9333ea": "purple-600",
}
SHADCN_HSL = {"222.2 84% 4.9%", "210 40% 98%", "222.2 47.4% 11.2%", "210 40% 96.1%",
              "215.4 16.3% 46.9%", "214.3 31.8% 91.4%"}
SHADCN_OKLCH = {"oklch(0.145 0 0)", "oklch(0.205 0 0)", "oklch(0.985 0 0)", "oklch(0.97 0 0)",
                "oklch(0.922 0 0)", "oklch(0.556 0 0)", "oklch(0.708 0 0)"}

CONTRAST_PAIRS = (("text", "ground", 4.5), ("text-2", "ground", 4.5), ("text", "surface", 4.5),
                  ("on-action", "action", 4.5), ("text-3", "ground", 3.0))

_HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
_OKLCH = re.compile(r"^oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)\s*\)$", re.I)
_REF = re.compile(r"^([a-z][a-z0-9-]*)\.(\d{1,2})$")


def _gamma(x):
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055


def _linear(x):
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4


def oklch_to_srgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bl = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    return tuple(min(1.0, max(0.0, _gamma(max(0.0, v)))) for v in (r, g, bl))


def srgb_to_oklch(rgb):
    r, g, b = (_linear(v) for v in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


def parse(c):
    """A colour string as (r, g, b) floats 0..1 in sRGB. Accepts #rgb, #rrggbb, oklch(L C H)."""
    s = str(c).strip()
    m = _HEX.match(s)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    m = _OKLCH.match(s)
    if m:
        L = float(m.group(1)) / (100 if m.group(2) else 1)
        return oklch_to_srgb(L, float(m.group(3)), float(m.group(4)))
    raise ValueError(f"unsupported colour {c!r} (use #rgb, #rrggbb or oklch(L C H))")


def to_hex(rgb):
    return "#" + "".join(f"{round(min(1, max(0, v)) * 255):02x}" for v in rgb)


def to_oklch_str(rgb):
    L, C, H = srgb_to_oklch(rgb)
    if C < 0.0005:
        C, H = 0.0, 0.0
    return f"oklch({L:.3f} {C:.3f} {H:.1f})"


def to_hsl_triplet(rgb):
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    l = (mx + mn) / 2
    d = mx - mn
    if d == 0:
        h = s = 0.0
    else:
        s = d / (1 - abs(2 * l - 1))
        if mx == r:
            h = 60 * (((g - b) / d) % 6)
        elif mx == g:
            h = 60 * ((b - r) / d + 2)
        else:
            h = 60 * ((r - g) / d + 4)
    return f"{h:.1f} {s * 100:.1f}% {l * 100:.1f}%"


def luminance(rgb):
    r, g, b = (_linear(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(c1, c2):
    a, b = luminance(parse(c1)), luminance(parse(c2))
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def load_theme(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve(theme, mode, role):
    v = theme["color"][mode][role]
    m = _REF.match(v)
    if m:
        return theme["color"]["primitives"][m.group(1)][m.group(2)]
    return v


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _str(x):
    return isinstance(x, str) and x.strip() != ""


def validate_theme(t):
    """Every structural problem in a theme, as human-readable lines. [] means valid."""
    e = []
    if not isinstance(t, dict):
        return ["theme is not an object"]
    if not _str(t.get("name")):
        e.append("name missing")

    ty = t.get("type") or {}
    for face in ("display", "body"):
        f = ty.get(face) or {}
        if not _str(f.get("family")):
            e.append(f"type.{face}.family missing")
        if not (isinstance(f.get("weights"), list) and f["weights"] and all(w in WEIGHT_NAMES for w in f["weights"])):
            e.append(f"type.{face}.weights must list weights from 100 to 900 in steps of 100")
    if not _str(ty.get("pairing")):
        e.append("type.pairing missing (one line on why these faces)")
    ramp = ty.get("ramp") or {}
    for k in RAMP:
        r = ramp.get(k)
        if not isinstance(r, dict):
            e.append(f"type.ramp.{k} missing")
            continue
        for n in ("size", "line", "weight", "track"):
            if not _num(r.get(n)):
                e.append(f"type.ramp.{k} missing {n}")
        face = r.get("face")
        if face not in FACES:
            e.append(f"type.ramp.{k}.face must be display, body or mono")
        elif not _str((ty.get(face) or {}).get("family")):
            e.append(f"type.ramp.{k} uses face {face} but type.{face} is not defined")
        elif _num(r.get("weight")) and r["weight"] not in ((ty.get(face) or {}).get("weights") or []):
            e.append(f"type.ramp.{k} weight {r['weight']} is not in type.{face}.weights")

    col = t.get("color") or {}
    prims = col.get("primitives") or {}
    for name, steps in prims.items():
        for s in STEPS:
            if s not in (steps or {}):
                e.append(f"color.primitives.{name} missing step {s}")
                continue
            try:
                parse(steps[s])
            except ValueError as err:
                e.append(f"color.primitives.{name}.{s}: {err}")
    for mode in ("light", "dark"):
        roles = col.get(mode) or {}
        for role in ROLES:
            if role not in roles:
                e.append(f"color.{mode}.{role} missing")
                continue
            try:
                parse(resolve(t, mode, role))
            except (KeyError, TypeError):
                e.append(f"color.{mode}.{role} refers to {roles[role]!r}, which is not a primitive step")
            except ValueError as err:
                e.append(f"color.{mode}.{role}: {err}")

    lay = t.get("layout") or {}
    sp = lay.get("space")
    if not (isinstance(sp, list) and len(sp) >= 4 and all(_num(v) and v > 0 for v in sp) and sp == sorted(set(sp))):
        e.append("layout.space needs at least four increasing positive values")
    tps = lay.get("templates") or []
    if not 3 <= len(tps) <= 4:
        e.append(f"layout.templates needs 3 or 4 templates (has {len(tps)})")
    ids = set()
    for i, tp in enumerate(tps):
        tid = tp.get("id")
        if not _str(tid) or tid in ids:
            e.append(f"layout.templates[{i}] needs a unique id")
        ids.add(tid)
        if not _str(tp.get("label")):
            e.append(f"layout.templates.{tid} missing label")
        if not (isinstance(tp.get("columns"), int) and tp["columns"] >= 1):
            e.append(f"layout.templates.{tid} columns must be a whole number from 1")
        if tp.get("max") is not None and not _num(tp.get("max")):
            e.append(f"layout.templates.{tid} max must be a number or null")
        for n in ("gutter", "margin"):
            if not _num(tp.get(n)):
                e.append(f"layout.templates.{tid} missing {n}")
        if tp.get("density") not in DENSITIES:
            e.append(f"layout.templates.{tid} density must be compact, comfortable or spacious")
    if not (isinstance(lay.get("keylines"), list) and lay["keylines"] and all(_num(v) for v in lay["keylines"])):
        e.append("layout.keylines needs at least one value")

    rad = (t.get("shape") or {}).get("radius") or {}
    if not (rad and all(_num(v) for v in rad.values())):
        e.append("shape.radius needs named numeric values")
    elif len({v for v in rad.values() if v < 999}) < 2:
        e.append("shape.radius needs at least two distinct values below 999 (one radius everywhere reads as generated)")

    el = t.get("elevation") or {}
    if el.get("style") not in ELEVATION_STYLES:
        e.append("elevation.style must be border, shadow or layered")
    if not (isinstance(el.get("levels"), dict) and len(el["levels"]) >= 3 and all(isinstance(v, str) for v in el["levels"].values())):
        e.append("elevation.levels needs at least three named levels")

    ic = t.get("icons") or {}
    if not (_str(ic.get("set")) and _str(ic.get("license")) and _num(ic.get("stroke")) and isinstance(ic.get("sizes"), list) and ic["sizes"]):
        e.append("icons needs set, license, stroke and sizes")

    mo = t.get("motion") or {}
    if not all(_num(mo.get(k)) for k in ("fast", "base", "slow")):
        e.append("motion needs fast, base and slow durations in ms")
    if not all(_str((mo.get("easing") or {}).get(k)) for k in ("out", "in-out")):
        e.append("motion.easing needs out and in-out")

    st = t.get("states") or {}
    if not all(_num(st.get(k)) and 0 <= st[k] <= 1 for k in ("hover", "pressed", "disabled")):
        e.append("states needs hover, pressed and disabled as opacities from 0 to 1")
    if not all(_num((st.get("focus") or {}).get(k)) for k in ("width", "offset")):
        e.append("states.focus needs width and offset")

    sg = t.get("signature") or {}
    if not _str(sg.get("what")):
        e.append("signature.what missing")
    where = sg.get("where") or []
    if not (isinstance(where, list) and len(set(where) & set(SCREENS)) >= 2 and set(where) <= set(SCREENS)):
        e.append("signature.where needs at least two of s1, s2, s3, s4")
    if not _str(sg.get("never")):
        e.append("signature.never missing")
    if not isinstance(sg.get("uses", []), list):
        e.append("signature.uses must be a list")

    vo = t.get("voice") or {}
    if not (isinstance(vo.get("adjectives"), list) and len(vo["adjectives"]) == 3 and all(_str(a) for a in vo["adjectives"])):
        e.append("voice.adjectives needs exactly three words")
    strs = vo.get("strings") or []
    if not (len(strs) == 5 and all(_str(s.get("before")) and _str(s.get("after")) for s in strs)):
        e.append("voice.strings needs five before/after pairs")
    case = vo.get("case") or {}
    if not all(case.get(k) in CASES for k in ("button", "title", "label")):
        e.append("voice.case needs button, title and label set to sentence, title or upper")
    if not isinstance(vo.get("glossary"), dict):
        e.append("voice.glossary must be an object")

    br = t.get("brand") or {}
    if not (_str(br.get("wordmark")) and _str(br.get("icon"))):
        e.append("brand needs wordmark and icon")
    if not isinstance(t.get("reasons", {}), dict):
        e.append("reasons must be an object")
    return e


def contrast_errors(t):
    out = []
    for mode in ("light", "dark"):
        for fg, bg, need in CONTRAST_PAIRS:
            ratio = contrast(resolve(t, mode, fg), resolve(t, mode, bg))
            if ratio < need:
                out.append(f"{mode}: {fg} on {bg} {ratio:.2f}:1 (need {need:g})")
    return out


def default_hits(t):
    """(path, why) for every value that equals a framework default. Each needs a line in reasons."""
    hits = []
    col = t.get("color") or {}
    for name, ramp in (col.get("primitives") or {}).items():
        hexes = {to_hex(parse(v)) for v in ramp.values()}
        tw = sorted(TAILWIND_HEX[h] for h in hexes if h in TAILWIND_HEX)
        if tw:
            hits.append((f"color.primitives.{name}", "Tailwind default " + ", ".join(tw)))
        if name.startswith("neutral") and all(srgb_to_oklch(parse(v))[1] < 0.005 for v in ramp.values()):
            hits.append((f"color.primitives.{name}", "an untinted grey ramp"))
    for mode in ("light", "dark"):
        for role, raw in (col.get(mode) or {}).items():
            if not _REF.match(raw) and to_hex(parse(raw)) in TAILWIND_HEX:
                hits.append((f"color.{mode}.{role}", "Tailwind default " + TAILWIND_HEX[to_hex(parse(raw))]))
    ty = t.get("type") or {}
    fams = {(ty.get(f) or {}).get("family", "").lower() for f in ("display", "body")}
    if fams == {"inter"}:
        hits.append(("type.body.family", "Inter as the only face"))
    if ((t.get("shape") or {}).get("radius") or {}).get("md") == 8:
        hits.append(("shape.radius.md", "shadcn's 0.5rem radius"))
    ic = t.get("icons") or {}
    if str(ic.get("set", "")).lower().startswith("lucide") and ic.get("stroke") == 2:
        hits.append(("icons.stroke", "Lucide at its default 2px stroke"))
    return hits


def second_order_hits(t):
    """(id, why) for the 'tasteful' defaults a glow-up drifts into. Allowed only as the named signature."""
    out = []

    def lch(mode, role):
        try:
            return srgb_to_oklch(parse(resolve(t, mode, role)))
        except Exception:
            return None

    for mode in ("light", "dark"):
        g = lch(mode, "ground")
        hot = [x for x in (lch(mode, "action"), lch(mode, "accent")) if x]
        if not g:
            continue
        if g[0] > 0.92 and 0.008 < g[1] < 0.05 and 50 < g[2] < 110 and any(20 < h < 55 and c > 0.09 and 0.45 < L < 0.72 for L, c, h in hot):
            out.append(("cream-terracotta", f"{mode}: a cream ground with a terracotta accent"))
        if g[0] < 0.2 and any(c > 0.17 and 95 < h < 145 for L, c, h in hot):
            out.append(("black-acid", f"{mode}: a near-black ground with an acid accent"))
    eb = ((t.get("type") or {}).get("ramp") or {}).get("eyebrow") or {}
    if eb.get("face") == "mono" and eb.get("upper"):
        out.append(("mono-chrome", "all-caps mono eyebrows"))
    return out
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 tests/glowup_test.py -v`
Expected: all `ThemeCoreTest` tests PASS. If `test_reference_theme_is_clean` fails on contrast, fix the fixture colour named in the message, never the threshold.

- [ ] **Step 6: Commit**

```bash
git add skills/design-studio/scripts/theme_core.py tests/glowup_test.py tests/fixtures/glowup-smoke/r1/v01/theme.json
git commit -m "feat(glowup): theme_core colour maths and theme.json validation"
```

---

### Task 2: `theme_tokens.py`

**Files:**
- Create: `skills/design-studio/scripts/theme_tokens.py`
- Modify: `tests/glowup_test.py` (append a test class above `if __name__`)

**Interfaces:**
- Consumes: `theme_core` (Task 1): `ROLES`, `RAMP`, `WEIGHT_NAMES`, `parse`, `to_hex`, `to_oklch_str`, `to_hsl_triplet`, `resolve`, `validate_theme`, `load_theme`.
- Produces: `css(t) -> str` (the exact text of a direction's `tokens.css`; `glowup_check` compares against it), `css_vars(t) -> str`, `tailwind(t) -> str`, `tailwind3(t) -> str`, `shadcn(t, hsl=False) -> str`, `rn(t) -> str`, `google_fonts_url(t) -> str`. CLI: `theme_tokens.py <theme.json> --css|--css-vars|--tailwind|--tailwind3|--shadcn|--shadcn-hsl|--rn [--out file]`; prints `FAIL <error>` lines and exits 1 on an invalid theme.
- Token names in `--css` are the contract with `screen.css` and `web.css`: `--c-<role>` for every role, the compat aliases `--c-background-root --c-text-secondary --c-text-tertiary --c-primary --c-button-text`, `--space-1..n` and `--space-xs..2xl`, `--gap-screen-x`, `--radius-<name>`, `--radius-card --radius-card-raised --radius-sheet`, `--shadow-<level>`, `--shadow-card`, `--container`, `--gutter`, `--f-display`, `--f-body`, `--font-sans`, `--dur-*`, `--ease-*`, `--state-*`, `--focus-width`, `--focus-offset`, `--icon-stroke`; classes `.t-<ramp key>`, `.t-title`, `.tpl-<template id>`, `.tnum`, `.span-all`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/glowup_test.py`:

```python
class ThemeTokensTest(unittest.TestCase):
    def setUp(self):
        import theme_tokens
        self.tt = theme_tokens
        self.t = theme()

    def test_css_contract(self):
        css = self.tt.css(self.t)
        self.assertTrue(css.startswith("/* Generated by theme_tokens.py from theme.json (Ledger). Do not edit by hand. */\n@import url(\"https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Inter+Tight:wght@400;500;600&display=swap\");\n"))
        for line in ("  --c-action: #3e63dd;", "  --c-background-root: var(--c-ground);", "  --c-text-secondary: var(--c-text-2);",
                     "  --space-1: 4px;", "  --space-lg: 16px;", "  --gap-screen-x: 24px;", "  --radius-md: 10px;",
                     "  --radius-card: 10px;", "  --shadow-card: 0 1px 2px rgba(17, 17, 19, 0.06), 0 1px 1px rgba(17, 17, 19, 0.04);",
                     "  --container: 680px;", "  --gutter: 24px;", '  --f-display: "Fraunces", Georgia, serif;',
                     '  --f-body: "Inter Tight", system-ui, sans-serif;', "  --dur-fast: 120ms;", "  --focus-width: 2px;"):
            self.assertIn(line, css)
        dark = css.split('[data-theme="dark"] {', 1)[1]
        self.assertIn("  --c-ground: #111113;", dark)
        self.assertIn('@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {', css)
        self.assertIn(".t-display { font-family: var(--f-display); font-size: 40px; line-height: 44px; font-weight: 700; letter-spacing: -0.02em; }", css)
        self.assertIn(".t-eyebrow { font-family: var(--f-body); font-size: 12px; line-height: 16px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }", css)
        self.assertIn(".t-title { font-family: var(--f-display); font-size: 24px;", css)
        self.assertIn(".tpl-dashboard { max-width: 1280px; margin-inline: auto; padding-inline: 24px; display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 16px; row-gap: 16px; }", css)

    def test_css_is_deterministic(self):
        self.assertEqual(self.tt.css(self.t), self.tt.css(theme()))

    def test_css_vars_has_no_import_or_classes(self):
        v = self.tt.css_vars(self.t)
        self.assertNotIn("@import", v)
        self.assertNotIn(".t-display", v)
        self.assertIn("  --c-action: #3e63dd;", v)

    def test_tailwind_v4(self):
        out = self.tt.tailwind(self.t)
        self.assertIn("@theme inline {", out)
        for line in ("  --color-action: var(--c-action);", "  --text-display: 40px;", "  --text-display--line-height: 44px;", "  --radius-md: 10px;", "  --spacing: 4px;"):
            self.assertIn(line, out)

    def test_tailwind_v3(self):
        out = self.tt.tailwind3(self.t)
        self.assertTrue(out.splitlines()[1].startswith("module.exports = {"))
        cfg = json.loads(out.split("module.exports = ", 1)[1].rstrip().rstrip(";"))
        ext = cfg["theme"]["extend"]
        self.assertEqual(ext["colors"]["action"], "var(--c-action)")
        self.assertEqual(ext["fontSize"]["display"], ["40px", {"lineHeight": "44px", "letterSpacing": "-0.02em", "fontWeight": "700"}])
        self.assertEqual(ext["borderRadius"]["md"], "10px")

    def test_shadcn_oklch_and_hsl(self):
        ok = self.tt.shadcn(self.t)
        self.assertIn("  --background: oklch(", ok)
        self.assertIn("  --radius: 0.625rem;", ok)
        self.assertIn("\n.dark {\n", ok)
        hsl = self.tt.shadcn(self.t, hsl=True)
        self.assertIn("  --background: 240.0 20.0% 99.0%;", hsl)
        self.assertIn("  --primary-foreground: 0.0 0.0% 100.0%;", hsl)

    def test_rn(self):
        out = self.tt.rn(self.t)
        self.assertTrue(out.startswith("// Generated by theme_tokens.py from theme.json (Ledger). Do not edit by hand.\nexport const theme = {"))
        obj = json.loads(out.split("export const theme = ", 1)[1].split(" as const;", 1)[0])
        self.assertEqual(obj["light"]["ground"], "#fcfcfd")
        self.assertEqual(obj["dark"]["action"], "#3e63dd")
        self.assertEqual(obj["type"]["display"]["fontFamily"], "Fraunces_700Bold")
        self.assertEqual(obj["type"]["display"]["letterSpacing"], -0.8)
        self.assertEqual(obj["type"]["eyebrow"]["textTransform"], "uppercase")
        self.assertEqual(obj["elevation"]["2"], {"shadowColor": "#000000", "shadowOpacity": 0.06, "shadowRadius": 1.0, "shadowOffset": {"width": 0.0, "height": 1.0}, "elevation": 1})
        self.assertIn('export const fonts = ["Fraunces_600SemiBold", "Fraunces_700Bold", "InterTight_400Regular", "InterTight_500Medium", "InterTight_600SemiBold"] as const;', out)

    def test_cli_rejects_invalid_theme(self):
        bad = os.path.join(FIX, "glowup-smoke", "_bad.json")
        t = theme(); del t["voice"]
        with open(bad, "w") as f:
            json.dump(t, f)
        try:
            r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "theme_tokens.py"), bad, "--css"], capture_output=True, text=True)
        finally:
            os.remove(bad)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL voice.adjectives needs exactly three words", r.stdout)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 tests/glowup_test.py -v ThemeTokensTest`
Expected: `ModuleNotFoundError: No module named 'theme_tokens'`.

- [ ] **Step 3: Write `theme_tokens.py`**

```python
#!/usr/bin/env python3
"""Turn a glow-up theme.json into every output a mockup or an app needs.

  theme_tokens.py <theme.json> --css|--css-vars|--tailwind|--tailwind3|--shadcn|--shadcn-hsl|--rn [--out file]

--css        a direction's tokens.css for mockups (fonts, variables, type and template classes)
--css-vars   only the :root and dark variable blocks, for an app's global stylesheet
--tailwind   a Tailwind v4 @theme inline block that maps utilities to the variables
--tailwind3  a Tailwind v3 config fragment to merge into theme.extend
--shadcn     shadcn/ui :root and .dark variables as OKLCH (--shadcn-hsl for HSL triplets)
--rn         a TypeScript theme module for React Native (hex colours, @expo-google-fonts names)
Prints FAIL lines and exits 1 when the theme is invalid.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme_core import (RAMP, ROLES, WEIGHT_NAMES, load_theme, parse, resolve, to_hex,
                        to_hsl_triplet, to_oklch_str, validate_theme)

GENERIC = "system-ui, sans-serif"
COMPAT = (("background-root", "ground"), ("text-secondary", "text-2"), ("text-tertiary", "text-3"),
          ("primary", "action"), ("button-text", "on-action"))
SHADCN_MAP = (("background", "ground"), ("foreground", "text"), ("card", "surface"), ("card-foreground", "text"),
              ("popover", "surface"), ("popover-foreground", "text"), ("primary", "action"),
              ("primary-foreground", "on-action"), ("secondary", "surface-2"), ("secondary-foreground", "text"),
              ("muted", "surface-2"), ("muted-foreground", "text-2"), ("accent", "surface-2"),
              ("accent-foreground", "text"), ("destructive", "error"), ("border", "border"), ("input", "border"),
              ("ring", "focus"))
SHADOW = re.compile(r"(-?[\d.]+)(?:px)?\s+(-?[\d.]+)(?:px)?\s+([\d.]+)(?:px)?(?:\s+(-?[\d.]+)(?:px)?)?\s+(rgba?\([^)]*\)|#[0-9a-fA-F]{3,8})")


def _head(t):
    return f"Generated by theme_tokens.py from theme.json ({t['name']}). Do not edit by hand."


def _px(v):
    return f"{float(v):g}px"


def _family(t, face):
    f = t["type"][face]
    return f'"{f["family"]}", {f.get("fallback", GENERIC)}'


def _faces(t):
    merged = {}
    for face in ("display", "body", "mono"):
        f = t["type"].get(face)
        if f and f.get("family"):
            merged.setdefault(f["family"], set()).update(f["weights"])
    return [(fam, sorted(ws)) for fam, ws in merged.items()]


def google_fonts_url(t):
    fams = "&".join(f"family={fam.replace(' ', '+')}:wght@{';'.join(str(w) for w in ws)}" for fam, ws in _faces(t))
    return f"https://fonts.googleapis.com/css2?{fams}&display=swap"


def _finite_radii(t):
    return sorted(v for v in t["shape"]["radius"].values() if v < 999)


def _root_lines(t):
    sp = t["layout"]["space"]
    rad = t["shape"]["radius"]
    finite = _finite_radii(t)
    lv = t["elevation"]["levels"]
    tpl0 = t["layout"]["templates"][0]
    m, s = t["motion"], t["states"]
    out = [f'  --f-display: {_family(t, "display")};', f'  --f-body: {_family(t, "body")};', "  --font-sans: var(--f-body);"]
    if (t["type"].get("mono") or {}).get("family"):
        out.append(f'  --f-mono: {_family(t, "mono")};')
    out += [f"  --c-{r}: {resolve(t, 'light', r)};" for r in ROLES]
    out += [f"  --c-{k}: var(--c-{v});" for k, v in COMPAT]
    out += [f"  --space-{i + 1}: {_px(v)};" for i, v in enumerate(sp)]
    out += [f"  --space-{n}: {_px(sp[min(i, len(sp) - 1)])};" for i, n in enumerate(("xs", "sm", "md", "lg", "xl", "2xl"))]
    out.append(f"  --gap-screen-x: {_px(t['layout']['keylines'][0])};")
    out += [f"  --radius-{k}: {_px(v)};" for k, v in rad.items()]
    out += [f"  --radius-card: {_px(rad.get('md', finite[0]))};",
            f"  --radius-card-raised: {_px(rad.get('lg', finite[-1]))};",
            f"  --radius-sheet: {_px(finite[-1] * 2)};"]
    out += [f"  --shadow-{k}: {v};" for k, v in lv.items()]
    out.append(f"  --shadow-card: {lv.get('1', 'none')};")
    out.append(f"  --container: {_px(tpl0['max'])};" if tpl0.get("max") else "  --container: 100%;")
    out.append(f"  --gutter: {_px(tpl0['gutter'])};")
    out += [f"  --dur-{k}: {m[k]}ms;" for k in ("fast", "base", "slow")]
    out += [f"  --ease-{k}: {v};" for k, v in m["easing"].items()]
    out += [f"  --state-hover: {s['hover']};", f"  --state-pressed: {s['pressed']};", f"  --state-disabled: {s['disabled']};",
            f"  --focus-width: {_px(s['focus']['width'])};", f"  --focus-offset: {_px(s['focus']['offset'])};",
            f"  --icon-stroke: {t['icons']['stroke']};"]
    return out


def _vars_body(t):
    dark = [f"  --c-{r}: {resolve(t, 'dark', r)};" for r in ROLES]
    return (":root {\n" + "\n".join(_root_lines(t)) + "\n}\n"
            "@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {\n"
            + "\n".join("  " + line for line in dark) + "\n  }\n}\n"
            "[data-theme=\"dark\"] {\n" + "\n".join(dark) + "\n}\n")


def _decl(r):
    d = [f"font-family: var(--f-{r['face']})", f"font-size: {_px(r['size'])}", f"line-height: {_px(r['line'])}",
         f"font-weight: {r['weight']}", f"letter-spacing: {r['track']:g}em"]
    if r.get("upper"):
        d.append("text-transform: uppercase")
    return "{ " + "; ".join(d) + "; }"


def _classes(t):
    ramp = t["type"]["ramp"]
    out = [f".t-{k} {_decl(ramp[k])}" for k in RAMP]
    out.append(f".t-title {_decl(ramp['h2'])}")
    for tp in t["layout"]["templates"]:
        mx = f"max-width: {_px(tp['max'])}; " if tp.get("max") else ""
        out.append(f".tpl-{tp['id']} {{ {mx}margin-inline: auto; padding-inline: {_px(tp['margin'])}; display: grid; "
                   f"grid-template-columns: repeat({tp['columns']}, minmax(0, 1fr)); column-gap: {_px(tp['gutter'])}; "
                   f"row-gap: {_px(tp['gutter'])}; }}")
    out += [".span-all { grid-column: 1 / -1; }", ".tnum { font-variant-numeric: tabular-nums; }"]
    return "\n".join(out) + "\n"


def css(t):
    return f"/* {_head(t)} */\n@import url(\"{google_fonts_url(t)}\");\n" + _vars_body(t) + _classes(t)


def css_vars(t):
    return f"/* {_head(t)} */\n" + _vars_body(t)


def tailwind(t):
    ramp = t["type"]["ramp"]
    out = [f"  --color-{r}: var(--c-{r});" for r in ROLES]
    out += [f'  --font-display: {_family(t, "display")};', f'  --font-sans: {_family(t, "body")};']
    out += [f"  --radius-{k}: {_px(v)};" for k, v in t["shape"]["radius"].items()]
    out += [f"  --shadow-{k}: {v};" for k, v in t["elevation"]["levels"].items()]
    out.append(f"  --spacing: {_px(t['layout']['space'][0])};")
    for k in RAMP:
        r = ramp[k]
        out += [f"  --text-{k}: {_px(r['size'])};", f"  --text-{k}--line-height: {_px(r['line'])};",
                f"  --text-{k}--letter-spacing: {r['track']:g}em;", f"  --text-{k}--font-weight: {r['weight']};"]
    out += [f"  --ease-{k}: {v};" for k, v in t["motion"]["easing"].items()]
    return f"/* {_head(t)} */\n@theme inline {{\n" + "\n".join(out) + "\n}\n"


def tailwind3(t):
    ramp = t["type"]["ramp"]
    fam = lambda face: [t["type"][face]["family"]] + [x.strip() for x in t["type"][face].get("fallback", GENERIC).split(",")]
    ext = {
        "colors": {r: f"var(--c-{r})" for r in ROLES},
        "fontFamily": {"display": fam("display"), "sans": fam("body")},
        "borderRadius": {k: _px(v) for k, v in t["shape"]["radius"].items()},
        "boxShadow": dict(t["elevation"]["levels"]),
        "fontSize": {k: [_px(ramp[k]["size"]), {"lineHeight": _px(ramp[k]["line"]), "letterSpacing": f"{ramp[k]['track']:g}em",
                                                 "fontWeight": str(ramp[k]["weight"])}] for k in RAMP},
        "transitionDuration": {k: f"{t['motion'][k]}ms" for k in ("fast", "base", "slow")},
        "transitionTimingFunction": dict(t["motion"]["easing"]),
    }
    return f"// {_head(t)}\nmodule.exports = " + json.dumps({"theme": {"extend": ext}}, indent=2, ensure_ascii=False) + ";\n"


def shadcn(t, hsl=False):
    fmt = (lambda c: to_hsl_triplet(parse(c))) if hsl else (lambda c: to_oklch_str(parse(c)))
    block = lambda mode: "\n".join(f"  --{k}: {fmt(resolve(t, mode, r))};" for k, r in SHADCN_MAP)
    md = t["shape"]["radius"].get("md", _finite_radii(t)[0])
    return (f"/* {_head(t)} */\n:root {{\n" + block("light") + f"\n  --radius: {md / 16:g}rem;\n}}\n"
            ".dark {\n" + block("dark") + "\n}\n")


def _rn_shadow(v):
    last = None
    for last in SHADOW.finditer(v):
        pass
    if not last:
        return None
    x, y, blur, _, col = last.groups()
    alpha = float(col.rstrip(")").split(",")[-1]) if col.startswith("rgba") else 1.0
    return {"shadowColor": "#000000", "shadowOpacity": alpha, "shadowRadius": float(blur) / 2,
            "shadowOffset": {"width": float(x), "height": float(y)}, "elevation": max(1, round(float(blur) / 2))}


def rn(t):
    ramp = t["type"]["ramp"]
    font = lambda face, w: t["type"][face]["family"].replace(" ", "") + f"_{w}{WEIGHT_NAMES[w]}"
    typ = {}
    for k in RAMP:
        r = ramp[k]
        typ[k] = {"fontFamily": font(r["face"], r["weight"]), "fontSize": r["size"], "lineHeight": r["line"],
                  "letterSpacing": round(r["track"] * r["size"], 2)}
        if r.get("upper"):
            typ[k]["textTransform"] = "uppercase"
    motion = {k: t["motion"][k] for k in ("fast", "base", "slow")}
    if t["motion"].get("spring"):
        motion["spring"] = t["motion"]["spring"]
    obj = {
        "light": {r: to_hex(parse(resolve(t, "light", r))) for r in ROLES},
        "dark": {r: to_hex(parse(resolve(t, "dark", r))) for r in ROLES},
        "space": t["layout"]["space"],
        "keylines": t["layout"]["keylines"],
        "radius": t["shape"]["radius"],
        "type": typ,
        "elevation": {k: s for k, s in ((k, _rn_shadow(v)) for k, v in t["elevation"]["levels"].items()) if s},
        "motion": motion,
        "states": t["states"],
        "iconStroke": t["icons"]["stroke"],
    }
    fonts = sorted({font(face, w) for face in ("display", "body", "mono") if (t["type"].get(face) or {}).get("family")
                    for w in t["type"][face]["weights"]})
    return (f"// {_head(t)}\nexport const theme = " + json.dumps(obj, indent=2, ensure_ascii=False) + " as const;\n\n"
            "export const fonts = " + json.dumps(fonts) + " as const;\n\nexport type Theme = typeof theme;\n")


MODES = {"--css": css, "--css-vars": css_vars, "--tailwind": tailwind, "--tailwind3": tailwind3,
         "--shadcn": shadcn, "--shadcn-hsl": lambda t: shadcn(t, hsl=True), "--rn": rn}


def main(argv):
    if len(argv) < 2 or argv[1] not in MODES:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    t = load_theme(argv[0])
    errs = validate_theme(t)
    if errs:
        for e in errs:
            print("FAIL", e)
        return 1
    out = MODES[argv[1]](t)
    if "--out" in argv:
        with open(argv[argv.index("--out") + 1], "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

Note on `fonts`: it lists every loaded weight of every face (the test expects all five), so the app loads exactly what the theme declares.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 tests/glowup_test.py -v`
Expected: all ThemeCoreTest and ThemeTokensTest tests PASS. In `test_rn`, elevation level `"2"`'s last shadow layer is `0 1px 2px rgba(17, 17, 19, 0.06)`, which gives the asserted dict.

- [ ] **Step 5: Commit**

```bash
git add skills/design-studio/scripts/theme_tokens.py tests/glowup_test.py
git commit -m "feat(glowup): theme_tokens writes css, tailwind, shadcn and rn from one theme"
```

---

### Task 3: Fixture apps and `entropy.py`

**Files:**
- Create: `tests/fixtures/glowup-web/package.json`, `components.json`, `src/index.css`, `src/App.tsx`, `src/pages/Settings.tsx`
- Create: `tests/fixtures/glowup-native/package.json`, `app.json`, `App.tsx`
- Create: `skills/design-studio/scripts/entropy.py`
- Modify: `tests/glowup_test.py` (append a test class)

**Interfaces:**
- Produces: `walk(root) -> iterator[(relpath, text)]` (also used by Task 4), `measure(root) -> dict` with keys `root`, `files`, `colors`, `font-sizes`, `font-weights`, `spacing`, `radii`, `shadows` (each `{"count": n, "values": {value: {"count": c, "files": [relpath, ...]}}}`), `total`, `headline`. CLI: `entropy.py <repo> [--out file]` prints `ENTROPY <total> (<headline>)`.

- [ ] **Step 1: Write the web fixture app**

The counts in Step 3 depend on these files exactly. Do not reformat them.

`tests/fixtures/glowup-web/package.json`:

```json
{
  "name": "glowup-web-fixture",
  "private": true,
  "dependencies": { "react": "^18.3.1", "react-dom": "^18.3.1", "lucide-react": "^0.400.0", "react-hook-form": "^7.52.0", "react-countup": "^6.5.3" },
  "devDependencies": { "vite": "^5.3.0", "tailwindcss": "^3.4.4" }
}
```

`tests/fixtures/glowup-web/components.json`:

```json
{ "style": "default", "tailwind": { "css": "src/index.css", "baseColor": "slate", "cssVariables": true } }
```

`tests/fixtures/glowup-web/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --border: 214.3 31.8% 91.4%;
    --radius: 0.5rem;
  }
}

body {
  font-family: "Inter", sans-serif;
}

.legacy-note {
  color: #6b7280;
  padding: 18px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

`tests/fixtures/glowup-web/src/App.tsx`:

```tsx
import { useState } from "react";
import { Sparkles, ArrowRight } from "lucide-react";
import CountUp from "react-countup";

const features = ["Fast sync", "Smart tags", "Team spaces"];

export default function App() {
  const [open, setOpen] = useState(false);
  return (
    <main className="min-h-screen bg-white">
      <section className="text-center py-24 px-6 bg-gradient-to-r from-purple-600 to-blue-500">
        <h1 className="text-5xl font-bold bg-clip-text text-transparent">Elevate your notes seamlessly</h1>
        <p className="mt-4 text-lg text-gray-500">The AI notebook for teams.</p>
        <button className="mt-8 px-6 py-3 rounded-lg bg-indigo-600 text-white outline-none">Get Started <ArrowRight /></button>
      </section>
      <section className="grid grid-cols-3 gap-6 p-8">
        {features.map((f) => (
          <div key={f} className="rounded-2xl shadow-lg p-6 bg-white">
            <Sparkles className="text-indigo-500" />
            <h3 className="mt-4 text-xl font-semibold">{f}</h3>
          </div>
        ))}
        <div className="rounded-2xl shadow-lg p-6 bg-white">Teams</div>
        <div className="rounded-2xl shadow-lg p-5 bg-slate-50">Notes</div>
      </section>
      <div className="p-8 text-sm" onClick={() => setOpen(!open)}><CountUp end={12000} /> notes taken. Oops, that's a lot.</div>
      <p className="text-xs text-gray-400">Syncing...</p>
      <button className="transition-all">Submit</button>
    </main>
  );
}
```

`tests/fixtures/glowup-web/src/pages/Settings.tsx`:

```tsx
import { useForm } from "react-hook-form";
import { Loader2 } from "lucide-react";

export function Settings({ isLoading, price }: { isLoading: boolean; price: number }) {
  const { register, formState } = useForm({ mode: "onChange" });
  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Loader2 className="animate-spin" />
      </div>
    );
  }
  return (
    <form className="max-w-md mx-auto p-6 space-y-4">
      <label className="text-sm font-medium">Email *</label>
      <input className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="Email" {...register("email")} />
      <input className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm" type="password" placeholder="Password" {...register("password")} />
      <p className="text-gray-500">Plan: ${price.toFixed(1)} per month</p>
      <button disabled={!formState.isValid} className="w-full rounded-md bg-indigo-600 py-2 text-white">Save</button>
      <button type="button" className="text-sm">Reset password</button>
    </form>
  );
}
```

- [ ] **Step 2: Write the native fixture app**

`tests/fixtures/glowup-native/package.json`:

```json
{ "name": "glowup-native-fixture", "private": true, "dependencies": { "expo": "~51.0.0", "react-native": "0.74.0", "expo-notifications": "~0.28.0" } }
```

`tests/fixtures/glowup-native/app.json`:

```json
{ "expo": { "name": "Fixture", "slug": "fixture", "splash": { "image": "./assets/splash.png", "backgroundColor": "#ffffff" } } }
```

`tests/fixtures/glowup-native/App.tsx`:

```tsx
import { useEffect } from "react";
import { ActivityIndicator, StyleSheet, Text, TextInput, View } from "react-native";
import * as Notifications from "expo-notifications";

export default function App({ loading }: { loading: boolean }) {
  useEffect(() => {
    Notifications.requestPermissionsAsync();
  }, []);
  if (loading) {
    return <ActivityIndicator size="large" />;
  }
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Welcome to your dashboard</Text>
      <TextInput style={styles.input} placeholder="Email address" />
      <View style={styles.card}><Text style={styles.body}>Oops! Something went wrong</Text></View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, padding: 20, backgroundColor: "#F9FAFB" },
  title: { fontSize: 28, fontWeight: "700", color: "#111827", marginBottom: 12 },
  input: { fontSize: 14, borderWidth: 1, borderColor: "#E5E7EB", borderRadius: 8, padding: 10 },
  card: { marginTop: 16, padding: 16, borderRadius: 12, backgroundColor: "#fff", shadowColor: "#000", shadowOpacity: 0.1, shadowRadius: 6, elevation: 3 },
  body: { fontSize: 16, color: "#6B7280" },
});
```

- [ ] **Step 3: Write the failing tests**

Append to `tests/glowup_test.py`:

```python
KINDS = ("colors", "font-sizes", "font-weights", "spacing", "radii", "shadows")


class EntropyTest(unittest.TestCase):
    def setUp(self):
        import entropy
        self.e = entropy

    def test_web_counts(self):
        r = self.e.measure(os.path.join(FIX, "glowup-web"))
        self.assertEqual({k: r[k]["count"] for k in KINDS},
                         {"colors": 11, "font-sizes": 5, "font-weights": 3, "spacing": 8, "radii": 4, "shadows": 2})
        self.assertEqual(r["total"], 33)
        for v in ("tw:indigo-600", "tw:white", "#6b7280", "rgba(0,0,0,0.1)"):
            self.assertIn(v, r["colors"]["values"])
        self.assertEqual(sorted(r["spacing"]["values"], key=lambda v: float(v[:-2])),
                         ["8px", "12px", "16px", "18px", "20px", "24px", "32px", "96px"])
        self.assertEqual(sorted(r["radii"]["values"]), ["10px", "16px", "6px", "8px"])
        self.assertEqual(r["colors"]["values"]["#6b7280"]["files"], ["src/index.css"])
        self.assertEqual(r["colors"]["values"]["tw:indigo-600"]["files"], ["src/App.tsx", "src/pages/Settings.tsx"])

    def test_native_counts(self):
        r = self.e.measure(os.path.join(FIX, "glowup-native"))
        self.assertEqual({k: r[k]["count"] for k in KINDS},
                         {"colors": 6, "font-sizes": 3, "font-weights": 1, "spacing": 4, "radii": 2, "shadows": 2})
        self.assertIn("#ffffff", r["colors"]["values"])
        self.assertIn("rn:elevation-3", r["shadows"]["values"])
        self.assertEqual(r["headline"], "6 colours · 3 font sizes · 1 weight · 4 spacing values · 2 radii · 2 shadows")

    def test_cli(self):
        out = os.path.join(FIX, "_entropy.json")
        try:
            r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "entropy.py"), os.path.join(FIX, "glowup-web"), "--out", out],
                               capture_output=True, text=True)
            self.assertEqual(r.stdout, "ENTROPY 33 (11 colours · 5 font sizes · 3 weights · 8 spacing values · 4 radii · 2 shadows)\n")
            self.assertEqual(json.load(open(out))["total"], 33)
        finally:
            if os.path.exists(out):
                os.remove(out)
```

- [ ] **Step 4: Run the tests to verify they fail**

Run: `python3 tests/glowup_test.py -v EntropyTest`
Expected: `ModuleNotFoundError: No module named 'entropy'`.

- [ ] **Step 5: Write `entropy.py`**

```python
#!/usr/bin/env python3
"""Count the distinct style values an app's source uses.

  entropy.py <repo> [--out entropy.json]

Counts colours, font sizes, font weights, spacing values, radii and shadows
across web source (CSS, Tailwind classes) and React Native StyleSheets. A
designed app uses a handful of each; a generated one uses dozens. Prints
"ENTROPY <total> (<headline>)"; --out writes every value with its files.
"""
import json, os, re, sys

SKIP_DIRS = {"node_modules", "dist", "build", "coverage", "out", "ios", "android", "public"}
EXTS = (".tsx", ".ts", ".jsx", ".js", ".mjs", ".css", ".scss", ".html")
KINDS = (("colors", "colour", "colours"), ("font-sizes", "font size", "font sizes"), ("font-weights", "weight", "weights"),
         ("spacing", "spacing value", "spacing values"), ("radii", "radius", "radii"), ("shadows", "shadow", "shadows"))

TW_COLORS = "slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose"
TW_SIZE = {"xs": 12, "sm": 14, "base": 16, "lg": 18, "xl": 20, "2xl": 24, "3xl": 30, "4xl": 36, "5xl": 48, "6xl": 60,
           "7xl": 72, "8xl": 96, "9xl": 128}
TW_WEIGHT = {"thin": 100, "extralight": 200, "light": 300, "normal": 400, "medium": 500, "semibold": 600, "bold": 700,
             "extrabold": 800, "black": 900}
TW_RADIUS = {"": 4, "none": 0, "sm": 2, "md": 6, "lg": 8, "xl": 12, "2xl": 16, "3xl": 24, "full": 9999}
B, E = r"(?<![\w-])", r"(?![\w-])"
ARB = r"\[[\d.]+(?:px|rem)\]"
RX = {
    "hex": re.compile(r"(?<![&\w])#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b"),
    "fn": re.compile(r"\b(?:rgba?|hsla?|oklch)\([^)]*\)"),
    "tw_color": re.compile(B + r"(?:bg|text|border|ring|from|via|to|fill|stroke|outline|divide|placeholder|shadow|accent|caret|decoration)-(?:(white|black)|(" + TW_COLORS + r")-(\d{2,3}))" + E),
    "tw_size": re.compile(B + r"text-(xs|sm|base|lg|xl|[2-9]xl|" + ARB + r")" + E),
    "css_size": re.compile(r"\bfont-size\s*:\s*([\d.]+(?:px|rem))"),
    "rn_size": re.compile(r"\bfontSize\s*:\s*([\d.]+)"),
    "tw_weight": re.compile(B + r"font-(" + "|".join(TW_WEIGHT) + r")" + E),
    "css_weight": re.compile(r"\bfont-weight\s*:\s*(\d{3}|bold|normal)"),
    "rn_weight": re.compile(r"\bfontWeight\s*:\s*[\"']?(\d{3}|bold|normal)"),
    "tw_space": re.compile(B + r"-?(?:px|py|pt|pr|pb|pl|ps|pe|p|mx|my|mt|mr|mb|ml|ms|me|m|gap-x|gap-y|gap|space-x|space-y)-(\d+(?:\.5)?|px|" + ARB + r")" + E),
    "css_space": re.compile(r"\b(?:padding|margin|gap)(?:-[a-z]+)?\s*:\s*([^;\n{}]+);"),
    "rn_space": re.compile(r"\b(?:padding|margin)(?:Horizontal|Vertical|Top|Bottom|Left|Right|Start|End)?\s*:\s*(-?\d+(?:\.\d+)?)\b|\b(?:gap|rowGap|columnGap)\s*:\s*(\d+(?:\.\d+)?)\b"),
    "tw_radius": re.compile(B + r"rounded(?:-(?:t|r|b|l|tl|tr|br|bl|s|e|ss|se|es|ee))?(?:-(none|sm|md|lg|xl|2xl|3xl|full|" + ARB + r"))?" + E),
    "css_radius": re.compile(r"\bborder-radius\s*:\s*([^;\n{}]+);"),
    "rn_radius": re.compile(r"\bborder(?:TopLeft|TopRight|BottomLeft|BottomRight)?Radius\s*:\s*(\d+(?:\.\d+)?)"),
    "tw_shadow": re.compile(B + r"shadow(?:-(sm|md|lg|xl|2xl|inner|\[[^\]\s]+\]))?" + E),
    "css_shadow": re.compile(r"\bbox-shadow\s*:\s*([^;\n{}]+);"),
    "rn_shadow": re.compile(r"\b(shadowRadius|elevation)\s*:\s*(\d+(?:\.\d+)?)"),
}


def walk(root):
    """(relpath, text) for every source file under root, skipping dependencies, builds and native projects."""
    for dp, dns, fns in os.walk(root):
        dns[:] = sorted(d for d in dns if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(fns):
            if not fn.endswith(EXTS) or fn.endswith((".d.ts", ".min.js")):
                continue
            p = os.path.join(dp, fn)
            try:
                with open(p, encoding="utf-8") as f:
                    text = f.read()
            except (UnicodeDecodeError, OSError):
                continue
            yield os.path.relpath(p, root).replace(os.sep, "/"), text


def _px(v):
    return f"{float(v):g}px"


def length(s):
    """A CSS length as 'Npx', or None for zero, auto and anything that isn't a length."""
    m = re.fullmatch(r"(-?[\d.]+)(px|rem|em)?", s.strip())
    if not m:
        return None
    v = abs(float(m.group(1))) * (16 if m.group(2) in ("rem", "em") else 1)
    return _px(v) if v else None


def collect(text, add):
    for m in RX["hex"].finditer(text):
        h = m.group(1).lower()
        add("colors", "#" + ("".join(c * 2 for c in h) if len(h) in (3, 4) else h))
    for m in RX["fn"].finditer(text):
        add("colors", re.sub(r"\s+", "", m.group(0).lower()))
    for m in RX["tw_color"].finditer(text):
        add("colors", "tw:" + (m.group(1) or f"{m.group(2)}-{m.group(3)}"))
    for m in RX["tw_size"].finditer(text):
        k = m.group(1)
        add("font-sizes", _px(TW_SIZE[k]) if k in TW_SIZE else length(k[1:-1]))
    for m in RX["css_size"].finditer(text):
        add("font-sizes", length(m.group(1)))
    for m in RX["rn_size"].finditer(text):
        add("font-sizes", _px(m.group(1)))
    for m in RX["tw_weight"].finditer(text):
        add("font-weights", str(TW_WEIGHT[m.group(1)]))
    for key in ("css_weight", "rn_weight"):
        for m in RX[key].finditer(text):
            add("font-weights", {"bold": "700", "normal": "400"}.get(m.group(1), m.group(1)))
    for m in RX["tw_space"].finditer(text):
        v = m.group(1)
        add("spacing", "1px" if v == "px" else length(v[1:-1]) if v.startswith("[") else (_px(float(v) * 4) if float(v) else None))
    for m in RX["css_space"].finditer(text):
        for part in m.group(1).split():
            add("spacing", length(part))
    for m in RX["rn_space"].finditer(text):
        add("spacing", length(m.group(1) or m.group(2)))
    for m in RX["tw_radius"].finditer(text):
        k = m.group(1) or ""
        add("radii", length(k[1:-1]) if k.startswith("[") else (_px(TW_RADIUS[k]) if TW_RADIUS[k] else None))
    for m in RX["css_radius"].finditer(text):
        for part in m.group(1).split():
            add("radii", length(part))
    for m in RX["rn_radius"].finditer(text):
        add("radii", length(m.group(1)))
    for m in RX["tw_shadow"].finditer(text):
        add("shadows", "tw:shadow" + (f"-{m.group(1)}" if m.group(1) else ""))
    for m in RX["css_shadow"].finditer(text):
        v = re.sub(r"\s+", " ", m.group(1).strip())
        if v != "none":
            add("shadows", v)
    for m in RX["rn_shadow"].finditer(text):
        add("shadows", f"rn:{m.group(1)}-{m.group(2)}")


def measure(root):
    vals = {k: {} for k, _, _ in KINDS}
    nfiles = 0
    for rel, text in walk(root):
        nfiles += 1

        def add(kind, v, rel=rel):
            if v is None:
                return
            e = vals[kind].setdefault(v, {"count": 0, "files": []})
            e["count"] += 1
            if rel not in e["files"]:
                e["files"].append(rel)

        collect(text, add)
    out = {"root": os.path.basename(os.path.abspath(root)), "files": nfiles}
    for k, _, _ in KINDS:
        out[k] = {"count": len(vals[k]), "values": dict(sorted(vals[k].items()))}
    out["total"] = sum(out[k]["count"] for k, _, _ in KINDS)
    out["headline"] = " · ".join(f"{out[k]['count']} {one if out[k]['count'] == 1 else many}" for k, one, many in KINDS)
    return out


def main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    r = measure(argv[0])
    if "--out" in argv:
        with open(argv[argv.index("--out") + 1], "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print(f"ENTROPY {r['total']} ({r['headline']})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 tests/glowup_test.py -v EntropyTest`
Expected: PASS. If a count is off, print `measure(...)[kind]["values"]` and find the rule that over- or under-matched. Fix the rule, not the expected number, unless a fixture line really does contain that value.

- [ ] **Step 7: Commit**

```bash
git add skills/design-studio/scripts/entropy.py tests/glowup_test.py tests/fixtures/glowup-web tests/fixtures/glowup-native
git commit -m "feat(glowup): entropy.py counts an app's distinct style values"
```

---

### Task 4: `tells_lint.py`

**Files:**
- Create: `skills/design-studio/scripts/tells_lint.py`
- Modify: `tests/glowup_test.py` (append a test class)

**Interfaces:**
- Consumes: `entropy.walk` (Task 3); `theme_core.TAILWIND_HEX`, `SHADCN_HSL`, `SHADCN_OKLCH` (Task 1).
- Produces: `FAMILIES = ("fingerprint", "forms", "copy", "a11y", "loading", "second-order")`, `scan_text(text, rel) -> list[finding]` (rules that need only one file; used by `glowup_check` on mockup HTML), `scan(root) -> list[finding]` (`scan_text` on every file plus repo-wide rules), `summary(findings) -> str`. A finding is `{"rule": str, "family": str, "file": str, "line": int, "message": str}`; repo-wide findings with no single place use `"file": ""` and `"line": 0`. CLI: `tells_lint.py <repo> [--json out.json]` prints `TELL ...` lines then `TELLS <n> (fingerprint a · forms b · copy c · a11y d · loading e · second-order f)`; always exits 0. The JSON is `{"total": n, "families": {...}, "findings": [...]}`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/glowup_test.py`:

```python
class TellsTest(unittest.TestCase):
    def setUp(self):
        import tells_lint
        self.tl = tells_lint

    def families(self, fs):
        c = {f: 0 for f in self.tl.FAMILIES}
        for x in fs:
            c[x["family"]] += 1
        return c

    def test_web_fixture(self):
        fs = self.tl.scan(os.path.join(FIX, "glowup-web"))
        self.assertEqual(self.families(fs), {"fingerprint": 9, "forms": 9, "copy": 8, "a11y": 4, "loading": 2, "second-order": 0}, fs)
        rules = {x["rule"] for x in fs}
        for r in ("F-gradient-purple", "F-gradient-text", "F-sparkles", "F-count-up", "F-arrow-cta", "F-shadcn-untouched",
                  "F-inter-only", "F-uniform-card", "F-tailwind-hex", "FM-placeholder-only", "FM-no-autocomplete",
                  "FM-small-input", "FM-asterisk", "FM-disabled-invalid", "FM-validate-onchange", "C-oops", "C-submit",
                  "C-three-dots", "C-straight-quote", "C-buzzwords", "C-number-format", "C-tabular", "C-mixed-case",
                  "A-outline-none", "A-div-onclick", "A-transition-all", "A-no-reduced-motion", "L-fullscreen-spinner",
                  "L-no-delay"):
            self.assertIn(r, rules)

    def test_native_fixture(self):
        fs = self.tl.scan(os.path.join(FIX, "glowup-native"))
        self.assertEqual(self.families(fs), {"fingerprint": 4, "forms": 3, "copy": 3, "a11y": 0, "loading": 4, "second-order": 0}, fs)
        rules = {x["rule"] for x in fs}
        for r in ("FM-small-input-rn", "C-generic-welcome", "C-generic-error", "L-permission-on-mount", "L-launch-image"):
            self.assertIn(r, rules)

    def test_second_order_html(self):
        html = ('<h1 class="t-h1">Notes for <em>teams</em> that ship</h1>\n<p>01</p><p>02</p><p>03</p>\n'
                '<span class="dot"></span><span class="dot"></span><span class="dot"></span>')
        rules = {x["rule"] for x in self.tl.scan_text(html, "x.html")}
        self.assertTrue({"S-accent-word", "S-numbered-sections", "S-window-dots"} <= rules, rules)

    def test_clean_markup_has_no_tells(self):
        self.assertEqual(self.tl.scan_text('<h1 class="t-h1">Your notes</h1>\n<p class="t-body">12 notes this week</p>', "x.html"), [])

    def test_cli_summary(self):
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "tells_lint.py"), os.path.join(FIX, "glowup-web")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.splitlines()[-1], "TELLS 32 (fingerprint 9 · forms 9 · copy 8 · a11y 4 · loading 2 · second-order 0)")
        self.assertIn("TELL forms FM-asterisk src/pages/Settings.tsx:15 asterisk as the required marker", r.stdout)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 tests/glowup_test.py -v TellsTest`
Expected: `ModuleNotFoundError: No module named 'tells_lint'`.

- [ ] **Step 3: Write `tells_lint.py`**

```python
#!/usr/bin/env python3
"""Scan an app's source for the tells that make it read as vibe-coded.

  tells_lint.py <repo> [--json out.json]

Six families: fingerprint (framework defaults nobody chose), forms, copy,
a11y, loading, and second-order (the 'tasteful' defaults). Prints one TELL
line per finding, then "TELLS <n> (<counts by family>)". Always exits 0: it
reports, and the glow-up audit and apply boards decide what to do with it.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entropy import walk
from theme_core import SHADCN_HSL, SHADCN_OKLCH, TAILWIND_HEX

FAMILIES = ("fingerprint", "forms", "copy", "a11y", "loading", "second-order")

LINE_RULES = [(rid, fam, re.compile(rx), msg) for rid, fam, rx, msg in (
    ("F-gradient-purple", "fingerprint", r"\bfrom-(?:purple|indigo|violet|fuchsia)-\d{2,3}\b.*\bto-(?:blue|indigo|purple|pink|cyan|violet)-\d{2,3}\b", "purple-to-blue gradient"),
    ("F-gradient-text", "fingerprint", r"bg-clip-text(?=.*text-transparent)|text-transparent(?=.*bg-clip-text)", "gradient headline text"),
    ("F-sparkles", "fingerprint", r"<Sparkles\b", "the sparkle icon"),
    ("F-count-up", "fingerprint", r"from\s+[\"'](?:react-countup|countup\.js)[\"']|\buseCountUp\(", "count-up stats"),
    ("F-arrow-cta", "fingerprint", r"(?=.*<(?:button|Button)\b)(?=.*<ArrowRight\b)", "an arrow welded onto a CTA"),
    ("FM-disabled-invalid", "forms", r"disabled=\{\s*!\s*(?:[\w.]+\.)?isValid\b", "submit disabled until the form is valid"),
    ("FM-asterisk", "forms", r"<(?:label|Label)\b[^>]*>[^<]*\*\s*<", "asterisk as the required marker"),
    ("FM-validate-onchange", "forms", r"\bmode\s*:\s*[\"']onChange[\"']", "validation on every keystroke"),
    ("FM-small-input-rn", "forms", r"^\s*(?:input|textInput|field)\w*\s*:\s*\{[^}]*\bfontSize\s*:\s*(?:1[0-5]|\d)\b", "input text under 16"),
    ("C-oops", "copy", r"\bOops\b", "\"Oops\""),
    ("C-generic-error", "copy", r"Something went wrong", "an error that says nothing"),
    ("C-generic-welcome", "copy", r"Welcome to your (?:dashboard|app)\b", "placeholder welcome copy"),
    ("C-submit", "copy", r">\s*Submit\s*<|[\"']Submit[\"']", "\"Submit\" instead of what happens"),
    ("C-click-here", "copy", r"(?i)\bclick here\b", "\"click here\""),
    ("C-three-dots", "copy", r"[A-Za-z]\.\.\.[\"'<]", "three dots instead of an ellipsis"),
    ("C-straight-quote", "copy", r">[^<>{}]*[A-Za-z]'[a-z][^<>{}]*<", "straight apostrophe in UI text"),
    ("C-buzzwords", "copy", r"(?i)\b(?:seamless(?:ly)?|elevate|unleash|supercharge|revolutioni[sz]e|effortless(?:ly)?)\b", "marketing filler words"),
    ("C-number-format", "copy", r"\.toFixed\(|\btoLocaleString\(\s*\)|\{[^}]*\.toISOString\(\)[^}]*\}", "number or date formatted without Intl options"),
    ("A-outline-none", "a11y", r"^(?!.*focus-visible:).*\boutline-none\b", "focus outline removed with no replacement"),
    ("A-no-zoom", "a11y", r"user-scalable\s*=\s*(?:no|0)|maximum-scale\s*=\s*1(?:\.0)?\b", "zoom disabled"),
    ("A-div-onclick", "a11y", r"<(?:div|span)\b[^>]*\bonClick=", "a clickable div"),
    ("A-icon-button", "a11y", r"<(?:button|Button)\b(?![^>]*aria-label)[^>]*>\s*<[A-Z]\w*\b[^>]*/>\s*</(?:button|Button)>", "icon-only button with no label"),
    ("A-transition-all", "a11y", r"\btransition-all\b|\btransition\s*:\s*all\b", "transition: all"),
)]
SECOND_ORDER = [
    ("S-numbered-sections", re.compile(r">\s*0[1-9]\s*[.·/]?\s*<"), 3, "01 / 02 / 03 section numbering"),
    ("S-window-dots", re.compile(r"(?:<span\b[^>]*class=\"[^\"]*\bdot\b[^\"]*\"[^>]*>\s*</span>\s*){3}"), 1, "fake window dots"),
    ("S-accent-word", re.compile(r"<h1\b[^>]*>[^<]*<(em|span|i|mark)\b[^>]*>[^<]{1,40}</\1>[^<]*</h1>"), 1, "one accented word in the headline"),
]
SPINNER = re.compile(r"animate-spin|<ActivityIndicator\b|<Spinner\b|<Loader2\b")
NUMBERS = re.compile(r"\.toFixed\(|toLocaleString\(|Intl\.NumberFormat")
UNIFORM = re.compile(r"\brounded-(?:xl|2xl|3xl)\b.*\bshadow-(?:md|lg|xl)\b|\bshadow-(?:md|lg|xl)\b.*\brounded-(?:xl|2xl|3xl)\b")
ENTRANCE = re.compile(r"initial=\{\{\s*opacity:\s*0|\banimate-(?:fade|slide)-(?:in|up)\b")
HEX_LIT = re.compile(r"(?<![&\w])#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
BUTTON_TEXT = re.compile(r"<(?:button|Button)\b[^>]*>\s*([^<{]+?)\s*<")
FONT_DECL = re.compile(r"font-family\s*:\s*([^;}\n]+)|fontFamily\s*:\s*[\"']([^\"']+)[\"']|@fontsource(?:-variable)?/([\w-]+)")
NEXT_FONT = re.compile(r"import\s*\{([^}]+)\}\s*from\s*[\"']next/font/google[\"']")
GENERIC_FONTS = {"sans-serif", "serif", "monospace", "system-ui", "-apple-system", "blinkmacsystemfont", "inherit",
                 "ui-sans-serif", "ui-serif", "ui-monospace", "cursive", "emoji"}


def _finding(rule, family, rel, line, message):
    return {"rule": rule, "family": family, "file": rel, "line": line, "message": message}


def _line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def _first(lines, rx):
    for i, ln in enumerate(lines, 1):
        if re.search(rx, ln):
            return i
    return 1


def _elements(text):
    """(line, tag, attrs) for every input element, reading past braces so arrow functions don't end the tag."""
    for m in re.finditer(r"<(input|Input|TextInput)\b", text):
        i, depth = m.end(), 0
        while i < len(text):
            ch = text[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            elif ch == ">" and depth == 0:
                break
            i += 1
        yield _line_of(text, m.start()), m.group(1), text[m.end():i]


def scan_text(text, rel):
    """Findings that need only this one file."""
    out = []
    add = lambda rule, fam, line, msg: out.append(_finding(rule, fam, rel, line, msg))
    lines = text.splitlines()
    for i, ln in enumerate(lines, 1):
        for rid, fam, rx, msg in LINE_RULES:
            if rx.search(ln):
                add(rid, fam, i, msg)
    has_for = "htmlFor=" in text or re.search(r"<label\b[^>]*\bfor=", text)
    for line, tag, attrs in _elements(text):
        labelled = re.search(r"aria-label|aria-labelledby|accessibilityLabel", attrs)
        if "placeholder" in attrs and not labelled and not has_for:
            add("FM-placeholder-only", "forms", line, "placeholder used as the only label")
        sensitive = re.search(r"type=[\"'](?:email|password|tel)[\"']|placeholder=[\"'][^\"']*(?:email|password|phone)", attrs, re.I)
        if sensitive and not re.search(r"autoComplete|autocomplete|textContentType", attrs):
            add("FM-no-autocomplete", "forms", line, "no autocomplete hint on a field browsers can fill")
        if tag != "TextInput" and re.search(r"className=[\"'][^\"']*\btext-(?:xs|sm)\b", attrs):
            add("FM-small-input", "forms", line, "input text under 16px, so iOS zooms the page")
    if rel.endswith((".css", ".scss")):
        n = sum(1 for v in SHADCN_HSL | SHADCN_OKLCH if v in text)
        if n >= 4:
            add("F-shadcn-untouched", "fingerprint", 1, f"{n} untouched shadcn default colours")
    if NUMBERS.search(text) and not re.search(r"tabular-nums|fontVariant", text):
        add("C-tabular", "copy", _first(lines, NUMBERS.pattern), "numbers without tabular figures")
    for i, ln in enumerate(lines):
        if re.search(r"if\s*\(\s*!?\s*\w*[lL]oading\w*\s*\)", ln) and any(SPINNER.search(x) for x in lines[i:i + 5]):
            add("L-fullscreen-spinner", "loading", i + 1, "a spinner replaces the whole page while loading")
    if SPINNER.search(text) and not re.search(r"delay|setTimeout|useDeferredValue|startTransition", text, re.I):
        add("L-no-delay", "loading", _first(lines, SPINNER.pattern), "the loader shows at once; wait 150 to 300 ms")
    for i, ln in enumerate(lines):
        if re.search(r"request\w*PermissionsAsync\(", ln) and any("useEffect(" in x for x in lines[max(0, i - 5):i]):
            add("L-permission-on-mount", "loading", i + 1, "permission asked on mount; ask when the feature is first used")
    for rid, rx, minimum, msg in SECOND_ORDER:
        hits = list(rx.finditer(text))
        if len(hits) >= minimum:
            add(rid, "second-order", _line_of(text, hits[0].start()), msg)
    return out


def _font_families(text):
    for i, ln in enumerate(text.splitlines(), 1):
        for m in FONT_DECL.finditer(ln):
            raw = m.group(1) or m.group(2) or (m.group(3) or "").replace("-", " ")
            for f in raw.split(","):
                f = f.strip().strip("\"'").strip()
                if f and f.lower() not in GENERIC_FONTS and not f.startswith("var("):
                    yield f, i
        for m in NEXT_FONT.finditer(ln):
            for f in m.group(1).split(","):
                if f.strip():
                    yield f.strip().replace("_", " "), i


def scan(root):
    files = list(walk(root))
    out = []
    for rel, text in files:
        out += scan_text(text, rel)
    add = lambda rule, fam, rel, line, msg: out.append(_finding(rule, fam, rel, line, msg))

    fams = {}
    for rel, text in files:
        for fam, line in _font_families(text):
            fams.setdefault(fam.lower(), (rel, line))
    if set(fams) == {"inter"}:
        add("F-inter-only", "fingerprint", *fams["inter"], "Inter is the only typeface")
    cards = [(rel, i) for rel, text in files for i, ln in enumerate(text.splitlines(), 1) if UNIFORM.search(ln)]
    if len(cards) >= 3:
        add("F-uniform-card", "fingerprint", *cards[0], f"the same rounded, shadowed card on {len(cards)} elements")
    ent = [(rel, i) for rel, text in files for i, ln in enumerate(text.splitlines(), 1) if ENTRANCE.search(ln)]
    if len(ent) >= 4:
        add("F-entrance-everywhere", "fingerprint", *ent[0], f"the same entrance animation on {len(ent)} elements")
    seen = {}
    for rel, text in files:
        for i, ln in enumerate(text.splitlines(), 1):
            for h in HEX_LIT.findall(ln):
                h6 = "#" + ("".join(c * 2 for c in h) if len(h) == 3 else h).lower()
                if h6 in TAILWIND_HEX and h6 not in seen:
                    seen[h6] = (rel, i)
    for h6, (rel, i) in seen.items():
        add("F-tailwind-hex", "fingerprint", rel, i, f"{h6} is Tailwind's {TAILWIND_HEX[h6]}")
    styles = {}
    for rel, text in files:
        for m in BUTTON_TEXT.finditer(text):
            words = m.group(1).split()
            if len(words) < 2 or not words[0][0].isupper():
                continue
            kind = "title" if all(w[0].isupper() for w in words if w[0].isalpha()) else "sentence"
            styles.setdefault(kind, (rel, _line_of(text, m.start())))
    if len(styles) == 2:
        add("C-mixed-case", "copy", *styles["title"], "buttons mix Title Case and sentence case")
    anim = any(re.search(r"framer-motion|react-native-reanimated|@keyframes|\banimate-|\btransition", t) for _, t in files)
    calm = any(re.search(r"prefers-reduced-motion|useReducedMotion|motion-reduce|motion-safe|ReduceMotion|reduceMotion", t) for _, t in files)
    if anim and not calm:
        add("A-no-reduced-motion", "a11y", "", 0, "animation with no reduced-motion handling")
    for name in ("app.json", "app.config.json"):
        p = os.path.join(root, name)
        if not os.path.isfile(p):
            continue
        try:
            cfg = json.load(open(p, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if ((cfg.get("expo") or cfg).get("splash") or {}).get("image"):
            add("L-launch-image", "loading", name, 1, "the launch screen shows an image; it should look like the first screen")
    return out


def summary(findings):
    c = {f: 0 for f in FAMILIES}
    for x in findings:
        c[x["family"]] += 1
    return f"TELLS {len(findings)} (" + " · ".join(f"{f} {c[f]}" for f in FAMILIES) + ")"


def main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    fs = scan(argv[0])
    for x in fs:
        where = f"{x['file']}:{x['line']}" if x["file"] else "(repo)"
        print(f"TELL {x['family']} {x['rule']} {where} {x['message']}")
    if "--json" in argv:
        fams = {f: sum(1 for x in fs if x["family"] == f) for f in FAMILIES}
        with open(argv[argv.index("--json") + 1], "w", encoding="utf-8") as f:
            json.dump({"total": len(fs), "families": fams, "findings": fs}, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print(summary(fs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 tests/glowup_test.py -v TellsTest`
Expected: PASS. If a family count is off, print the findings (the assertion message does this) and check them against the fixture line by line. The expected web findings are:
- fingerprint: 5 line rules, shadcn, Inter, uniform card, `#6b7280`
- forms: 2 placeholder, 2 autocomplete, 2 small input, asterisk, disabled, onChange
- copy: oops, submit, dots, quote, buzzwords, toFixed, tabular, mixed case
- a11y: outline, div, transition, reduced motion
- loading: spinner, no delay

- [ ] **Step 5: Commit**

```bash
git add skills/design-studio/scripts/tells_lint.py tests/glowup_test.py
git commit -m "feat(glowup): tells_lint finds the six families of vibe-coded tells"
```

---

### Task 5: Smoke fixture and `glowup_check.py`

**Files:**
- Create: `tests/fixtures/glowup-smoke/make.py`, `context.md`, `category.md`, `r1/manifest.json`, `r2/manifest.json`, `r3/manifest.json`
- Generated by `make.py` (commit them): `r1/v01/{tokens.css,s1..s4.html}`, `r1/v02/{theme.json,tokens.css,s1..s4.html}`, `r2/v01/{theme.json,tokens.css,routes/home.html,routes/settings.html}`, `before/s1..s4.png`, `r3/after/home.png`, `entropy-before.json`, `tells-before.json`, `r3/entropy-after.json`, `r3/tells-after.json`
- Create: `skills/design-studio/scripts/glowup_check.py`
- Modify: `tests/studio.test.sh` (new section above `# --- new tests above this line ---`)

**Interfaces:**
- Consumes: `theme_core.load_theme`, `validate_theme`, `contrast_errors`, `default_hits`, `second_order_hits`, `SCREENS` (Task 1); `theme_tokens.css` (Task 2); `tells_lint.scan_text` (Task 4).
- Produces: `glowup_check.py <round-dir>`, with these summaries:
  - `OK <n> glow-up direction(s) (<stage>, 4 screens)`
  - `OK <n> glow-up system (<k> routes)`
  - `OK glow-up apply stage <s> (entropy <a> → <b>, tells <c> → <d>)`

  It exits 1 on any FAIL. The manifest shapes below are the contract that Tasks 6, 7 and 9 rely on.

- [ ] **Step 1: Write the static fixture files**

`tests/fixtures/glowup-smoke/context.md`:

```markdown
# Notes app: context

**Job:** keep a small team's notes findable and shared.
**Surface:** web (Vite, React, Tailwind 3, shadcn)
**Key screens:** s1 Dashboard (dashboard), s2 Notes list (split), s3 New note (column), s4 Empty state (column)

## Content contract
- Dashboard: notes this week, shared count, recent notes
- Notes list: every note title, the long title case
- New note: title field, save action
- Empty state: first-note prompt, start action

## UI strings
- Welcome to your dashboard
- Oops! Something went wrong
- Get Started
- Submit
- No notes yet

## Fixture
- Longest title: "Q3 planning review with the design, research and platform teams"
```

`tests/fixtures/glowup-smoke/category.md`:

```markdown
# Category: team notes

| App | Type | Colour field | Neutral | Shape | Density | Tone | Signature | Source |
|---|---|---|---|---|---|---|---|---|
| Example A | Grotesk | Light | Cool | Soft | Balanced | Calm | Page icons | public site |

## Table stakes
1. Calm neutrals and one action colour.

## White space
1. Nobody uses a serif for headings.
```

`tests/fixtures/glowup-smoke/r1/manifest.json`:

```json
{
  "project": "demo", "topic": "notes", "title": "Notes app glow-up", "round": 1,
  "mode": "glowup", "surface": "web", "stage": "directions",
  "brief": "Smoke fixture: two theme directions for a small team notes app.",
  "agentPick": "v01", "predictedPick": "v02",
  "screens": [
    { "id": "s1", "label": "Dashboard" }, { "id": "s2", "label": "Notes list" },
    { "id": "s3", "label": "New note" }, { "id": "s4", "label": "Empty state" }
  ],
  "before": {
    "s1": "../before/s1.png", "s2": "../before/s2.png", "s3": "../before/s3.png", "s4": "../before/s4.png",
    "headline": "33 values: 11 colours · 5 font sizes · 3 weights · 8 spacing values · 4 radii · 2 shadows",
    "summary": "32 tells (fingerprint 9 · forms 9 · copy 8 · a11y 4 · loading 2)"
  },
  "category": "../category.md",
  "variations": [
    { "id": "v01", "dir": "v01", "name": "Ledger", "idea": "A calm, ruled notebook: serif headings, one blue action, a generous reading column.", "tags": ["conventional"],
      "notes": { "market": "Team notes tools earn trust with calm neutrals and one action colour (category.md, table stakes 1).", "signature": "A ruled line under every section heading.", "convention": "Neutral ground, blue action, sidebar on desktop.", "different": "A serif display face where the category uses grotesks.", "ripple": "Settings and onboarding take the ruled headings too." } },
    { "id": "v02", "dir": "v02", "name": "Studio", "idea": "A drafting table: square corners, hairline borders, a technical grotesk.", "tags": ["twist"],
      "notes": { "market": "Keeps the category's calm neutrals (table stakes 1) and swaps softness for precision.", "signature": "Corner ticks on every card.", "convention": "Neutral ground, one action colour.", "different": "Hairline borders instead of shadows.", "ripple": "Every card in the app gets corner ticks." } }
  ]
}
```

`tests/fixtures/glowup-smoke/r2/manifest.json`:

```json
{
  "project": "demo", "topic": "notes", "title": "Notes app glow-up", "round": 2,
  "mode": "glowup", "surface": "web", "stage": "system",
  "brief": "Smoke fixture: Ledger across every route.",
  "parent": { "round": 1, "id": "v01", "name": "Ledger" },
  "agentPick": "v01", "predictedPick": "v01",
  "screens": [
    { "id": "s1", "label": "Dashboard" }, { "id": "s2", "label": "Notes list" },
    { "id": "s3", "label": "New note" }, { "id": "s4", "label": "Empty state" }
  ],
  "routes": [ { "id": "home", "label": "Home" }, { "id": "settings", "label": "Settings" } ],
  "variations": [
    { "id": "v01", "dir": "v01", "name": "Ledger", "idea": "Ledger on every route.", "tags": [], "notes": { "market": "As round 1.", "signature": "Ruled headings." } }
  ]
}
```

`tests/fixtures/glowup-smoke/r3/manifest.json`:

```json
{
  "project": "demo", "topic": "notes", "title": "Notes app glow-up", "round": 3,
  "mode": "glowup", "surface": "web", "stage": "apply",
  "brief": "Smoke fixture: apply stage 3 of Ledger.",
  "parent": { "round": 2, "id": "v01", "name": "Ledger" },
  "apply": {
    "stage": 3, "branch": "glowup/notes",
    "themeFiles": ["src/index.css", "tailwind.config.js"],
    "entropyBefore": "../entropy-before.json", "entropyAfter": "entropy-after.json",
    "tellsBefore": "../tells-before.json", "tellsAfter": "tells-after.json",
    "build": "pass", "reverted": false,
    "headline": "Entropy 33 → 15 · tells 32 → 9",
    "routes": [ { "id": "home", "label": "Home", "before": "../before/s1.png", "after": "after/home.png" } ],
    "followUps": ["FM-validate-onchange in src/pages/Settings.tsx:5 changes behaviour, so apply left it alone"]
  }
}
```

- [ ] **Step 2: Write `make.py` and run it**

`tests/fixtures/glowup-smoke/make.py`:

```python
#!/usr/bin/env python3
"""Regenerate the glow-up smoke fixture from r1/v01/theme.json and the two
fixture apps. Run from the repo root: python3 tests/fixtures/glowup-smoke/make.py"""
import base64, copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(FIX))
SCRIPTS = os.path.join(REPO, "skills", "design-studio", "scripts")
sys.path.insert(0, SCRIPTS)
import theme_tokens as tt

PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
SCREENS = {
    "s1": ("Dashboard", "dashboard", '<h1 class="t-h1 span-all"{sig}>Your notes</h1>\n  <p class="t-eyebrow span-all">This week</p>\n  <p class="t-body tnum span-all">12 notes, 3 shared with the team</p>'),
    "s2": ("Notes list", "split", '<h2 class="t-h2 span-all"{sig}>All notes</h2>\n  <ul class="t-body span-all">\n    <li>Q3 planning review with the design, research and platform teams</li>\n    <li>Standup</li>\n    <li>Hiring loop</li>\n  </ul>'),
    "s3": ("New note", "column", '<h2 class="t-h2"{sig}>New note</h2>\n  <label class="t-small" for="title">Title</label>\n  <input id="title" name="title" autocomplete="off">\n  <button class="btn">Save note</button>'),
    "s4": ("Empty state", "column", '<h2 class="t-h2"{sig}>No notes yet</h2>\n  <p class="t-body">Your first one takes ten seconds.</p>\n  <button class="btn">Start a note</button>'),
}
SETTINGS = ("Settings", "column", '<h2 class="t-h2"{sig}>Settings</h2>\n  <p class="t-body">Notifications are on for shared notes.</p>')


def write(path, text, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        f.write(text)


def page(theme, screen, frame_href, tokens_href, sig):
    title, tpl, body = screen
    body = body.replace("{sig}", " data-signature" if sig else "")
    return (f'<!doctype html>\n<html lang="en" data-theme="light">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{theme["name"]} · {title}</title>\n'
            f'<link rel="stylesheet" href="{frame_href}">\n<link rel="stylesheet" href="{tokens_href}">\n</head>\n'
            f'<body data-template="{tpl}">\n<main class="tpl-{tpl}">\n  {body}\n</main>\n</body>\n</html>\n')


def direction(vdir, theme):
    write(os.path.join(vdir, "theme.json"), json.dumps(theme, indent=2, ensure_ascii=False) + "\n")
    write(os.path.join(vdir, "tokens.css"), tt.css(theme))


def main():
    v01 = json.load(open(os.path.join(HERE, "r1", "v01", "theme.json"), encoding="utf-8"))
    v02 = copy.deepcopy(v01)
    v02["name"] = "Studio"
    v02["type"]["display"] = {"family": "Space Grotesk", "weights": [500, 700]}
    v02["type"]["body"] = {"family": "IBM Plex Sans", "weights": [400, 500, 600]}
    v02["type"]["pairing"] = "A technical grotesk with a humanist workhorse: precise without being cold."
    v02["type"]["ramp"]["h2"]["weight"] = 500
    v02["shape"]["radius"] = {"sm": 2, "md": 6, "lg": 12, "full": 999}
    v02["elevation"]["style"] = "border"
    v02["signature"] = {"what": "Corner ticks on every card, like a drafting table", "where": ["s1", "s3"],
                        "never": "Never on buttons or the page edge", "uses": []}
    v02["voice"]["adjectives"] = ["direct", "technical", "dry"]
    for vid, th in (("v01", v01), ("v02", v02)):
        vdir = os.path.join(HERE, "r1", vid)
        direction(vdir, th)
        for sid, screen in SCREENS.items():
            write(os.path.join(vdir, f"{sid}.html"), page(th, screen, "../web.css", "tokens.css", sid in th["signature"]["where"]))
    sysdir = os.path.join(HERE, "r2", "v01")
    direction(sysdir, v01)
    for rid, screen in (("home", SCREENS["s1"]), ("settings", SETTINGS)):
        write(os.path.join(sysdir, "routes", f"{rid}.html"), page(v01, screen, "../../web.css", "../tokens.css", rid == "home"))
    for s in SCREENS:
        write(os.path.join(HERE, "before", f"{s}.png"), PNG, "wb")
    write(os.path.join(HERE, "r3", "after", "home.png"), PNG, "wb")
    for script, flag, name in (("entropy.py", "--out", "entropy-before.json"), ("tells_lint.py", "--json", "tells-before.json")):
        subprocess.run([sys.executable, os.path.join(SCRIPTS, script), os.path.join(FIX, "glowup-web"), flag, os.path.join(HERE, name)],
                       check=True, stdout=subprocess.DEVNULL)
    after = {"root": "glowup-web", "files": 3, "total": 15,
             "colors": {"count": 1, "values": {"#ffffff": {"count": 1, "files": ["src/index.css"]}}},
             "font-sizes": {"count": 4, "values": {}}, "font-weights": {"count": 2, "values": {}},
             "spacing": {"count": 5, "values": {}}, "radii": {"count": 2, "values": {}}, "shadows": {"count": 1, "values": {}},
             "headline": "1 colour · 4 font sizes · 2 weights · 5 spacing values · 2 radii · 1 shadow"}
    write(os.path.join(HERE, "r3", "entropy-after.json"), json.dumps(after, indent=2, ensure_ascii=False) + "\n")
    tells = {"total": 9, "families": {"fingerprint": 0, "forms": 3, "copy": 2, "a11y": 2, "loading": 2, "second-order": 0}, "findings": []}
    write(os.path.join(HERE, "r3", "tells-after.json"), json.dumps(tells, indent=2) + "\n")
    print("OK glow-up smoke fixture regenerated")


if __name__ == "__main__":
    main()
```

Run: `python3 tests/fixtures/glowup-smoke/make.py`
Expected: `OK glow-up smoke fixture regenerated`. `tests/fixtures/glowup-smoke/entropy-before.json` has `"total": 33` and `tells-before.json` has `"total": 32`.

- [ ] **Step 3: Write the failing shell tests**

Insert into `tests/studio.test.sh` directly above `# --- new tests above this line ---`:

```bash
echo "glow-up: python units"
out="$(python3 "$HERE/glowup_test.py" 2>&1)"; st=$?
[ $st -eq 0 ] && ok "glowup_test.py passes" || bad "glowup_test.py passes" "$(tail -30 <<<"$out")"

echo "glow-up: check"
SCRIPTS="$REPO/skills/design-studio/scripts"
gfresh() { stage glowup-smoke demo "g$RANDOM$RANDOM"; }
regen() { python3 "$SCRIPTS/theme_tokens.py" "$1/theme.json" --css --out "$1/tokens.css"; }
jedit() { python3 - "$1" "$2" <<'PY'
import json, sys
p, code = sys.argv[1], sys.argv[2]
d = json.load(open(p)); exec(code); json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)
PY
}
t="$(gfresh)"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$(tail -1 <<<"$out")" = "OK 2 glow-up directions (directions, 4 screens)" ] && ok "check passes a directions round" || bad "check passes a directions round" "$out"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r2" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$(tail -1 <<<"$out")" = "OK 1 glow-up system (2 routes)" ] && ok "check passes a system round" || bad "check passes a system round" "$out"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK glow-up apply stage 3 (entropy 33 → 15, tells 32 → 9)" ] && ok "check passes an apply round" || bad "check passes an apply round" "$out"

t="$(gfresh)"; perl -pi -e 's/ data-signature//' "$t/r1/v01/s2.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"; st=$?
[ $st -ne 0 ] && grep -q "FAIL v01: signature element appears on 1 screen (need 2)" <<<"$out" && ok "check wants the signature on two screens" || bad "check wants the signature on two screens" "$out"

t="$(gfresh)"; jedit "$t/r1/v01/theme.json" 'd["shape"]["radius"]["md"] = 8'; regen "$t/r1/v01"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01: shape.radius.md is shadcn's 0.5rem radius; give it a line in reasons or change it" <<<"$out" && ok "check wants a reason for a default" || bad "check wants a reason for a default" "$out"
jedit "$t/r1/v01/theme.json" 'd["reasons"]["shape.radius.md"] = "8px matches the platform input radius"'; regen "$t/r1/v01"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"; st=$?
[ $st -eq 0 ] && ok "a reason clears the default" || bad "a reason clears the default" "$out"

t="$(gfresh)"; echo "/* hand edit */" >> "$t/r1/v02/tokens.css"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v02/tokens.css is stale; regenerate it with theme_tokens.py --css" <<<"$out" && ok "check fails stale tokens" || bad "check fails stale tokens" "$out"

t="$(gfresh)"; perl -pi -e 's|<h2 class="t-h2">New note</h2>|<h2 class="t-h2" style="color:#ff0000">New note</h2>|' "$t/r1/v01/s3.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01/s3.html: literal colour '#ff0000'; use the tokens" <<<"$out" && ok "check fails a literal colour" || bad "check fails a literal colour" "$out"

t="$(gfresh)"; perl -ni -e 'print unless /^- Submit$/' "$t/context.md"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01: voice string 'Submit' is not in context.md" <<<"$out" && ok "check wants real voice strings" || bad "check wants real voice strings" "$out"

t="$(gfresh)"; perl -pi -e 's/data-template="column"/data-template="hero"/' "$t/r1/v01/s4.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01/s4.html: data-template hero is not in theme.layout.templates" <<<"$out" && ok "check wants a declared layout template" || bad "check wants a declared layout template" "$out"

t="$(gfresh)"; perl -pi -e 's|>Your notes<|>Elevate your notes<|' "$t/r1/v01/s1.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01/s1.html:[0-9]*: C-buzzwords" <<<"$out" && ok "check runs the tells on screens" || bad "check runs the tells on screens" "$out"

t="$(gfresh)"; jedit "$t/r1/v01/theme.json" 'd["color"]["light"]["ground"] = "oklch(0.96 0.02 80)"; d["color"]["light"]["action"] = "oklch(0.55 0.13 40)"'; regen "$t/r1/v01"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01: second-order tell cream-terracotta" <<<"$out" && ok "check fails an unnamed second-order tell" || bad "check fails an unnamed second-order tell" "$out"
jedit "$t/r1/v01/theme.json" 'd["signature"]["uses"] = ["cream-terracotta"]'; regen "$t/r1/v01"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "second-order tell cream-terracotta" <<<"$out" && bad "a named signature allows a second-order pattern" "$out" || ok "a named signature allows a second-order pattern"

t="$(gfresh)"; rm "$t/r2/v01/routes/settings.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r2" 2>&1)"
grep -q "FAIL v01: missing route settings (routes/settings.html)" <<<"$out" && ok "check wants every route" || bad "check wants every route" "$out"

t="$(gfresh)"; jedit "$t/r3/entropy-after.json" 'd["colors"]["count"] = 30'
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"
grep -q "FAIL entropy rose: 33 → 44" <<<"$out" && ok "check fails rising entropy" || bad "check fails rising entropy" "$out"

t="$(gfresh)"; jedit "$t/r3/entropy-after.json" 'd["colors"]["values"]["#ffffff"]["files"].append("src/App.tsx")'
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"
grep -q "FAIL literal colours outside the theme files: src/App.tsx" <<<"$out" && ok "check fails stray literal colours" || bad "check fails stray literal colours" "$out"

t="$(gfresh)"; jedit "$t/r3/manifest.json" 'd["apply"]["build"] = "fail"'
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"
grep -q "FAIL build failed and the stage was not reverted" <<<"$out" && ok "check fails an unreverted broken build" || bad "check fails an unreverted broken build" "$out"
```

The cream-terracotta mutation darkens the action to L 0.55 so `on-action` keeps its contrast. The test only greps for the second-order line, so a contrast line, if one appears, doesn't affect it.

- [ ] **Step 4: Run them to verify they fail**

Run: `bash tests/studio.test.sh 2>&1 | grep -A2 "glow-up: check"`
Expected: FAIL lines with `can't open file '.../glowup_check.py'`.

- [ ] **Step 5: Write `glowup_check.py`**

```python
#!/usr/bin/env python3
"""Validate a glow-up round before the link goes out.

  glowup_check.py <round-dir>

directions / converge: every direction has a valid theme.json (contrast,
defaults with reasons, second-order tells only as the named signature), a
tokens.css that matches theme_tokens.py --css, voice strings found in
context.md, notes.market and notes.signature, and four key screens that link
their tokens and frame, declare a layout template, use no literal colours,
carry no fingerprint, copy or second-order tells, and show the signature on
at least two screens.
system: the same theme checks, plus every manifest route as routes/<id>.html.
apply: before/after evidence exists, entropy and tells did not rise (and
entropy fell from stage 3), no literal colours outside the theme files, and
a failed build was reverted.
Prints WARN/FAIL lines, then "OK|FAIL <summary>". Exits 1 on any FAIL.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tells_lint as tl
import theme_core as tc
import theme_tokens as tt

LITERAL = re.compile(r"(?<!&)#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch)\(")
TEMPLATE = re.compile(r'data-template="([\w-]+)"')
TOKENS_LINK = re.compile(r'href="(?:\.\./)?tokens\.css"')
LINT_FAMILIES = ("fingerprint", "copy", "second-order")
ENTROPY_KINDS = ("colors", "font-sizes", "font-weights", "spacing", "radii", "shadows")


def _context(d, warns):
    p = os.path.join(d, "..", "context.md")
    if not os.path.isfile(p):
        warns.append("no ../context.md for this topic")
        return ""
    return open(p, encoding="utf-8").read()


def theme_errors(vdir, vid, context_text):
    try:
        t = tc.load_theme(os.path.join(vdir, "theme.json"))
    except (OSError, ValueError) as e:
        return None, [f"{vid}/theme.json unreadable: {e}"]
    errs = [f"{vid}/theme.json: {m}" for m in tc.validate_theme(t)]
    if errs:
        return None, errs
    errs += [f"{vid}: contrast {m}" for m in tc.contrast_errors(t)]
    reasons = t.get("reasons") or {}
    errs += [f"{vid}: {path} is {why}; give it a line in reasons or change it" for path, why in tc.default_hits(t) if path not in reasons]
    uses = set(t["signature"].get("uses") or [])
    errs += [f"{vid}: second-order tell {sid} ({why}) is not the named signature" for sid, why in tc.second_order_hits(t) if sid not in uses]
    tok = os.path.join(vdir, "tokens.css")
    if not os.path.isfile(tok):
        errs.append(f"{vid}: no tokens.css (run theme_tokens.py {vid}/theme.json --css --out {vid}/tokens.css)")
    elif open(tok, encoding="utf-8").read() != tt.css(t):
        errs.append(f"{vid}/tokens.css is stale; regenerate it with theme_tokens.py --css")
    for s in t["voice"]["strings"]:
        if s["before"] not in context_text:
            errs.append(f"{vid}: voice string {s['before']!r} is not in context.md")
    return t, errs


def page_errors(path, rel, t, frame):
    html = open(path, encoding="utf-8").read()
    errs = []
    if not TOKENS_LINK.search(html):
        errs.append(f"{rel}: does not link its direction's tokens.css")
    if frame not in html:
        errs.append(f"{rel}: does not link {frame}")
    ids = {tp["id"] for tp in t["layout"]["templates"]}
    m = TEMPLATE.search(html)
    if not m:
        errs.append(f"{rel}: no data-template (every screen uses one of {', '.join(sorted(ids))})")
    elif m.group(1) not in ids:
        errs.append(f"{rel}: data-template {m.group(1)} is not in theme.layout.templates")
    lit = LITERAL.search(html)
    if lit:
        errs.append(f"{rel}: literal colour {lit.group(0)!r}; use the tokens")
    if re.search(r"lorem ipsum", html, re.I):
        errs.append(f"{rel}: lorem ipsum")
    uses = set(t["signature"].get("uses") or [])
    for f in tl.scan_text(html, rel):
        if f["family"] in LINT_FAMILIES and f["rule"] not in uses:
            errs.append(f"{rel}:{f['line']}: {f['rule']} ({f['message']})")
    return errs, html


def _frame(m):
    return "web.css" if m.get("surface") == "web" else "screen.css"


def _names(vs, errs):
    seen = set()
    for v in vs:
        n = (v.get("name") or "").strip().lower()
        if n in seen:
            errs.append(f"duplicate name {n}")
        seen.add(n)


def check_directions(d, m, errs, warns):
    stage = m["stage"]
    got = [s.get("id") for s in m.get("screens", [])]
    if got != list(tc.SCREENS):
        errs.append(f"manifest screens must be {', '.join(tc.SCREENS)} (got {', '.join(map(str, got)) or 'none'})")
    ctx = _context(d, warns)
    vs = m.get("variations", [])
    if stage == "directions" and len(vs) < 2:
        errs.append(f"only {len(vs)} directions")
    _names(vs, errs)
    for v in vs:
        vid = v.get("id", "?")
        vdir = os.path.join(d, v.get("dir", vid))
        notes = v.get("notes") or {}
        for k in ("market", "signature"):
            if not str(notes.get(k, "")).strip():
                errs.append(f"{vid}: notes.{k} is empty")
        t, te = theme_errors(vdir, vid, ctx)
        errs += te
        if t is None:
            continue
        sig = 0
        for s in tc.SCREENS:
            p = os.path.join(vdir, f"{s}.html")
            if not os.path.isfile(p):
                errs.append(f"{vid}: missing {s}.html")
                continue
            pe, html = page_errors(p, f"{vid}/{s}.html", t, _frame(m))
            errs += pe
            sig += "data-signature" in html
        if sig < 2:
            errs.append(f"{vid}: signature element appears on {sig} screen{'' if sig == 1 else 's'} (need 2)")
    return f"{len(vs)} glow-up direction{'' if len(vs) == 1 else 's'} ({stage}, {len(tc.SCREENS)} screens)"


def check_system(d, m, errs, warns):
    routes = [r.get("id") for r in m.get("routes", [])]
    if not routes:
        errs.append("system round lists no routes")
    ctx = _context(d, warns)
    vs = m.get("variations", [])
    if not 1 <= len(vs) <= 2:
        errs.append(f"system round holds 1 or 2 variations, has {len(vs)}")
    _names(vs, errs)
    for v in vs:
        vid = v.get("id", "?")
        vdir = os.path.join(d, v.get("dir", vid))
        t, te = theme_errors(vdir, vid, ctx)
        errs += te
        if t is None:
            continue
        for r in routes:
            p = os.path.join(vdir, "routes", f"{r}.html")
            if not os.path.isfile(p):
                errs.append(f"{vid}: missing route {r} (routes/{r}.html)")
                continue
            errs += page_errors(p, f"{vid}/routes/{r}.html", t, _frame(m))[0]
    return f"{len(vs)} glow-up system ({len(routes)} routes)"


def _entropy_total(e):
    return sum(e[k]["count"] for k in ENTROPY_KINDS)


def check_apply(d, m, errs, warns):
    a = m.get("apply") or {}
    st = a.get("stage")
    if st not in (1, 2, 3, 4):
        errs.append(f"apply.stage must be 1 to 4 (got {st!r})")
        return "glow-up apply"
    paths = {}
    for k in ("entropyBefore", "entropyAfter", "tellsBefore", "tellsAfter"):
        paths[k] = os.path.normpath(os.path.join(d, a.get(k) or "missing"))
        if not a.get(k) or not os.path.isfile(paths[k]):
            errs.append(f"apply.{k} missing ({a.get(k)})")
    if not a.get("routes"):
        errs.append("apply board shows no routes")
    for r in a.get("routes") or []:
        for side in ("before", "after"):
            if not r.get(side) or not os.path.isfile(os.path.join(d, r[side])):
                errs.append(f"route {r.get('id')}: missing {side} image {r.get(side)}")
    if a.get("build") == "fail" and not a.get("reverted"):
        errs.append("build failed and the stage was not reverted")
    if errs:
        return f"glow-up apply stage {st}"
    before = json.load(open(paths["entropyBefore"], encoding="utf-8"))
    after = json.load(open(paths["entropyAfter"], encoding="utf-8"))
    eb, ea = _entropy_total(before), _entropy_total(after)
    tb = json.load(open(paths["tellsBefore"], encoding="utf-8"))["total"]
    ta = json.load(open(paths["tellsAfter"], encoding="utf-8"))["total"]
    if ea > eb:
        errs.append(f"entropy rose: {eb} → {ea}")
    elif st >= 3 and ea == eb:
        errs.append(f"entropy did not drop at stage {st}: {eb} → {ea}")
    if ta > tb:
        errs.append(f"tells rose: {tb} → {ta}")
    if st >= 3:
        theme_files = set(a.get("themeFiles") or [])
        stray = sorted({f for v in after["colors"]["values"].values() for f in v["files"] if f not in theme_files})
        if stray:
            errs.append("literal colours outside the theme files: " + ", ".join(stray[:5]))
    return f"glow-up apply stage {st} (entropy {eb} → {ea}, tells {tb} → {ta})"


def main(d):
    errs, warns = [], []
    try:
        m = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"FAIL manifest.json unreadable: {e}")
        return 1
    if m.get("mode") != "glowup":
        errs.append("manifest mode is not glowup")
    stage = m.get("stage")
    if stage in ("directions", "converge"):
        summary = check_directions(d, m, errs, warns)
    elif stage == "system":
        summary = check_system(d, m, errs, warns)
    elif stage == "apply":
        summary = check_apply(d, m, errs, warns)
    else:
        errs.append(f"unknown stage {stage}")
        summary = "glow-up round"
    if stage in ("directions", "converge", "system"):
        for k in ("agentPick", "predictedPick"):
            if k not in m:
                warns.append(f"manifest has no {k}")
    for w in warns:
        print("WARN", w)
    for e in errs:
        print("FAIL", e)
    print(f"{'FAIL' if errs else 'OK'} {summary}")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1].rstrip("/")))
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `bash tests/studio.test.sh`
Expected: every `glow-up: check` line is `ok`, every older line is still `ok`, and the run ends with `N passed, 0 failed`.

- [ ] **Step 7: Commit**

```bash
git add skills/design-studio/scripts/glowup_check.py tests/fixtures/glowup-smoke tests/studio.test.sh
git commit -m "feat(glowup): glowup_check gates directions, system and apply rounds"
```

---

### Task 6: `studio.sh` routing and `glowup_sheets.py`

**Files:**
- Modify: `skills/design-studio/scripts/studio.sh` (header line 4, `new_round`, add `mode_of`, `check`, `sheets`, dispatcher `new)` line)
- Create: `skills/design-studio/scripts/glowup_sheets.py`
- Modify: `tests/studio.test.sh`

**Interfaces:**
- Consumes: manifest shapes from Task 5.
- Produces: `studio.sh new <project> <topic> --glowup [--web]` copies `assets/gallery-glowup.html` as `index.html` plus `screen.css` and `web.css`, and prints `MODE glowup` (and `SURFACE web` with `--web`). `studio.sh check` and `studio.sh sheets` route glow-up rounds. `glowup_sheets.py <round-dir>` writes `_sheet-before.html`, then `_sheet-<vid>.html` per direction (directions/converge) or `_sheet-<vid>-<n>.html` per four routes (system), and prints `SHEETS <n>`.

- [ ] **Step 1: Write the failing tests**

Insert above `# --- new tests above this line ---` in `tests/studio.test.sh`:

```bash
echo "glow-up: new, check and sheets routing"
out="$(bash "$STUDIO" new demo glow --glowup 2>&1)"
rd="$DESIGN_STUDIO_ROOT/demo/glow/r1"
grep -qx "MODE glowup" <<<"$out" && ok "new --glowup prints MODE glowup" || bad "new --glowup prints MODE glowup" "$out"
[ -f "$rd/screen.css" ] && [ -f "$rd/web.css" ] && ok "new --glowup copies both frame stylesheets" || bad "new --glowup copies both frame stylesheets" "$(ls "$rd")"
grep -q "^SURFACE" <<<"$out" && bad "app glow-up prints no SURFACE line" "$out" || ok "app glow-up prints no SURFACE line"
out="$(bash "$STUDIO" new demo glowweb --glowup --web 2>&1)"
grep -qx "MODE glowup" <<<"$out" && grep -qx "SURFACE web" <<<"$out" && ok "new --glowup --web prints both lines" || bad "new --glowup --web prints both lines" "$out"
out="$(bash "$STUDIO" new demo nope --sparkle 2>&1)"; st=$?
[ $st -eq 2 ] && grep -q "unknown flag: --sparkle" <<<"$out" && ok "new rejects an unknown flag" || bad "new rejects an unknown flag" "$out"
t="$(stage glowup-smoke demo groute)"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
[ "$(tail -1 <<<"$out")" = "OK 2 glow-up directions (directions, 4 screens)" ] && ok "check routes glow-up rounds by mode" || bad "check routes glow-up rounds by mode" "$out"
if bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO" >/dev/null 2>&1; then
  t="$(stage glowup-smoke demo gsheets)"
  cp "$ASSETS/web.css" "$t/r1/"
  out="$(bash "$STUDIO" sheets "$t/r1" 2>&1)"
  [ -s "$t/r1/sheet-v01.png" ] && [ -s "$t/r1/sheet-v02.png" ] && ok "glow-up sheets write one sheet per direction" || bad "glow-up sheets write one sheet per direction" "$out"
  [ -s "$t/r1/sheet-before.png" ] && ok "glow-up sheets write the before sheet" || bad "glow-up sheets write the before sheet" "$out"
  ls "$t/r1" | grep -q '^_' && bad "glow-up sheets clean up wrappers" "$(ls "$t/r1")" || ok "glow-up sheets clean up wrappers"
else
  echo "  skip glow-up sheets (no Chrome/Chromium)"
fi
```

The `new` test for `gallery-glowup.html` existing comes in Task 7. Here `new --glowup` needs the file to exist, so Step 3 creates a one-line placeholder that Task 7 replaces.

- [ ] **Step 2: Run them to verify they fail**

Run: `bash tests/studio.test.sh 2>&1 | grep -A12 "glow-up: new"`
Expected: FAIL on `MODE glowup` and on the unknown flag.

- [ ] **Step 3: Change `studio.sh`**

Replace header line 4:

```bash
#   studio.sh new <project> <topic> [--web|--paywall] → next round dir + gallery for that mode
```

with (same line count, so the `sed -n '2,23p'` usage print still works):

```bash
#   studio.sh new <project> <topic> [--web|--paywall|--glowup [--web]] → next round + gallery
```

Replace the start of `new_round` up to and including the existing `if [ -n "$web" ]; then` line:

```bash
new_round() {
  local project topic dir n web="" pw="" glow="" a
  project="$(slug "$1")"; topic="$(slug "$2")"; shift 2
  for a in "$@"; do
    case "$a" in
      --web) web=1 ;;
      --paywall) pw=1 ;;
      --glowup) glow=1 ;;
      "") ;;
      *) echo "unknown flag: $a" >&2; exit 2 ;;
    esac
  done
  dir="$ROOT/$project/$topic"
  mkdir -p "$dir"
  n=1; while [ -d "$dir/r$n" ]; do n=$((n+1)); done
  mkdir -p "$dir/r$n"
  if [ -n "$glow" ]; then
    cp "$SKILL_DIR/assets/gallery-glowup.html" "$dir/r$n/index.html"
    cp "$SKILL_DIR/assets/screen.css" "$dir/r$n/screen.css"
    cp "$SKILL_DIR/assets/web.css" "$dir/r$n/web.css"
  elif [ -n "$web" ]; then
```

Keep the rest of the existing branches as they are. After the existing `echo "TOPIC_DIR $dir"` line, add:

```bash
  [ -n "$glow" ] && echo "MODE glowup"
```

Add after `surface_of()`:

```bash
# mode_of <round-dir>: the manifest's "mode" (glowup), or nothing
mode_of() {
  python3 - "$1" <<'PY' 2>/dev/null || true
import json, os, sys
try:
    m = json.load(open(os.path.join(sys.argv[1], "manifest.json")))
except Exception:
    sys.exit(0)
print(m.get("mode") or "")
PY
}
```

In `check()`, directly after `local d="${1%/}"`:

```bash
  if [ "$(mode_of "$d")" = "glowup" ]; then python3 "$SKILL_DIR/scripts/glowup_check.py" "$d"; return; fi
```

In `sheets()`, directly after the `local chrome; chrome=...` line:

```bash
  if [ "$(mode_of "$d")" = "glowup" ]; then
    python3 "$SKILL_DIR/scripts/glowup_sheets.py" "$d" >/dev/null; shoot "$d" "$rel" "$chrome"; return
  fi
```

In the dispatcher, replace the `new)` line:

```bash
  new)   [ $# -ge 2 ] || { echo "usage: studio.sh new <project> <topic> [--web|--paywall|--glowup [--web]]" >&2; exit 2; }; new_round "$@" ;;
```

Create the placeholder so `new --glowup` has something to copy (Task 7 replaces it):

```bash
printf '<!doctype html><title>Design Studio · Glow-up</title>\n' > skills/design-studio/assets/gallery-glowup.html
```

- [ ] **Step 4: Write `glowup_sheets.py`**

```python
#!/usr/bin/env python3
"""Write contact-sheet wrapper pages for a glow-up round.

  glowup_sheets.py <round-dir>

_sheet-before.html (the audit's before screens), then one _sheet-<id>.html
per direction with its four key screens in a row, or in the system stage one
_sheet-<id>-<n>.html per four routes. studio.sh screenshots each wrapper to
sheet-*.png and deletes it. Prints "SHEETS <n>".
"""
import html, json, os, sys

CSS = ("body{margin:0;padding:24px;background:#ECECEF;display:flex;gap:24px;align-items:flex-start;"
       "font:600 22px -apple-system,system-ui,sans-serif;color:#1C1C1E}"
       ".lbl{width:200px;flex:none;font-size:15px;color:#6B6B73}.lbl b{display:block;font-size:28px;font-weight:800;color:#1C1C1E}"
       "figure{margin:0}figcaption{height:40px;font-size:16px;color:#6B6B73}"
       "iframe,img{width:393px;height:852px;border:0;border-radius:44px;background:#fff;"
       "box-shadow:0 10px 30px rgba(0,0,0,.12);display:block;object-fit:cover;object-position:top}")
IMG = (".png", ".jpg", ".jpeg", ".webp")


def cell(src, cap):
    s = html.escape(src)
    tag = f'<img src="{s}">' if src.lower().endswith(IMG) else f'<iframe src="{s}?theme=light"></iframe>'
    return f"<figure><figcaption>{html.escape(cap)}</figcaption>{tag}</figure>"


def page(label, sub, cells):
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>'
            f'<div class="lbl"><b>{html.escape(label)}</b>{html.escape(sub)}</div>' + "".join(cells))


def main(d):
    m = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
    screens = m.get("screens", [])
    out = []
    b = m.get("before") or {}
    shots = [s for s in screens if b.get(s["id"])]
    if shots:
        out.append(("before", page("Before", b.get("headline", ""), [cell(b[s["id"]], s["label"]) for s in shots])))
    stage = m.get("stage")
    for i, v in enumerate(m.get("variations", []), 1):
        vd = v.get("dir", v["id"])
        if stage == "system":
            routes = m.get("routes", [])
            for k in range(0, len(routes), 4):
                group = routes[k:k + 4]
                out.append((f"{v['id']}-{k // 4 + 1}", page(v.get("name", ""), f"routes {k + 1} to {k + len(group)}",
                                                            [cell(f"{vd}/routes/{r['id']}.html", r.get("label", r["id"])) for r in group])))
        elif stage in ("directions", "converge"):
            out.append((v["id"], page(f"{i} {v.get('name', '')}", v.get("idea", ""),
                                      [cell(f"{vd}/{s['id']}.html", s["label"]) for s in screens])))
    for name, body in out:
        with open(os.path.join(d, f"_sheet-{name}.html"), "w", encoding="utf-8") as f:
            f.write(body)
    print(f"SHEETS {len(out)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `bash tests/studio.test.sh`
Expected: all glow-up routing lines `ok`; the existing mobile, web and paywall `new` and `check` lines still `ok`; `0 failed`.

- [ ] **Step 6: Commit**

```bash
git add skills/design-studio/scripts/studio.sh skills/design-studio/scripts/glowup_sheets.py skills/design-studio/assets/gallery-glowup.html tests/studio.test.sh
git commit -m "feat(glowup): studio.sh new --glowup, mode routing for check and sheets"
```

---

### Task 7: `gallery-glowup.html`

**Files:**
- Modify (replace the placeholder): `skills/design-studio/assets/gallery-glowup.html`
- Modify: `tests/studio.test.sh`

**Interfaces:**
- Consumes: the manifests from Task 5 (`screens`, `before`, `category`, `variations[].dir`, `routes`, `apply`), each direction's `theme.json`.
- Produces: the DOM contract the tests read:
  - `section.row[data-row="<vid>"]` holding iframes `src="<dir>/<sid>.html?theme=light"`
  - `section.row.before[data-row="before"]`
  - `section.row.pair[data-route="<id>"]` in apply
  - `div.spec[data-spec="<vid>"]` with `i[data-role="<role>"]` swatches once `#<vid>` is opened
  - URL state in `?tab=before|category|main` and `#<vid>`

- [ ] **Step 1: Write the failing tests**

Insert above `# --- new tests above this line ---`:

```bash
echo "glow-up: gallery"
out="$(bash "$STUDIO" new demo glowgal --glowup 2>&1)"
cmp -s "$DESIGN_STUDIO_ROOT/demo/glowgal/r1/index.html" "$ASSETS/gallery-glowup.html" && ok "new --glowup copies gallery-glowup.html" || bad "new --glowup copies gallery-glowup.html" "$out"
grep -q "—" "$ASSETS/gallery-glowup.html" && bad "gallery-glowup.html has no em dashes" || ok "gallery-glowup.html has no em dashes"
if bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO" >/dev/null 2>&1; then
  CHROME_BIN="$(bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO")"
  t="$(stage glowup-smoke demo ggal)"
  for r in r1 r2 r3; do cp "$ASSETS/gallery-glowup.html" "$t/$r/index.html"; cp "$ASSETS/web.css" "$t/$r/"; done
  bash "$STUDIO" serve >/dev/null
  base="http://127.0.0.1:$DESIGN_STUDIO_PORT/demo/ggal"
  dump() { "$CHROME_BIN" --headless=new --disable-gpu --virtual-time-budget=6000 --dump-dom "$1" 2>/dev/null; }
  dom="$(dump "$base/r1/index.html")"
  grep -q 'data-row="v01"' <<<"$dom" && grep -q 'src="v02/s4.html?theme=light"' <<<"$dom" && ok "gallery renders direction rows across the key screens" || bad "gallery renders direction rows across the key screens"
  dom="$(dump "$base/r1/index.html?tab=before")"
  grep -q 'data-row="before"' <<<"$dom" && grep -q 'src="../before/s1.png"' <<<"$dom" && ok "gallery ?tab=before shows the audit screens" || bad "gallery ?tab=before shows the audit screens"
  dom="$(dump "$base/r1/index.html?tab=category")"
  grep -q 'class="cat"' <<<"$dom" && grep -q "Table stakes" <<<"$dom" && ok "gallery ?tab=category shows category.md" || bad "gallery ?tab=category shows category.md"
  dom="$(dump "$base/r1/index.html#v02")"
  grep -q 'data-spec="v02"' <<<"$dom" && grep -q 'data-role="action"' <<<"$dom" && ok "gallery #v02 opens the spec card" || bad "gallery #v02 opens the spec card"
  dom="$(dump "$base/r2/index.html")"
  grep -q 'src="v01/routes/settings.html?theme=light"' <<<"$dom" && ok "gallery shows system routes" || bad "gallery shows system routes"
  dom="$(dump "$base/r3/index.html")"
  grep -q 'data-route="home"' <<<"$dom" && grep -q "Entropy 33 → 15" <<<"$dom" && ok "gallery shows the apply board" || bad "gallery shows the apply board"
else
  echo "  skip glow-up gallery DOM tests (no Chrome/Chromium)"
fi
```

- [ ] **Step 2: Run them to verify they fail**

Run: `bash tests/studio.test.sh 2>&1 | grep -A8 "glow-up: gallery"`
Expected: the DOM lines FAIL (the placeholder renders nothing).

- [ ] **Step 3: Write the gallery**

Build `skills/design-studio/assets/gallery-glowup.html` like this:

1. Copy every line of `skills/design-studio/assets/gallery-paywall.html` from `<!doctype html>` up to, but not including, the `</style>` line, verbatim. This keeps the gallery family's look, phone frame, chips and focus overlay.
2. In the copy, change `<title>Design Studio · Paywall</title>` to `<title>Design Studio · Glow-up</title>`.
3. Append this CSS, then `</style>`, `</head>`, and the body and script below:

```html
  main.board { display: grid; grid-template-columns: 1fr; gap: 34px; }
  .row { display: grid; grid-template-columns: 240px repeat(4, var(--w)); gap: 18px; align-items: start; overflow-x: auto; }
  .row.pair { grid-template-columns: 240px repeat(2, var(--w)); }
  .row.sys { grid-template-columns: 240px 1fr; }
  .routes { display: grid; grid-template-columns: repeat(auto-fill, var(--w)); gap: 18px; }
  .row .meta { width: auto; }
  .row.before .phone { outline: 2px dashed var(--ink3); outline-offset: 4px; }
  .screenlbl { font-size: 11px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--ink2); margin-bottom: 6px; }
  .more { justify-self: start; border: 1px solid var(--line); background: var(--panel); color: var(--ink); border-radius: 999px; padding: 4px 12px; font: inherit; font-size: 12px; font-weight: 650; cursor: pointer; }
  .headline { margin: 0; font-size: 18px; font-weight: 700; }
  pre.cat { margin: 0; white-space: pre-wrap; background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 18px; font: 13px/1.55 ui-monospace, SFMono-Regular, Menlo, monospace; }
  .spec { display: grid; gap: 14px; max-height: 80vh; overflow: auto; }
  .spec .lbl { display: block; font-size: 10.5px; letter-spacing: .06em; text-transform: uppercase; color: var(--ink2); margin-bottom: 6px; }
  .spec small { display: block; color: var(--ink2); margin-top: 4px; }
  .spec ul { margin: 4px 0 0; padding-left: 18px; }
  .sw { display: flex; flex-wrap: wrap; gap: 6px; }
  .sw i { width: 30px; height: 30px; border-radius: 8px; border: 1px solid var(--line); }
  .tpls { display: grid; gap: 8px; }
  .tpl { display: grid; gap: 3px; height: 34px; padding: 4px; border: 1px solid var(--line); border-radius: 6px; }
  .tpl i { background: var(--line); border-radius: 2px; }
</style>
</head>
<body>
<header id="head"></header>
<div class="bar"><div>
  <div class="seg" id="tab"></div>
  <div class="seg" id="theme"><button data-v="light" class="on">Light</button><button data-v="dark">Dark</button></div>
  <div class="seg" id="size"><button data-v="s">S</button><button data-v="m" class="on">M</button><button data-v="l">L · 1:1</button></div>
  <span class="hint">Spec card opens a direction · ← → to step · 1 to 9, 0 = #10 · Esc</span>
</div></div>
<main id="grid" class="board"></main>
<div class="focus" id="focus">
  <button class="close" id="close">Close · Esc</button>
  <button class="nav prev" id="prev">‹</button>
  <button class="nav next" id="next">›</button>
</div>
<script>
const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const ROLES = ["ground", "surface", "surface-2", "border", "text", "text-2", "text-3", "action", "on-action", "accent", "on-accent", "good", "warn", "error", "focus"];
const RAMP = ["display", "h1", "h2", "h3", "lede", "body", "small", "caption", "eyebrow"];
let M, theme = "light", tab = "main", cur = -1;
const themes = {};

function applyTheme(t) {
  theme = t;
  document.documentElement.dataset.theme = t;
  document.querySelectorAll("#theme button").forEach((b) => b.classList.toggle("on", b.dataset.v === t));
  document.querySelectorAll("iframe").forEach(setFrameTheme);
}
function setFrameTheme(f) { try { f.contentDocument.documentElement.dataset.theme = theme; } catch {} }
function frame(src, title, lazy = true) {
  const inner = /\.(png|jpe?g|webp)$/i.test(src)
    ? `<img src="${esc(src)}" alt="${esc(title)}">`
    : `<iframe ${lazy ? 'loading="lazy" ' : ""}src="${esc(src)}?theme=${theme}" title="${esc(title)}" onload="setFrameTheme(this)"></iframe>`;
  return `<div class="phone"><div class="viewport">${inner}</div></div>`;
}
function mainLabel() { return M.stage === "system" ? "System" : M.stage === "apply" ? `Apply · stage ${M.apply?.stage ?? ""}` : "Directions"; }
function tabs() { return [M.before && ["before", "Before"], M.category && ["category", "Category"], ["main", mainLabel()]].filter(Boolean); }
function renderHead() {
  const r = M.round ?? 1;
  const rounds = Array.from({ length: r }, (_, k) => k + 1).map((k) => `<a href="../r${k}/" class="${k === r ? "on" : ""}">R${k}</a>`).join("");
  const fb = M.feedback ? `<div class="feedback"><b>Your feedback</b>${esc(M.feedback)}</div>` : "";
  $("#head").innerHTML = `<div class="crumbs">${esc(M.project ?? "")} / ${esc(M.topic ?? "")} · glow-up ${rounds}</div>
    <h1>${esc(M.title ?? "Glow-up")} <span style="color:var(--ink3);font-weight:600">· ${esc(mainLabel())}</span></h1>
    <p class="brief">${esc(M.brief ?? "")}</p>${fb}`;
}
function renderTabs() {
  $("#tab").innerHTML = tabs().map(([k, l]) => `<button data-v="${k}" class="${k === tab ? "on" : ""}">${esc(l)}</button>`).join("");
  document.querySelectorAll("#tab button").forEach((b) => (b.onclick = () => setTab(b.dataset.v)));
}
function setTab(k) {
  tab = k;
  const u = new URL(location.href); u.searchParams.set("tab", k); u.hash = ""; history.replaceState(null, "", u);
  renderTabs(); renderBody();
}
function rowMeta(v, i) {
  const badges = [v.id === M.agentPick && `<span class="chip pick">Claude’s pick</span>`, v.id === M.predictedPick && `<span class="chip fav">Your likely pick</span>`].filter(Boolean).join("");
  const tags = (v.tags ?? []).map((t) => `<span class="chip ${t === "wildcard" ? "wild" : ""}">${esc(t)}</span>`).join("");
  return `<div class="meta"><div class="top"><span class="num">${i + 1}</span><span class="name">${esc(v.name)}</span></div>
    <p class="idea">${esc(v.idea)}</p><div class="chips">${badges}${tags}</div>
    ${v.notes?.market ? `<p class="idea"><b>Market:</b> ${esc(v.notes.market)}</p>` : ""}
    <button class="more" data-i="${i}">Spec card</button></div>`;
}
function cells(items) { return items.map(([src, label, title]) => `<div class="cell"><div class="screenlbl">${esc(label)}</div>${src ? frame(src, title) : ""}</div>`).join(""); }
function renderMain() {
  const vs = M.variations ?? [];
  if (M.stage === "apply") {
    const a = M.apply ?? {};
    const rows = (a.routes ?? []).map((r) => `<section class="row pair" data-route="${esc(r.id)}"><div class="meta"><span class="name">${esc(r.label ?? r.id)}</span></div>
      ${cells([[r.before, "Before", `${r.label} before`], [r.after, "After", `${r.label} after`]])}</section>`).join("");
    const fu = (a.followUps ?? []).map((f) => `<li>${esc(f)}</li>`).join("");
    return `<p class="headline">${esc(a.headline ?? "")}</p>${rows}${fu ? `<div class="notes"><div><b>Recommended follow-ups</b><ul>${fu}</ul></div></div>` : ""}`;
  }
  if (M.stage === "system") {
    return vs.map((v, i) => `<section class="row sys" data-row="${esc(v.id)}">${rowMeta(v, i)}<div class="routes">${cells((M.routes ?? []).map((r) => [`${v.dir ?? v.id}/routes/${r.id}.html`, r.label ?? r.id, `${v.name} · ${r.label ?? r.id}`]))}</div></section>`).join("");
  }
  return vs.map((v, i) => `<section class="row" data-row="${esc(v.id)}">${rowMeta(v, i)}${cells((M.screens ?? []).map((s) => [`${v.dir ?? v.id}/${s.id}.html`, s.label, `${v.name} · ${s.label}`]))}</section>`).join("");
}
function renderBefore() {
  const b = M.before ?? {};
  return `<p class="headline">${esc(b.headline ?? "")}</p><section class="row before" data-row="before"><div class="meta"><span class="name">Before</span><p class="idea">${esc(b.summary ?? "")}</p></div>
    ${cells((M.screens ?? []).map((s) => [b[s.id], s.label, `Before · ${s.label}`]))}</section>`;
}
async function renderCategory() {
  try { const r = await fetch(M.category, { cache: "no-store" }); if (!r.ok) throw new Error(r.status); return `<pre class="cat">${esc(await r.text())}</pre>`; }
  catch (e) { return `<div class="err">Could not read ${esc(M.category)} (${esc(e.message)}).</div>`; }
}
async function renderBody() {
  const g = $("#grid");
  g.innerHTML = tab === "before" ? renderBefore() : tab === "category" ? await renderCategory() : renderMain();
  g.querySelectorAll("button.more").forEach((b) => (b.onclick = () => open(+b.dataset.i)));
}
async function loadTheme(v) {
  const dir = v.dir ?? v.id;
  if (!themes[dir]) themes[dir] = await fetch(`${dir}/theme.json`, { cache: "no-store" }).then((r) => r.json());
  return themes[dir];
}
function resolve(t, mode, role) {
  const v = t.color[mode][role]; const m = /^([a-z][a-z0-9-]*)\.(\d{1,2})$/.exec(v);
  return m ? t.color.primitives[m[1]][m[2]] : v;
}
function fontLink(t) {
  const q = [t.type.display, t.type.body, t.type.mono].filter((f) => f?.family)
    .map((f) => `family=${f.family.replace(/ /g, "+")}:wght@${[...new Set(f.weights)].sort((a, b) => a - b).join(";")}`).join("&");
  const href = `https://fonts.googleapis.com/css2?${q}&display=swap`;
  if (![...document.querySelectorAll("link")].some((l) => l.href === href)) document.head.insertAdjacentHTML("beforeend", `<link rel="stylesheet" href="${esc(href)}">`);
}
function spec(t, v) {
  fontLink(t);
  const mode = theme === "dark" ? "dark" : "light";
  const sw = ROLES.map((r) => `<i data-role="${r}" title="${r} ${esc(resolve(t, mode, r))}" style="background:${esc(resolve(t, mode, r))}"></i>`).join("");
  const fam = (face) => t.type[face]?.family ?? t.type.body.family;
  const ramp = RAMP.map((k) => { const r = t.type.ramp[k]; return `<div style="font-family:'${esc(fam(r.face))}';font-size:${Math.min(r.size, 40)}px;line-height:1.2;font-weight:${r.weight};letter-spacing:${r.track}em;${r.upper ? "text-transform:uppercase;" : ""}">${k} · ${r.size}/${r.line}</div>`; }).join("");
  const tpls = t.layout.templates.map((p) => { const n = Math.min(p.columns, 12); return `<div><div class="tpl" style="grid-template-columns:repeat(${n},1fr)">${"<i></i>".repeat(n)}</div><small>${esc(p.label)} · ${p.columns} col · ${p.max ? p.max + "px" : "full width"} · ${esc(p.density)}</small></div>`; }).join("");
  const st = t.states;
  const voice = t.voice.strings.map((s) => `<li><s>${esc(s.before)}</s> → ${esc(s.after)}</li>`).join("");
  const notes = Object.entries(v.notes ?? {}).map(([k, x]) => `<div><b>${esc(k)}</b>${esc(x)}</div>`).join("");
  return `<div class="spec" data-spec="${esc(v.id)}">
    <div><b class="lbl">Colour (${mode})</b><div class="sw">${sw}</div></div>
    <div><b class="lbl">Type · ${esc(t.type.display.family)} + ${esc(t.type.body.family)}</b>${ramp}<small>${esc(t.type.pairing)}</small></div>
    <div><b class="lbl">Layout · space ${t.layout.space.join(" ")}</b><div class="tpls">${tpls}</div></div>
    <div><b class="lbl">States</b><small>hover ${st.hover} · pressed ${st.pressed} · disabled ${st.disabled} · focus ${st.focus.width}px ring, ${st.focus.offset}px offset</small></div>
    <div><b class="lbl">Signature</b>${esc(t.signature.what)}<small>On ${esc(t.signature.where.join(", "))}. ${esc(t.signature.never)}</small></div>
    <div><b class="lbl">Voice · ${esc(t.voice.adjectives.join(", "))}</b><ul>${voice}</ul></div>
    <div class="notes">${notes}</div></div>`;
}
async function open(i) {
  const vs = M.variations ?? [];
  if (!vs.length || M.stage === "apply") return;
  cur = (i + vs.length) % vs.length;
  const v = vs[cur], f = $("#focus");
  f.querySelectorAll(".phone, .side").forEach((n) => n.remove());
  const first = M.stage === "system" ? `${v.dir ?? v.id}/routes/${M.routes?.[0]?.id}.html` : `${v.dir ?? v.id}/${M.screens?.[0]?.id ?? "s1"}.html`;
  f.insertAdjacentHTML("beforeend", frame(first, v.name, false) + `<div class="side"><div class="top"><span class="num">${cur + 1}</span> <span class="name">${esc(v.name)}</span></div><p class="idea">${esc(v.idea)}</p><div class="loading">Loading spec…</div></div>`);
  f.classList.add("open");
  history.replaceState(null, "", `${location.pathname}${location.search}#${v.id}`);
  try { const t = await loadTheme(v); f.querySelector(".loading").outerHTML = spec(t, v); }
  catch (e) { f.querySelector(".loading").textContent = `No readable theme.json (${e.message}).`; }
}
function close() { $("#focus").classList.remove("open"); cur = -1; history.replaceState(null, "", location.pathname + location.search); }
$("#close").onclick = close;
$("#prev").onclick = () => open(cur - 1);
$("#next").onclick = () => open(cur + 1);
document.querySelectorAll("#theme button").forEach((b) => (b.onclick = () => { applyTheme(b.dataset.v); if (cur >= 0) open(cur); }));
document.querySelectorAll("#size button").forEach((b) => (b.onclick = () => { document.body.dataset.size = b.dataset.v; document.querySelectorAll("#size button").forEach((x) => x.classList.toggle("on", x === b)); }));
addEventListener("keydown", (e) => {
  if (e.key === "Escape") return close();
  if (cur >= 0 && e.key === "ArrowRight") return open(cur + 1);
  if (cur >= 0 && e.key === "ArrowLeft") return open(cur - 1);
  if (/^[0-9]$/.test(e.key)) { const n = e.key === "0" ? 10 : +e.key; if (n <= (M.variations ?? []).length) open(n - 1); }
});
fetch("manifest.json", { cache: "no-store" }).then((r) => r.json()).then(async (m) => {
  M = m;
  const q = new URLSearchParams(location.search).get("tab");
  tab = tabs().some(([k]) => k === q) ? q : "main";
  renderHead(); renderTabs(); await renderBody();
  const i = (M.variations ?? []).findIndex((x) => x.id === location.hash.slice(1));
  if (i >= 0) open(i);
}).catch((e) => { $("#grid").outerHTML = `<div class="err">No readable <code>manifest.json</code> next to this page (${esc(e.message)}).</div>`; });
</script>
</body>
</html>
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `bash tests/studio.test.sh`
Expected: all glow-up gallery lines `ok` (or `skip` without Chrome), `0 failed`. Then open the fixture by hand once (`bash skills/design-studio/scripts/studio.sh serve`, copy the fixture into `~/design-studio/demo/notes`, open `r1/`) and check that light/dark switching, the spec card and the Before tab look right at desktop width.

- [ ] **Step 5: Commit**

```bash
git add skills/design-studio/assets/gallery-glowup.html tests/studio.test.sh
git commit -m "feat(glowup): theme board gallery with before, category, spec card and apply boards"
```

---

### Task 8: References for craft and research

**Files:**
- Create: `skills/design-studio/references/glowup-craft.md`
- Create: `skills/design-studio/references/category-research.md`
- Modify: `tests/studio.test.sh`

**Interfaces:**
- Consumes: the spec sections "What one direction contains", "The system layer", "The human rules", "Direction axes", "Category research", "Sources"; the fixture theme from Task 1; the check messages from Task 5.
- Produces: the files `glowup.md` (Task 9) and `SKILL.md` (Task 10) point to.

- [ ] **Step 1: Write the failing doc tests**

Insert above `# --- new tests above this line ---`:

```bash
echo "glow-up: craft references"
SK="$REPO/skills/design-studio"
need_heads() { local f="$1"; shift; local h; for h in "$@"; do grep -qx "$h" "$SK/references/$f" && ok "$f has '$h'" || bad "$f has '$h'"; done; }
need_heads glowup-craft.md "## theme.json" "## The system layer" "### 1. Layout system" "### 2. Brand surface" "### 3. Colour construction" "### 4. Component state matrix" "### 5. Type construction" "### 6. Signature element" "### 7. Content and voice system" "### 8. Loading policy" "### 9. Form system" "### 10. Numbers and tables" "### 11. Feedback and haptics" "### 12. Responsive components and navigation" "### 13. Density" "## Construction details" "## The human rules" "## The tells" "## Layout templates on each surface" "## Screens" "## Pre-send checklist" "## Sources"
need_heads category-research.md "## Choosing comparables" "## Gathering screens" "## What to record" "## Table stakes and white space" "## Rules" "## category.md template"
for f in glowup-craft.md category-research.md; do grep -q "—" "$SK/references/$f" && bad "$f has no em dashes" || ok "$f has no em dashes"; done
grep -q "tests/fixtures/glowup-smoke/r1/v01/theme.json" "$SK/references/glowup-craft.md" && ok "glowup-craft.md points at the worked example" || bad "glowup-craft.md points at the worked example"
```

- [ ] **Step 2: Run them to verify they fail**

Run: `bash tests/studio.test.sh 2>&1 | grep -c "FAIL glowup-craft.md has"`
Expected: a non-zero count (the files don't exist).

- [ ] **Step 3: Write `glowup-craft.md`**

Write it as instructions to the agent rendering a direction, in the voice of `web-craft.md`: second person, imperative, short paragraphs, no em dashes. Use exactly the headings the test lists, in that order, with this content:

- Title line: `# Glow-up craft: the system a vibe-coded app never had`. Opening paragraph: principles.md assumes a system exists (scale, ramp, neutrals, states) and checks that screens follow it. Glow-up designs that system first, as `theme.json`, and every screen is built from it.
- `## theme.json`: every top-level key with one line on what it holds and the rule `validate_theme` enforces, taken from Task 1's `validate_theme`. This covers `type` (display and body faces, weights, pairing reason, the nine-step ramp with face/size/line/weight/track/upper), `color` (12-step primitive ramps, the 15 roles in light and dark, references like `neutral.11`), `layout`, `shape`, `elevation`, `icons`, `motion`, `states`, `signature`, `voice`, `brand` and `reasons`. Point at `tests/fixtures/glowup-smoke/r1/v01/theme.json` as the worked example. End with the generation command: `python3 <SKILL_DIR>/scripts/theme_tokens.py vNN/theme.json --css --out vNN/tokens.css`. Say never hand-edit `tokens.css`; `check` fails a stale one.
- `## The system layer`: one `###` per item, numbered and named exactly as in the test. Each gives the rule as an instruction plus the vibe-coded tell it replaces. Take the content from the spec's "The system layer" items 1 to 13. For item 1, add the layout-template guidance: three or four templates, each screen declares one with `data-template`, data views run denser than reading views. For item 2, add that wordmark and icon are designed in `system` and applied in apply stage 4.
- `## Construction details`: the bullets from the spec's "Construction details `glowup-craft.md` carries from the research" list, verbatim in meaning. Mark the Material state-layer opacities `practice`.
- `## The human rules`: the spec's five rules, plus that the count-up ban overrides web-craft.md inside glow-up rounds only.
- `## The tells`: two lists (first-order, second-order) from the spec. For each, give the `tells_lint.py` rule id where one exists (for example `F-gradient-text`, `S-numbered-sections`) and the `second_order_hits` id (`cream-terracotta`, `black-acid`, `mono-chrome`). Explain `signature.uses`: listing an id there is how a direction claims a second-order pattern as its named signature.
- `## Layout templates on each surface`: app surface, put the template class on the scroller (`<div class="scroll tpl-column">`), where the template margin is the screen inset. Web surface, put it on `<main>`, where the container and gutter come from the template.
- `## Screens`: each `sN.html` links `../screen.css` or `../web.css` and then `tokens.css`, puts `data-template="<id>"` on `<body>`, and marks the signature element with `data-signature` on every screen in `signature.where`. It uses only tokens (no hex, `rgb()`, `hsl()` or `oklch()` literals), uses the shared fixture from context.md including the long string, and puts real strings in the direction's voice. It keeps the content contract and never drops a datum or action. Typographic quotes and `…`.
- `## Pre-send checklist`: numbered.
  1. `theme_tokens.py` ran after the last theme edit.
  2. Every screen declares a template from the theme.
  3. The signature shows on its screens.
  4. Voice strings are real lines from context.md.
  5. Every framework default has a reason.
  6. No second-order pattern unless it's in `signature.uses`.
  7. It differs from every other direction on two axes, and type or colour alone doesn't count.
  8. Contrast passes in light and dark.
  9. The principles.md checklist (mobile items for app, web items for web) passes.
- `## Sources`: the list from the spec's "Sources" section.

- [ ] **Step 4: Write `category-research.md`**

Same voice. Headings as tested:

- `# Category research` and an opening: research finds what signals trust in this market and what nobody is doing. Budget about 20 tool calls, fanned out to a subagent when the Agent tool is available.
- `## Choosing comparables`: start from `brief.md`'s list. Eight to twelve in total: direct competitors, two or three adjacent apps the same buyer uses, and one or two aspirational apps from outside the category. Skip apps that are themselves templates from the same builder (Lovable, v0 and Bolt showcases).
- `## Gathering screens`:
  - Web: open each home page and one product page with the available browser tool, take one desktop and one 390-wide screenshot each, and save them as `TOPIC_DIR/category/<slug>-<n>.png`.
  - Mobile: use the public iTunes Search API, with this exact command:

    ```bash
    curl -s "https://itunes.apple.com/search?term=<name>&entity=software&limit=1" | python3 -c 'import json,sys; r=json.load(sys.stdin)["results"]; print("\n".join(r[0]["screenshotUrls"]) if r else "")'
    ```

    Then download the first three URLs into `TOPIC_DIR/category/`.
  - No sign-ins, no paid content.
- `## What to record`: the table columns App, Type, Colour field, Neutral, Shape, Density, Tone, Signature, Source, each with one line on how to judge it.
- `## Table stakes and white space`: table stakes are the conventions that three or more comparables share and that a buyer would miss. White space is what none of them do and the brief supports. Each item is numbered so direction notes can cite it ("category.md, table stakes 2").
- `## Rules`: screenshots are reference only. No direction reuses a comparable's logo, palette or signature element. Every claim in category.md names its source app. If research can't reach a comparable, say so and don't guess.
- `## category.md template`: the shape of `tests/fixtures/glowup-smoke/category.md`, with the heading, the table, and the two numbered lists.

- [ ] **Step 5: Run the tests to verify they pass**

Run: `bash tests/studio.test.sh`
Expected: every `glow-up: craft references` line `ok`, `0 failed`.

- [ ] **Step 6: Commit**

```bash
git add skills/design-studio/references/glowup-craft.md skills/design-studio/references/category-research.md tests/studio.test.sh
git commit -m "docs(glowup): craft and category research references"
```

---

### Task 9: References for the loop and the two apply playbooks

**Files:**
- Create: `skills/design-studio/references/glowup.md`
- Create: `skills/design-studio/references/apply-web.md`
- Create: `skills/design-studio/references/apply-native.md`
- Modify: `tests/studio.test.sh`

**Interfaces:**
- Consumes: every script interface above; the manifest shapes in Task 5; the spec sections "Stages", "Intake", "Audit", "Apply", "Pick question".
- Produces: the loop document that `SKILL.md` (Task 10) points to.

- [ ] **Step 1: Write the failing doc tests**

Insert above `# --- new tests above this line ---`:

```bash
echo "glow-up: loop and apply references"
need_heads glowup.md "## When it's on" "## Stages" "## Intake" "## Audit" "## Category research" "## Directions and converge" "## System" "## Apply" "## Pick question" "## TASTE.md" "## Manifest reference"
need_heads apply-web.md "## Before you start" "## Stage 1: theme layer" "## Stage 2: shared components" "## Stage 3: routes" "## Stage 4: brand surface" "## After every stage" "## Hard limits" "## Follow-ups"
need_heads apply-native.md "## Before you start" "## Stage 1: theme layer" "## Stage 2: shared components" "## Stage 3: screens" "## Stage 4: brand surface" "## After every stage" "## Hard limits" "## Follow-ups"
for f in glowup.md apply-web.md apply-native.md; do grep -q "—" "$SK/references/$f" && bad "$f has no em dashes" || ok "$f has no em dashes"; done
for s in entropy.py tells_lint.py theme_tokens.py glowup_check.py; do grep -q "$s" "$SK/references/glowup.md" && ok "glowup.md uses $s" || bad "glowup.md uses $s"; done
grep -q -- "--shadcn-hsl" "$SK/references/apply-web.md" && ok "apply-web.md covers HSL shadcn" || bad "apply-web.md covers HSL shadcn"
grep -q -- "--rn" "$SK/references/apply-native.md" && ok "apply-native.md uses --rn" || bad "apply-native.md uses --rn"
```

- [ ] **Step 2: Run them to verify they fail**

Run: `bash tests/studio.test.sh 2>&1 | grep -c "FAIL glowup.md has"`
Expected: non-zero.

- [ ] **Step 3: Write `glowup.md`**

Model it on `references/web.md` (same voice, same "Everything in SKILL.md holds unless this file says otherwise" opening). Headings as tested:

- `## When it's on`: the adapter says `mode: glowup`, or the brief says glow-up, makeover, "make it look professional", "looks vibe-coded / AI-made", "give it a real design", "rebrand the app", or asks for themes for the whole app. Start with `studio.sh new <project> <topic> --glowup`, adding `--web` for a web app. Glow-up is a job on top of the app or web frames, so read `mockup-craft.md` (app) or `web-craft.md` (web) too.
- `## Stages`: the spec's stage table, plus three rules. Intake and audit run in one turn. Research and r1 run back to back. A bare pick in `directions` or `converge` goes to `system`.
- `## Intake`:
  - The stack table: `package.json` dependencies to surface. next, vite, react-router, tailwind and `components.json` mean web; expo, react-native and nativewind mean app.
  - Route discovery per stack (Next `app/` and `pages/`, react-router definitions, expo-router `app/`, navigator files).
  - The `brief.md` fields.
  - The confirm question as an AskUserQuestion with exactly the three options from the spec. Typed corrections go into `brief.md` verbatim.
- `## Audit`:
  - Commands, with outputs in the topic dir:
    - `python3 <SKILL_DIR>/scripts/entropy.py <repo> --out TOPIC_DIR/entropy-before.json`
    - `python3 <SKILL_DIR>/scripts/tells_lint.py <repo> --json TOPIC_DIR/tells-before.json`
  - Before screenshots by surface:
    - web: headless Chrome at 390 and 1440 against the running dev server
    - app: `xcrun simctl io booted screenshot`, else Expo web, else HTML recreations labelled as such
  - Save the screenshots to `TOPIC_DIR/before/<sid>.png`.
  - Choosing the four key screens, the content contract, and the `## UI strings` section in context.md. Every real UI string the app shows goes there, because `check` reads voice strings from it.
  - The Before tab's `headline` and `summary` strings come from the two command outputs.
- `## Category research`: one paragraph and a pointer to `category-research.md`. Its output is `TOPIC_DIR/category.md` and the manifest's `"category": "../category.md"`.
- `## Directions and converge`:
  - The r1 mix: 3 conventional, 5 with a twist, 2 wildcards.
  - The axes live in `variations.md` under glow-up.
  - The per-direction file list.
  - The subagent brief: five subagents × two directions; "Read first" = `glowup-craft.md`, `mockup-craft.md` or `web-craft.md`, `principles.md`, `context.md`, `category.md`. Each writes `theme.json`, runs `theme_tokens.py --css`, then writes `s1.html` to `s4.html`.
  - Converge: #1 Faithful.
  - Then the one-pass check and `studio.sh check ROUND_DIR`.
- `## System`:
  - One or two variations.
  - Every route in the intake inventory as `vNN/routes/<id>.html`, with empty, loading and error states for routes that have them.
  - Light and dark.
  - The brand surface designed here: wordmark, app icon and favicon concept, as images in `vNN/brand/`.
- `## Apply`:
  - Runs only after `Apply #N`.
  - Pick `apply-web.md` or `apply-native.md` by surface.
  - The four stages and the hard limits, copied from the spec.
  - The per-stage `rN/manifest.json` with `"stage": "apply"` and the `apply` block from the Manifest reference.
  - After every stage, the board goes out with the same link-then-ask flow.
- `## Pick question`: the options per stage from the spec. directions/converge use the usual four, with `System proof #N` from converge on. system uses `Apply #N (Recommended)`, a converge option and a mix. Each apply stage uses "Approve stage (Recommended)", "Flag a route", "Revert stage".
- `## TASTE.md`: log glow-up rounds with `glowup` in the Project / topic column. `predictedPick` reads glow-up rows when there are any; with none, say the prediction is from the brief alone.
- `## Manifest reference`: the three manifests from Task 5 Step 1 (r1, r2, r3) as fenced JSON with `demo`/`notes` replaced by `<project>`/`<topic>`, plus one line on each field `check` reads.

- [ ] **Step 4: Write `apply-web.md`**

Headings as tested:

- `## Before you start`:
  - `git status --porcelain` must be clean for the paths apply will touch, otherwise stop and say which files.
  - `git switch -c glowup/<topic>` from the current branch, never main. Record the base commit in the apply manifest.
  - Detect:
    - Tailwind v3 (`tailwind.config.*`) or v4 (`@import "tailwindcss"` in CSS)
    - shadcn (`components.json`), and whether its `globals.css` variables are HSL triplets or `oklch()`
    - fonts (`next/font/google`, `@fontsource`, or `<link>`)
- `## Stage 1: theme layer`, by stack:
  - Write `theme_tokens.py <theme.json> --css-vars` into the global stylesheet, replacing nothing else.
  - Tailwind v4: add `--tailwind` output after it.
  - Tailwind v3: merge `--tailwind3` output's `theme.extend` into `tailwind.config.*`.
  - shadcn: replace its `:root` and `.dark` blocks with `--shadcn` (oklch projects) or `--shadcn-hsl` (HSL projects).
  - Fonts through the project's existing mechanism (`next/font/google` with the theme's families and weights, or `@fontsource` packages).
  - Commit: `style(glowup): theme layer for <name>`.
- `## Stage 2: shared components`:
  - Restyle `components/ui/*` (or the project's shared components) from tokens.
  - Give every interactive component the full state matrix from `theme.json.states`: hover, pressed, focus-visible ring, disabled, loading, selected and error.
  - Loading buttons keep their label.
  - Commit.
- `## Stage 3: routes`:
  - Use `entropy-before.json`'s `files` lists to find every literal per route.
  - Map each literal to a token or utility. A table shows the common Tailwind cases: `bg-indigo-600` becomes `bg-action`; `text-gray-500` becomes `text-text-2`; arbitrary sizes go to ramp classes; spacing goes to the scale.
  - Wrap each route in its layout template.
  - Layout polish inside the content contract.
  - Rewrite copy with the voice, glossary and case map.
  - Fix the tells that are inside the allowed diff: labels, `aria-label`, focus rings, `tabular-nums`, input `type`/`autoComplete`/`inputMode`, punctuation, copy.
  - About five routes per commit.
- `## Stage 4: brand surface`:
  - `favicon.svg` plus `apple-touch-icon.png` (180×180)
  - page titles: Next `metadata` or `<title>` per route
  - OG image at 1200×630
  - `theme-color` meta in both schemes
- `## After every stage`:
  - Run the project's `build`, `typecheck` and `lint` scripts when `package.json` has them.
  - Run the dev server or preview and screenshot touched routes at 390 and 1440 into `ROUND_DIR/after/`.
  - `entropy.py <repo> --out ROUND_DIR/entropy-after.json`
  - `tells_lint.py <repo> --json ROUND_DIR/tells-after.json`
  - `studio.sh check ROUND_DIR`
  - A failing build is fixed before the board goes out. If it can't be fixed, run `git revert` on that stage's commits, set `"reverted": true`, and say so on the board.
- `## Hard limits`: the spec's list.
- `## Follow-ups`: tells outside the allowed diff (validation timing, loader delays, permission timing) go into `apply.followUps`, one line each with file:line and why apply left it alone.

- [ ] **Step 5: Write `apply-native.md`**

Same headings except `## Stage 3: screens`. Content:

- `## Before you start`: the same git rules. Detect expo-router or react-navigation, NativeWind (v4 reads CSS variables from `global.css`; earlier versions need literal values) or StyleSheet, and the existing theme module, if any.
- `## Stage 1: theme layer`:
  - `theme_tokens.py <theme.json> --rn --out <theme dir>/theme.ts`.
  - A `useTheme()` hook on `useColorScheme()` that returns `theme.light` or `theme.dark`.
  - Fonts: `npx expo install @expo-google-fonts/<family>` for each family and `useFonts(fonts)` at the root, with the splash held until loaded.
  - NativeWind v4: `--css-vars` into `global.css` plus `--tailwind3` merged into `tailwind.config.js`.
- `## Stage 2: shared components`: buttons, inputs, cards, list rows, sheets and headers from the theme. Pressed state via `Pressable` and `states.pressed`. Haptics through `expo-haptics` only in their documented meanings.
- `## Stage 3: screens`: replace StyleSheet literals with theme references, using the `files` lists in `entropy-before.json`. Wrap each screen in its template (screen inset = template margin). Then copy, voice and the allowed-diff tells. About five screens per commit.
- `## Stage 4: brand surface`:
  - `icon` (1024×1024) and `android.adaptiveIcon` in `app.json`
  - a splash that matches the first screen's ground colour with no logo or text
- `## After every stage`:
  - `npx tsc --noEmit` and lint when configured, and `npx expo export --platform ios` as the build check when no other build script exists.
  - Screenshots:
    - `xcrun simctl io booted screenshot ROUND_DIR/after/<id>.png` when a simulator is booted
    - else Expo web through headless Chrome when the project supports react-native-web
    - else HTML recreations, labelled "not from the device" on the board
  - `entropy.py`, `tells_lint.py` and `check` as on web.
- `## Hard limits` and `## Follow-ups`: as on web.

- [ ] **Step 6: Run the tests to verify they pass**

Run: `bash tests/studio.test.sh`
Expected: every `glow-up: loop and apply references` line `ok`, `0 failed`.

- [ ] **Step 7: Commit**

```bash
git add skills/design-studio/references/glowup.md skills/design-studio/references/apply-web.md skills/design-studio/references/apply-native.md tests/studio.test.sh
git commit -m "docs(glowup): the loop and the web and native apply playbooks"
```

---

### Task 10: SKILL.md, axes, release

**Files:**
- Modify: `skills/design-studio/SKILL.md` (description line, new section after "## Paywall mode", four common-mistakes rows)
- Modify: `skills/design-studio/references/variations.md` (new subsection after "### Paywall mode axes")
- Modify: `CHANGELOG.md`, `README.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- Modify: `tests/studio.test.sh` (the existing version assertion moves to 1.3.0; new docs checks)

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Write the failing tests**

In `tests/studio.test.sh`, change the existing line

```bash
grep -q '"version": "1.2.0"' "$REPO/.claude-plugin/plugin.json" && grep -q '"version": "1.2.0"' "$REPO/.claude-plugin/marketplace.json" && ok "version is 1.2.0" || bad "version is 1.2.0"
```

to

```bash
grep -q '"version": "1.3.0"' "$REPO/.claude-plugin/plugin.json" && grep -q '"version": "1.3.0"' "$REPO/.claude-plugin/marketplace.json" && ok "version is 1.3.0" || bad "version is 1.3.0"
```

and insert above `# --- new tests above this line ---`:

```bash
echo "glow-up: docs"
grep -qi "vibe-coded" <(sed -n '1,6p' "$SK/SKILL.md") && ok "SKILL.md description triggers on vibe-coded apps" || bad "SKILL.md description triggers on vibe-coded apps"
grep -q "^## Glow-up mode" "$SK/SKILL.md" && ok "SKILL.md has a Glow-up mode section" || bad "SKILL.md has a Glow-up mode section"
for f in glowup.md glowup-craft.md category-research.md apply-web.md apply-native.md; do
  grep -q "references/$f\|\`$f\`" "$SK/SKILL.md" "$SK/references/glowup.md" && ok "$f is referenced" || bad "$f is referenced"
done
grep -q "^### Glow-up mode axes" "$SK/references/variations.md" && ok "variations.md has glow-up axes" || bad "variations.md has glow-up axes"
grep -q "^## 1.3.0" "$REPO/CHANGELOG.md" && ok "CHANGELOG has 1.3.0" || bad "CHANGELOG has 1.3.0"
grep -q "^## Glow-up mode" "$REPO/README.md" && ok "README has a Glow-up mode section" || bad "README has a Glow-up mode section"
new_sections="$(sed -n '/^## Glow-up mode/,/^## [^G]/p' "$SK/SKILL.md"; sed -n '/^## 1.3.0/,/^## 1.2.0/p' "$REPO/CHANGELOG.md"; sed -n '/^## Glow-up mode/,/^## [^G]/p' "$REPO/README.md")"
grep -q "—" <<<"$new_sections" && bad "the glow-up doc sections have no em dashes" "$(grep -n "—" <<<"$new_sections" | head -3)" || ok "the glow-up doc sections have no em dashes"
```

The check reads only the glow-up sections, because older text (CHANGELOG's `## 1.0.0 — 2026-09-28` heading) already has em dashes and is out of scope.

- [ ] **Step 2: Run them to verify they fail**

Run: `bash tests/studio.test.sh 2>&1 | grep -E "glow-up: docs" -A12`
Expected: FAIL lines for the description, the section, the axes, the CHANGELOG, the README and the version.

- [ ] **Step 3: Edit `SKILL.md`**

In the frontmatter `description`, before `including "render an HTML doc with designs"`, insert:

```
or for turning a vibe-coded or AI-made app into a professionally designed one across every screen (glow-up mode),
```

Add after the "## Paywall mode" section:

```markdown
## Glow-up mode (a vibe-coded app into a designed one)

On when the adapter says `mode: glowup` or the brief asks to make an app
look professional, says it looks vibe-coded or AI-made, or asks for themes
for the whole app. Read `references/glowup.md` before step 1, and
`references/glowup-craft.md`, `references/category-research.md`,
`references/apply-web.md` and `references/apply-native.md` as it directs.
In short:

- `studio.sh new <project> <topic> --glowup` (add `--web` for a web app):
  the round gets the theme board (`gallery-glowup.html`) and both frame
  stylesheets.
- Glow-up is a job, not a surface: directions render in the phone frames
  (app) or the web frames (web) the other modes already use.
- Stages: `intake` (a confirmed brief), `audit` (before screenshots,
  `entropy.py`, `tells_lint.py`, four key screens), `research`
  (`category.md`), `directions` (ten themes on the four key screens),
  `converge`, `system` (every route), `apply` (staged commits on
  `glowup/<topic>`).
- A direction is `vNN/theme.json` (the whole system), `tokens.css` from
  `theme_tokens.py --css`, and `s1.html` to `s4.html`.
- `check` runs `glowup_check.py`: a valid theme, contrast, a reason for
  every framework default, second-order tells only as the named
  signature, fresh tokens, a layout template on every screen, the
  signature on two screens, voice strings from context.md; at apply,
  entropy and tells fall.
- The pick question adds `System proof #N` from `converge`, `Apply #N` in
  `system`, and approve, flag or revert on every apply board.
```

Add to the Common mistakes table:

```markdown
| Matching the vibe-coded app's own look | Glow-up replaces it; the current screens are the Before board, not the authority |
| A theme that only swaps colours and fonts | `theme.json` carries layout templates, states, voice and a signature; `check` fails without them |
| Trading purple slop for tasteful slop | Second-order patterns only as the named signature (`signature.uses`) |
| An apply that changes behaviour | Apply touches styles, markup, copy and assets; behaviour goes to follow-ups |
```

- [ ] **Step 4: Edit `variations.md`**

Add after the "### Paywall mode axes" table:

```markdown
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
| Signature | a shape motif · a corner or edge treatment · an illustration style · a texture · a type treatment |
| Voice | plain · warm coach · expert · playful |

Round 1 mix of ten: three conventional done well, five in-category with a
distinctive twist, two labelled wildcards that break the category.
```

- [ ] **Step 5: Release files**

`CHANGELOG.md`, new top entry:

```markdown
## 1.3.0 · 2026-09-30

Glow-up mode, for turning a vibe-coded or AI-made app into a designed one.

- `studio.sh new <project> <topic> --glowup [--web]` starts a glow-up topic: a theme board gallery with Before, Category and Directions tabs and a spec card per direction.
- Stages: `intake`, `audit`, `research`, `directions`, `converge`, `system` (every route) and `apply` (staged commits on a `glowup/<topic>` branch).
- New scripts: `entropy.py` (distinct colours, sizes, weights, spacing, radii and shadows in an app), `tells_lint.py` (six families of vibe-coded tells), `theme_tokens.py` (one `theme.json` to CSS, Tailwind v3 and v4, shadcn and React Native), `glowup_check.py`, `glowup_sheets.py`.
- New references: `glowup.md`, `glowup-craft.md` (the 13-part system layer and the tells), `category-research.md`, `apply-web.md`, `apply-native.md`.
- Mobile, web and paywall modes are unchanged by glow-up mode.
```

`.claude-plugin/plugin.json`: set `"version": "1.3.0"`. Change the description's parenthesis to `(phone mockups, full scrollable web pages, paywalls in every offer state, or whole-app themes for vibe-coded apps)`. Add `"vibe-coded", "theme", "design-system", "glow-up"` to `keywords`.

`.claude-plugin/marketplace.json`: set the plugin's `"version": "1.3.0"` and its `description` to the same string as plugin.json.

`README.md`: add after the "## Paywall mode" section:

```markdown
## Glow-up mode

Built an app with Lovable, v0, Bolt or Cursor and it looks like every other
one? Ask for a glow-up ("make this look professional", "it looks
vibe-coded"). Tenfold measures what's there (how many colours, font sizes
and spacing values the code really uses, and which AI-design tells it
carries), studies the apps in your category, then shows ten complete
themes on the same four screens of your app. Pick one, see it on every
screen, and it applies the theme to your code on a branch, one reviewable
stage at a time, with before and after screenshots. Web (React, Next,
Vite, Tailwind, shadcn) and React Native / Expo.
```

- [ ] **Step 6: Run the full suite**

Run: `bash tests/studio.test.sh`
Expected: `N passed, 0 failed`, with the new version assertion at 1.3.0.

- [ ] **Step 7: Commit**

```bash
git add skills/design-studio/SKILL.md skills/design-studio/references/variations.md CHANGELOG.md README.md .claude-plugin/plugin.json .claude-plugin/marketplace.json tests/studio.test.sh
git commit -m "Tenfold 1.3.0: glow-up mode for design-studio"
```

---

### Task 11: Hand run on three vibe-coded apps, from screenshots

**Files:**
- Create: `specs/research/2026-10-glowup-handrun.md`

Changed 2026-09-30: the hand run uses the screenshot path (`source: images`, see the spec's "From screenshots" section), which is the version a SaaS would launch with. It needs no repo, so licences don't limit the choice of apps.

- [ ] **Step 1: Pick three apps.** Public vibe-coded apps you can open in a browser (the Lovable, v0 and Bolt showcase galleries are fine), two web and one mobile. For each, take three or four screenshots of different screens (main, densest list, a form, an empty or onboarding state). Record the app URL and which screens.
- [ ] **Step 2: Run glow-up on each** from intake through handoff, uploading the screenshots. Time each stage and note tokens at each stage boundary.
- [ ] **Step 3: Record results** in `specs/research/2026-10-glowup-handrun.md`: per app, the image-audit headline, the visible tells found, how many key screens were invented, the three picks (yours, Claude's, predicted), wall-clock and tokens per stage, and one paragraph on what looked professional and what still looked generated. Note any check that let a bad round through. No screenshots of other people's apps in the public repo; numbers and notes only.
- [ ] **Step 4: Commit** `docs(glowup): hand run on three vibe-coded apps from screenshots`.

---

## Self-review

Spec coverage, section by section:

| Spec section | Task(s) |
|---|---|
| Why | Background only |
| Constraints | Global Constraints, Task 6 |
| How a project turns glow-up on | Tasks 6, 9, 10 |
| Stages | Tasks 5, 7, 9 |
| Intake | Task 9 |
| Audit | Tasks 3, 4, 9 |
| Category research | Tasks 7, 8 |
| What one direction contains | Tasks 1, 2, 5 |
| The system layer | Tasks 1 and 8, with checks in Task 5 |
| The human rules | Tasks 1, 4, 5, 8 |
| Direction axes | Task 10 |
| The theme board | Task 7 |
| Apply | Tasks 5 and 9 |
| Tooling | Tasks 2 to 6 |
| Pick question | Task 9 |
| Testing | Tasks 1 to 7 |
| Build order | Followed |
| Out of scope | Nothing built |

Deviations from the spec, all small:

- **Golden files.** "Golden files" are the committed fixture `tokens.css` files, kept honest by `glowup_check`'s stale-tokens rule, plus the contract assertions in `ThemeTokensTest`.
- **Extra output mode.** `--css-vars` is added to `theme_tokens.py` because apply needs variables without the mockup classes.
- **Show-delay rule.** The tells lint's show-delay rule is a static heuristic (a spinner in a file with no delay or transition token).

Type consistency:

- **theme_core.** `ROLES`, `RAMP` and `SCREENS` are defined in Task 1 and used unchanged in Tasks 2, 5 and 7.
- **Finding shape.** The finding dict `{rule, family, file, line, message}` is defined in Task 4 and read in Task 5.
- **Manifest shapes.** The Task 5 manifests are read by Tasks 6, 7 and 9.
- **Shared functions.** `css(t)` is shared by `make.py` and `glowup_check.py`, and `walk()` by `entropy.py` and `tells_lint.py`.
