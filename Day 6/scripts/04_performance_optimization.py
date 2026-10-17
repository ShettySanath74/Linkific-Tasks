
from pathlib import Path
import time

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("DAY 6: PANDAS PERFORMANCE OPTIMIZATION")
print("=" * 65)

# 1. Create a sample dataset
rng = np.random.default_rng(42)
number_of_rows = 200_000

df = pd.DataFrame({
    "employee_id": np.arange(1, number_of_rows + 1),
    "department": rng.choice(
        ["Engineering", "Analytics", "Marketing", "HR"],
        size=number_of_rows
    ),
    "salary": rng.integers(25000, 150000, size=number_of_rows),
    "experience_years": rng.integers(0, 21, size=number_of_rows),
    "performance_score": rng.uniform(1, 5, size=number_of_rows)
})

input_file = DATA_DIR / "large_employee_dataset.csv"
df.to_csv(input_file, index=False)

print(f"\n1. Dataset created: {len(df):,} rows")
print(f"Original memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 2. Optimize data types
optimized_df = df.copy()

optimized_df["department"] = optimized_df["department"].astype("category")
optimized_df["salary"] = optimized_df["salary"].astype("int32")
optimized_df["experience_years"] = optimized_df["experience_years"].astype("int8")
optimized_df["performance_score"] = optimized_df["performance_score"].astype("float32")

original_memory = df.memory_usage(deep=True).sum()
optimized_memory = optimized_df.memory_usage(deep=True).sum()

print("\n2. MEMORY OPTIMIZATION")
print(f"Original:  {original_memory / 1024**2:.2f} MB")
print(f"Optimized: {optimized_memory / 1024**2:.2f} MB")
print(f"Memory reduction: {(1 - optimized_memory / original_memory) * 100:.2f}%")

# 3. Compare Python loop and vectorized operation
values = list(range(200_000))

start = time.perf_counter()
loop_result = [value * 2 for value in values]
loop_seconds = time.perf_counter() - start

array = np.asarray(values)

start = time.perf_counter()
vectorized_result = array * 2
vectorized_seconds = time.perf_counter() - start

print("\n3. LOOP VS VECTORIZATION")
print(f"Python list comprehension: {loop_seconds:.6f} seconds")
print(f"NumPy vectorization:        {vectorized_seconds:.6f} seconds")
print("Results equivalent:", loop_result == vectorized_result.tolist())

# 4. Compare apply with vectorized calculation
small_df = df.head(50_000).copy()

start = time.perf_counter()
small_df["bonus_apply"] = small_df["salary"].apply(
    lambda salary: salary * 0.10
)
apply_seconds = time.perf_counter() - start

start = time.perf_counter()
small_df["bonus_vectorized"] = small_df["salary"] * 0.10
vector_seconds = time.perf_counter() - start

print("\n4. APPLY VS VECTORIZED PANDAS")
print(f"apply():       {apply_seconds:.6f} seconds")
print(f"Vectorized:    {vector_seconds:.6f} seconds")
print(
    "Results equivalent:",
    np.allclose(small_df["bonus_apply"], small_df["bonus_vectorized"])
)

# 5. Compare query() and Boolean filtering
condition = "salary >= 80000 and experience_years >= 5"

start = time.perf_counter()
query_result = df.query(condition)
query_seconds = time.perf_counter() - start

start = time.perf_counter()
boolean_result = df[
    (df["salary"] >= 80000) &
    (df["experience_years"] >= 5)
]
boolean_seconds = time.perf_counter() - start

print("\n5. QUERY VS BOOLEAN FILTERING")
print(f"query():           {query_seconds:.6f} seconds")
print(f"Boolean indexing:  {boolean_seconds:.6f} seconds")
print("Same row count:", len(query_result) == len(boolean_result))

# 6. Process a large CSV in chunks
chunk_size = 25_000
chunk_summaries = []

for chunk_number, chunk in enumerate(
    pd.read_csv(input_file, chunksize=chunk_size),
    start=1
):
    summary = chunk.groupby("department", as_index=False).agg(
        employee_count=("employee_id", "count"),
        total_salary=("salary", "sum")
    )
    summary["chunk_number"] = chunk_number
    chunk_summaries.append(summary)

chunk_summary_df = pd.concat(chunk_summaries, ignore_index=True)

chunk_summary_file = OUTPUT_DIR / "chunk_processing_summary.csv"
chunk_summary_df.to_csv(chunk_summary_file, index=False)

print("\n6. CHUNK PROCESSING")
print(f"Chunk size: {chunk_size:,}")
print(f"Chunks processed: {len(chunk_summaries)}")
print(f"Chunk summary saved: {chunk_summary_file}")

# 7. Save performance measurements
benchmark_df = pd.DataFrame([
    {"test": "Python list comprehension", "seconds": loop_seconds},
    {"test": "NumPy vectorization", "seconds": vectorized_seconds},
    {"test": "Pandas apply", "seconds": apply_seconds},
    {"test": "Pandas vectorized", "seconds": vector_seconds},
    {"test": "DataFrame query", "seconds": query_seconds},
    {"test": "Boolean indexing", "seconds": boolean_seconds},
])

benchmark_file = OUTPUT_DIR / "performance_benchmarks.csv"
benchmark_df.to_csv(benchmark_file, index=False)

print("\n7. BENCHMARK RESULTS")
print(benchmark_df.to_string(index=False))

print("\nAll performance optimization examples completed.")
print(f"Output directory: {OUTPUT_DIR}")
