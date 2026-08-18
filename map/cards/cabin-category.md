# cabin_category — the per-line cabin product, on a TWO-layer cabin model

status: live
source: pg:cruise_v2.cabin_category (2,185 rows: 1,748 live + 437 soft-deleted, live 2026-08-18) · pg_indexes: uq_cabin_category_slug UNIQUE (slug) WHERE (deleted_at IS NULL) · pg:cruise_v2.cabin_class (7) · pg:cruise_v2.cabin_macro_category (36)

## What it is (and why it is shaped this way)

The cabin model is deliberately two layers. **Layer 1, universal:**
`cabin_class` — 7 buckets every line maps into; the cross-line search
axis. **Layer 2, per line:** `cabin_macro_category` (36) and
`cabin_category` (2,185) — the line's own product taxonomy down to the
bookable category with its code and slug. Search filters on Layer 1;
product pages and booking resolve Layer 2. The table is **soft-deleted**:
437 tombstones share the namespace, and slug uniqueness is a PARTIAL index
over live rows only — 72 slugs exist ONLY as tombstones. `\d` the table
before writing any resolver against it.

## Hits — if you change this

- Any slug-based resolver must carry `AND deleted_at IS NULL` — without
  it, a tombstone-only slug resolves to exactly one DELETED row, row-count
  guards never fire, and corroborating columns (a tombstone keeps its live
  twin's `code`) pass cleanly.
- The product page's "pick your cabin" grid derives from the SELECTED
  fare's lattice cells, not from this table's aggregate — a category
  change surfaces through prices (cards/departure-and-prices.md).
- `cv2_cabin_category` + `cv2_cabin_macro_category` project to D1
  (cards/d1-mirror.md); `unresolved_cabin_grade` (1 row) is the ingest's
  holding pen for codes that didn't resolve.

## Does not hit — the wrong neighbour

- **`cabin_class`.** Adding a line's new suite type goes in the LINE's
  layer (category/macro), not the universal 7-bucket axis — widening
  Layer 1 for one supplier breaks the cross-line filter contract.
- **UPDATE ... WHERE slug IN (...).** Slug is unique only among live rows;
  bulk writes key on the PK with rowcount asserts, or not at all.
