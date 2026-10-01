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
