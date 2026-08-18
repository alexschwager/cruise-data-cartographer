# Catalog — the cruise data layer

Load this file, open ONE card, stop. Inventory grounded live 2026-08-18
(PG via `pg_stat_user_tables` / `pg_constraint`; D1 via the sync engine).

## The product spine
- What is a cruise, as sold? → cards/offering.md
- Where do prices actually live? → cards/departure-and-prices.md
- What is a fare / a promo / "what's included"? → cards/fare-tier.md
- What is a cabin — and which of the TWO cabin axes am I on? → cards/cabin-category.md

## Geography
- What is a port? (there is no cruise_v2.port) → cards/ports-master.md
- How does a supplier's port code become our port? → cards/port-supplier-mappings.md
- Which "region" is which? (three namespaces) → cards/region-namespace.md

## The edge
- What does the storefront actually read? What mirrors to D1? → cards/d1-mirror.md

## Money & people
- Bookings, payments, guests — and what I must never SELECT → cards/booking-family.md

## Feeds
- Where does raw supplier data land before ingest? → cards/staging-feeds.md
- Why is the MSC live-fare table empty? → cards/msc-live-fare.md

## Dead and undead
- A populated table nothing reads (leftover) → cards/port-id-translation.md
- A table no code has ever touched (ghost) → cards/destination-supplier-codes.md
