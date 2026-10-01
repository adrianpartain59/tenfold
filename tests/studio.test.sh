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
out="$(python3 "$LINT" "$REPO/skills/design-studio/references" 2>&1)"; st=$?
[ $st -eq 0 ] && ok "shipped paywall references pass the lint" || bad "shipped paywall references pass the lint" "$out"

echo "paywall mode: new --paywall"
out="$(bash "$STUDIO" new demo pay --paywall 2>&1)"
rd="$DESIGN_STUDIO_ROOT/demo/pay/r1"
cmp -s "$rd/paywall.css" "$ASSETS/paywall.css" && ok "new --paywall copies paywall.css" || bad "new --paywall copies paywall.css" "$out"
cmp -s "$rd/screen.css" "$ASSETS/screen.css" && ok "new --paywall copies screen.css" || bad "new --paywall copies screen.css"
grep -qx "SURFACE paywall" <<<"$out" && ok "new --paywall prints SURFACE paywall" || bad "new --paywall prints SURFACE paywall" "$out"
[ ! -e "$rd/web.css" ] && ok "paywall round has no web.css" || bad "paywall round has no web.css"

echo "paywall mode: check"
pfresh() { stage paywall-smoke demo "p$RANDOM$RANDOM"; }
t="$(pfresh)"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK 2 paywall variations (concept, 3 states)" ] && ok "check passes a concept round" || bad "check passes a concept round" "$out"
out="$(bash "$STUDIO" check "$t/r2" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK 2 paywall variations (ab, 1 state)" ] && ok "check passes an ab round" || bad "check passes an ab round" "$out"

t="$(pfresh)"; rm "$t/r1/v02/exit.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"; st=$?
[ $st -ne 0 ] && grep -q "FAIL v02: missing state exit (v02/exit.html)" <<<"$out" && ok "check fails a missing state" || bad "check fails a missing state" "$out"

t="$(pfresh)"; perl -ni -e 'print unless /data-pw="renewal"/' "$t/r1/v01/alt-plan.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
grep -q "FAIL v01/alt-plan: missing data-pw renewal" <<<"$out" && ok "check fails a missing marker" || bad "check fails a missing marker" "$out"

t="$(pfresh)"; perl -pi -e 's|(<button class="pw-cta")|<button data-pw="cta">Also buy</button>$1|' "$t/r1/v01/main.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
grep -q "FAIL v01/main: 2 data-pw cta (need exactly 1)" <<<"$out" && ok "check fails two CTAs" || bad "check fails two CTAs" "$out"

t="$(pfresh)"; perl -ni -e 'print unless /data-pw="trial-terms"/' "$t/r1/v02/main.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
grep -q "FAIL v02/main: missing data-pw trial-terms" <<<"$out" && ok "check wants trial terms when trial is on" || bad "check wants trial terms when trial is on" "$out"

t="$(pfresh)"; perl -pi -e 's/two months/two weeks/' "$t/r1/v01/main.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
grep -q "FAIL v01/main: proof P1 text not in context.md" <<<"$out" && ok "check fails invented proof" || bad "check fails invented proof" "$out"

t="$(pfresh)"; perl -pi -e 's/data-src="P2"/data-src="P9"/' "$t/r1/v02/main.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
grep -q "FAIL v02/main: proof P9 not in context.md" <<<"$out" && ok "check fails an unknown proof id" || bad "check fails an unknown proof id" "$out"

t="$(pfresh)"
python3 - "$t/r2/manifest.json" <<'PY'
import json, sys
p = sys.argv[1]; m = json.load(open(p)); del m["variations"][1]["variable"]; json.dump(m, open(p, "w"))
PY
out="$(bash "$STUDIO" check "$t/r2" 2>&1)"
grep -q "FAIL v02: ab variant has no variable" <<<"$out" && ok "check wants a variable per ab variant" || bad "check wants a variable per ab variant" "$out"

t="$(pfresh)"
python3 - "$t/r2/manifest.json" <<'PY'
import json, sys
p = sys.argv[1]; m = json.load(open(p)); del m["variations"][0]["control"]; json.dump(m, open(p, "w"))
PY
out="$(bash "$STUDIO" check "$t/r2" 2>&1)"
grep -q "FAIL ab round needs exactly one control, has 0" <<<"$out" && ok "check wants one control" || bad "check wants one control" "$out"

