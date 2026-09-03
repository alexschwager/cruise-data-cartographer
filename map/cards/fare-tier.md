# fare_tier — a line's fare product: inclusions on one axis, promo identity on the other

status: live
source: pg:cruise_v2.fare_tier (78 rows) · pg:cruise_v2.fare_tier_item (598) · pg:cruise_v2.fare_tier_item_price (260) · pg:cruise_v2.fare_tier_supplier_codes (74) — live 2026-08-18 · checkable: evidence/cv2-projection-lists.txt (the fare_tier/inclusion split)

## What it is (and why it is shaped this way)

A fare tier is a cruise line's named fare product ("All Inclusive",
"Christmas Special"). It deliberately carries TWO independent identity
axes that must never be collapsed: the **inclusions axis** (which items —
drinks, wifi, gratuities — via `fare_tier_item`) and the **promo axis**
(the named offer). Two fares with byte-identical item sets can be
DIFFERENT fares (same inclusions, different promotion); deduping on items
alone merges promotions a supplier keeps distinct. `_supplier_codes` maps
each supplier's raw fare code onto the normalized tier.

## Hits — if you change this

- **Search cards.** The storefront's card-level facts (what's included,
  deal badges) derive from fare tiers, not from the offering. At the edge
  the projection is SPLIT: `cv2_fare_tier` carries tier metadata ONLY
  (slug/name/blurb/badge/availability — `sync/schema_mapper.py:1569`,
  read 2026-08-18), while the inclusion set travels separately as
  `cv2_inclusion` scoped rows the worker resolves at read. An
  inclusion-shaped fact is usually already at the edge; a tier-level fact
  may need the projection widened (cards/d1-mirror.md).
- **"Included" vs paid add-on.** `fare_tier_item_price` prices PAID
  add-ons; a priced item is not "included" — any included-badge logic
  keys on unpriced items / `cv2_inclusion` kind, never on mere item
  presence.
- The price lattice keys on tier: a new/renamed tier changes which
  `departure_cabin_fare_price` cells exist (cards/departure-and-prices.md).
- `deal_tag` (6) and `theme` (4) hang classification off tiers — "is this
  a deal / a thematic cruise" is decided here, per doctrine, never by
  cross-currency price comparison.

## Does not hit — the wrong neighbour

- **`offering`.** The reflexive place to put "what's included" is the
  offering row; inclusions are tier-scoped, per line — same ship, same
  sailing, different fare, different inclusions.
- **`inclusion` (2,157 rows)** is the shared vocabulary of includable
  items, not a fare — editing an inclusion's definition touches every
  tier that references it, across lines.
