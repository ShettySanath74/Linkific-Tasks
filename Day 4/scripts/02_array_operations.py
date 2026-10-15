import numpy as np

print("=" * 50)
print("NUMPY ARRAY OPERATIONS")
print("=" * 50)

# 1. Create an array
numbers = np.array([10, 20, 30, 40, 50])
print("\n1. Original array:", numbers)

# 2. Addition
print("2. Addition:", numbers + 5)

# 3. Subtraction
print("3. Subtraction:", numbers - 5)

# 4. Multiplication
print("4. Multiplication:", numbers * 2)

# 5. Division
print("5. Division:", numbers / 10)

# 6. Square each element
print("6. Square:", np.square(numbers))

# 7. Square root
print("7. Square root:", np.sqrt(numbers))

# 8. Sum
print("8. Sum:", np.sum(numbers))

# 9. Mean (average)
print("9. Mean:", np.mean(numbers))

# 10. Median (middle value)
print("10. Median:", np.median(numbers))

# 11. Standard deviation (spread of values)
print("11. Standard deviation:", np.std(numbers))

# 12. Minimum and maximum
print("12. Minimum:", np.min(numbers))
print("    Maximum:", np.max(numbers))

# 13. Percentile
print("13. 75th percentile:", np.percentile(numbers, 75))

# 14. Sorting
unsorted = np.array([40, 10, 50, 20, 30])
print("14. Sorted:", np.sort(unsorted))

# 15. Unique values
values = np.array([10, 20, 10, 30, 20, 40, 10])
print("15. Unique values:", np.unique(values))

# 16. Count occurrences of each unique value
unique_values, counts = np.unique(values, return_counts=True)
print("16. Unique values:", unique_values)
print("    Occurrence counts:", counts)

# 17. Find the index of the maximum value
print("17. Index of maximum:", np.argmax(numbers))

# 18. Find the index of the minimum value
print("18. Index of minimum:", np.argmin(numbers))

# 19. Element-wise comparison
print("19. Values greater than 25:", numbers > 25)

# 20. Operations on a two-dimensional array
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print("20. Matrix:\n", matrix)
print("    Sum of all elements:", np.sum(matrix))
print("    Sum of each column:", np.sum(matrix, axis=0))
print("    Sum of each row:", np.sum(matrix, axis=1))

print("\nAll 20 array operation examples completed!")