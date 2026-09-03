# port_id_translation_v2_to_master — 306 rows nothing reads

status: leftover
source: pg:public.port_id_translation_v2_to_master (306 rows, live 2026-08-18) · checkable: evidence/row-counts.txt (still 306, 2026-09-03)

## What it is (and why it is shaped this way)

A migration shim from the port cutover: when the old cruise-side port ids
were folded into `ports_master`, this table carried old-id → new-id so
in-flight references could be rewritten. The cutover completed; the
rewrites happened; the shim stayed. It is honest residue — the data is
real and was correct, and keeping it cost nothing — but nothing living
consumes it.

## Evidence of absence

- Wiring: `grep -rl "port_id_translation_v2_to_master" backend/ scripts/`
  in the platform repo returns **0 files** (run 2026-08-18; re-run before
  trusting this card).
- Data: 306 rows present via `pg_stat_user_tables` (same date) — so this
  is rows-without-readers: the definition of leftover, per
  reference/card-types.md, on two independent instruments.

## Hits — if you change this

- Nothing at runtime. Dropping it destroys only the historical old→new
  crosswalk — worth keeping until nobody could ever need to trace a
  pre-cutover port id, which is an operator call, not a cleanup reflex.

## Does not hit — the wrong neighbour

- **`port_supplier_mappings`** — the similarly-named table that is
  intensely alive (8,729 rows, every ingest's resolver). Confusing the
  two in a cleanup sweep would take down port resolution while "removing
  dead code." The wrong neighbour here bites in the delete direction.