echo "paywall mode: gallery"
out="$(bash "$STUDIO" new demo pay2 --paywall 2>&1)"
cmp -s "$DESIGN_STUDIO_ROOT/demo/pay2/r1/index.html" "$ASSETS/gallery-paywall.html" && ok "new --paywall copies gallery-paywall.html" || bad "new --paywall copies gallery-paywall.html" "$out"
if bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO" >/dev/null 2>&1; then
  CHROME_BIN="$(bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO")"
  t="$(stage paywall-smoke demo pgal)"
  cp "$ASSETS/gallery-paywall.html" "$t/r1/index.html"; cp "$ASSETS/gallery-paywall.html" "$t/r2/index.html"
  bash "$STUDIO" serve >/dev/null
  dom="$("$CHROME_BIN" --headless=new --disable-gpu --virtual-time-budget=5000 --dump-dom "http://127.0.0.1:$DESIGN_STUDIO_PORT/demo/pgal/r1/index.html?state=exit" 2>/dev/null)"
  grep -q 'src="v01/exit.html' <<<"$dom" && ok "gallery ?state=exit frames exit.html" || bad "gallery ?state=exit frames exit.html" "$(grep -o 'src="[^"]*"' <<<"$dom" | head -5)"
  grep -q 'data-v="alt-plan"' <<<"$dom" && ok "gallery renders a state switch" || bad "gallery renders a state switch"
  dom="$("$CHROME_BIN" --headless=new --disable-gpu --virtual-time-budget=5000 --dump-dom "http://127.0.0.1:$DESIGN_STUDIO_PORT/demo/pgal/r2/index.html" 2>/dev/null)"
  grep -q 'class="chip ctl">Control<' <<<"$dom" && grep -q 'Tests: CTA copy' <<<"$dom" && ok "gallery labels control and variable" || bad "gallery labels control and variable"
else
  echo "  skip gallery DOM tests (no Chrome/Chromium)"
fi

echo "paywall mode: sheets"
if bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO" >/dev/null 2>&1; then
  t="$(stage paywall-smoke demo psheets)"
  cp "$ASSETS/screen.css" "$ASSETS/paywall.css" "$t/r1/"
  out="$(bash "$STUDIO" sheets "$t/r1" 2>&1)"
  for s in main alt-plan exit; do
    [ -s "$t/r1/sheet-$s-1.png" ] && ok "sheets writes sheet-$s-1.png" || bad "sheets writes sheet-$s-1.png" "$out"
  done
  ls "$t/r1" | grep -q '^_' && bad "paywall sheets clean up wrappers" "$(ls "$t/r1")" || ok "paywall sheets clean up wrappers"
  t="$(stage mobile-smoke demo msheets)"
  out="$(bash "$STUDIO" sheets "$t/r1" 2>&1)"
  [ -s "$t/r1/sheet-1.png" ] && ok "mobile sheets still write sheet-1.png" || bad "mobile sheets still write sheet-1.png" "$out"
else
  echo "  skip paywall sheets (no Chrome/Chromium)"
fi

echo "paywall mode: docs"
SK="$REPO/skills/design-studio"
grep -q "paywall" <(sed -n '1,6p' "$SK/SKILL.md") && ok "SKILL.md description triggers on paywalls" || bad "SKILL.md description triggers on paywalls"
grep -q "^## Paywall mode" "$SK/SKILL.md" && ok "SKILL.md has a Paywall mode section" || bad "SKILL.md has a Paywall mode section"
for f in paywall.md paywall-craft.md paywall-playbook.md paywall-archetypes.md; do
  grep -q "references/$f\|\`$f\`" "$SK/SKILL.md" "$SK/references/paywall.md" && ok "$f is referenced" || bad "$f is referenced"
done
grep -q '"version": "1.3.0"' "$REPO/.claude-plugin/plugin.json" && grep -q '"version": "1.3.0"' "$REPO/.claude-plugin/marketplace.json" && ok "version is 1.3.0" || bad "version is 1.3.0"
grep -q "^## 1.2.0" "$REPO/CHANGELOG.md" && ok "CHANGELOG has 1.2.0" || bad "CHANGELOG has 1.2.0"

echo "paywall mode: check (void-tag proof holes)"
t="$(pfresh)"
perl -pi -e 's|(<blockquote class="pw-quote" data-pw="proof" data-src="P1">.*</blockquote>)|$1\n  <img data-pw="proof" data-src="P9" alt="5 stars 99,000 ratings">|' "$t/r1/v01/main.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"; st=$?
[ $st -ne 0 ] && grep -q "FAIL v01/main: proof P9 not in context.md" <<<"$out" && ok "check fails an img proof with an unknown data-src" || bad "check fails an img proof with an unknown data-src" "$out"

t="$(pfresh)"
perl -pi -e 's|(<blockquote class="pw-quote" data-pw="proof" data-src="P1">.*</blockquote>)|$1\n  <img data-pw="proof" data-src="P2" alt="Never happier with an app">|' "$t/r1/v01/main.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"; st=$?
[ $st -ne 0 ] && grep -q "FAIL v01/main: proof P2 text not in context.md" <<<"$out" && ok "check fails an img proof with alt text not in context.md" || bad "check fails an img proof with alt text not in context.md" "$out"

t="$(pfresh)"
perl -pi -e 's|(<blockquote class="pw-quote" data-pw="proof" data-src="P1">.*</blockquote>)|$1\n  <img data-pw="proof" data-src="P2" alt="★★★★★">|' "$t/r1/v01/main.html"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"; st=$?
[ $st -ne 0 ] && grep -q "FAIL v01/main: proof P2 has no checkable text (use alt or visible text)" <<<"$out" && ok "check fails a stars-only proof with no checkable text" || bad "check fails a stars-only proof with no checkable text" "$out"

t="$(pfresh)"; perl -pi -e 's/^## Proof$/## Proof (fixture reviews)/' "$t/context.md"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK 2 paywall variations (concept, 3 states)" ] && ok "check accepts a Proof heading with a suffix" || bad "check accepts a Proof heading with a suffix" "$out"

echo "glow-up: python units"
out="$(python3 "$HERE/glowup_test.py" 2>&1)"; st=$?
[ $st -eq 0 ] && ok "glowup_test.py passes" || bad "glowup_test.py passes" "$(tail -30 <<<"$out")"

echo "glow-up: check"
SCRIPTS="$REPO/skills/design-studio/scripts"
gfresh() { stage glowup-smoke demo "g$RANDOM$RANDOM"; }
regen() { python3 "$SCRIPTS/theme_tokens.py" "$1/theme.json" --css --out "$1/tokens.css"; }
jedit() { python3 - "$1" "$2" <<'PY'
import json, sys
p, code = sys.argv[1], sys.argv[2]
d = json.load(open(p)); exec(code); json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)
PY
}
t="$(gfresh)"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$(tail -1 <<<"$out")" = "OK 2 glow-up directions (directions, 4 screens)" ] && ok "check passes a directions round" || bad "check passes a directions round" "$out"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r2" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$(tail -1 <<<"$out")" = "OK 1 glow-up system (2 routes)" ] && ok "check passes a system round" || bad "check passes a system round" "$out"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK glow-up apply stage 3 (entropy 33 → 15, tells 32 → 9)" ] && ok "check passes an apply round" || bad "check passes an apply round" "$out"

