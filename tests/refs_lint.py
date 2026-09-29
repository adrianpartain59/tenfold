#!/usr/bin/env python3
"""Lint design-studio's paywall knowledge references.

  refs_lint.py <references-dir>

paywall-playbook.md: every line with a result number (a % or an N-times lift)
carries a [S#] citation; every [S#] cited in the playbook or the archetype
catalog is defined in the playbook's Sources table; every source row has a URL,
a YYYY-MM[-DD] date and a strength of benchmark, case study or practice.
paywall-archetypes.md: at least 14 "## N. Name" entries, each with all seven
bold fields. Prints FAIL lines, then "OK|FAIL refs (<n> sources, <k> archetypes)".
"""
import os, re, sys

RESULT = re.compile(r"\d+(?:\.\d+)?\s?(?:%|×|x\b)")
CITE = re.compile(r"\[S(\d+)\]")
ROW = re.compile(r"^\|\s*S(\d+)\s*\|(.+)\|\s*$")
DATE = re.compile(r"^\d{4}-\d{2}(?:-\d{2})?$")
ENTRY = re.compile(r"^## (\d+)\. (.+)$")
STRENGTHS = ("benchmark", "case study", "practice")
FIELDS = ("Mechanism", "Anatomy", "Wins when", "Loses when", "Axes", "Hazards", "Seen in")


def main(d):
    errs = []
    pb = open(os.path.join(d, "paywall-playbook.md"), encoding="utf-8").read().splitlines()
    ar = open(os.path.join(d, "paywall-archetypes.md"), encoding="utf-8").read().splitlines()

    sources, in_src = {}, False
    for i, line in enumerate(pb, 1):
        if line.startswith("## "):
            in_src = line.strip() == "## Sources"
            continue
        if in_src:
            mt = ROW.match(line)
            if not mt:
                continue
            sid, cells = mt.group(1), [c.strip() for c in mt.group(2).split("|")]
            if len(cells) != 4:
                errs.append(f"playbook:{i}: S{sid} needs Source | URL | Date | Strength")
                continue
            _, url, date, strength = cells
            if not url.startswith("http"):
                errs.append(f"playbook:{i}: S{sid} has no URL")
            if not DATE.match(date):
                errs.append(f"playbook:{i}: S{sid} date {date!r} is not YYYY-MM[-DD]")
            if strength not in STRENGTHS:
                errs.append(f"playbook:{i}: S{sid} strength {strength!r} is not one of {', '.join(STRENGTHS)}")
            sources[sid] = strength
            continue
        if RESULT.search(line) and not CITE.search(line):
            errs.append(f"playbook:{i}: a result number with no [S#]: {line.strip()[:80]}")

    for name, lines in (("playbook", pb), ("archetypes", ar)):
        for i, line in enumerate(lines, 1):
            if name == "playbook" and ROW.match(line):
                continue
            for sid in CITE.findall(line):
                if sid not in sources:
                    errs.append(f"{name}:{i}: [S{sid}] is not in the Sources table")

    entries, cur = [], None
    for line in ar:
        mt = ENTRY.match(line)
        if mt:
            cur = (mt.group(2).strip(), set())
            entries.append(cur)
            continue
        if line.startswith("## "):
            cur = None
            continue
        if cur:
            for f in FIELDS:
                if line.startswith(f"**{f}:**"):
                    cur[1].add(f)
    for name, got in entries:
        missing = [f for f in FIELDS if f not in got]
        if missing:
            errs.append(f"archetypes: {name} is missing {', '.join(missing)}")
    if len(entries) < 14:
        errs.append(f"archetypes: {len(entries)} entries, need at least 14")

    for e in errs:
        print("FAIL", e)
    print(f"{'FAIL' if errs else 'OK'} refs ({len(sources)} sources, {len(entries)} archetypes)")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
