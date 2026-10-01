#!/usr/bin/env python3
"""Regenerate the glow-up smoke fixture from r1/v01/theme.json and the two
fixture apps. Run from the repo root: python3 tests/fixtures/glowup-smoke/make.py"""
import copy, json, os, struct, subprocess, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(FIX))
SCRIPTS = os.path.join(REPO, "skills", "design-studio", "scripts")
sys.path.insert(0, SCRIPTS)
import theme_tokens as tt

def _png(w, h, rgb):
    """An opaque single-colour RGB PNG, so the before screens have something for image_audit.py to measure."""
    chunk = lambda k, d: struct.pack(">I", len(d)) + k + d + struct.pack(">I", zlib.crc32(k + d) & 0xFFFFFFFF)
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


PNG = _png(8, 8, (0x6b, 0x72, 0x80))
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
    import handoff
    hdir = os.path.join(HERE, "r4", "handoff")
    handoff.write_handoff(v01, hdir)
    sections = "".join(f"## {title}\n\nLayout: {tpl}. Keep every datum; restyle with the tokens and rewrite the copy in the voice.\n\n"
                       for title, tpl, _ in SCREENS.values())
    write(os.path.join(hdir, "screens.md"), "# Screens\n\n" + sections)
    print("OK glow-up smoke fixture regenerated")


if __name__ == "__main__":
    main()