t="$(gfresh)"; perl -pi -e 's/ data-signature//' "$t/r1/v01/s2.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"; st=$?
[ $st -ne 0 ] && grep -q "FAIL v01: signature element appears on 1 screen (need 2)" <<<"$out" && ok "check wants the signature on two screens" || bad "check wants the signature on two screens" "$out"

t="$(gfresh)"; jedit "$t/r1/v01/theme.json" 'd["shape"]["radius"]["md"] = 8'; regen "$t/r1/v01"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01: shape.radius.md is shadcn's 0.5rem radius; give it a line in reasons or change it" <<<"$out" && ok "check wants a reason for a default" || bad "check wants a reason for a default" "$out"
jedit "$t/r1/v01/theme.json" 'd["reasons"]["shape.radius.md"] = "8px matches the platform input radius"'; regen "$t/r1/v01"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"; st=$?
[ $st -eq 0 ] && ok "a reason clears the default" || bad "a reason clears the default" "$out"

t="$(gfresh)"; jedit "$t/r1/manifest.json" 'del d["variations"][0]["notes"]["composition"]'
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01: notes.composition is empty" <<<"$out" && ok "check wants a reasoned composition" || bad "check wants a reasoned composition" "$out"

t="$(gfresh)"; echo "/* hand edit */" >> "$t/r1/v02/tokens.css"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v02/tokens.css is stale; regenerate it with theme_tokens.py --css" <<<"$out" && ok "check fails stale tokens" || bad "check fails stale tokens" "$out"

