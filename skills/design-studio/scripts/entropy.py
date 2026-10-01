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
