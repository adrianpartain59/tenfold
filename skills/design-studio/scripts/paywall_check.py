#!/usr/bin/env python3
"""Validate a design-studio paywall round before the link goes out.

  paywall_check.py <round-dir>                      static checks
  paywall_check.py <round-dir> --measured <file>    static checks + layout measures
  paywall_check.py measure-page <round-dir> [name]  write _pwmeasure.html (studio.sh
                                                     dumps it through headless Chrome)

Prints WARN/FAIL lines, then "OK|FAIL <n> paywall variation(s) (<stage>, <k> state(s))".
Exits 1 on any FAIL. Checks: known stage and states; every variation has a
file for every state and every screen of its flow (manifest.flow or the
variation's own flow, ending in main); every screen carries a data-pw="visual"
hero; every non-step frame carries the required data-pw markers with exactly
one cta (plus trial-terms when manifest.trial is true); every proof element's
data-src is in the topic's context.md "## Proof" list and its text matches;
ab rounds have one control and a variable per variant; no lorem ipsum; unique
names. With --measured: the visual share of each screen's first viewport and
its word count stay inside the budgets below (paywall-craft.md, "Visual first").
"""
import json, os, re, sys
from html.parser import HTMLParser

STAGES = ("concepts", "concept", "converge", "ab")
STATE = re.compile(r"^(main|alt-plan|exit|friend|promo|winback|step-[0-9]+)$")
REQUIRED = ("billed-price", "renewal", "restore", "terms", "privacy", "cta")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
PROOF_LINE = re.compile(r"^\s*[-*]\s*(P\d+)\s*:\s*(.+)$")

# Visual-first budgets, per screen, measured in the first 393x852 viewport.
# visual = share of the viewport covered by data-pw="visual" elements.
# words  = visible words outside the purchase machinery (plan cards, price,
#          trial terms, CTA, legal) and outside a data-pw="note" letter.
VISUAL_MIN = {"step": 0.40, "purchase": 0.25}
WORDS_MAX = {"step": 30, "purchase": 40}
NOTE_WORDS_MAX = 60
EXEMPT = ("renewal", "terms", "privacy", "restore", "trial-terms", "legal", "plan", "cta", "billed-price")


class Frame(HTMLParser):
    """Collects data-pw markers, stylesheet hrefs and the text of every proof element."""

    def __init__(self):
        super().__init__()
        self.pw, self.css, self.proofs = [], [], []  # proofs: [data-src, text]
        self.acts = []  # [(data-pw tokens, data-action)] for every element carrying either
        self._open = []  # [depth, index into proofs] for proof elements still open

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and "stylesheet" in (a.get("rel") or "") and a.get("href"):
            self.css.append(a["href"])
        toks = (a.get("data-pw") or "").split()
        self.pw += toks
        if toks or a.get("data-action"):
            self.acts.append((toks, a.get("data-action") or ""))
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


def screens(d, m):
    """[(variation, rel path)] for every screen of every flow and state."""
    out = []
    for v in m.get("variations", []):
        if not v.get("dir"):
            continue
        flow = v.get("flow") or m.get("flow") or []
        for s in dict.fromkeys(flow + (m.get("states") or ["main"])):
            out.append(f"{v['dir']}/{s}.html")
    return out