t="$(gfresh)"; perl -pi -e 's|<h2 class="t-h2">New note</h2>|<h2 class="t-h2" style="color:#ff0000">New note</h2>|' "$t/r1/v01/s3.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01/s3.html: literal colour '#ff0000'; use the tokens" <<<"$out" && ok "check fails a literal colour" || bad "check fails a literal colour" "$out"

t="$(gfresh)"; perl -ni -e 'print unless /^- Submit$/' "$t/context.md"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01: voice string 'Submit' is not in context.md" <<<"$out" && ok "check wants real voice strings" || bad "check wants real voice strings" "$out"

t="$(gfresh)"; perl -pi -e 's/data-template="column"/data-template="hero"/' "$t/r1/v01/s4.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01/s4.html: data-template hero is not in theme.layout.templates" <<<"$out" && ok "check wants a declared layout template" || bad "check wants a declared layout template" "$out"

t="$(gfresh)"; perl -pi -e 's|>Your notes<|>Elevate your notes<|' "$t/r1/v01/s1.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01/s1.html:[0-9]*: C-buzzwords" <<<"$out" && ok "check runs the tells on screens" || bad "check runs the tells on screens" "$out"

t="$(gfresh)"; jedit "$t/r1/v01/theme.json" 'd["color"]["light"]["ground"] = "oklch(0.96 0.02 80)"; d["color"]["light"]["action"] = "oklch(0.55 0.13 40)"'; regen "$t/r1/v01"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "FAIL v01: second-order tell cream-terracotta" <<<"$out" && ok "check fails an unnamed second-order tell" || bad "check fails an unnamed second-order tell" "$out"
jedit "$t/r1/v01/theme.json" 'd["signature"]["uses"] = ["cream-terracotta"]'; regen "$t/r1/v01"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r1" 2>&1)"
grep -q "second-order tell cream-terracotta" <<<"$out" && bad "a named signature allows a second-order pattern" "$out" || ok "a named signature allows a second-order pattern"

t="$(gfresh)"; rm "$t/r2/v01/routes/settings.html"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r2" 2>&1)"
grep -q "FAIL v01: missing route settings (routes/settings.html)" <<<"$out" && ok "check wants every route" || bad "check wants every route" "$out"

t="$(gfresh)"; jedit "$t/r3/entropy-after.json" 'd["colors"]["count"] = 30'
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"
grep -q "FAIL entropy rose: 33 → 44" <<<"$out" && ok "check fails rising entropy" || bad "check fails rising entropy" "$out"

t="$(gfresh)"; jedit "$t/r3/entropy-after.json" 'd["colors"]["values"]["#ffffff"]["files"].append("src/App.tsx")'
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"
grep -q "FAIL literal colours outside the theme files: src/App.tsx" <<<"$out" && ok "check fails stray literal colours" || bad "check fails stray literal colours" "$out"

t="$(gfresh)"; jedit "$t/r3/manifest.json" 'd["apply"]["build"] = "fail"'
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"
grep -q "FAIL build failed and the stage was not reverted" <<<"$out" && ok "check fails an unreverted broken build" || bad "check fails an unreverted broken build" "$out"

