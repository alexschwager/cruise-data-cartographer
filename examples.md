# Examples — one worked walk, one change, one ghost

The full worked map is `map/` (13 cards). These are walks through it,
showing the two-hop discipline — not additional map content.

## Walk 1 — a cold model asks: "where do prices live?"

**Hop 1** — load `map/catalog.md` only. Under *The product spine*:
"Where do prices actually live? → cards/departure-and-prices.md".

**Hop 2** — open that one card. It answers: prices attach at two grains
under `departure` — the 1.3M-row lattice
(`departure_cabin_fare_price`) for checkout and `departure_market_price`
for search — and its *Does not hit* preempts the two wrong reaches
(`offering` has no money; `fare_tier_item_price` prices add-ons, not
cruises).

**Stop.** The model never loaded the other twelve cards, and if it needs
the column list it runs `\d cruise_v2.departure_cabin_fare_price` — the
source, which wins.

## Walk 2 — a change: "add a 'wifi included' badge to search cards"

Catalog door: "What is a fare / what's included? → cards/fare-tier.md".
The card's *Hits* says card-level inclusion facts derive from fare tiers
and reach the storefront via the `cv2_fare_tier` projection — and points
at cards/d1-mirror.md, whose *Hits* names the three wired steps a
projection change needs (create + map + fetch-list) and the engine's own
warning that two of three manufactures a ghost at the edge. The change
plan falls out: tier item data → projection column → all three sync steps.
**What it does not hit,** per the cards: `offering` (the reflexive wrong
home for "included"), and D1 directly (the mirror is never written by
hand).

## Walk 3 — the ghost answers a question by being a ghost

"How do supplier destination codes resolve?" Catalog: *Dead and undead* →
cards/destination-supplier-codes.md. Status line: **ghost** — 0 rows,
0 code references, searches cited in the card. The answer to the question
is that the mechanism doesn't exist: destinations derive from port
geography (the card hands you the two live cards for that). A reader who
skipped the status line and "populated" the table would have implemented
the wrong world — which is exactly what the ghost marking is for.

## The refusal

**Reader:** "This is great — just load all the cards into my project so
I have the whole picture."

**Cartographer:** "That's the one rule. The catalog is 30 lines — load
that. Open the card your question names, and stop. The whole picture is
the territory's job; the map's job is doors. If you find a question the
catalog can't door in one hop, THAT is a defect — tell me and the catalog
grows a line, not your context."
