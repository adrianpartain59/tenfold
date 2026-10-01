#!/usr/bin/env python3
"""Find what every direction in a glow-up round has in common.

  round_audit.py <round-dir>

Ten directions that differ in type and colour can still share a layout, an
interaction model or an icon family that nobody chose. This reads every
direction's theme.json and screens, extracts a fixed set of features, and
prints each feature that all directions but at most one share (SHARED),
and each value 60% or more of them hold (MAJORITY), since a cluster can
come from the brief's own examples rather than from a decision. A shared
feature is not a failure: the category may call for it. Each one is a
question for the agent before the link goes out: decided (a theme.json
decision says why) or defaulted (fix it in the fix batch). Needs at least
four directions. Always exits 0.
"""
import json, os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme_core import parse, resolve, srgb_to_oklch

MIN_DIRECTIONS = 4
MAJORITY = 0.6  # a value this share of directions holds is a cluster worth a second look


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _yes(b):
    return "yes" if b else "no"


def _ground(t, html):
    mode = "dark" if re.search(r'<html[^>]*data-theme="dark"', html) else "light"
    try:
        return "dark" if srgb_to_oklch(parse(resolve(t, mode, "ground")))[0] < 0.5 else "light"
    except Exception:
        return "unknown"


def _bucket(v, edges, names):
    for e, n in zip(edges, names):
        if v <= e:
            return n
    return names[-1]


# (label, function(theme, screens dict) -> value)
FEATURES = [
    ("home hero alignment", lambda t, s: "centred" if re.search(r"text-align:\s*center", s["s1"]) else "left or split"),
    ("core task is keyboard-first", lambda t, s: _yes("keyboard" in t.get("decisions", {}).get("interaction", "").lower())),
    ("quiz moves with Previous / Next", lambda t, s: _yes(re.search(r"Previous", s["s4"]) and re.search(r"Next", s["s4"]))),
    ("quiz answers in a 2-column grid", lambda t, s: _yes(re.search(r"grid-template-columns:\s*(repeat\(2|1fr 1fr)", s["s4"]))),
    ("no <img> on any screen", lambda t, s: _yes(not any("<img" in h for h in s.values()))),
    ("no drawn SVG art (only icons)", lambda t, s: _yes(not any(re.search(r"<svg\b(?:(?!<use)(?!</svg>).)*<(path|circle|rect|polyline|line|ellipse)\b", h, re.S) for h in s.values()))),
    ("icon set", lambda t, s: t["icons"]["set"]),
    ("ground", lambda t, s: _ground(t, s["s1"])),
    ("sidebar navigation", lambda t, s: _yes(re.search(r"<aside\b(?:(?!</aside>).)*Home(?:(?!</aside>).)*Quizzes", s["s2"], re.S))),
    ("footer on home", lambda t, s: _yes("<footer" in s["s1"])),
    ("FAQ on home", lambda t, s: _yes(re.search(r"FAQ|frequently asked|questions you", s["s1"], re.I))),
    ("brand mark is text only", lambda t, s: _yes(not re.search(r"<(header|nav)\b[^>]*>(?:(?!</(header|nav)>).)*<svg\b(?:(?!<use).)*?</svg>", s["s1"], re.S))),
    ("moment uses @keyframes", lambda t, s: _yes("@keyframes" in s.get("moment", ""))),
    ("elevation style", lambda t, s: t["elevation"]["style"]),
    ("one family for display and body", lambda t, s: _yes(t["type"]["display"]["family"] == t["type"]["body"]["family"])),
    ("card radius", lambda t, s: _bucket(t["shape"]["radius"].get("md", 0), (4, 10, 16), ("sharp", "soft", "round", "very round"))),
]


def audit(round_dir):
    m = json.load(open(os.path.join(round_dir, "manifest.json"), encoding="utf-8"))
    vs = m.get("variations", [])
    if len(vs) < MIN_DIRECTIONS:
        return [f"AUDIT {len(vs)} directions: too few to compare (needs {MIN_DIRECTIONS})"]
    values = {label: [] for label, _ in FEATURES}
    for v in vs:
        d = os.path.join(round_dir, v.get("dir", v["id"]))
        t = json.load(open(os.path.join(d, "theme.json"), encoding="utf-8"))
        screens = {k: _read(os.path.join(d, f"{k}.html")) for k in ("s1", "s2", "s3", "s4", "moment")}
        for label, fn in FEATURES:
            try:
                values[label].append(str(fn(t, screens)))
            except Exception:
                values[label].append("unknown")
    n = len(vs)
    lines = []
    for label, _ in FEATURES:
        value, count = Counter(values[label]).most_common(1)[0]
        if value == "unknown":
            continue
        if count >= n - 1:
            lines.append(f"SHARED {count}/{n} {label}: {value}")
        elif count / n >= MAJORITY and value != "no":  # most directions NOT doing something is not a cluster
            lines.append(f"MAJORITY {count}/{n} {label}: {value}")
    shared = sum(1 for l in lines if l.startswith("SHARED"))
    lines.append(f"AUDIT {n} directions · {shared} shared features · {len(lines) - shared} majority clusters · decided or defaulted? check each against theme.json decisions")
    return lines


def main(argv):
    if len(argv) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    print("\n".join(audit(argv[0].rstrip("/"))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
