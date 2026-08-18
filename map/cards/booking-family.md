# booking family — real money, real people, and a standing SELECT exclusion (access-rule card)

status: live
source: pg:cruise_v2.booking (405 rows) · pg:cruise_v2.booking_guest (665) · pg:cruise_v2.payment (404) · pg:cruise_v2.booking_price_line (242) · pg:cruise_v2.manage_session (44) · pg:cruise_v2.manage_otp (72) — live 2026-08-18 (counts via pg_stat, no rows read)

## What it is (and why it is shaped this way)

Live production bookings: `booking` → its `booking_price_line`s (the
priced components), `payment` (+ `payment_transaction`, currently 0 —
wired, awaiting its flow), `booking_guest` (traveller PII), and the
manage-trip surface (`manage_session`, `manage_otp` — OTP gates cancel
only, by doctrine). The standing rule that IS this card:
**`booking_guest` and any PII-bearing table are SELECT-excluded for
automated sessions.** Shape may be introspected; rows are never read.
Row counts here come from `pg_stat_user_tables`, which is the sanctioned
way to know "is it populated" without touching a row.

## Hits — if you change this

- Price lines are settlement-currency records — the client pays the
  settlement amount; display projections never sum across currencies.
- Booking writes come from live supplier flows; test bookings follow the
  named authorization rules per line (real assigned cabins, agents never
  cancel) — schema changes here change what live money flows write.
- The manage-trip surface reads this family through capability gates —
  a column rename ripples into those tokens/gates, not just queries.

## Does not hit — the wrong neighbour

- **Analytics on guests.** Any "how many guests did X" question that needs
  rows is off-limits to automated sessions — aggregate via pg_stat or
  hand the query to the operator.
- **`staging.*` supplier feeds** — despite carrying booking-ish fields,
  nothing there is a booking; bookings exist only here.
