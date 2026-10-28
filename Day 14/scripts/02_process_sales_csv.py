from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, count

spark = (
    SparkSession.builder
    .appName("Day14-Sales-CSV-Processing")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Read CSV with header and inferred data types
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/sales.csv")
)

print("\n--- CSV Data ---")
df.show()

print("\n--- Data Types ---")
df.printSchema()

# Calculate total revenue per order
sales_df = df.withColumn(
    "revenue",
    col("quantity") * col("unit_price")
)

print("\n--- Revenue by Order ---")
sales_df.show()

print("\n--- Category-wise Summary ---")
sales_df.groupBy("category").agg(
    count("*").alias("number_of_orders"),
    spark_sum("revenue").alias("total_revenue")
).orderBy(col("total_revenue").desc()).show()

# Save processed output
sales_df.write.mode("overwrite").option(
    "header", True
).csv("outputs/processed_sales")

print("\nProcessed CSV data saved to outputs/processed_sales")

spark.stop()

