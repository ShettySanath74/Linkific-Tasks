
-- Day 11: Slowly Changing Dimension Type 2
-- Demonstration: Priya moves from Mangaluru to Bengaluru.
-- Run in ecommerce_warehouse.

BEGIN;

-- 1. Close the existing current version.
UPDATE dim_customer
SET effective_end_date = DATE '2026-10-24',
    is_current = FALSE
WHERE customer_id = 102
  AND is_current = TRUE
  AND city <> 'Bengaluru';

-- 2. Insert a new version only if the change was applied.
INSERT INTO dim_customer (
    customer_id,
    first_name,
    last_name,
    email,
    city,
    effective_start_date,
    effective_end_date,
    is_current
)
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    'Bengaluru',
    DATE '2026-10-25',
    DATE '9999-12-31',
    TRUE
FROM dim_customer
WHERE customer_id = 102
  AND is_current = FALSE
  AND effective_end_date = DATE '2026-10-24'
  AND NOT EXISTS (
      SELECT 1
      FROM dim_customer current_customer
      WHERE current_customer.customer_id = 102
        AND current_customer.is_current = TRUE
  )
ORDER BY customer_key DESC
LIMIT 1;

COMMIT;
