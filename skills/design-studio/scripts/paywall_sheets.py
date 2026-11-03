#!/usr/bin/env python3
"""Write contact-sheet wrapper pages for a paywall round, one set per state.

  paywall_sheets.py <round-dir>

Writes _sheet-<state>-<k>.html (five variations each, captioned with number,
name and, in ab rounds, the variable) and, when the round has flows,
_sheet-flow-<k>.html (four variations each, every screen of the flow in a row
at half size). studio.sh screenshots each to sheet-*.png and deletes the wrapper.
"""
import html, json, os, sys

STYLE = ("body{margin:0;padding:24px;background:#ECECEF;display:flex;gap:24px;"
         "font:600 22px -apple-system,system-ui,sans-serif;color:#1C1C1E}"
         "figure{margin:0}figcaption{height:40px;white-space:nowrap;overflow:hidden;max-width:393px}"
         "figcaption b{font-weight:800;margin-right:6px}figcaption i{font-style:normal;color:#6B6B73}"
         "iframe{width:393px;height:852px;border:0;border-radius:44px;background:#fff;"
         "box-shadow:0 10px 30px rgba(0,0,0,.12);display:block}")


FLOW_STYLE = ("body{margin:0;padding:20px 24px;background:#ECECEF;display:grid;grid-template-columns:1fr 1fr;gap:18px 28px;"
              "font:600 18px -apple-system,system-ui,sans-serif;color:#1C1C1E;align-content:start}"
              "section{display:grid;gap:8px}h2{margin:0;font-size:18px;white-space:nowrap;overflow:hidden}h2 b{font-weight:800;margin-right:6px}"
              ".row{display:flex;gap:10px;align-items:flex-start}.cell{display:grid;gap:4px;justify-items:center}"
              ".cell span{font-size:11px;color:#6B6B73;text-transform:uppercase;letter-spacing:.05em}"
              ".ph{width:197px;height:426px;border-radius:24px;overflow:hidden;background:#fff;box-shadow:0 6px 18px rgba(0,0,0,.12)}"
              "iframe{width:393px;height:852px;border:0;transform:scale(.5);transform-origin:0 0;display:block}")


def flow_sheets(d, m, vs):
    flows = [(i, v, v.get("flow") or m.get("flow")) for i, v in enumerate(vs)]
    flows = [x for x in flows if x[2]]
    for k in range(0, len(flows), 4):
        secs = []
        for i, v, flow in flows[k:k + 4]:
            cells = "".join(
                f'<div class="cell"><div class="ph"><iframe src="{html.escape(v["dir"])}/{html.escape(s)}.html?theme=light"></iframe></div>'
                f'<span>{j + 1}. {html.escape("plans" if s == "main" else s)}</span></div>' for j, s in enumerate(flow))
            secs.append(f'<section><h2><b>{i + 1}</b>{html.escape(v.get("name", ""))}</h2><div class="row">{cells}</div></section>')
        name = f"_sheet-flow-{k // 4 + 1}.html"
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><meta charset="utf-8"><style>{FLOW_STYLE}</style>' + "".join(secs))
        print(name)


def main(d):
    m = json.load(open(os.path.join(d, "manifest.json")))
    vs = [v for v in m.get("variations", []) if v.get("dir")]
    flow_sheets(d, m, vs)
    for state in m.get("states") or ["main"]:
        for k in range(0, len(vs), 5):
            cells = []
            for i, v in enumerate(vs[k:k + 5]):
                extra = f" · {v['variable']}" if v.get("variable") else (" · control" if v.get("control") else "")
                cells.append(
                    f'<figure><figcaption><b>{k + i + 1}</b> {html.escape(v.get("name", ""))}'
                    f'<i>{html.escape(extra)} · {html.escape(state)}</i></figcaption>'
                    f'<iframe src="{html.escape(v["dir"])}/{html.escape(state)}.html?theme=light"></iframe></figure>')
            name = f"_sheet-{state}-{k // 5 + 1}.html"
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write(f'<!doctype html><meta charset="utf-8"><style>{STYLE}</style>' + "".join(cells))
            print(name)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1].rstrip("/")))
