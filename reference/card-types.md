# Card types — the closed set

Four card types. A new card must be one of these; a card that wants a fifth
type is usually a movement trying to become a noun (see rules.md Rule 1).

## 1. Noun card (the default)
One table or one tight table family (a spine table plus its `_supplier_codes`
/ item / price satellites). Sections, in order:

```
# <noun> — <one-line>
status: live | live-empty | leftover | ghost
source: <locator> · <locator> ...

## What it is (and why it is shaped this way)
## Hits — if you change this
## Does not hit — the wrong neighbour
```

`leftover` and `ghost` cards add `## Evidence of absence` (the search a
reader can re-run). `live-empty` states its reason in *What it is*.

## 2. Namespace card
For a WORD, not a table — when one name spans several objects and the
collision itself is the hazard ("region", "port"). Same sections; the
*What it is* disambiguates the namespaces; *Does not hit* names the
default-wrong resolution.

## 3. Mirror card
For an edge-cache projection family (the D1 `cv2_*` tables). Adds the
ownership line — who writes it, who must never — and the wiring steps a
new projection needs (the load-bearing list problem). Same sections
otherwise.

## 4. Access-rule card
For an object whose primary fact is a standing restriction (PII exclusion,
operator-only writes). The restriction is the *What it is*; *Hits* covers
what the restriction implies for queries and tooling.

## Status taxonomy (evidence rules in rules.md Rule 2)
`live` → wired + data. `live-empty` → wired, no data, reason stated.
`leftover` → data present, wiring absent (honest residue). `ghost` → name
present, wiring and data absent (tripwire).
