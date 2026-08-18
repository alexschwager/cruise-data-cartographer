# Cold walk 1 — 2026-08-18 — verbatim, defects kept

Protocol: a fresh model instance with NO memory of the territory or this
repo was handed the task below, permitted to read `map/catalog.md` plus AT
MOST ONE card, and instructed that finding defects is a success condition.
Its output is preserved verbatim; the disposition table at the end records
what happened to each defect and was written by the map's author afterward.

**Task given:** "Product wants a 'wifi included' badge on cruise search
results. Which single card do you open? Based on the catalog + that one
card only: (a) where does 'what a fare includes' live, (b) what is the
change path for getting a new fact onto search results at the edge, and
(c) what is the tempting-but-wrong place a naive developer would put this?"

## The walker's output (verbatim)

1. WALK LOG
- map/catalog.md
- map/cards/fare-tier.md

2. ANSWERS

(a) Where "what a fare includes" lives — from cards/fare-tier.md: the inclusions axis of `pg:cruise_v2.fare_tier`, concretely the `fare_tier_item` join table (598 rows) linking tiers to items from the shared `inclusion` vocabulary (2,157 rows). Wifi-included is a tier-level fact: which items (drinks, wifi, gratuities) a tier carries via `fare_tier_item`. The catalog's door text ("What is a fare / a promo / 'what's included'? → cards/fare-tier.md") routed me here unambiguously.

(b) Change path for a new fact onto search results at the edge — from cards/fare-tier.md, "Hits" section: search-card facts (what's included, deal badges) derive from fare tiers, not the offering, and reach the storefront via the `cv2_fare_tier` projection into the D1 mirror (the card names the projection and points at cards/d1-mirror.md). So the path is: fact on the tier (fare_tier / fare_tier_item in PG) → `cv2_fare_tier` projection → D1 mirror → storefront card. The catalog corroborates that the edge is D1 ("What does the storefront actually read? What mirrors to D1?").

(c) Tempting-but-wrong place — from cards/fare-tier.md, "Does not hit" section, which names it explicitly: the `offering` row. A naive developer would put "wifi included" on the cruise offering, but inclusions are tier-scoped per line — same ship, same sailing, different fare, different inclusions — so an offering-level badge would be wrong whenever a sailing sells multiple fares. Secondary trap, also named on the card: editing the shared `inclusion` vocabulary row, which bleeds across every tier on every line.

3. DEFECTS

- The `cv2_fare_tier` projection is named but underspecified. The card tells me search cards derive from tiers "via the `cv2_fare_tier` projection (cards/d1-mirror.md)" — but not whether that projection already carries the item/inclusion set or only tier name + deal/theme tags. That is exactly the load-bearing fact for this task: if `cv2_fare_tier` doesn't project inclusions today, the change path includes widening the projection (a sync-engine change), which is a very different ticket from "the data's already at the edge, just render it." I was strongly tempted to open cards/d1-mirror.md for precisely this, and under the one-card rule I cannot say which side of that line reality is on. One clause on the fare-tier card ("the projection carries columns X, Y; item sets are/are not projected") would have closed it.
- Catalog door ambiguity: for this question two doors plausibly apply — fare-tier ("what's included") and d1-mirror ("what does the storefront actually read"). A reader anchoring on "badge on search results" (presentation) rather than "wifi included" (fact) picks d1-mirror first and may then lack the offering-vs-tier trap. The doors resolved correctly for me only because the catalog literally quotes "what's included" on the fare-tier line — good, but the d1-mirror line could cross-reference "card facts come from fare tiers" to make either entry point safe.
- Minor: the card says wifi is an item "via `fare_tier_item`" but never states how items relate to the `inclusion` vocabulary (FK? free text + code?). `fare_tier_item_price` (260 rows) appears in the source line and is never explained — is a priced item still "included"? For a badge that claims "included," paid-add-on vs bundled matters, and the card is silent.

4. VERDICT

YES — with a caveat. Two hops answered (a) and (c) crisply and gave the shape of (b), including the projection name and the offering trap. But the last mile of (b) — whether the inclusion set is already projected to D1 or the sync must be extended — is genuinely unresolvable without a third file, and that's the fact Product's engineer needs on day one.

## Disposition (author, after grounding each defect against source)

| # | Defect | Disposition |
|---|---|---|
| 1 | `cv2_fare_tier` projection contents unstated | **CONFIRMED + FIXED.** Grounded against `sync/schema_mapper.py:1569` + the cache DDL: `cv2_fare_tier` carries tier metadata ONLY; inclusions travel separately as `cv2_inclusion` scoped rows resolved at read. The fare-tier card now states the split. The walker's guess ("fact → cv2_fare_tier → edge") was reasonable and WRONG — exactly the gap it reported. |
| 2 | d1-mirror door unsafe as an entry point for fact-questions | **CONFIRMED + FIXED.** The d1-mirror card now routes fact-questions upstream to fare-tier in its opening section. |
| 3 | `fare_tier_item` vs `inclusion` relation + paid-vs-included unstated | **CONFIRMED + PARTIALLY FIXED.** The paid-vs-included hazard is now on the fare-tier card (`fare_tier_item_price` = paid add-ons). The full item↔inclusion wire shape (item_code text keys, market/applicability scoping — read live 2026-08-18) is deliberately NOT expanded onto the card: that is `\d`-level detail the source owns. Recorded here instead. |
