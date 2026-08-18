# offering — a cruise as sold: one ship sailing one itinerary, marketed

status: live
source: pg:cruise_v2.offering (4,167 rows, live 2026-08-18) · pg_constraint FKs (same date) · sync/sync_engine.py:211-214 (rebuild-gate sources)

## What it is (and why it is shaped this way)

The product spine. One row = one sellable cruise product: FKs (all
verified live) to `itinerary`, `cruise_line`, `ship`, `destination`, and
`sub_region`. It is deliberately thin — an offering carries identity and
marketing shape, NOT prices and NOT dates: multiple `departure` rows
realize it on calendar dates, and every money figure hangs off the
departure/fare/cabin axes. This split is what lets prices churn daily
without touching the product, and it is why "add a field to the cruise"
is usually a question about which OTHER table the field belongs to.

## Hits — if you change this

- The D1 search-card rebuild gate: `cruise_v2.offering` is in
  `CRUISE_V2_SOURCE_TABLES` (`sync/sync_engine.py:211-214`), so an
  `updated_at` change here triggers the blue-green cache rebuild — see
  cards/d1-mirror.md.
- A new column the storefront needs must ALSO be projected: create + map +
  fetch-list in the sync engine, or it silently never reaches the edge.
- `itinerary` / `itinerary_stop` (60,461 rows) hang off the itinerary FK —
  reshaping an offering's itinerary is a change to those, not to offering.

## Does not hit — the wrong neighbour

- **Prices.** Nothing money-shaped lives here. The reach for
  "offering.price" lands on cards/departure-and-prices.md.
- **Fare inclusions/promos** — that is `fare_tier` (cards/fare-tier.md),
  keyed per line, not per offering.
