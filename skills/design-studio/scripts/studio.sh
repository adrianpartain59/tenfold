#!/usr/bin/env bash
# design-studio round manager + localhost server.
#
#   studio.sh new <project> <topic>   → create the next round dir, copy the gallery,
#                                        print ROUND_DIR and the URL
#   studio.sh serve                   → make sure the server is up (idempotent)
#   studio.sh url <path-under-root>   → print localhost (+ LAN) URLs for a path
#   studio.sh check <round-dir>       → validate manifest + files before sending the link;
#                                        on OK it also opens the round (see `open`)
#   studio.sh open <round-dir>        → open the round's gallery in the user's default
#                                        browser. Set DESIGN_STUDIO_NO_OPEN=1 to skip the
#                                        automatic open after `check`.
#   studio.sh icons <topic-dir>       → download the Feather icon sprite (MIT) into the topic
#                                        as icons.svg + icons.txt, for apps with no icon export
#   studio.sh sheets <round-dir>      → contact sheets: sheet-1.png / sheet-2.png, five
#                                        variations side by side (needs Chrome or Chromium)
#
# Everything lives under $DESIGN_STUDIO_ROOT (default ~/design-studio), served at
# http://localhost:$DESIGN_STUDIO_PORT (default 4545). One server serves every
# project and round, so old links keep working. It binds to 127.0.0.1; set
# DESIGN_STUDIO_BIND=0.0.0.0 to open rounds from a phone on the same Wi-Fi
# (anyone on that network can then see them).
set -euo pipefail

ROOT="${DESIGN_STUDIO_ROOT:-$HOME/design-studio}"
PORT="${DESIGN_STUDIO_PORT:-4545}"
BIND="${DESIGN_STUDIO_BIND:-127.0.0.1}"   # 0.0.0.0 lets a phone on the same Wi-Fi open it
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="$ROOT/.server.log"

slug() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g'; }

lan_ip() {
  ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null ||
    { hostname -I 2>/dev/null | awk '{print $1}'; } || true
}

serving() { curl -s -o /dev/null -m 2 "http://127.0.0.1:$PORT/.studio-ok" ; }

serve() {
  mkdir -p "$ROOT"
  [ -f "$ROOT/.studio-ok" ] || echo ok > "$ROOT/.studio-ok"
  if serving; then echo "SERVER up on :$PORT"; return 0; fi
  if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "PORT $PORT is taken by something else:" >&2
    lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >&2
    echo "Set DESIGN_STUDIO_PORT to a free port and retry." >&2
    exit 3
  fi
  nohup python3 -m http.server "$PORT" --bind "$BIND" --directory "$ROOT" >"$LOG" 2>&1 &
  disown || true
  for _ in 1 2 3 4 5 6 7 8 9 10; do serving && { echo "SERVER started on :$PORT (pid $!)"; return 0; }; sleep 0.3; done
  echo "SERVER failed to start; log:" >&2; tail -20 "$LOG" >&2; exit 4
}

url() {
  local p="${1#/}"
  echo "URL http://localhost:$PORT/$p"
  local ip; ip="$(lan_ip)"
  if [ -n "$ip" ] && [ "$BIND" = "0.0.0.0" ]; then echo "LAN http://$ip:$PORT/$p"; fi
}

new_round() {
  local project topic dir n
  project="$(slug "$1")"; topic="$(slug "$2")"
  dir="$ROOT/$project/$topic"
  mkdir -p "$dir"
  n=1; while [ -d "$dir/r$n" ]; do n=$((n+1)); done
  mkdir -p "$dir/r$n"
  cp "$SKILL_DIR/assets/gallery.html" "$dir/r$n/index.html"
  cp "$SKILL_DIR/assets/screen.css" "$dir/r$n/screen.css"
  # Tokens live once per topic; rounds link ../tokens.css so every round matches.
  serve >/dev/null
  echo "ROUND r$n"
  echo "ROUND_DIR $dir/r$n"
  echo "TOPIC_DIR $dir"
  [ "$n" -gt 1 ] && echo "PREV_ROUND_DIR $dir/r$((n-1))"
  url "$project/$topic/r$n/"
}

check() {
  local d="${1%/}"
  python3 - "$d" <<'PY'
import json, os, sys, re
d = sys.argv[1]
errs, warns = [], []
mf = os.path.join(d, "manifest.json")
try:
    m = json.load(open(mf))
except Exception as e:
    print(f"FAIL manifest.json unreadable: {e}"); sys.exit(1)
vs = m.get("variations", [])
if len(vs) < 2: errs.append(f"only {len(vs)} variations")
names = set()
for v in vs:
    f = v.get("file")
    if not f or not os.path.exists(os.path.join(d, f)):
        errs.append(f"{v.get('id')}: missing file {f}")
        continue
    html = open(os.path.join(d, f)).read()
    if "tokens.css" not in html: warns.append(f"{v['id']}: does not link tokens.css")
    if "screen.css" not in html: warns.append(f"{v['id']}: does not link screen.css")
    if re.search(r"lorem ipsum", html, re.I): errs.append(f"{v['id']}: lorem ipsum")
    if not v.get("idea"): warns.append(f"{v['id']}: no one-line idea")
    n = (v.get("name") or "").strip().lower()
    if n in names: errs.append(f"duplicate name {n}")
    names.add(n)
for k in ("agentPick", "predictedPick"):
    if k not in m: warns.append(f"manifest has no {k}")
if not os.path.exists(os.path.join(d, "..", "tokens.css")): warns.append("no ../tokens.css for this topic")
for w in warns: print("WARN", w)
for e in errs: print("FAIL", e)
print(f"{'FAIL' if errs else 'OK'} {len(vs)} variations")
sys.exit(1 if errs else 0)
PY
}

