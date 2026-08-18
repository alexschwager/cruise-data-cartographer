# departure & the price grain — where money numbers actually live

status: live
source: pg:cruise_v2.departure (12,833 rows) · pg:cruise_v2.departure_cabin_fare_price (1,311,791 rows) · pg:cruise_v2.departure_market_price (12,438 rows) · pg:cruise_v2.price_fingerprint (11,059) · pg:cruise_v2.cache_fare_watermark (7,970) — all live 2026-08-18

## What it is (and why it is shaped this way)

A `departure` is one offering on one calendar date. Prices attach at TWO
grains beneath it: `departure_cabin_fare_price` — the full lattice
(departure × cabin category × fare tier × occupancy), the largest table in
the schema at 1.3M rows — and `departure_market_price`, the collapsed
per-market "from" price the search surface reads. The split exists because
search needs one cheap number while checkout needs the exact lattice cell.
`price_fingerprint` and `cache_fare_watermark` are change-detection, not
prices: they exist so re-ingests and cache rebuilds can tell "price moved"
from "supplier re-sent the same number."

## Hits — if you change this

- `departure_market_price` and `departure` are rebuild-gate sources for the
  D1 search cache (`sync/sync_engine.py:211-214`) — price movement is what
  triggers the edge rebuild (cards/d1-mirror.md).
- The lattice table's SIZE is load-bearing: anything that scans
  `departure_cabin_fare_price` unindexed, or re-ingests it wholesale, is a
  1.3M-row operation. Change-detection (fingerprints/watermarks) exists
  precisely so you don't.
- Live-supplier warm-writes land here on price change — PG stays the truth,
  the active D1 slot mirrors it.

## Does not hit — the wrong neighbour

- **`fare_tier` prices.** `fare_tier_item_price` (260 rows) prices fare
  ADD-ONS, not cruises. The cruise number is always in the departure grain.
- **The offering.** Price churn never touches `offering` rows — if your
  price change is editing offering, you are on the wrong card.
- **Settlement currency.** What the client pays is settlement doctrine
  (`cruise_line_settlement`, 30 rows) — never derived by summing display
  prices across currencies.
