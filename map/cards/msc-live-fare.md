# staging.msc_live_fare — wired, empty, and empty for a reason

status: live-empty
source: pg:staging.msc_live_fare (0 rows, live 2026-08-18) · wiring: grep across backend/ + scripts/ hits 4 files (2026-08-18)

## What it is (and why it is shaped this way)

The MSC live-fare staging table: the ingest's landing zone for scraped
live fares. It is **wired** — four code files still read/write it — and
**empty**, and the emptiness is history, not design: its ~640,000 rows
were destroyed in 2026 by a test-verification step that executed a
neutralized DELETE predicate against the live connection
(unrecoverable; the incident is why live-DB revert-verification is now
sandboxed by doctrine). A refill exists but is **gated** — the re-ingest
is founder-held while the price corpus question is settled. So: 0 rows,
4 wiring points, one standing gate.

## Hits — if you change this

- Running the MSC re-ingest refills it AND re-triggers everything
  downstream of MSC prices — that is exactly the gated decision; do not
  "helpfully" run it to make the table look healthy.
- The 4 wiring files assume its shape; schema changes here must move with
  them even while the table is empty.

## Does not hit — the wrong neighbour

- **`destination_supplier_codes`** — the other famous 0-row table, and the
  opposite diagnosis: that one has no wiring at all
  (cards/destination-supplier-codes.md). Same count, different status —
  this is the taxonomy's poster pair.
- **`departure_cabin_fare_price`** — the normalized price lattice was NOT
  lost; sold prices never lived here.
