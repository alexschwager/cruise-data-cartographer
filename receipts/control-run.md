# Control run — 2026-08-19 — no walk instructions, verbatim, caveats kept

Protocol (borrowed with credit from a rival comp entrant, Cassini, whose
receipts include a naked-Claude control): a fresh model instance with NO
memory of the territory or this repo was handed the same product question
as cold walk 1 and the WHOLE repo — with **no instruction to use the
catalog, the one-rule, or any walk order**. "Do whatever you think is
best." The test: does the map's structure route a reader who was never
told to be routed — or does the two-hop discipline only work when
imposed? Its output is preserved verbatim below; the author's disposition
notes follow.

**Task given:** the wifi-included badge question, identical to cold walk 1
(where does the fact live / change path to the edge / tempting-wrong
place), full repo access, log every file read.

## The control's output (verbatim)

[The full output as returned, unedited:]

All answers were formed from the catalog + two cards before I opened the receipt; the receipt confirmed them (and revealed the cards I read had already absorbed that walk's fixes).

READ LOG (in order): directory listing; README.md; map/catalog.md; map/cards/fare-tier.md; map/cards/d1-mirror.md; receipts/cold-walk-1.md — read LAST, deliberately after answers were formed, as a cross-check.

(a) Where "what a fare includes" lives — cited from map/cards/fare-tier.md (routed there by the catalog's door): on the fare tier's inclusions axis — `cruise_v2.fare_tier` joined to items via `fare_tier_item`, drawing from the shared `inclusion` vocabulary. Critical refinement the card carries: `fare_tier_item_price` prices paid add-ons — a priced item is NOT "included." So "wifi included" = the wifi item present on the tier via `fare_tier_item` and unpriced. Tier-scoped: same ship, same sailing, different fare → different inclusions.

(b) Change path to the edge — from fare-tier.md (Hits) + d1-mirror.md: PG is truth; the CW-side sync engine is the one writer; the projection is SPLIT — `cv2_fare_tier` carries tier metadata only, the inclusion set travels as `cv2_inclusion` scoped rows resolved at read. A wifi badge is inclusion-shaped, so it is likely already at the edge — the ticket is a render change keying on unpriced items / `cv2_inclusion` kind, not a projection change. If a tier-level fact were needed instead: three wired steps (create + map + fetch-list; a table created + mapped but absent from the list "is never fetched/filled") plus the rebuild-gate watermark list; slotted tables addressed by logical name only; prod sync operator-gated.

(c) The tempting-but-wrong place — from fare-tier.md (Does-not-hit), corroborated by d1-mirror.md: the `offering` row. Secondary traps named: keying "included" on mere item presence; editing the shared `inclusion` vocabulary row (bleeds across every tier on every line); writing directly into D1 (overwritten by the next refill); assuming `cv2_fare_tier` carries the inclusion set (it doesn't — split projection).

TOKEN OF EFFORT: 5 files read. Strictly needed: 3 — catalog.md, fare-tier.md, d1-mirror.md (the second card was a sanctioned hop: the fare-tier card explicitly pointers to it for the edge mechanics). README was the entry point; the receipt was pure verification, deferred until after answering to keep the walk honest. The map's two-hop claim held: this repo answers a real product question in ~2-3 short markdown files instead of a schema spelunk.

WHAT CONFUSED OR MISLED ME: Nothing misled me — but the walk was pre-warmed. The README revealed that receipts/cold-walk-1.md is a prior cold walk of this identical question, and that the cards were patched from its defects. So my clean two-hop success is partly because the map already absorbed a previous walker's failure — the original walker reasonably guessed "fact → cv2_fare_tier → edge" and was wrong; the exact fact that now sits on the card I read. My walk validates the fixed map, not the map's virgin state. Mild door ambiguity (also flagged by the original walker, now mitigated): a presentation-anchored reader opens d1-mirror.md first — but that card now routes fact-questions upstream in its opening paragraph, so either entry point converges. One residual open point the map deliberately leaves to the live source: the exact `fare_tier_item` ↔ `inclusion` wire shape is recorded only in the receipt's disposition table, not on any card — an implementing engineer still needs a live `\d` before writing the query; the map says so on purpose (cite-never-copy), so this is a design choice, not a defect.

## Disposition (author)

| # | Finding | Disposition |
|---|---|---|
| 1 | An uninstructed reader converged on catalog → one card → stop unaided (5 read, 3 needed) | **The structural claim this control existed to test.** The doors route by shape, not only by obedience. Held. |
| 2 | The walk was pre-warmed — cards already carry cold-walk-1's fixes | **CONFIRMED, kept prominently.** This control validates the map as it stands, not its virgin state. The virgin state's failure is already on the record in cold-walk-1, defects kept — the two receipts together are the honest pair. |
| 3 | Door ambiguity (presentation vs fact anchoring) mitigated, not eliminated | **ACCEPTED AS RESIDUAL.** Both entry points now converge; a third receipt from a presentation-anchored walker would settle it. |
| 4 | The item↔inclusion wire shape lives only in a receipt, not a card | **NO CHANGE, by design.** Cite-never-copy: `\d`-level detail is the source's job. Recorded here so the choice stays visible. |

The same question now has two walks on the record: one that found the map
wrong and fixed it (cold-walk-1), one that tested whether the fixed map
routes a reader who was never told the rules (this file). The next receipt
should be a NEW question.
