# port_supplier_mappings — the ONE supplier-code → port map

status: live
source: pg:public.port_supplier_mappings (8,729 rows, live 2026-08-18) — key shape (supplier, supplier_port_code, port_id)

## What it is (and why it is shaped this way)

Every supplier names ports its own way (codes, city codes, misspelled
names). This is the single cross-vertical translation table: one row per
(supplier, their code) → our `ports_master.id`. It is deliberately the
ONLY place that mapping lives, so a resolution fixed once is fixed for
every ingest — the doctrine's design intent is that ingests resolve
through this central table rather than each keeping a private map (parts
of the older wiring predate that and flow the other way; check the ingest
you touch before assuming which direction it reads).

## Hits — if you change this

- Every supplier ingest's port resolution — a wrong row here attaches
  itineraries, images, and geography to the wrong real-world port with no
  error anywhere (a "confidently wrong link, not a missing one").
- Unresolvable codes are supposed to FLAG for the port-resolver lane, not
  fall back to name-matching — a name-match "fix" in a loader reintroduces
  exactly the hazard this table exists to end. (That resolver lane is an
  ingest AGENT, outside this data map's territory — the next hop is a
  process, not a table.)
- Deleting rows orphans nothing mechanically (no cascade) but silently
  degrades the next ingest run to unresolved.

## Does not hit — the wrong neighbour

- **`ports_master` itself.** A supplier using a weird code is a MAPPING
  row, not a new port. Minting a near-duplicate port to make one supplier
  resolve is how the port table forks.
- **`port_id_translation_v2_to_master`** — looks related, is a dead
  migration shim: 306 rows, zero code references
  (cards/port-id-translation.md).
