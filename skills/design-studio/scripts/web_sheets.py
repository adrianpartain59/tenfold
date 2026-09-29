#!/usr/bin/env python3
"""Web-mode contact sheets for design-studio.

  web_sheets.py measure <round-dir>   write _measure.html, which loads every page at
                                      phone width and prints their heights as JSON
  web_sheets.py layout <round-dir>    read _measure.out (Chrome --dump-dom of
                                      _measure.html), write the sheet pages, print
                                      "<file> <width> <height>" per sheet on stdout
                                      and "MEASURED k/n" on stderr
"""
import html, json, os, re, sys

PHONE_W, PHONE_H, DESK_W, DESK_H = 390, 844, 1440, 900
MAX_H, FALLBACK_H, PAD, CAP = 9000, 3000, 24, 40
HERO = 0.4
STYLE = ("body{margin:0;padding:%dpx;background:#ECECEF;display:flex;gap:%dpx;align-items:flex-start;"
         "font:600 22px -apple-system,system-ui,sans-serif;color:#1C1C1E}"
         "figure{margin:0}figcaption{height:%dpx;white-space:nowrap}figcaption b{font-weight:800;margin-right:6px}"
         "iframe{border:0;display:block;background:#fff}.slice{overflow:hidden;background:#fff}") % (PAD, PAD, CAP)
# Each phone slice scrolls its own copy of the page to its offset. The last one
# can't scroll past the end, so it is pulled up by however far it fell short.
SLICES = ("<script>addEventListener('load',()=>document.querySelectorAll('iframe[data-y]').forEach(f=>{"
          "try{const w=f.contentWindow,y=+f.dataset.y;w.document.documentElement.style.scrollBehavior='auto';"
          "w.scrollTo(0,y);f.style.marginTop=(-(y-w.scrollY))+'px'}catch(e){}}))</script>")


def load(d):
    m = json.load(open(os.path.join(d, "manifest.json")))
    vs = [v for v in m.get("variations", []) if v.get("file") or v.get("pages")]
    for v in vs:
        v["_pages"] = v.get("pages") or [{"template": "home", "file": v["file"]}]
        v.setdefault("file", v["_pages"][0]["file"])
    return m, vs


def files(m, vs):
    fs = [v["file"] for v in vs]
    if m.get("stage") == "system":
        fs += [p["file"] for v in vs for p in v["_pages"]]
    return list(dict.fromkeys(fs))


def measure(d):
    m, vs = load(d)
    frames = "".join(
        f'<iframe src="{html.escape(f)}" data-f="{html.escape(f)}" width="{PHONE_W}" height="{PHONE_H}"></iframe>'
        for f in files(m, vs))
    script = ("addEventListener('load',()=>setTimeout(()=>{const o={};"
              "document.querySelectorAll('iframe').forEach(f=>{try{const doc=f.contentDocument;"
              "o[f.dataset.f]=Math.max(doc.documentElement.scrollHeight,doc.body?doc.body.scrollHeight:0)}"
              "catch(x){o[f.dataset.f]=0}});"
              "document.getElementById('out').textContent=JSON.stringify(o)},1500));")
    page = f"<!doctype html><meta charset='utf-8'><body>{frames}<pre id='out'></pre><script>{script}</script>"
    open(os.path.join(d, "_measure.html"), "w").write(page)


def heights(d):
    try:
        raw = open(os.path.join(d, "_measure.out"), encoding="utf-8").read()
    except OSError:
        return {}
    mo = re.search(r'<pre id="out">(.*?)</pre>', raw, re.S)
    try:
        return json.loads(html.unescape(mo.group(1))) if mo else {}
    except ValueError:
        return {}


def cell(label, num, inner):
    return f"<figure><figcaption><b>{num}</b> {html.escape(label)}</figcaption>{inner}</figure>"


def phone(f, h):
    """A full-length phone page as a stack of phone-height slices. One tall
    iframe would stretch every vh unit to the page's height and push content
    off the bottom; slices keep the viewport a real phone's."""
    n = -(-h // PHONE_H)
    out = []
    for k in range(n):
        vis = PHONE_H if k < n - 1 else h - (n - 1) * PHONE_H
        out.append(f'<div class="slice" style="height:{vis}px"><iframe src="{html.escape(f)}" data-y="{k * PHONE_H}" '
                   f'style="width:{PHONE_W}px;height:{PHONE_H}px"></iframe></div>')
    return f'<div style="width:{PHONE_W}px">{"".join(out)}</div>'


def write(d, name, body, w, h):
    open(os.path.join(d, name), "w").write(f"<!doctype html><meta charset='utf-8'><style>{STYLE}</style>{body}{SLICES}")
    print(name, w, h)


def layout(d):
    m, vs = load(d)
    hs = heights(d)
    fs = files(m, vs)
    print(f"MEASURED {sum(1 for f in fs if int(hs.get(f) or 0) > 0)}/{len(fs)}", file=sys.stderr)

    def H(f):
        return min(MAX_H, max(844, int(hs.get(f) or 0) or FALLBACK_H))

    # heroes.png: every variation's desktop first screen, five per row
    hw, hh = int(DESK_W * HERO), int(DESK_H * HERO)
    cells = "".join(cell(v.get("name", ""), i + 1,
                         f'<div style="width:{hw}px;height:{hh}px;overflow:hidden;border-radius:10px;'
                         f'box-shadow:0 6px 20px rgba(0,0,0,.12)"><iframe src="{html.escape(v["file"])}" '
                         f'style="width:{DESK_W}px;height:{DESK_H}px;transform:scale({HERO});transform-origin:0 0">'
                         f"</iframe></div>")
                    for i, v in enumerate(vs))
    cols, rows = min(5, len(vs)), (len(vs) + 4) // 5
    body = f'<div style="display:grid;grid-template-columns:repeat({cols},{hw}px);gap:{PAD}px">{cells}</div>'
    write(d, "_heroes.html", body, PAD * 2 + cols * hw + (cols - 1) * PAD, PAD * 2 + rows * (CAP + hh) + (rows - 1) * PAD)

    # sheet-N.png: five variations as full-length phone pages
    for k in range(0, len(vs), 5):
        chunk = vs[k:k + 5]
        body = "".join(cell(v.get("name", ""), k + i + 1, phone(v["file"], H(v["file"]))) for i, v in enumerate(chunk))
        write(d, f"_sheet-{k // 5 + 1}.html", body,
              PAD * 2 + len(chunk) * PHONE_W + (len(chunk) - 1) * PAD, PAD * 2 + CAP + max(H(v["file"]) for v in chunk))

    # pages-<vid>.png (system stage): every template of a variation at phone width
    if m.get("stage") == "system":
        labels = {t.get("id"): t.get("label") or t.get("id") for t in m.get("templates", [])}
        for v in vs:
            ps = v["_pages"]
            body = "".join(cell(p.get("label") or labels.get(p.get("template"), p.get("template") or ""), i + 1,
                                phone(p["file"], H(p["file"]))) for i, p in enumerate(ps))
            write(d, f"_pages-{v['id']}.html", body,
                  PAD * 2 + len(ps) * PHONE_W + (len(ps) - 1) * PAD, PAD * 2 + CAP + max(H(p["file"]) for p in ps))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("measure", "layout"):
        print(__doc__)
        sys.exit(2)
    (measure if sys.argv[1] == "measure" else layout)(sys.argv[2].rstrip("/"))
