#!/usr/bin/env python3
"""Write contact-sheet wrapper pages for a glow-up round.

  glowup_sheets.py <round-dir>

_sheet-before.html (the audit's before screens), then one _sheet-<id>.html
per direction with its four key screens in a row, or in the system stage one
_sheet-<id>-<n>.html per four routes. studio.sh screenshots each wrapper to
sheet-*.png and deletes it. Prints "SHEETS <n>".
"""
import html, json, os, sys

CSS = ("body{margin:0;padding:24px;background:#ECECEF;display:flex;gap:24px;align-items:flex-start;"
       "font:600 22px -apple-system,system-ui,sans-serif;color:#1C1C1E}"
       ".lbl{width:200px;flex:none;font-size:15px;color:#6B6B73}.lbl b{display:block;font-size:28px;font-weight:800;color:#1C1C1E}"
       "figure{margin:0}figcaption{height:40px;font-size:16px;color:#6B6B73}"
       "iframe,img{width:393px;height:852px;border:0;border-radius:44px;background:#fff;"
       "box-shadow:0 10px 30px rgba(0,0,0,.12);display:block;object-fit:cover;object-position:top}")
IMG = (".png", ".jpg", ".jpeg", ".webp")
# Web surface: four 1440 x 900 screens at 0.45 scale in a 2 x 2 grid (fits the 2133 x 964 shot).
WEB_CSS = (".grid{display:grid;grid-template-columns:repeat(2,648px);gap:24px}"
           ".d{width:648px;height:405px;overflow:hidden;border-radius:10px;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.12)}"
           ".d iframe,.d img{width:1440px;height:900px;border:0;border-radius:0;box-shadow:none;transform:scale(.45);transform-origin:0 0;object-fit:cover;object-position:top}"
           "figcaption{height:30px}")


WEB = False


def cell(src, cap):
    s = html.escape(src)
    tag = f'<img src="{s}">' if src.lower().endswith(IMG) else f'<iframe src="{s}"></iframe>'
    if WEB:
        tag = f'<div class="d">{tag}</div>'
    return f"<figure><figcaption>{html.escape(cap)}</figcaption>{tag}</figure>"


def page(label, sub, cells):
    body = f'<div class="grid">{"".join(cells)}</div>' if WEB else "".join(cells)
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}{WEB_CSS if WEB else ""}</style>'
            f'<div class="lbl"><b>{html.escape(label)}</b>{html.escape(sub)}</div>' + body)


def main(d):
    global WEB
    m = json.load(open(os.path.join(d, "manifest.json"), encoding="utf-8"))
    WEB = m.get("surface") == "web"
    screens = m.get("screens", [])
    out = []
    b = m.get("before") or {}
    shots = [s for s in screens if b.get(s["id"])]
    if shots:
        out.append(("before", page("Before", b.get("headline", ""), [cell(b[s["id"]], s["label"]) for s in shots])))
    stage = m.get("stage")
    for i, v in enumerate(m.get("variations", []), 1):
        vd = v.get("dir", v["id"])
        if stage == "system":
            routes = m.get("routes", [])
            for k in range(0, len(routes), 4):
                group = routes[k:k + 4]
                out.append((f"{v['id']}-{k // 4 + 1}", page(v.get("name", ""), f"routes {k + 1} to {k + len(group)}",
                                                            [cell(f"{vd}/routes/{r['id']}.html", r.get("label", r["id"])) for r in group])))
        elif stage in ("directions", "converge"):
            out.append((v["id"], page(f"{i} {v.get('name', '')}", v.get("idea", ""),
                                      [cell(f"{vd}/{s['id']}.html", s["label"]) for s in screens])))
    for name, body in out:
        with open(os.path.join(d, f"_sheet-{name}.html"), "w", encoding="utf-8") as f:
            f.write(body)
    print(f"SHEETS {len(out)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
