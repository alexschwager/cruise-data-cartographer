#!/usr/bin/env python3
"""Offline verifier for the cruise-data cartographer. No API key, no network, stdlib only.

Modes:
  verify.py map [map_dir]     structural audit of a whole map (default: ../map)
  verify.py card <card.md>    audit one card file
  verify.py selftest          audit the shipped map (expect pass) + the bad
                              fixture card (expect fail)

What it enforces (rules.md): catalog<->cards bijection, doors that resolve,
a catalog that stores no counts, per-card status/source/sections, evidence
of absence on dead cards, dated live cites, size caps (no photocopies),
resolving cross-references.

Exit 0 = all checks pass. Exit 1 = at least one FAIL.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATUSES = {"live", "live-empty", "leftover", "ghost"}
REQUIRED = ["## What it is", "## Hits", "## Does not hit"]
CARD_MAX_LINES = 60
FENCE_MAX_LINES = 6
DATE_RE = re.compile(r"20\d\d-\d\d-\d\d")

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
    return ok


def section(text, heading_prefix):
    """Return the body of the first '## ' section whose heading starts with prefix."""
    pattern = rf"^{re.escape(heading_prefix)}[^\n]*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    return m.group(1) if m else None


def check_card(path, cards_dir=None):
    text = Path(path).read_text(encoding="utf-8")
    name = Path(path).name
    lines = text.splitlines()

    status = re.search(r"^status: (\S+)$", text, re.MULTILINE)
    check(f"{name}: status line valid", bool(status) and status.group(1) in STATUSES,
          f"status: {status.group(1) if status else None}")
    st = status.group(1) if status else None

    src = re.search(r"^source: (.+)$", text, re.MULTILINE)
    check(f"{name}: source line with a locator", bool(src) and
          bool(re.search(r"(pg:\S+|\S+\.(py|md|sql|ts):?\d*|pg_constraint|pg_indexes|pg_stat)", src.group(1))))
    if src:
        check(f"{name}: live cites carry a capture date", bool(DATE_RE.search(src.group(1))))

    for sec in REQUIRED:
        check(f"{name}: has '{sec}'", sec in text)

    if st in ("leftover", "ghost"):
        ev = section(text, "## Evidence of absence")
        check(f"{name}: dead card carries Evidence of absence", ev is not None)
        if ev is not None:
            sightings = re.findall(r"^- ", ev, re.MULTILINE)
            check(f"{name}: dead status rests on >=2 named sightings",
                  len(sightings) >= 2,
                  f"{len(sightings)} sighting bullets (one search lies too easily)")
    if st == "live-empty":
        check(f"{name}: live-empty cites the 0-row count", "0 rows" in text)

    check(f"{name}: card size <= {CARD_MAX_LINES} lines (no photocopy)",
          len(lines) <= CARD_MAX_LINES, f"{len(lines)} lines")
    for block in re.findall(r"^```[^\n]*\n(.*?)^```", text, re.DOTALL | re.MULTILINE):
        blines = [l for l in block.splitlines() if l.strip()]
        check(f"{name}: fenced excerpt <= {FENCE_MAX_LINES} lines", len(blines) <= FENCE_MAX_LINES,
              f"{len(blines)}-line block (photocopy)")

    if cards_dir is not None:
        for ref in set(re.findall(r"cards/([a-z0-9-]+\.md)", text)):
            check(f"{name}: cross-ref cards/{ref} resolves", (cards_dir / ref).exists())


def check_map(map_dir):
    map_dir = Path(map_dir)
    catalog = map_dir / "catalog.md"
    cards_dir = map_dir / "cards"
    if not check("catalog.md exists", catalog.exists()):
        return
    text = catalog.read_text(encoding="utf-8")

    doors = re.findall(r"^- (.+?) → cards/([a-z0-9-]+\.md)\s*$", text, re.MULTILINE)
    check("catalog has doors", len(doors) > 0, "no '- question → cards/x.md' lines")
    for q, target in doors:
        check(f"door resolves: {target}", (cards_dir / target).exists())
        check(f"door stores no counts: {target}", not re.search(r"\d{2,}", q),
              f"door text carries a number: {q!r}")

    doored = {t for _, t in doors}
    card_files = sorted(p.name for p in cards_dir.glob("*.md"))
    for cf in card_files:
        check(f"card is doored from catalog: {cf}", cf in doored,
              "card exists but no catalog door points at it")
    for cf in card_files:
        check_card(cards_dir / cf, cards_dir=cards_dir)


def run_mode(argv):
    global results
    results = []
    if argv[0] == "map":
        check_map(argv[1] if len(argv) > 1 else HERE.parent / "map")
    elif argv[0] == "card":
        check_card(argv[1])
    else:
        raise SystemExit(f"unknown mode: {argv[0]}")
    ok = all(results)
    print(("ALL CHECKS PASS" if ok else "CHECKS FAILED") + f" ({sum(results)}/{len(results)})")
    return ok


def selftest():
    expectations = [
        (["map", str(HERE.parent / "map")], True, "the shipped map passes the structural audit"),
        (["card", str(HERE / "fixtures" / "card-bad.md")], False,
         "a photocopy card with no status and no wrong neighbour is caught"),
    ]
    failures = 0
    for argv, expected, label in expectations:
        print(f"\n=== selftest: {label} — expect {'PASS' if expected else 'FAIL'} ===")
        got = run_mode(argv)
        if got != expected:
            failures += 1
        print(f"=== {'OK' if got == expected else 'SELFTEST MISMATCH'}: got {'PASS' if got else 'FAIL'} ===")
    print(f"\nselftest: {len(expectations) - failures}/{len(expectations)} expectations met")
    return failures == 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        raise SystemExit(2)
    if args[0] == "selftest":
        raise SystemExit(0 if selftest() else 1)
    raise SystemExit(0 if run_mode(args) else 1)