echo "glow-up: from screenshots"
t="$(gfresh)"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r4" 2>&1)"; st=$?
[ $st -eq 0 ] && [ "$out" = "OK glow-up handoff (8 files, 3 screens)" ] && ok "check passes a handoff round" || bad "check passes a handoff round" "$out"
t="$(gfresh)"; echo "/* hand edit */" >> "$t/r4/handoff/tokens.css"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r4" 2>&1)"
grep -q "FAIL handoff/tokens.css is stale; rerun handoff.py" <<<"$out" && ok "check fails stale handoff tokens" || bad "check fails stale handoff tokens" "$out"
t="$(gfresh)"; rm "$t/r4/handoff/theme.ts"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r4" 2>&1)"
grep -q "FAIL handoff is missing theme.ts" <<<"$out" && ok "check wants every handoff file" || bad "check wants every handoff file" "$out"
t="$(gfresh)"; perl -ni -e 'print unless /^## New note$/' "$t/r4/handoff/screens.md"
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r4" 2>&1)"
grep -q "FAIL handoff/screens.md has no section for New note" <<<"$out" && ok "check wants a section per uploaded screen" || bad "check wants a section per uploaded screen" "$out"
t="$(gfresh)"; jedit "$t/r3/manifest.json" 'd["source"] = "images"'
out="$(python3 "$SCRIPTS/glowup_check.py" "$t/r3" 2>&1)"
grep -q "FAIL apply needs the codebase; an image-sourced topic ends at handoff" <<<"$out" && ok "check refuses apply on an image-sourced topic" || bad "check refuses apply on an image-sourced topic" "$out"
out="$(python3 "$SCRIPTS/image_audit.py" "$t/before/s1.png" 2>&1)"
grep -q "^IMAGE-AUDIT 1 colour across 1 screen" <<<"$out" && ok "image_audit reads a fixture screenshot" || bad "image_audit reads a fixture screenshot" "$out"

echo "glow-up: new, check and sheets routing"
out="$(bash "$STUDIO" new demo glow --glowup 2>&1)"
rd="$DESIGN_STUDIO_ROOT/demo/glow/r1"
grep -qx "MODE glowup" <<<"$out" && ok "new --glowup prints MODE glowup" || bad "new --glowup prints MODE glowup" "$out"
[ -f "$rd/screen.css" ] && [ -f "$rd/web.css" ] && ok "new --glowup copies both frame stylesheets" || bad "new --glowup copies both frame stylesheets" "$(ls "$rd")"
grep -q "^SURFACE" <<<"$out" && bad "app glow-up prints no SURFACE line" "$out" || ok "app glow-up prints no SURFACE line"
out="$(bash "$STUDIO" new demo glowweb --glowup --web 2>&1)"
grep -qx "MODE glowup" <<<"$out" && grep -qx "SURFACE web" <<<"$out" && ok "new --glowup --web prints both lines" || bad "new --glowup --web prints both lines" "$out"
out="$(bash "$STUDIO" new demo nope --sparkle 2>&1)"; st=$?
[ $st -eq 2 ] && grep -q "unknown flag: --sparkle" <<<"$out" && ok "new rejects an unknown flag" || bad "new rejects an unknown flag" "$out"
t="$(stage glowup-smoke demo groute)"
out="$(bash "$STUDIO" check "$t/r1" 2>&1)"
[ "$(tail -1 <<<"$out")" = "OK 2 glow-up directions (directions, 4 screens)" ] && ok "check routes glow-up rounds by mode" || bad "check routes glow-up rounds by mode" "$out"
if bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO" >/dev/null 2>&1; then
  t="$(stage glowup-smoke demo gsheets)"
  cp "$ASSETS/web.css" "$t/r1/"
  out="$(bash "$STUDIO" sheets "$t/r1" 2>&1)"
  [ -s "$t/r1/sheet-v01.png" ] && [ -s "$t/r1/sheet-v02.png" ] && ok "glow-up sheets write one sheet per direction" || bad "glow-up sheets write one sheet per direction" "$out"
  [ -s "$t/r1/sheet-before.png" ] && ok "glow-up sheets write the before sheet" || bad "glow-up sheets write the before sheet" "$out"
  ls "$t/r1" | grep -q '^_' && bad "glow-up sheets clean up wrappers" "$(ls "$t/r1")" || ok "glow-up sheets clean up wrappers"
else
  echo "  skip glow-up sheets (no Chrome/Chromium)"
fi

