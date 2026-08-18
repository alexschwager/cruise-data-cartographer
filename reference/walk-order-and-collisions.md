# Walk order, and this territory's naming collisions

## How a cold reader (or model) walks

1. Load `map/catalog.md`. Nothing else.
2. Find the door: catalog lines are phrased as the questions people actually
   ask ("where do prices live?"), each pointing at ONE card.
3. Open that one card. Read its status line first — a `ghost` or `leftover`
   answer to your question IS the answer.
4. Check *Does not hit* before acting — the wrong neighbour listed there is
   the one you were about to reach for.
5. Need the full column list or DDL? Go to the SOURCE the card cites
   (`\d table`, the named file). The card never carries it.
6. Stop. A follow-up question is a fresh walk from the catalog.

**Never** load `map/cards/` wholesale into a session. The map exists so you
don't have to.

## Naming collisions — write them down or relive them

- **"port" is not port.** The canonical port table is
  `public.ports_master` (cross-vertical). `cruise_v2` has NO port table —
  yet internal agent manifests still say "cruise_v2.port", and the D1
  mirror's `ports_master` "was cv2_port, renamed in the port cutover"
  (`sync/sync_engine.py:189`). Three names, one object, one of them stale.
- **"region" is three namespaces.** `cruise_v2.sub_region` (46 rows —
  maritime cruise regions, the one `ports_master.sub_region_id` actually
  FKs, verified in `pg_constraint`); `public.subregions` (146 rows — a
  DIFFERENT, non-cruise geo axis); `public.regions` (26,688 rows — the
  hotel/zone geo spine). Joining by name instead of by FK here has
  historically "faked corruption."
- **"cv2_" does not always mean cruise-only.** Most `cv2_*` D1 tables are
  cruise projections; `ports_master` in D1 carries no prefix precisely
  because it is cross-vertical. Prefix is a hint, not a boundary.
- **"empty" is not one thing.** `staging.msc_live_fare` (0 rows) is wired
  and awaiting a gated refill; `destination_supplier_codes` (0 rows) is a
  ghost no code has ever read. Same row count, opposite meanings — the
  status taxonomy exists for this.
- **"slot" tables are not tables you query by name.** `cv2_search_card` is
  a logical name resolved to a physical `_a`/`_b` slot by the active-slot
  pointer at read time. Querying `cv2_search_card_a` directly answers a
  question about a coin flip.
