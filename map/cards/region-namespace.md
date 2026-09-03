# "region" — one word, three namespaces (namespace card)

status: live
source: pg:cruise_v2.sub_region (46 rows) · pg:public.subregions (146) · pg:public.regions (26,688) · pg:public.cruise_line_subregions (550) — live 2026-08-18

## What it is (and why it is shaped this way)

Three unrelated geo systems share the word:
1. **`cruise_v2.sub_region` (46)** — maritime cruise regions
   (Mediterranean, Caribbean...). The one `ports_master.sub_region_id`
   actually FKs. The cruise search/rollup axis.
2. **`public.subregions` (146)** — a different, non-cruise sub-national
   geo axis. Similar name, overlapping id range, wrong world.
3. **`public.regions` (26,688)** — the hotel/zone geo spine (with
   `hotelbeds_zones`, `accommodation_zone_coverage` beside it).
They coexist because cruise geography is maritime (basins and coasts)
while hotel geography is administrative (countries and zones) — one
hierarchy genuinely cannot serve both. `cruise_line_subregions` (550) maps
each line's own marketing regions onto axis 1.

## Hits — if you change this

- Axis 1 changes reshape cruise search facets, destination rollups, and
  the `cv2_sub_region` D1 projection — and via `ON DELETE SET NULL` on
  ports_master, a deleted sub_region silently un-regions its ports.
- Axis 3 changes belong to the hotel/zone pipeline entirely — nothing
  cruise reads them.
- **To add a maritime region** (e.g. Norwegian Fjords): INSERT one row into
  `cruise_v2.sub_region` (`\d cruise_v2.sub_region` for columns), then
  attach ports via `ports_master.sub_region_id`. Check the 46 live rows
  first — the region may already exist.

## Does not hit — the wrong neighbour

- **Joining `ports_master.sub_region_id` to `public.subregions`.** The
  name says yes; `pg_constraint` says no. Ids overlap enough that the join
  RUNS and returns plausible garbage — the documented way this territory
  fakes "corruption." Always resolve region joins from the FK definition,
  never the table name.
- **Adding a region to `cruise_line_subregions` instead.** That table (550)
  maps a LINE's own marketing region names onto axis 1 — it is not the
  canonical axis. A new maritime region goes in `cruise_v2.sub_region`
  first; a line's marketing label for it is a *later, separate* row here.