open_round() {
  serve >/dev/null
  local d; d="$(cd "$1" && pwd)"
  local rel="${d#"$ROOT"/}"
  local u="http://localhost:$PORT/$rel/"
  if command -v open >/dev/null 2>&1; then open "$u"; echo "OPENED $u"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$u" >/dev/null 2>&1 & echo "OPENED $u"
  else echo "OPEN manually: $u"; fi
}

icons() {
  local d="${1%/}"
  [ -d "$d" ] || { echo "no such topic dir: $d" >&2; exit 2; }
  if [ -s "$d/icons.svg" ]; then echo "ICONS already in $d/icons.svg"; else
    curl -fsSL "https://cdn.jsdelivr.net/npm/feather-icons@4/dist/feather-sprite.svg" -o "$d/icons.svg" \
      || { echo "download failed; write inline SVG icons instead" >&2; exit 5; }
    echo "ICONS $d/icons.svg (Feather, MIT; use <svg class=\"ic feather\">)"
  fi
  grep -o 'symbol id="[^"]*"' "$d/icons.svg" | sed 's/symbol id="//; s/"$//' > "$d/icons.txt"
  echo "IDS $(wc -l < "$d/icons.txt" | tr -d ' ') in $d/icons.txt"
}

chrome_bin() {
  local c
  for c in "${CHROME:-}" "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium" google-chrome chromium chromium-browser; do
    [ -n "$c" ] || continue
    if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then echo "$c"; return 0; fi
  done
  return 1
}

sheets() {
  serve >/dev/null
  local d; d="$(cd "$1" && pwd)"
  local rel="${d#"$ROOT"/}"
  local chrome; chrome="$(chrome_bin)" || { echo "no Chrome/Chromium found (set CHROME=/path)" >&2; exit 6; }
  python3 - "$d" <<'PY'
import json, os, sys, html
d = sys.argv[1]
m = json.load(open(os.path.join(d, "manifest.json")))
vs = [v for v in m.get("variations", []) if v.get("file")]
for k in range(0, len(vs), 5):
    cells = "".join(
        f'<figure><figcaption><b>{k+i+1}</b> {html.escape(v.get("name",""))}</figcaption>'
        f'<iframe src="{html.escape(v["file"])}?theme=light"></iframe></figure>'
        for i, v in enumerate(vs[k:k+5]))
    page = ('<!doctype html><meta charset="utf-8"><style>'
            'body{margin:0;padding:24px;background:#ECECEF;display:flex;gap:24px;'
            'font:600 22px -apple-system,system-ui,sans-serif;color:#1C1C1E}'
            'figure{margin:0}figcaption{height:40px}figcaption b{font-weight:800;margin-right:6px}'
            'iframe{width:393px;height:852px;border:0;border-radius:44px;background:#fff;'
            'box-shadow:0 10px 30px rgba(0,0,0,.12);display:block}</style>' + cells)
    open(os.path.join(d, f"_sheet-{k//5+1}.html"), "w").write(page)
PY
  local f n
  for f in "$d"/_sheet-*.html; do
    n="$(basename "$f" .html)"; n="${n#_}"
    "$chrome" --headless=new --hide-scrollbars --disable-gpu --force-device-scale-factor=1 \
      --window-size=2133,964 --virtual-time-budget=6000 \
      --screenshot="$d/$n.png" "http://127.0.0.1:$PORT/$rel/$(basename "$f")" >/dev/null 2>&1 || true
    rm -f "$f"
    if [ -s "$d/$n.png" ]; then echo "SHEET $d/$n.png"; else echo "SHEET failed: $n" >&2; fi
  done
}

cmd="${1:-}"; shift || true
case "$cmd" in
  new)   [ $# -ge 2 ] || { echo "usage: studio.sh new <project> <topic>" >&2; exit 2; }; new_round "$1" "$2" ;;
  serve) serve; url "" ;;
  url)   url "${1:-}" ;;
  check) check "$1"; [ -n "${DESIGN_STUDIO_NO_OPEN:-}" ] || open_round "$1" ;;
  open)  open_round "$1" ;;
  icons) [ $# -ge 1 ] || { echo "usage: studio.sh icons <topic-dir>" >&2; exit 2; }; icons "$1" ;;
  sheets) [ $# -ge 1 ] || { echo "usage: studio.sh sheets <round-dir>" >&2; exit 2; }; sheets "$1" ;;
  *) sed -n '2,23p' "$0"; exit 2 ;;
esac