echo "glow-up: gallery"
out="$(bash "$STUDIO" new demo glowgal --glowup 2>&1)"
cmp -s "$DESIGN_STUDIO_ROOT/demo/glowgal/r1/index.html" "$ASSETS/gallery-glowup.html" && ok "new --glowup copies gallery-glowup.html" || bad "new --glowup copies gallery-glowup.html" "$out"
grep -q "—" "$ASSETS/gallery-glowup.html" && bad "gallery-glowup.html has no em dashes" || ok "gallery-glowup.html has no em dashes"
if bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO" >/dev/null 2>&1; then
  CHROME_BIN="$(bash -c 'eval "$(sed -n "/^chrome_bin()/,/^}/p" "$0")"; chrome_bin' "$STUDIO")"
  t="$(stage glowup-smoke demo ggal)"
  for r in r1 r2 r3; do cp "$ASSETS/gallery-glowup.html" "$t/$r/index.html"; cp "$ASSETS/web.css" "$t/$r/"; done
  bash "$STUDIO" serve >/dev/null
  base="http://127.0.0.1:$DESIGN_STUDIO_PORT/demo/ggal"
  dump() { "$CHROME_BIN" --headless=new --disable-gpu --virtual-time-budget=6000 --dump-dom "$1" 2>/dev/null; }
  dom="$(dump "$base/r1/index.html")"
  grep -q 'data-row="v01"' <<<"$dom" && grep -q 'src="v02/s4.html?theme=native"' <<<"$dom" && ok "gallery renders direction rows across the key screens" || bad "gallery renders direction rows across the key screens"
  dom="$(dump "$base/r1/index.html?tab=before")"
  grep -q 'data-row="before"' <<<"$dom" && grep -q 'src="../before/s1.png"' <<<"$dom" && ok "gallery ?tab=before shows the audit screens" || bad "gallery ?tab=before shows the audit screens"
  dom="$(dump "$base/r1/index.html?tab=category")"
  grep -q 'class="cat"' <<<"$dom" && grep -q "Table stakes" <<<"$dom" && ok "gallery ?tab=category shows category.md" || bad "gallery ?tab=category shows category.md"
  dom="$(dump "$base/r1/index.html#v02")"
  grep -q 'data-spec="v02"' <<<"$dom" && grep -q 'data-role="action"' <<<"$dom" && ok "gallery #v02 opens the spec card" || bad "gallery #v02 opens the spec card"
  dom="$(dump "$base/r2/index.html")"
  grep -q 'src="v01/routes/settings.html?theme=native"' <<<"$dom" && ok "gallery shows system routes" || bad "gallery shows system routes"
  dom="$(dump "$base/r3/index.html")"
  grep -q 'data-route="home"' <<<"$dom" && grep -q "Entropy 33 → 15" <<<"$dom" && ok "gallery shows the apply board" || bad "gallery shows the apply board"
  cp "$ASSETS/gallery-glowup.html" "$t/r4/index.html"
  dom="$(dump "$base/r4/index.html")"
  grep -q 'href="handoff/theme.ts"' <<<"$dom" && grep -q "Apply the Ledger design system" <<<"$dom" && grep -q "## Empty state" <<<"$dom" && ok "gallery shows the handoff" || bad "gallery shows the handoff"
  jedit "$t/r1/manifest.json" 'd["screens"][3]["invented"] = True'
  dom="$(dump "$base/r1/index.html")"
  grep -q "Empty state · invented" <<<"$dom" && ok "gallery labels invented screens" || bad "gallery labels invented screens"
  grep -q 'class="desk"' <<<"$dom" && ! grep -q 'class="phone"' <<<"$dom" && ok "gallery uses desktop frames for a web surface" || bad "gallery uses desktop frames for a web surface"
  jedit "$t/r1/manifest.json" 'd["surface"] = "app"'
  dom="$(dump "$base/r1/index.html")"
  grep -q 'class="phone"' <<<"$dom" && ! grep -q 'class="desk"' <<<"$dom" && ok "gallery keeps phone frames for an app surface" || bad "gallery keeps phone frames for an app surface"
else
  echo "  skip glow-up gallery DOM tests (no Chrome/Chromium)"
fi

