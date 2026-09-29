#!/usr/bin/env python3
"""Validate a design-studio web round before the link goes out.

  web_check.py <round-dir>

Prints WARN/FAIL lines, then "OK|FAIL <n> web variation(s) (<stage>)".
Exits 1 on any FAIL. Checks: every page file exists; every page links the
direction's own tokens.css; every local .html link (in pages and in the
direction's chrome.js) resolves; no lorem ipsum; unique names; in the system
stage, every manifest template is covered by every variation.
"""
import json, os, re, sys
from html.parser import HTMLParser

STAGES = ("directions", "converge", "system")
SKIP = re.compile(r"^(https?:|mailto:|tel:|#|javascript:|data:)", re.I)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.css = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "link" and "stylesheet" in (a.get("rel") or "") and a.get("href"):
            self.css.append(a["href"])


def broken(base, hrefs):
    """Local .html (or directory) links under base that don't resolve to a file."""
    out = []
    for h in hrefs:
        if SKIP.match(h):
            continue
        target = h.split("#")[0].split("?")[0]
        if target.endswith("/"):
            target += "index.html"
        if not target.endswith(".html"):
            continue
        if not os.path.isfile(os.path.normpath(os.path.join(base, target))):
            out.append(h)
    return out


def main(d):
    errs, warns = [], []
    try:
        m = json.load(open(os.path.join(d, "manifest.json")))
    except Exception as e:
        print(f"FAIL manifest.json unreadable: {e}")
        return 1
    stage = m.get("stage", "directions")
    if stage not in STAGES:
        errs.append(f"unknown stage {stage}")
    vs = m.get("variations", [])
    if not vs:
        errs.append("no variations")
    elif stage != "system" and len(vs) < 2:
        errs.append(f"only {len(vs)} variations")
    templates = [t.get("id") for t in m.get("templates", [])]
    if stage == "system" and not templates:
        errs.append("system stage needs manifest.templates")

    names = set()
    for v in vs:
        vid = v.get("id", "?")
        pages = v.get("pages") or ([{"template": "home", "file": v["file"]}] if v.get("file") else [])
        if not pages:
            errs.append(f"{vid}: no file or pages")
            continue
        covered, dirs = set(), set()
        for p in pages:
            f = p.get("file") or ""
            path = os.path.join(d, f)
            if not f or not os.path.isfile(path):
                errs.append(f"{vid}: missing page {f}")
                continue
            covered.add(p.get("template"))
            base = os.path.dirname(path)
            dirs.add(base)
            html = open(path, encoding="utf-8").read()
            if re.search(r"lorem ipsum", html, re.I):
                errs.append(f"{vid}/{f}: lorem ipsum")
            links = Links()
            links.feed(html)
            # The direction's own tokens.css sits next to the page, not ../../tokens.css (the brand base).
            if not any(c == "tokens.css" or (c.endswith("/tokens.css") and not c.startswith("..")) for c in links.css):
                errs.append(f"{vid}/{f}: does not link a direction tokens.css")
            for h in broken(base, links.hrefs):
                errs.append(f"{vid}/{f}: broken link {h}")
        for base in sorted(dirs):
            chrome = os.path.join(base, "chrome.js")
            if os.path.isfile(chrome):
                hrefs = re.findall(r'href="([^"]+)"', open(chrome, encoding="utf-8").read())
                rel = os.path.relpath(chrome, d)
                for h in broken(base, hrefs):
                    errs.append(f"{rel}: broken link {h}")
        if stage == "system":
            missing = [t for t in templates if t not in covered]
            if missing:
                errs.append(f"{vid}: missing templates {', '.join(missing)}")
        if not v.get("idea"):
            warns.append(f"{vid}: no one-line idea")
        n = (v.get("name") or "").strip().lower()
        if n in names:
            errs.append(f"duplicate name {n}")
        names.add(n)

    if stage != "system":
        for k in ("agentPick", "predictedPick"):
            if k not in m:
                warns.append(f"manifest has no {k}")
    if not os.path.exists(os.path.join(d, "..", "tokens.css")):
        warns.append("no ../tokens.css (brand base) for this topic")
    for w in warns:
        print("WARN", w)
    for e in errs:
        print("FAIL", e)
    s = "" if len(vs) == 1 else "s"
    print(f"{'FAIL' if errs else 'OK'} {len(vs)} web variation{s} ({stage})")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1].rstrip("/")))
