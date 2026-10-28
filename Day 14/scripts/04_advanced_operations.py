from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    col, sum as spark_sum, row_number, rank, udf
)
from pyspark.sql.types import StringType

spark = (
    SparkSession.builder
    .appName("Day14-Advanced-PySpark")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

# Sample orders
orders = [
    (101, "Aarav", "Electronics", 30000),
    (102, "Diya", "Furniture", 12000),
    (103, "Rohan", "Electronics", 15000),
    (104, "Isha", "Clothing", 4000),
    (105, "Kabir", "Furniture", 15000),
]

orders_df = spark.createDataFrame(
    orders, ["order_id", "customer", "category", "revenue"]
)

# Customer lookup table
customers = [
    ("Aarav", "Bengaluru"),
    ("Diya", "Mysuru"),
    ("Rohan", "Mangaluru"),
    ("Isha", "Udupi"),
    ("Kabir", "Bengaluru"),
]

customers_df = spark.createDataFrame(
    customers, ["customer", "city"]
)

print("\n--- Join orders with customer locations ---")
joined_df = orders_df.join(
    customers_df, on="customer", how="inner"
)
joined_df.show()

# Window function: rank orders within each category
window_spec = Window.partitionBy("category").orderBy(
    col("revenue").desc()
)

print("\n--- Rank orders within each category ---")
ranked_df = orders_df.withColumn(
    "category_rank", row_number().over(window_spec)
)
ranked_df.show()

# Window function: cumulative revenue by category
cumulative_window = (
    Window.partitionBy("category")
    .orderBy("order_id")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
)

print("\n--- Cumulative revenue by category ---")
orders_df.withColumn(
    "cumulative_revenue",
    spark_sum("revenue").over(cumulative_window)
).show()

# User-defined function (UDF)
def revenue_label(amount):
    if amount >= 20000:
        return "High"
    elif amount >= 10000:
        return "Medium"
    return "Low"

revenue_udf = udf(revenue_label, StringType())

print("\n--- Revenue classification using UDF ---")
orders_df.withColumn(
    "revenue_level", revenue_udf(col("revenue"))
).show()

spark.stop()

