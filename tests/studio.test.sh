#!/usr/bin/env bash
# Tests for studio.sh. Run from the repo root: bash tests/studio.test.sh
# Uses a throwaway DESIGN_STUDIO_ROOT and port, never ~/design-studio.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
STUDIO="$REPO/skills/design-studio/scripts/studio.sh"
ASSETS="$REPO/skills/design-studio/assets"
export DESIGN_STUDIO_ROOT="$(mktemp -d)"
export DESIGN_STUDIO_PORT="${TEST_PORT:-4599}"
export DESIGN_STUDIO_NO_OPEN=1
pass=0; fail=0
ok()  { pass=$((pass+1)); echo "  ok   $1"; }
bad() { fail=$((fail+1)); echo "  FAIL $1"; if [ -n "${2:-}" ]; then printf '%s\n' "$2" | sed 's/^/       /'; fi; }
cleanup() {
  local pid; pid="$(lsof -tiTCP:"$DESIGN_STUDIO_PORT" -sTCP:LISTEN 2>/dev/null || true)"
  [ -n "$pid" ] && kill $pid 2>/dev/null
  rm -rf "$DESIGN_STUDIO_ROOT"
}
trap cleanup EXIT
# stage <fixture> <project> <topic>: copy a fixture topic into the test root, echo its path
stage() { mkdir -p "$DESIGN_STUDIO_ROOT/$2"; cp -R "$HERE/fixtures/$1" "$DESIGN_STUDIO_ROOT/$2/$3"; echo "$DESIGN_STUDIO_ROOT/$2/$3"; }

echo "mobile mode (must match 1.0.0)"
out="$(bash "$STUDIO" new demo phone 2>&1)"
rd="$DESIGN_STUDIO_ROOT/demo/phone/r1"
cmp -s "$rd/index.html" "$ASSETS/gallery.html" && ok "new copies gallery.html" || bad "new copies gallery.html" "$out"
cmp -s "$rd/screen.css" "$ASSETS/screen.css" && ok "new copies screen.css" || bad "new copies screen.css"
[ ! -e "$rd/web.css" ] && ok "mobile round has no web.css" || bad "mobile round has no web.css"
grep -q "^SURFACE" <<<"$out" && bad "mobile new prints no SURFACE line" "$out" || ok "mobile new prints no SURFACE line"
t="$(stage mobile-smoke demo mcheck)"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
[ "$out" = "OK 2 variations" ] && ok "mobile check output unchanged" || bad "mobile check output unchanged" "$out"

echo "web mode: new --web"
out="$(bash "$STUDIO" new demo web --web 2>&1)"
rd="$DESIGN_STUDIO_ROOT/demo/web/r1"
cmp -s "$rd/index.html" "$ASSETS/gallery-web.html" && ok "new --web copies gallery-web.html" || bad "new --web copies gallery-web.html" "$out"
cmp -s "$rd/web.css" "$ASSETS/web.css" && ok "new --web copies web.css" || bad "new --web copies web.css"
[ ! -e "$rd/screen.css" ] && ok "web round has no screen.css" || bad "web round has no screen.css"
grep -qx "SURFACE web" <<<"$out" && ok "new --web prints SURFACE web" || bad "new --web prints SURFACE web" "$out"
out="$(bash "$STUDIO" new demo web --web 2>&1)"
[ -f "$DESIGN_STUDIO_ROOT/demo/web/r2/index.html" ] && grep -q "^PREV_ROUND_DIR" <<<"$out" && ok "second web round is r2" || bad "second web round is r2" "$out"

echo "web mode: check"
t="$(stage web-smoke demo wcheck)"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK 2 web variations (directions)" ] && ok "check passes a directions round" || bad "check passes a directions round" "$out"
out="$(bash "$STUDIO" check "$t/r2" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK 1 web variation (system)" ] && ok "check passes a system round" || bad "check passes a system round" "$out"

perl -pi -e 's|<h2>Plans that adapt</h2>|<h2>Plans that adapt</h2><a href="pricing.html">Pricing</a>|' "$t/r1/v01/index.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"; st=$?
[ $st -ne 0 ] && grep -q "FAIL v01/v01/index.html: broken link pricing.html" <<<"$out" && ok "check fails a broken page link" || bad "check fails a broken page link" "$out"

perl -ni -e 'print unless /href="tokens.css"/' "$t/r1/v02/index.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
grep -q "FAIL v02/v02/index.html: does not link a direction tokens.css" <<<"$out" && ok "check fails a page without its direction tokens" || bad "check fails a page without its direction tokens" "$out"