MEASURE_JS = r"""
const W = 393, H = 852, EX = %s.map((k) => `[data-pw~="${k}"]`).join(","), KIT = %s;
// Build-target audit (manifest.kit): every drawn element is a node type the
// target can build, and no computed style uses something it can't render.
function audit(doc) {
  const out = [], leaf = KIT.leaves.map((t) => `[data-sw="${t}"]`).join(",");
  const chrome = (KIT.chrome || []).join(",");
  const say = (el, msg) => {
    const id = el.tagName.toLowerCase() + (el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/)[0] : "");
    out.push(`${id}: ${msg}`);
  };
  for (const el of doc.body.querySelectorAll("*")) {
    if (el.closest("script,style") || (chrome && el.closest(chrome))) continue;
    const up = el.parentElement && el.parentElement.closest(leaf);
    if (up && up.getAttribute("data-sw") !== "text") continue;  // insides of an image/svg/lottie leaf
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) continue;
    const sw = el.getAttribute("data-sw"), cs = doc.defaultView.getComputedStyle(el);
    if (up) {
      if (!(KIT.inline_in_text || []).includes(el.tagName.toLowerCase())) say(el, "only inline spans may sit inside a text node");
    } else if (!sw) say(el, "no data-sw node type (wrap it in a buildable node)");
    else if (!KIT.nodes.includes(sw)) say(el, `"${sw}" is not a node type this target has`);
    for (const rule of KIT.css || []) {
      const v = cs.getPropertyValue(rule.prop);
      if (v && new RegExp(rule.bad).test(v) && !(rule.ok && new RegExp(rule.ok).test(v))) say(el, `${rule.prop}: ${v.slice(0, 40)} (${rule.why})`);
    }
    for (const ps of ["::before", "::after"]) {
      const c = doc.defaultView.getComputedStyle(el, ps).content;
      if (c && c !== "none" && c !== "normal") say(el, `${ps} draws content (pseudo-elements don't exist in the editor; make it a node)`);
    }
    if (sw === "text") for (const lit of KIT.literal || []) {
      if (new RegExp(lit.pattern).test(el.textContent) && !el.hasAttribute(lit.attr)) say(el, `"${el.textContent.trim().slice(0, 30)}": ${lit.why} (${lit.attr})`);
    }
    if (KIT.fonts && (sw === "text" || up) && el.textContent.trim()) {
      const fam = cs.fontFamily.split(",")[0].replace(/["']/g, "").trim();
      if (!KIT.fonts.some((f) => f.toLowerCase() === fam.toLowerCase())) say(el, `font "${fam}" is not available on the target`);
    }
  }
  // Unmarked nodes are the commonest and least specific failure: list the rest first.
  return [...new Set(out)].sort((a, b) => a.includes("no data-sw") - b.includes("no data-sw"));
}
const out = {};
function measure(doc) {
  const vis = [...doc.querySelectorAll('[data-pw~="visual"]')].map((e) => e.getBoundingClientRect());
  let hit = 0, tot = 0;
  for (let y = 0; y < H; y += 6) for (let x = 0; x < W; x += 6) {
    tot++; if (vis.some((r) => x >= r.left && x < r.right && y >= r.top && y < r.bottom)) hit++;
  }
  let words = 0, note = 0;
  const w = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const el = n.parentElement;
    if (!el || el.closest("script,style,.status-bar,[aria-hidden=true]") || el.closest(EX)) continue;
    const cs = doc.defaultView.getComputedStyle(el);
    if (cs.visibility === "hidden" || cs.display === "none" || +cs.opacity === 0) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height || r.top >= H || r.bottom <= 0) continue;
    const k = (n.textContent.match(/[\p{L}\p{N}][\p{L}\p{N}'’.,%%$-]*/gu) || []).length;
    if (el.closest('[data-pw~="note"]')) note += k; else words += k;
  }
  return { visual: Math.round((hit / tot) * 100) / 100, words, note, kit: KIT ? audit(doc) : null };
}
const files = %s;
let left = files.length;
for (const f of files) {
  const fr = document.createElement("iframe");
  fr.style.cssText = `width:${W}px;height:${H}px;border:0`;
  fr.onload = () => { setTimeout(() => { try { out[f] = measure(fr.contentDocument); } catch (e) { out[f] = { error: String(e) }; }
    if (--left === 0) document.getElementById("out").textContent = JSON.stringify(out); }, 400); };
  fr.src = f + "?theme=light";
  document.body.appendChild(fr);
}
"""


def load_kit(m):
    """The build-target kit named by manifest.kit (kits/<name>/kit.json in the skill), or None."""
    name = m.get("kit")
    if not name:
        return None
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kits", name, "kit.json")
    return json.load(open(p)) if os.path.isfile(p) else {"missing": name}