echo "glow-up: craft references"
SK="$REPO/skills/design-studio"
need_heads() { local f="$1"; shift; local h; for h in "$@"; do grep -qx "$h" "$SK/references/$f" && ok "$f has '$h'" || bad "$f has '$h'"; done; }
need_heads glowup-craft.md "## theme.json" "## The system layer" "### 1. Layout system" "### 2. Brand surface" "### 3. Colour construction" "### 4. Component state matrix" "### 5. Type construction" "### 6. Signature element" "### 7. Content and voice system" "### 8. Loading policy" "### 9. Form system" "### 10. Numbers and tables" "### 11. Feedback and haptics" "### 12. Responsive components and navigation" "### 13. Density" "## Construction details" "## The human rules" "## The tells" "## Layout templates on each surface" "## Screens" "## Pre-send checklist" "## Sources"
need_heads category-research.md "## Choosing comparables" "## Gathering screens" "## What to record" "## Table stakes and white space" "## Rules" "## category.md template"
for f in glowup-craft.md category-research.md; do grep -q "—" "$SK/references/$f" && bad "$f has no em dashes" || ok "$f has no em dashes"; done
grep -q "tests/fixtures/glowup-smoke/r1/v01/theme.json" "$SK/references/glowup-craft.md" && ok "glowup-craft.md points at the worked example" || bad "glowup-craft.md points at the worked example"

echo "glow-up: loop and apply references"
need_heads glowup.md "## When it's on" "## Stages" "## Intake" "## Audit" "## Category research" "## Directions and converge" "## System" "## Apply" "## Pick question" "## TASTE.md" "## Manifest reference"
need_heads apply-web.md "## Before you start" "## Stage 1: theme layer" "## Stage 2: shared components" "## Stage 3: routes" "## Stage 4: brand surface" "## After every stage" "## Hard limits" "## Follow-ups"
need_heads apply-native.md "## Before you start" "## Stage 1: theme layer" "## Stage 2: shared components" "## Stage 3: screens" "## Stage 4: brand surface" "## After every stage" "## Hard limits" "## Follow-ups"
for f in glowup.md apply-web.md apply-native.md; do grep -q "—" "$SK/references/$f" && bad "$f has no em dashes" || ok "$f has no em dashes"; done
need_heads glowup.md "## From screenshots" "## Handoff"
for s in entropy.py tells_lint.py theme_tokens.py glowup_check.py image_audit.py handoff.py; do grep -q "$s" "$SK/references/glowup.md" && ok "glowup.md uses $s" || bad "glowup.md uses $s"; done
grep -q -- "--shadcn-hsl" "$SK/references/apply-web.md" && ok "apply-web.md covers HSL shadcn" || bad "apply-web.md covers HSL shadcn"
grep -q -- "--rn" "$SK/references/apply-native.md" && ok "apply-native.md uses --rn" || bad "apply-native.md uses --rn"

echo "glow-up: docs"
grep -qi "vibe-coded" <(sed -n '1,6p' "$SK/SKILL.md") && ok "SKILL.md description triggers on vibe-coded apps" || bad "SKILL.md description triggers on vibe-coded apps"
grep -q "^## Glow-up mode" "$SK/SKILL.md" && ok "SKILL.md has a Glow-up mode section" || bad "SKILL.md has a Glow-up mode section"
for f in glowup.md glowup-craft.md category-research.md apply-web.md apply-native.md; do
  grep -q "references/$f\|\`$f\`" "$SK/SKILL.md" "$SK/references/glowup.md" && ok "$f is referenced" || bad "$f is referenced"
done
grep -q "^### Glow-up mode axes" "$SK/references/variations.md" && ok "variations.md has glow-up axes" || bad "variations.md has glow-up axes"
grep -q "^## 1.3.0" "$REPO/CHANGELOG.md" && ok "CHANGELOG has 1.3.0" || bad "CHANGELOG has 1.3.0"
grep -q "^## Glow-up mode" "$REPO/README.md" && ok "README has a Glow-up mode section" || bad "README has a Glow-up mode section"
new_sections="$(sed -n '/^## Glow-up mode/,/^## [^G]/p' "$SK/SKILL.md"; sed -n '/^## 1.3.0/,/^## 1.2.0/p' "$REPO/CHANGELOG.md"; sed -n '/^## Glow-up mode/,/^## [^G]/p' "$REPO/README.md")"
grep -q "—" <<<"$new_sections" && bad "the glow-up doc sections have no em dashes" "$(grep -n "—" <<<"$new_sections" | head -3)" || ok "the glow-up doc sections have no em dashes"

# --- new tests above this line ---
echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
