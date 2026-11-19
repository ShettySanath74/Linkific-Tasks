# Implementation notes

## Transformation
- Text fields are trimmed.
- Quantity is converted to integer; unit price to float; dates/timestamps are parsed.
- Sales are joined to customer and product lookup dictionaries.
- Revenue is calculated as quantity × unit price.
- Daily/category aggregates calculate order count, units and revenue.

## Quality
- Header validation verifies required columns.
- Transform stage rejects missing keys, invalid types, non-positive quantities, negative prices, invalid dates, invalid booleans and broken customer/product references.
- Duplicate order IDs are detected before loading.

## CDC and loading
- SHA-256 over normalized transformed records is the change signature.
- `source_state` stores the latest signature and deletion state.
- SQLite `INSERT ... ON CONFLICT DO UPDATE` implements upsert.
- `is_deleted` is a soft-delete flag, preserving history in the target.
- Missing source rows are deleted only under the documented full-snapshot assumption.

## Reliability
- Pipeline logs to console and `logs/pipeline.log`.
- Database load uses a transaction.
- Retry decorator retries a failed operation up to three times.
- Optional SMTP email alert is sent on pipeline failure when configured.
- Unit and integration tests use `unittest`.
