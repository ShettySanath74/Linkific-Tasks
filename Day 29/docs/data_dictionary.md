# Data Dictionary

## Instructions
Populate this dictionary from the real Day 28 CSV headers and Power BI model. The entities below are suggested by the known project file names; column names and definitions must be verified rather than assumed.

## Dataset inventory
| Dataset | Purpose | Primary key (verify) | Foreign keys (verify) |
|---|---|---|---|
| customers.csv | Customer information | To confirm | To confirm |
| orders.csv | Order header / transaction information | To confirm | Customer key to confirm |
| order_items.csv | Product lines within orders | To confirm | Order and product keys to confirm |
| products.csv | Product catalogue | To confirm | To confirm |

## Column-level dictionary template
| Dataset | Column | Data type | Definition | Nullable? | Example | Validation rule |
|---|---|---|---|---|---|---|
| Fill in | Fill in | Fill in | Business meaning | Yes/No | Safe sample | Verified rule |

## Required checks
- Identify unique keys and test uniqueness.
- Identify foreign-key relationships and test referential integrity.
- Confirm date, numeric, and categorical data types.
- Document allowed nulls and business-approved defaults.
- Define currency, timezone, units, and calculation conventions.
- Document any derived fields and their formulas.

## Important
Do not infer business meaning from a column name alone. Confirm definitions against the transformation code and project requirements.
