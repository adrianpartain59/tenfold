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
# Decisions every direction makes and justifies in theme.json "decisions" (one line each).
DECISIONS = ("composition", "interaction", "navigation", "anatomy", "art", "icons", "mark", "motion", "mobile")
ICON_SETS = ("feather", "lucide", "tabler", "tabler-filled",
             "phosphor-thin", "phosphor-light", "phosphor-regular", "phosphor-bold", "phosphor-fill", "phosphor-duotone",
             "heroicons-outline", "heroicons-solid")
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
    if _str(ic.get("set")) and ic["set"] not in ICON_SETS:
        e.append(f"icons.set must be one of {', '.join(ICON_SETS)} (got {ic['set']!r})")
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
    dec = t.get("decisions") or {}
    for k in DECISIONS:
        if not _str(dec.get(k)):
            e.append(f"decisions.{k} missing (one line: what this direction chose and why)")
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
