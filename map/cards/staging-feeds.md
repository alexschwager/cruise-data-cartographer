# staging.* — where raw supplier data lands before ingest

status: live
source: pg:staging.msc_cache_itineraries (136,230 rows) · pg:staging.ncl_pricing (66,333) · pg:staging.ncl_itinerary (18,214) · pg:staging.ponant_itineraries (9,733) · pg:staging.explora_itineraries (9,165) · pg:staging.ponant_cruises (860) · pg:staging.ncl_load_watermark (7) — live 2026-08-18

## What it is (and why it is shaped this way)

Per-supplier landing zones: raw feed shapes, one table family per
supplier, deliberately OUTSIDE `cruise_v2` so a messy or aborted ingest
never dirties the normalized layer. Ingest jobs read staging, resolve
codes (ports via cards/port-supplier-mappings.md, fares via tier
normalization, cabins via category codes), and write `cruise_v2`.
Watermark tables (`ncl_load_watermark`) track feed progress. Staging
truth decays by design — it is what the supplier LAST SENT, not what we
sell.

## Hits — if you change this

- The supplier's ingest job is the only reader — reshaping a staging table
  means reshaping its ingest in the same change, nothing else notices.
- Wiping a staging table costs a re-fetch, not data loss — the normalized
  layer is the record. (The one staging table where a wipe DID mean loss
  has its own card: cards/msc-live-fare.md.)

## Does not hit — the wrong neighbour

- **`cruise_v2` itself.** Reading staging to answer a product question
  answers "what did the supplier say lately," not "what do we sell."
  Search, product pages, and bookings never touch staging.
- **Cross-supplier joins.** Staging tables share no keys across suppliers
  by design; the join surface is the normalized layer.