def measure_page(d, name="_pwmeasure.html"):
    m = json.load(open(os.path.join(d, "manifest.json")))
    files = screens(d, m)
    kit = load_kit(m)
    js = MEASURE_JS % (json.dumps(list(EXEMPT)), json.dumps(kit if kit and "missing" not in kit else None), json.dumps(files))
    with open(os.path.join(d, name), "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><meta charset="utf-8"><pre id="out"></pre><script>{js}</script>')
    print(name)
    return 0


def load_measured(path, errs):
    """The JSON the measure page wrote into <pre id="out">, from Chrome's --dump-dom output."""
    try:
        raw = open(path, encoding="utf-8").read()
        mt = re.search(r'<pre id="out">(.*?)</pre>', raw, re.S)
        import html as _h
        return json.loads(_h.unescape(mt.group(1))) if mt and mt.group(1).strip() else {}
    except Exception as e:
        errs.append(f"could not read layout measures: {e}")
        return {}


def check_actions(where, s, fr, acts, errs):
    """Every purchase control carries the tap action the build target wires it with (data-action)."""
    for marker, act in (("cta", acts.get("cta")), ("plan", acts.get("plan")), ("restore", acts.get("restore"))):
        if not act:
            continue
        for toks, a in fr.acts:
            if marker in toks and a != act:
                errs.append(f"{where}: data-pw {marker} needs data-action=\"{act}\" (has \"{a or 'none'}\")")
                break
    step = acts.get("step-continue")
    if step and s.startswith("step-") and not any(a == step for _, a in fr.acts):
        errs.append(f"{where}: no control with data-action=\"{step}\" (the step's Continue)")


def check_measures(where, s, r, errs):
    if not r:
        errs.append(f"{where}: not measured (frame failed to load in Chrome)")
        return
    if r.get("error"):
        errs.append(f"{where}: measure error {r['error']}")
        return
    kind = "step" if s.startswith("step-") else "purchase"
    if r["visual"] < VISUAL_MIN[kind]:
        errs.append(f"{where}: visual covers {r['visual']:.0%} of the first viewport (needs {VISUAL_MIN[kind]:.0%})")
    if r["words"] > WORDS_MAX[kind]:
        errs.append(f"{where}: {r['words']} words outside the price, plans and legal (budget {WORDS_MAX[kind]})")
    if r["note"] > NOTE_WORDS_MAX:
        errs.append(f"{where}: the note runs {r['note']} words (budget {NOTE_WORDS_MAX})")
    kv = r.get("kit") or []
    for v in kv[:8]:
        errs.append(f"{where}: not buildable: {v}")
    if len(kv) > 8:
        errs.append(f"{where}: not buildable: {len(kv) - 8} more")


def main(d, measured_path=None):
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
    measured = load_measured(measured_path, errs) if measured_path else None
    kit = load_kit(m)
    names = set()
    for v in vs:
        vid, vdir = v.get("id", "?"), v.get("dir")
        if not vdir:
            errs.append(f"{vid}: no dir")
            continue
        flow = v.get("flow") or m.get("flow") or []
        if flow:
            if flow[-1] != "main":
                errs.append(f"{vid}: flow must end with main (the purchase screen), ends with {flow[-1]}")
            for s in flow:
                if not STATE.match(s):
                    errs.append(f"{vid}: unknown flow screen {s}")
        for s in list(dict.fromkeys(flow + states)):
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
            if kit and "missing" not in kit:
                check_actions(where, s, fr, kit.get("actions") or {}, errs)
            if "visual" not in fr.pw:
                errs.append(f"{where}: no data-pw visual (every screen needs a hero visual)")
            if measured is not None:
                check_measures(where, s, measured.get(rel), errs)
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
    if measured is None:
        warns.append("layout not measured (visual share, word budget): run through studio.sh check")
    if kit is None:
        warns.append("manifest has no kit: buildability is not checked (paywall.md, 'Build target')")
    elif "missing" in kit:
        errs.append(f"kit {kit['missing']} not found in the skill's kits/")
    for w in warns:
        print("WARN", w)
    for e in errs:
        print("FAIL", e)
    nv, ns = len(vs), len(states)
    print(f"{'FAIL' if errs else 'OK'} {nv} paywall variation{'' if nv == 1 else 's'} "
          f"({stage}, {ns} state{'' if ns == 1 else 's'})")
    return 1 if errs else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) in (2, 3) and a[0] == "measure-page":
        sys.exit(measure_page(a[1].rstrip("/"), *a[2:]))
    if len(a) == 3 and a[1] == "--measured":
        sys.exit(main(a[0].rstrip("/"), a[2]))
    if len(a) != 1:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(a[0].rstrip("/")))
