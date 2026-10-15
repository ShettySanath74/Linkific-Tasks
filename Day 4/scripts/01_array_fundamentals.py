import numpy as np

print("=" * 50)
print("NUMPY ARRAY FUNDAMENTALS")
print("=" * 50)

# 1. Create a basic array
numbers = np.array([10, 20, 30, 40, 50])
print("\n1. Basic array:", numbers)

# 2. Create an array of zeros
zeros = np.zeros(5)
print("2. Zeros:", zeros)

# 3. Create an array of ones
ones = np.ones(5)
print("3. Ones:", ones)

# 4. Generate a sequence using arange
sequence = np.arange(0, 10, 2)
print("4. Arange:", sequence)

# 5. Generate evenly spaced numbers using linspace
spaced = np.linspace(0, 10, 5)
print("5. Linspace:", spaced)

# 6. Array indexing
print("6. First element:", numbers[0])
print("   Last element:", numbers[-1])

# 7. Array slicing
print("7. First three elements:", numbers[:3])
print("   Elements from index 2:", numbers[2:])

# 8. Reshape a one-dimensional array
matrix = np.arange(1, 10).reshape(3, 3)
print("8. Reshaped 3x3 matrix:\n", matrix)

# 9. Inspect array properties
print("9. Shape:", matrix.shape)
print("   Dimensions:", matrix.ndim)
print("   Number of elements:", matrix.size)
print("   Data type:", matrix.dtype)

# 10. Broadcasting
values = np.array([10, 20, 30])
print("10. Broadcasting (values + 5):", values + 5)

print("\nAll 10 fundamentals examples completed!")