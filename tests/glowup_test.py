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
