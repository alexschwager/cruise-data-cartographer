# ports_master — THE port table (there is no cruise_v2.port)

status: live
source: pg:public.ports_master (2,004 rows, live 2026-08-18) · pg_constraint: fk_ports_master_sub_region FOREIGN KEY (sub_region_id) REFERENCES cruise_v2.sub_region ON DELETE SET NULL · pg_constraint on cruise_v2.itinerary_stop: fk_itinerary_stop_port_id → ports_master(id)

## What it is (and why it is shaped this way)

The single cross-vertical port master, in `public` because ports serve
every vertical, not just cruise. Cruise itineraries FK straight into it
(`itinerary_stop.port_id`, verified live). Maritime geography is mapped
AT THE PORT: each port carries its ONE `sub_region_id` into
`cruise_v2.sub_region` — destinations and rollups derive from the ports a
sailing visits, which is why repositioning and world cruises need tagging
rather than a region column of their own.

## Hits — if you change this

- Everything that renders geography: itinerary stops (60,461 rows FK
  here), destination rollups, the D1 `ports_master` mirror
  (cards/d1-mirror.md — note: unprefixed there because it is
  cross-vertical, "was cv2_port, renamed in the port cutover",
  `sync/sync_engine.py:189`).
- Port images: `image_entity` rows target ports by id; supplier port codes
  resolve through cards/port-supplier-mappings.md before ever touching
  this table.
- `ON DELETE SET NULL` on the sub-region FK means deleting a sub_region
  silently un-regions its ports — no error, just NULLs.

## Does not hit — the wrong neighbour

- **`cruise_v2.port`** — does not exist. Internal manifests still name it;
  the live FK graph says `ports_master`. Trust `pg_constraint`, not prose.
- **`public.subregions`** — despite the name, `sub_region_id` does NOT
  point there. Joining it "works" (ids overlap) and returns garbage that
  has historically read as data corruption. The real target is
  `cruise_v2.sub_region` (cards/region-namespace.md).
