#!/usr/bin/env python3
"""Validate a glow-up round before the link goes out.

  glowup_check.py <round-dir>

directions / converge: every direction has a valid theme.json (contrast,
defaults with reasons, second-order tells only as the named signature), a
tokens.css that matches theme_tokens.py --css, voice strings found in
context.md, notes.market, notes.signature and notes.composition, and four key screens that link
their tokens and frame, declare a layout template, use no literal colours,
carry no fingerprint, copy or second-order tells, and show the signature on
at least two screens.
system: the same theme checks, plus every manifest route as routes/<id>.html.
apply: before/after evidence exists, entropy and tells did not rise (and
entropy fell from stage 3), no literal colours outside the theme files, and
a failed build was reverted. An image-sourced topic (source: images) has no
apply stage.
handoff: every handoff.py file exists, tokens.css matches the theme, and
screens.md has a "## <label>" section for every screen that wasn't invented.
Prints WARN/FAIL lines, then "OK|FAIL <summary>". Exits 1 on any FAIL.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import handoff as ho
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
        for k in ("market", "signature", "composition"):
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


def check_handoff(d, m, errs, warns):
    h = m.get("handoff") or {}
    hdir = os.path.join(d, h.get("dir", "handoff"))
    rel = os.path.relpath(hdir, d)
    try:
        t = tc.load_theme(os.path.normpath(os.path.join(d, h.get("theme") or "missing")))
    except (OSError, ValueError) as e:
        errs.append(f"handoff.theme unreadable ({h.get('theme')}): {e}")
        return "glow-up handoff"
    errs += [f"handoff theme: {e}" for e in tc.validate_theme(t)]
    missing = [f for f in ho.FILES if not os.path.isfile(os.path.join(hdir, f))]
    errs += [f"{rel} is missing {f}" for f in missing]
    tok = os.path.join(hdir, "tokens.css")
    if not errs and open(tok, encoding="utf-8").read() != tt.css_vars(t):
        errs.append(f"{rel}/tokens.css is stale; rerun handoff.py")
    screens = [s for s in m.get("screens", []) if not s.get("invented")]
    sp = os.path.join(hdir, "screens.md")
    if not os.path.isfile(sp):
        errs.append(f"{rel} is missing screens.md (one ## section per screen)")
    else:
        heads = {ln[3:].strip() for ln in open(sp, encoding="utf-8").read().splitlines() if ln.startswith("## ")}
        errs += [f"{rel}/screens.md has no section for {s['label']}" for s in screens if s.get("label") not in heads]
    return f"glow-up handoff ({len(ho.FILES)} files, {len(screens)} screens)"


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
    elif stage == "apply" and m.get("source") == "images":
        errs.append("apply needs the codebase; an image-sourced topic ends at handoff")
        summary = "glow-up apply"
    elif stage == "apply":
        summary = check_apply(d, m, errs, warns)
    elif stage == "handoff":
        summary = check_handoff(d, m, errs, warns)
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
