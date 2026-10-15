import numpy as np
import time

print("=" * 60)
print("NUMPY PERFORMANCE AND VECTORIZATION BENCHMARK")
print("=" * 60)

# 1. Create a dataset of one million numbers
size = 1_000_000
numbers = np.arange(size, dtype=np.float64)

print(f"\nDataset size: {size:,} elements")

# 2. Python loop approach
start_time = time.perf_counter()

loop_result = []
for number in numbers:
    loop_result.append(number * 2)

loop_time = time.perf_counter() - start_time

print(f"\n1. Python loop time: {loop_time:.6f} seconds")

# 3. NumPy vectorized approach
start_time = time.perf_counter()

vectorized_result = numbers * 2

vectorized_time = time.perf_counter() - start_time

print(f"2. NumPy vectorized time: {vectorized_time:.6f} seconds")

# 4. Compare performance
if vectorized_time > 0:
    speedup = loop_time / vectorized_time
    print(f"\n3. Speedup: {speedup:.2f}x")

# 5. Verify both methods produce the same values
results_match = np.array_equal(
    np.asarray(loop_result),
    vectorized_result
)

print("4. Results match:", results_match)

# 6. Demonstrate memory usage
python_list = [float(x) for x in range(100_000)]
numpy_array = np.arange(100_000, dtype=np.float64)

python_list_size = (
    python_list.__sizeof__()
    + sum(item.__sizeof__() for item in python_list)
)

numpy_array_size = numpy_array.nbytes

print("\n5. Memory comparison for 100,000 values:")
print(f"Python list approximate size: {python_list_size:,} bytes")
print(f"NumPy array data size:        {numpy_array_size:,} bytes")

# 7. Benchmark a mathematical transformation
start_time = time.perf_counter()
squared_values = np.square(numbers)
square_time = time.perf_counter() - start_time

print(f"\n6. NumPy square operation: {square_time:.6f} seconds")
print("First five squared values:", squared_values[:5])

# 8. Statistical operation on a large dataset
start_time = time.perf_counter()
average = np.mean(numbers)
stats_time = time.perf_counter() - start_time

print(f"\n7. Mean calculation: {average:.2f}")
print(f"8. Mean calculation time: {stats_time:.6f} seconds")

print("\nBenchmark completed successfully!")