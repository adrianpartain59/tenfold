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


if __name__ == "__main__":
    unittest.main()
