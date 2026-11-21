# Test Report – Day 27

## Execution result

- Automated tests: **10 passed, 0 failed**.
- End-to-end sample pipeline: **PASSED**.
- Sample source: 6 sales rows; 4 accepted and 2 rejected by the configured validation rules.
- Post-load quality checks: **4/4 passed** (all batch records loaded, no duplicate sale IDs, positive amounts, customer IDs present).
- Incremental/idempotency test: loading the same sale twice leaves one row for that sale ID.

## Test coverage

- Valid record acceptance and customer enrichment
- Unknown customer rejection
- Zero/negative and nonnumeric amount rejection
- Invalid date rejection
- Duplicate and missing sale ID rejection
- Missing input file error handling
- Idempotent incremental upsert
- Post-load quality check for the current batch

Run with `python -m unittest discover -s tests -v`.

## False-positive / false-negative evaluation

The labelled synthetic fixture reported: **TP=6**, **TN=2**, **FP=0**, **FN=0**, across 8 cases (accuracy 1.0). A false positive means a valid row was rejected; a false negative means an invalid row was accepted. This is a small deterministic rule test, not a claim about production-wide accuracy.

## Windows SQLite connection fix

The initial run exposed two test cleanup errors because SQLite connection context managers commit/rollback but do not close the connection. The loader and quality-check modules now explicitly close connections using `contextlib.closing`, while retaining transaction handling. This releases database file handles before temporary test directories are removed on Windows. CSV test readers also use context managers to close files cleanly.
