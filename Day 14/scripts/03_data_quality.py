from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when

spark = (
    SparkSession.builder
    .appName("Day14-Data-Quality")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/sales.csv")
)

results = []

def record_check(name, passed, details):
    status = "PASS" if passed else "FAIL"
    results.append((name, status, details))
    print(f"[{status}] {name}: {details}")

# 1. Dataset is not empty
record_check(
    "Non-empty dataset",
    df.limit(1).count() > 0,
    "At least one record exists"
)

# 2. Required columns contain no null values
required_columns = [
    "order_id", "customer", "category",
    "quantity", "unit_price"
]

null_conditions = [
    count(when(col(c).isNull(), 1)).alias(c)
    for c in required_columns
]

null_counts = df.agg(*null_conditions).first().asDict()
null_total = sum(null_counts.values())

record_check(
    "Required fields",
    null_total == 0,
    f"Total missing values: {null_total}"
)

# 3. Order IDs are unique
duplicate_count = (
    df.groupBy("order_id")
    .count()
    .filter(col("count") > 1)
    .count()
)

record_check(
    "Unique order IDs",
    duplicate_count == 0,
    f"Duplicate ID groups: {duplicate_count}"
)

# 4. Quantities must be positive
invalid_quantity_count = df.filter(
    col("quantity").isNull() | (col("quantity") <= 0)
).count()

record_check(
    "Positive quantities",
    invalid_quantity_count == 0,
    f"Invalid records: {invalid_quantity_count}"
)

# 5. Unit prices must not be negative
invalid_price_count = df.filter(
    col("unit_price").isNull() | (col("unit_price") < 0)
).count()

record_check(
    "Non-negative unit prices",
    invalid_price_count == 0,
    f"Invalid records: {invalid_price_count}"
)

# Create a validation report
report = spark.createDataFrame(
    results,
    ["check_name", "status", "details"]
)

print("\n--- Data Quality Report ---")
report.show(truncate=False)

report.write.mode("overwrite").option(
    "header", True
).csv("outputs/data_quality_report")

print("Validation report saved to outputs/data_quality_report")

spark.stop()

