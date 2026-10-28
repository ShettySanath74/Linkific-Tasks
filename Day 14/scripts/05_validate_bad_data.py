from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower

spark = (
    SparkSession.builder
    .appName("Day14-Negative-Quality-Tests")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/sales_invalid.csv")
)

print("\n--- Invalid Test Dataset ---")
df.show()

# Check duplicate order IDs
duplicate_ids = (
    df.groupBy("order_id")
    .count()
    .filter(col("count") > 1)
    .count()
)

# Check null or blank customer names
missing_customers = df.filter(
    col("customer").isNull()
    | (trim(col("customer")) == "")
).count()

# Check non-positive quantities
invalid_quantities = df.filter(
    col("quantity").isNull() | (col("quantity") <= 0)
).count()

# Check negative unit prices
invalid_prices = df.filter(
    col("unit_price").isNull() | (col("unit_price") < 0)
).count()

checks = [
    ("Duplicate order IDs", duplicate_ids, 1),
    ("Missing customer names", missing_customers, 1),
    ("Invalid quantities", invalid_quantities, 1),
    ("Negative unit prices", invalid_prices, 1),
]

print("\n--- Negative Test Results ---")

all_detected = True

for name, actual_count, expected_count in checks:
    passed = actual_count == expected_count
    status = "PASS" if passed else "FAIL"
    print(
        f"[{status}] {name}: "
        f"detected={actual_count}, expected={expected_count}"
    )
    if not passed:
        all_detected = False

print(
    "\nOverall test result:",
    "PASS" if all_detected else "FAIL"
)

spark.stop()

