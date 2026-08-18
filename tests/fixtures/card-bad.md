# everything_about_prices — the complete price documentation

## Overview

This card documents the entire pricing system so you never have to look
at the database. Here is the full table definition:

```sql
CREATE TABLE cruise_v2.departure_cabin_fare_price (
    price_id bigint PRIMARY KEY,
    departure_id bigint NOT NULL,
    cabin_category_id bigint NOT NULL,
    fare_tier_id bigint NOT NULL,
    occupancy text NOT NULL,
    market_code text NOT NULL,
    currency char(3) NOT NULL,
    amount numeric(12,2),
    taxes numeric(12,2),
    fees numeric(12,2),
    updated_at timestamptz DEFAULT now()
);
```

## All the columns explained

- price_id: the id of the price
- departure_id: the id of the departure
- cabin_category_id: the id of the cabin category
- fare_tier_id: the id of the fare tier
- occupancy: the occupancy
- market_code: the market code
- currency: the currency
- amount: the amount
- taxes: the taxes
- fees: the fees
- updated_at: when it was updated

## How the week goes

First the ingest runs on Monday, then prices update through the week, and
by Friday the cache has usually rebuilt a few times. New team members
should read this card top to bottom before touching anything, then read
all the other cards in order.