python3 - "$t/r2/manifest.json" <<'PY'
import json, sys
p = sys.argv[1]; m = json.load(open(p))
m["templates"].append({"id": "reviews", "label": "Reviews"})
json.dump(m, open(p, "w"))
PY
out="$(bash "$STUDIO" check "$t/r2" 2>&1)"
grep -q "FAIL v01: missing templates reviews" <<<"$out" && ok "check fails a system round missing a template" || bad "check fails a system round missing a template" "$out"

perl -pi -e 's|href="features.html">Features|href="feature.html">Features|' "$t/r2/v01/chrome.js"
out="$(bash "$STUDIO" check "$t/r2" 2>&1)"
grep -q "FAIL v01/chrome.js: broken link feature.html" <<<"$out" && ok "check follows links in chrome.js" || bad "check follows links in chrome.js" "$out"

echo "web mode: sheets"
if bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO" >/dev/null 2>&1; then
  t="$(stage web-smoke demo wsheets)"
  out="$(bash "$STUDIO" sheets "$t/r1" 2>&1)"
  [ -s "$t/r1/heroes.png" ] && ok "sheets writes heroes.png" || bad "sheets writes heroes.png" "$out"
  [ -s "$t/r1/sheet-1.png" ] && ok "sheets writes sheet-1.png" || bad "sheets writes sheet-1.png" "$out"
  grep -q "MEASURED 2/2" <<<"$out" && ok "sheets measured every page height" || bad "sheets measured every page height" "$out"
  h="$(python3 -c 'import struct,sys; print(struct.unpack(">II", open(sys.argv[1],"rb").read(24)[16:24])[1])' "$t/r1/sheet-1.png" 2>/dev/null || echo 0)"
  [ "$h" -gt 1500 ] && ok "sheet-1 is full length ($h px)" || bad "sheet-1 is full length" "height $h"
  out="$(bash "$STUDIO" sheets "$t/r2" 2>&1)"
  [ -s "$t/r2/pages-v01.png" ] && ok "system sheets write pages-v01.png" || bad "system sheets write pages-v01.png" "$out"
  # A single page-tall iframe stretches vh units and pushes content off the bottom;
  # phone sheets must be stacks of 844 px slices.
  sl="$(cd "$REPO/skills/design-studio/scripts" && python3 -B -c 'import re, web_sheets as w; h = w.phone("p.html", 2000); print(len(re.findall(r"<iframe", h)), sorted(set(re.findall(r"height:(\d+)px\"><iframe", h))))')"
  [ "$sl" = "3 ['312', '844']" ] && ok "phone sheets render as 844 px slices" || bad "phone sheets render as 844 px slices" "$sl"
  ls "$t/r1" | grep -q '^_' && bad "sheets cleans up its wrapper files" "$(ls "$t/r1")" || ok "sheets cleans up its wrapper files"
else
  echo "  skip sheets (no Chrome/Chromium)"
fi

echo "paywall references lint"
LINT="$REPO/tests/refs_lint.py"
out="$(python3 "$LINT" "$HERE/fixtures/refs-good" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK refs (1 sources, 14 archetypes)" ] && ok "lint passes good refs" || bad "lint passes good refs" "$out"
out="$(python3 "$LINT" "$HERE/fixtures/refs-bad" 2>&1)"; st=$?
[ $st -ne 0 ] && ok "lint fails bad refs" || bad "lint fails bad refs" "$out"
grep -q "FAIL playbook:4: a result number with no \[S#\]" <<<"$out" && ok "lint flags an uncited number" || bad "lint flags an uncited number" "$out"
grep -q "FAIL playbook:5: \[S7\] is not in the Sources table" <<<"$out" && ok "lint flags an undefined source" || bad "lint flags an undefined source" "$out"
grep -q "FAIL playbook:10: S1 has no URL" <<<"$out" && ok "lint flags a source with no URL" || bad "lint flags a source with no URL" "$out"
grep -q "FAIL playbook:10: S1 date 'March 2025' is not YYYY-MM\[-DD\]" <<<"$out" && ok "lint flags a bad date" || bad "lint flags a bad date" "$out"
grep -q "FAIL playbook:10: S1 strength 'vibes'" <<<"$out" && ok "lint flags a bad strength" || bad "lint flags a bad strength" "$out"
grep -q "FAIL archetypes: Trial timeline is missing Wins when, Loses when, Axes, Hazards, Seen in" <<<"$out" && ok "lint flags missing archetype fields" || bad "lint flags missing archetype fields" "$out"
grep -q "FAIL archetypes: 1 entries, need at least 14" <<<"$out" && ok "lint wants 14 archetypes" || bad "lint wants 14 archetypes" "$out"

# --- new tests above this line ---
echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
