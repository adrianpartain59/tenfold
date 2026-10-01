#!/usr/bin/env python3
"""Write a glow-up handoff: the picked theme in every token format plus a
paste-ready brief for an AI builder (Lovable, v0, Bolt, Cursor).

  handoff.py <theme.json> <out-dir>

The final stage for a topic with no codebase (source: images), or for a
code topic where the user wants the tokens without a branch. The agent adds
screens.md beside these files, one "## <screen label>" section per screen.
Prints "HANDOFF <n> files in <out-dir>"; FAIL lines and exit 1 on an invalid
theme.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme_tokens as tt
from theme_core import RAMP, ROLES, load_theme, parse, resolve, to_hex, validate_theme

FILES = {
    "tokens.css": tt.css_vars,
    "theme.css": tt.css,
    "tailwind-v4.css": tt.tailwind,
    "tailwind.config.v3.js": tt.tailwind3,
    "shadcn.css": tt.shadcn,
    "shadcn-hsl.css": lambda t: tt.shadcn(t, hsl=True),
    "theme.ts": tt.rn,
    "prompt.md": None,
}
CASE_WORDS = {"sentence": "sentence case", "title": "Title Case", "upper": "UPPER CASE"}


def _hex(t, mode, role):
    return to_hex(parse(resolve(t, mode, role)))


def _list(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def prompt(t):
    ty, lay, st, sg, vo = t["type"], t["layout"], t["states"], t["signature"], t["voice"]
    faces = [(k.capitalize(), ty[k]) for k in ("display", "body", "mono") if (ty.get(k) or {}).get("family")]
    by_case = {}
    for kind, case in vo["case"].items():
        by_case.setdefault(case, []).append(kind + "s")
    case_line = " ".join(f"Use {CASE_WORDS[c]} for {_list(kinds)}." for c, kinds in by_case.items())
    out = [f"# Apply the {t['name']} design system", "",
           "Paste this into your AI builder (Lovable, v0, Bolt or Cursor) together with the files in this folder. "
           "It restyles the app. It does not change what the app does.", "",
           "## Files", "",
           "- `tokens.css`: every colour, spacing, radius, shadow, motion and state value as CSS variables. Add it to the global stylesheet.",
           "- `tailwind-v4.css` or `tailwind.config.v3.js`: maps Tailwind utilities to those variables. Use the one that matches the project.",
           "- `shadcn.css` (OKLCH) or `shadcn-hsl.css` (HSL triplets): replaces shadcn/ui's `:root` and `.dark` blocks.",
           "- `theme.ts`: the same theme for React Native and Expo.",
           "- `theme.css`: the full stylesheet the mockups were built on, including type and layout classes, for reference.",
           "", "## Fonts", ""]
    out += [f"- {name}: {f['family']} ({', '.join(str(w) for w in f['weights'])})" for name, f in faces]
    out += ["", f"Why this pairing: {ty['pairing']}", "",
            "## Colours", "",
            "Use these roles, never raw colour values. `tokens.css` defines each one as `--c-<role>`.", "",
            "| Role | Light | Dark |", "|---|---|---|"]
    out += [f"| {r} | {_hex(t, 'light', r)} | {_hex(t, 'dark', r)} |" for r in ROLES]
    out += ["", "## Type", "", "| Style | Face | Size / line | Weight | Tracking |", "|---|---|---|---|---|"]
    for k in RAMP:
        r = ty["ramp"][k]
        upper = ", all caps" if r.get("upper") else ""
        out.append(f"| {k} | {ty[r['face']]['family']} | {r['size']:g} / {r['line']:g} px | {r['weight']} | {r['track']:g} em{upper} |")
    out += ["", "Numbers use tabular figures.", "",
            "## Spacing and layout", "",
            f"Spacing scale: {', '.join(f'{v:g}' for v in lay['space'])} px. Use only these values.", "",
            "Every screen uses exactly one of these layouts:", ""]
    for tp in lay["templates"]:
        width = f"max {tp['max']:g} px" if tp.get("max") else "full width"
        out.append(f"- {tp['label']}: {tp['columns']} column{'' if tp['columns'] == 1 else 's'}, {width}, "
                   f"{tp['gutter']:g} px gutter, {tp['margin']:g} px margin, {tp['density']}")
    out += ["", "## Shape and depth", "",
            "Radii: " + ", ".join(f"{k} {v:g} px" for k, v in t["shape"]["radius"].items()) + ".",
            f"Elevation style: {t['elevation']['style']}. Levels:", ""]
    out += [f"- {k}: `{v}`" for k, v in t["elevation"]["levels"].items()]
    out += ["", "## States", "",
            f"Every button, input and link has a hover overlay at {st['hover']:g}, a pressed overlay at {st['pressed']:g}, "
            f"{st['disabled']:g} opacity when disabled, and a {st['focus']['width']:g} px focus ring in the focus colour at "
            f"{st['focus']['offset']:g} px offset. Loading buttons keep their label. Inputs have an error state.", "",
            "## Signature", "",
            f"{sg['what']}. It appears on the screens `screens.md` marks as signature screens. {sg['never']}.", "",
            "## Voice", "",
            f"{_list(vo['adjectives']).capitalize()}. Buttons say what happens. {case_line}", "",
            "Rewrite these strings:", ""]
    out += [f"- “{s['before']}” → “{s['after']}”" for s in vo["strings"]]
    if vo["glossary"]:
        out += ["", "Glossary:", ""] + [f"- {k}: {v}" for k, v in vo["glossary"].items()]
    out += ["", "## Design decisions", "", "Why the design is the way it is. Keep these when you change anything.", ""]
    out += [f"- {k.capitalize()}: {v}" for k, v in t["decisions"].items()]
    out += ["", "## Screen by screen", "",
            "Follow `screens.md` in this folder: one section per screen, naming its layout and what to change.", "",
            "## Do not change", "",
            "- Data, logic, API calls, routing, navigation and features.",
            "- Test IDs and analytics events.",
            "", "Change styles, markup, copy and assets only.", ""]
    return "\n".join(out)


def write_handoff(t, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for name, fn in FILES.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(prompt(t) if fn is None else fn(t))
    return list(FILES)


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    t = load_theme(argv[0])
    errs = validate_theme(t)
    if errs:
        for e in errs:
            print("FAIL", e)
        return 1
    files = write_handoff(t, argv[1])
    print(f"HANDOFF {len(files)} files in {argv[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
