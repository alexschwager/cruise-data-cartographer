# cruise-data-cartographer

[![verify](https://github.com/alexschwager/cruise-data-cartographer/actions/workflows/verify.yml/badge.svg)](https://github.com/alexschwager/cruise-data-cartographer/actions/workflows/verify.yml)

**A cartographer for a production cruise data layer — and the worked map it left: 13 cards over a 60-table PostgreSQL schema, its supplier staging feeds, and the Cloudflare D1 edge cache that mirrors it. Every card cites the live source; one card is a ghost, one is a leftover, one is empty for a reason the map refuses to prettify.**

---

## The territory

A real, in-force data layer behind a cruise storefront: `cruise_v2` in
PostgreSQL (offerings, departures, a 1.3M-row price lattice, fares,
cabins, bookings), the cross-vertical geo tables it leans on, per-supplier
staging schemas, and a D1 edge cache rebuilt blue-green behind an
active-slot pointer. Supplier ingests write it daily; an autonomous
agent pipeline changes its schema weekly.

**The later reader is a model.** Every session against this layer starts
cold — a reviewer grounding a brief, a developer writing a migration —
and the expensive mistakes are not ignorance but **wrong neighbours**:

- `ports_master.sub_region_id` does **not** point at `public.subregions`,
  despite the name. The FK target is `cruise_v2.sub_region` (verified in
  `pg_constraint`). The name-join runs, returns plausible garbage, and has
  historically read as data corruption.
- An internal agent manifest still says `cruise_v2.port`. That table does
  not exist. The live FK graph says `public.ports_master`.
- Two tables both hold 0 rows. One (`staging.msc_live_fare`) is wired in
  four files and empty because its 640k rows were destroyed by an
  un-sandboxed test in 2026, with the refill founder-gated. The other
  (`destination_supplier_codes`) has never been read or written by any
  code, ever. Same count, opposite meanings — trusting either wrongly
  implements the wrong world.

The map exists so a cold reader lands on those facts in two hops instead
of rediscovering them at 3am.

## The one rule

**Load `map/catalog.md`, open ONE card, stop.** Never the whole cards
folder. The catalog is ~30 lines of question-phrased doors; each card
answers its question, names what a change **Hits**, names the
**wrong neighbour** a reader was about to reach for, and cites the live
source — which always wins over the card.

## Ninety seconds to see it hold

No API key, no network, Python 3 stdlib only:

```
git clone https://github.com/alexschwager/cruise-data-cartographer
cd cruise-data-cartographer
python3 tests/verify.py selftest
```

Two expectations: the shipped map passes the full structural audit
(153 checks: every door resolves, catalog↔cards bijection, no counts
stored in the catalog, per-card status/source/sections, evidence-of-absence
on dead cards, dated cites, size caps, resolving cross-refs) — and the
fixture photocopy card (`tests/fixtures/card-bad.md`: pasted DDL, a
column-by-column restatement, a "how the week goes" tour, no wrong
neighbour) **fails on six checks.** `verify.py map` runs the audit alone;
`verify.py card <file>` audits one card.

## One real cold walk, published with its defects (receipts/cold-walk-1.md)

A fresh model instance with no memory of the territory was handed the
catalog, allowed ONE card, and asked a real product question ("wifi
included" badge on search). It answered in two hops — right card, right
data home, and it named the offering-row trap unprompted. It also filed
**three defects**, instructed that finding them was a success condition.
All three were confirmed against source. Two are fixed on the cards; the
third is partially fixed with the remainder deliberately left to the
source and recorded. The walker's most important find: its own reasonable
guess about the change path was **wrong** (the projection splits tier
metadata from inclusions), which is exactly the fact the card now carries.
The walk is preserved verbatim, disposition table included.

## The folder

| File | The one job |
|---|---|
| `identity.md` | Who the cartographer is, the territory class, that the later reader is usually a model, what it is not (diagnostician / auditor / photocopy / tour). |
| `rules.md` | How it maps: inventory-before-cards, the evidence-backed status taxonomy, Hits / Does-not-hit, cite-never-copy, catalog-points-shelves-store, the two-hop walk, the disguised-photocopy refusals, decay. |
| `examples.md` | Three walks through the shipped map and one refusal. |
| `reference/card-types.md` | The closed set: noun, namespace, mirror, access-rule cards; the live / live-empty / leftover / ghost taxonomy. |
| `reference/walk-order-and-collisions.md` | How a cold model walks, and this territory's naming collisions written down. |
| `map/` | The product: `catalog.md` + 13 cards. |
| `receipts/` | The published cold walk, verbatim, defects and dispositions kept. |
| `tests/` | The offline verifier + the photocopy fixture it must reject. |

## Provenance

Hand-built (the method from the comp brief plus the two prior builds in
this series — [agent-brief-editor](https://github.com/alexschwager/agent-brief-editor),
[agent-run-diagnostician](https://github.com/alexschwager/agent-run-diagnostician) —
not the ICM Architect skill). The inventory was taken live on 2026-08-18:
`pg_stat_user_tables`, `pg_constraint`, `pg_indexes`, `information_schema`
over the production database (SELECT-only; PII tables counted via pg_stat,
never row-read), plus the sync engine's own source. Inventory-before-cards
corrected the author twice before a single card existed: the "port table"
a manifest named does not exist, and a table assumed dead is wired in four
files. Row counts are the capture date's; the map says so on every cite.

## Don't take the claims — where each would break

- **"Cards cite source; source wins."** The verifier checks cites exist
  and are dated — not that they are still true. A card is re-verified on
  touch (rules.md Rule 8); between touches it decays like any map.
- **"Two hops suffice."** Demonstrated on one real cold walk and one
  constructed set in examples.md. Walk 1's caveat stands: one question
  needed a fact the card lacked (now added). More walks would find more —
  that is what receipts/ is for.
- **"No photocopies."** Enforced by size caps and fence caps; a prose
  restatement under the cap slips the scanner. The real line is rules.md
  Rule 4, held by a human.
- **"The catalog covers the territory."** 13 cards cover the load-bearing
  nouns; `cruise_v2` has 60+ tables. Uncovered tables are deliberately
  undoored, not secretly covered — a question with no door is a map
  defect to file, and the catalog grows a line, not the reader's context.
- **Numbers are a snapshot.** Every count is stamped 2026-08-18. The
  territory moves daily; the map's honesty is the stamp, not the number.

## If you read one file

`map/cards/destination-supplier-codes.md` — a ghost card. Five live
sibling tables make its naming pattern scream "this is the mechanism";
zero rows and zero references say the mechanism was never built. The card
exists so the next reader spends that discovery in one hop instead of one
sprint — which is the whole argument for maps.
