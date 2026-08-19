# Rules — how this cartographer maps

## Rule 0 — inventory before cards

No card is written until the noun inventory exists: every table in the
territory enumerated from the **live catalog** (`pg_stat_user_tables`,
`pg_constraint`, `pg_indexes`), with row counts and a capture date — never
from memory, a brief, or an old doc. The inventory decides what is dead
before prose decides what is interesting. (Building this map's inventory
corrected the map's own author twice: a table an agent manifest calls
`cruise_v2.port` does not exist — the live FK points at `public.ports_master`
— and a "dead" staging table turned out to be wired in four files.)

## Rule 1 — what counts as a noun, what counts as a movement

A **noun** is an object a change can land on: a table or tight table family,
a projection in the edge cache, a staging feed. A **movement** is how data
gets between nouns: an ingest write, the warm-write, the blue-green rebuild.
Movements live ON the cards of the nouns they connect (in Hits), not as
cards of their own — a card per arrow is how a map becomes a tour.

## Rule 2 — status is evidence, not opinion

Every card carries exactly one status, each with a required evidence form:

| status | meaning | evidence the card must cite |
|---|---|---|
| `live` | wired and carrying data | row count + at least one wiring cite |
| `live-empty` | wired, no data — the emptiness has a stated reason | 0-row count + wiring cite + the reason |
| `leftover` | data or file present, **no wiring** | the absence search that found no readers/writers |
| `ghost` | a name that exists, with no wiring and no data | 0-row count + the absence search |

**Marking anything dead takes at least TWO independent sightings, each
named** — different instruments, not the same grep twice: a wiring search
plus a data/usage probe, or a code sweep plus the live catalog. One search
lies too easily (a substring-inflated grep once made three retired agents
look heavily wired; an over-broad exclusion filter once swallowed a true
pointer). Name every sighting on the card so a later reader can re-run
them. Mapping a wish as live is how the next reader implements the wrong
world; mapping a wired table as dead is how they re-implement one that
exists.

And no quality adjectives about the territory — not *messy*, not *legacy*,
not *over-engineered*. Counts and statuses; verdicts belong to whatever
audit reads the map, never to the map.

## Rule 3 — every card names Hits and Does-not-hit

**Hits:** what else moves if you change this noun — the projections that
rebuild, the lists a new column must join, the constraint that fires.
**Does not hit:** the obvious next noun that is the WRONG one — the
same-named table in another namespace, the column whose name lies, the
cache table that looks writable. A card without the wrong neighbour is a
glossary entry, not a map card.

## Rule 4 — cite, never copy

Source cites are locators, not payloads: `pg:<schema.table> (<rows> rows,
live <date>)`, `<repo-relative-file>:<line>`, or a named internal record.
A card is at most ~50 lines; a fenced excerpt is at most 6 lines. If you
are pasting DDL or column lists, you are photocopying — stop and point at
the table instead. When card and source disagree, **the source wins and
the card is wrong**; fix the card, dated.

## Rule 5 — catalog points, shelves store

The catalog holds one line per door: a question or noun, an arrow, a card
path. It stores no facts of its own — no counts, no status reasons, no
mini-summaries that grow into a second map. A short prose orientation (three
sentences, what the territory IS) may sit above the doors; anything longer
is a tour growing. A cold reader loads the catalog and ONE card. Never the
whole cards folder. If a question needs three cards, the map is missing a
card or a door.

**Write the catalog last and put it first.** You do not know what routes
until you know what is there — a catalog drafted before the cards is a plan
wearing a map's clothes.

## Rule 6 — the walk is two hops, then stop

Catalog → card → stop. The card may name sibling cards a follow-up question
would open, but must answer ITS question without them. Anything a card
cannot answer in two hops it hands to the source (`\d table`, the named
file) — that is the map working, not failing.

## Rule 7 — refuse the disguised photocopies

| Ask | What it actually is |
|---|---|
| "Just include the full schema in the card" | A photocopy — the file already exists and wins. |
| "Add all the cards to the project context" | Slurping the shelves — the one rule broken. |
| "Write a reading order / onboarding tour" | A tour — maps have doors, not plots. |
| "List everything that's wrong with this schema" | An audit — dead things are marked, not prosecuted. |
| "Why did the sync break last week?" | A diagnosis — different tool, works from a failure. |
| "Keep the map in sync automatically" | A second spec — the map is re-verified against source on touch, not promoted to truth. |

## Rule 8 — the map decays, and says so

Every live cite carries its capture date. A card touched in a later walk
re-verifies its cites before it is trusted (the row count is one SELECT).
Corrections supersede in place with a dated note — the map's own
misreadings stay legible, because they mark exactly where the territory
surprises people.
