# the D1 mirror — cv2_* edge cache the storefront reads (mirror card)

status: live
source: sync/sync_engine.py:180 (CRUISE_V2_TABLES, slotted) · sync/sync_engine.py:186-209 (CRUISE_V2_SINGLE) · sync/sync_engine.py:211+ (rebuild-gate sources) · sync/run_sync.py:16-24 (operator remote sequence) — all read 2026-08-18 · checkable: evidence/cv2-projection-lists.txt

## What it is (and why it is shaped this way)

PG is the truth; a Cloudflare D1 database is the storefront's read cache.
Ownership is singular: the CW-side sync engine is the ONE writer. Two
refresh patterns: `cv2_search_card` + `cv2_card_facet` are **blue-green
slotted** (`_a`/`_b` physical pairs behind an active-slot pointer — the
hot search join swaps atomically), while ~20 dimension/product projections
(`cv2_fare_tier`, `cv2_cabin_category`, `ports_master`, ...) are
single-table DELETE-and-refill. Rebuilds gate on `updated_at` watermarks
of named PG source tables. Live-supplier price changes warm-write PG and
the ACTIVE slot so search stays current between rebuilds. If you entered
through this door chasing a card-level FACT (a badge, an inclusion), the
fact's home is upstream: cards/fare-tier.md — this card owns only how
facts travel.

## Hits — if you change this

- **Adding a projection takes THREE wired steps** — create
  (`sync/create/create_cruise_v2_cache.py`), map (`schema_mapper.py`), AND
  the fetch list (`CRUISE_V2_SINGLE`). The engine's own comment:
  "LOAD-BEARING — a table CREATEd + mapped but absent from this list is
  never fetched/filled" (`sync_engine.py:195-197`). Two of three steps
  manufactures a wired-looking ghost at the edge.
- Adding a PG source a projection reads means adding it to the rebuild
  gate list, or edits stop triggering rebuilds.
- Remote (prod) runs are OPERATOR-gated with Cloudflare auth
  (`run_sync.py:16-24`) — agents run local only.

## Does not hit — the wrong neighbour

- **Writing to D1 directly.** Every non-sync write is overwritten by the
  next refill; D1 is never the place a data fix lands. Fix PG; let the
  mirror mirror.
- **Querying `cv2_search_card_a` by physical name** — the `_a`/`_b`
  choice is the pointer's, not yours; the logical name is the contract.
- **Assuming local D1 == prod D1.** Local bindings lack whole table
  families until seeded; an empty local result proves nothing about prod.
