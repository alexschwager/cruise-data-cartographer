# destination_supplier_codes — a name with no wiring and no data

status: ghost
source: pg:cruise_v2.destination_supplier_codes (0 rows, live 2026-08-18) · checkable: evidence/row-counts.txt (still 0, 2026-09-03)

## What it is (and why it is shaped this way)

A table minted by pattern: nearly every cruise_v2 noun has a
`_supplier_codes` satellite (ship, itinerary, departure, cabin_category,
fare_tier, cabin_class — all live), so `destination` got one too. But
destinations are DERIVED from port geography in this design (region lives
at the port), not resolved from supplier codes — so no ingest was ever
built to write this table, and none reads it. The scaffolding exists; the
building was never needed.

## Evidence of absence

- Rows: **0** (`pg_stat_user_tables`, 2026-08-18).
- Wiring: `grep -rl "destination_supplier_codes" backend/ scripts/` in the
  platform repo returns **0 files** (2026-08-18; re-run before trusting).
Both searches empty = ghost, per reference/card-types.md.

## Hits — if you change this

- Nothing — that is the point of the card. Time spent "populating" it
  implements a resolution path the design routes through ports instead.

## Does not hit — the wrong neighbour

- **The live `_supplier_codes` family.** The naming pattern screams "this
  is how destinations resolve," and five sibling tables reinforce it. A
  cold reader building a destination ingest will reach here first; the
  real mechanism is port sub-regions (cards/ports-master.md,
  cards/region-namespace.md). The pattern is the trap.
