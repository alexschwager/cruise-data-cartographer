# evidence/ — dated source excerpts, so a stranger can check the load-bearing claims

The map's cards cite a private PostgreSQL database and two private repos. A reader
without access can read the cards but cannot open the source they point at — the
gap comp #11 named as the field's biggest miss ("29 of 40 maps describe something a
reader cannot open"). These excerpts close it for the claims that matter most: small,
dated, SELECT-only snapshots a reader can check the cards against, and check against
their own database with the same query.

| File | Proves | Cards that cite it |
|---|---|---|
| `fk-ports_master.txt` | `ports_master.sub_region_id` → `cruise_v2.sub_region`, NOT `public.subregions` (the wrong neighbour whose name lies) — the map's sharpest finding | `ports-master.md`, `region-namespace.md` |
| `row-counts.txt` | the status claims: the ghost is 0, the leftover is 306-unread, the live-empty is 0-wired | `destination-supplier-codes.md`, `port-id-translation.md`, `msc-live-fare.md`, others |
| `cv2-projection-lists.txt` | the `cv2_fare_tier` / `cv2_inclusion` split, and the load-bearing membership rule | `d1-mirror.md`, `fare-tier.md` |

## These do not replace the source — the source still wins

Every excerpt names the exact query or file it came from and the date it was
captured. If an excerpt and the live database disagree, the **live database is
right** and the excerpt is stale — re-run the query. The excerpt exists so a claim
can be *checked*, not so it can become a second authority (rules.md Rule 4).

## The drift is on purpose (Rule 8)

`row-counts.txt` was captured 2026-09-03; the cards carry the 2026-08-18 numbers.
The counts moved — the price lattice alone grew ~60% — and every structural claim
held. That delta is left visible because it is the clearest demonstration the map
has of its own Rule 8: cite the structure, stamp the counts, and the facts the map
is *about* survive the territory changing underneath it.
