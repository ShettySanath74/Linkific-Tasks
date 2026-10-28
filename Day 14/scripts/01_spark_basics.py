from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum as spark_sum

# Create a Spark session
spark = (
    SparkSession.builder
    .appName("Day14-Spark-Basics")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Sample employee sales data
data = [
    (1, "Ananya", "Sales", 45000),
    (2, "Rahul", "IT", 60000),
    (3, "Priya", "Sales", 52000),
    (4, "Arjun", "IT", 70000),
    (5, "Meera", "HR", 40000),
]

columns = ["id", "name", "department", "salary"]

df = spark.createDataFrame(data, columns)

print("\n--- Original DataFrame ---")
df.show()

print("\n--- Schema ---")
df.printSchema()

print("\n--- Select name and salary ---")
df.select("name", "salary").show()

print("\n--- Employees with salary above 50000 ---")
df.filter(col("salary") > 50000).show()

print("\n--- Department-wise salary summary ---")
df.groupBy("department").agg(
    spark_sum("salary").alias("total_salary"),
    avg("salary").alias("average_salary")
).show()

spark.stop()

