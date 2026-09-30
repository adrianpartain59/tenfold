#!/usr/bin/env python3
"""Validate a design-studio paywall round before the link goes out.

  paywall_check.py <round-dir>

Prints WARN/FAIL lines, then "OK|FAIL <n> paywall variation(s) (<stage>, <k> state(s))".
Exits 1 on any FAIL. Checks: known stage and states; every variation has a
file for every state; every non-step frame carries the required data-pw
markers with exactly one cta (plus trial-terms when manifest.trial is true);
every proof element's data-src is in the topic's context.md "## Proof" list
and its text matches; ab rounds have one control and a variable per variant;
no lorem ipsum; unique names.
"""
import json, os, re, sys
from html.parser import HTMLParser

STAGES = ("concepts", "concept", "converge", "ab")
STATE = re.compile(r"^(main|alt-plan|exit|friend|promo|winback|step-[0-9]+)$")
REQUIRED = ("billed-price", "renewal", "restore", "terms", "privacy", "cta")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
PROOF_LINE = re.compile(r"^\s*[-*]\s*(P\d+)\s*:\s*(.+)$")


class Frame(HTMLParser):
    """Collects data-pw markers, stylesheet hrefs and the text of every proof element."""

    def __init__(self):
        super().__init__()
        self.pw, self.css, self.proofs = [], [], []  # proofs: [data-src, text]
        self._open = []  # [depth, index into proofs] for proof elements still open

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and "stylesheet" in (a.get("rel") or "") and a.get("href"):
            self.css.append(a["href"])
        toks = (a.get("data-pw") or "").split()
        self.pw += toks
        if tag in VOID:
            if "proof" in toks:
                text = a.get("alt") or a.get("aria-label") or ""
                self.proofs.append([a.get("data-src") or "", text])
            return
        for o in self._open:
            o[0] += 1
        if "proof" in toks:
            self.proofs.append([a.get("data-src") or "", ""])
            self._open.append([1, len(self.proofs) - 1])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for o in self._open:
            o[0] -= 1
        self._open = [o for o in self._open if o[0] > 0]

    def handle_data(self, data):
        for o in self._open:
            self.proofs[o[1]][1] += data


def proof_list(topic):
    """{"P1": entry text} from context.md's "## Proof" section, or None without a context.md."""
    p = os.path.join(topic, "context.md")
    if not os.path.isfile(p):
        return None
    out, on = {}, False
    for line in open(p, encoding="utf-8"):
        if line.startswith("## "):
            on = line.strip()[3:].lower().startswith("proof")
            continue
        mt = PROOF_LINE.match(line) if on else None
        if mt:
            out[mt.group(1)] = mt.group(2)
    return out


def norm(s):
    return re.sub(r"[^0-9a-z]+", "", s.lower())


def main(d):
    errs, warns = [], []
    try:
        m = json.load(open(os.path.join(d, "manifest.json")))
    except Exception as e:
        print(f"FAIL manifest.json unreadable: {e}")
        return 1
    stage = m.get("stage", "concepts")
    if stage not in STAGES:
        errs.append(f"unknown stage {stage}")
    states = m.get("states") or ["main"]
    if "main" not in states:
        errs.append("states must include main")
    for s in states:
        if not STATE.match(s):
            errs.append(f"unknown state {s}")
    required = REQUIRED + (("trial-terms",) if m.get("trial") else ())
    vs = m.get("variations", [])
    if len(vs) < 2:
        errs.append(f"only {len(vs)} variations")
    if stage == "ab":
        controls = [v for v in vs if v.get("control")]
        if len(controls) != 1:
            errs.append(f"ab round needs exactly one control, has {len(controls)}")
        for v in vs:
            if not v.get("control") and not (v.get("variable") or "").strip():
                errs.append(f"{v.get('id', '?')}: ab variant has no variable")

    proofs = proof_list(os.path.dirname(os.path.abspath(d)))
    names = set()
    for v in vs:
        vid, vdir = v.get("id", "?"), v.get("dir")
        if not vdir:
            errs.append(f"{vid}: no dir")
            continue
        for s in states:
            rel = f"{vdir}/{s}.html"
            path = os.path.join(d, rel)
            if not os.path.isfile(path):
                errs.append(f"{vid}: missing state {s} ({rel})")
                continue
            where = f"{vid}/{s}"
            html = open(path, encoding="utf-8").read()
            if re.search(r"lorem ipsum", html, re.I):
                errs.append(f"{where}: lorem ipsum")
            fr = Frame()
            fr.feed(html)
            if not any(c.endswith("tokens.css") for c in fr.css):
                warns.append(f"{where}: does not link tokens.css")
            if not any(c.endswith("paywall.css") for c in fr.css):
                warns.append(f"{where}: does not link paywall.css")
            if not s.startswith("step-"):
                for k in required:
                    if k not in fr.pw:
                        errs.append(f"{where}: missing data-pw {k}")
                n_cta = fr.pw.count("cta")
                if n_cta > 1:
                    errs.append(f"{where}: {n_cta} data-pw cta (need exactly 1)")
            for src, text in fr.proofs:
                if proofs is None:
                    errs.append(f"{where}: shows proof but the topic has no context.md")
                    break
                if src not in proofs:
                    errs.append(f"{where}: proof {src or '(no data-src)'} not in context.md")
                    continue
                nt = norm(text)
                if len(nt) < 4:
                    errs.append(f"{where}: proof {src} has no checkable text (use alt or visible text)")
                elif nt not in norm(proofs[src]):
                    errs.append(f"{where}: proof {src} text not in context.md")
        if not v.get("idea"):
            warns.append(f"{vid}: no one-line idea")
        n = (v.get("name") or "").strip().lower()
        if n in names:
            errs.append(f"duplicate name {n}")
        names.add(n)

    if stage != "ab":
        for k in ("agentPick", "predictedPick"):
            if k not in m:
                warns.append(f"manifest has no {k}")
    if not os.path.exists(os.path.join(d, "..", "tokens.css")):
        warns.append("no ../tokens.css for this topic")
    for w in warns:
        print("WARN", w)
    for e in errs:
        print("FAIL", e)
    nv, ns = len(vs), len(states)
    print(f"{'FAIL' if errs else 'OK'} {nv} paywall variation{'' if nv == 1 else 's'} "
          f"({stage}, {ns} state{'' if ns == 1 else 's'})")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1].rstrip("/")))
