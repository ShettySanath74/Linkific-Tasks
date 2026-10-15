import numpy as np

print("=" * 55)
print("NUMPY BOOLEAN INDEXING AND FILTERING")
print("=" * 55)

# Sample dataset: employee salaries in thousands
salaries = np.array([25000, 32000, 45000, 28000, 60000, 38000, 75000, 30000])

print("\nOriginal salaries:", salaries)

# 1. Create a Boolean mask
mask = salaries > 40000
print("\n1. Boolean mask (salary > 40000):", mask)

# 2. Filter values using a Boolean mask
high_salaries = salaries[mask]
print("2. Salaries above 40000:", high_salaries)

# 3. Direct conditional filtering
print("\n3. Salaries below 35000:", salaries[salaries < 35000])

# 4. Combine conditions using AND (&)
print("4. Salaries between 30000 and 50000:",
      salaries[(salaries >= 30000) & (salaries <= 50000)])

# 5. Combine conditions using OR (|)
print("5. Salaries below 30000 or above 60000:",
      salaries[(salaries < 30000) | (salaries > 60000)])

# 6. Use NOT (~) to reverse a Boolean mask
print("6. Salaries NOT above 40000:", salaries[~(salaries > 40000)])

# 7. Use np.where() for conditional selection
labels = np.where(salaries >= 40000, "High", "Standard")
print("\n7. Salary categories:", labels)

# 8. Use np.where() to find matching positions
positions = np.where(salaries >= 40000)
print("8. Positions with salaries >= 40000:", positions[0])

# 9. Fancy indexing: select specific positions
indices = [0, 3, 6]
print("\n9. Salaries at positions 0, 3, 6:", salaries[indices])

# 10. Replace values using a Boolean mask
updated_salaries = salaries.copy()
updated_salaries[updated_salaries < 30000] = 30000
print("10. Salaries with minimum 30000 applied:", updated_salaries)

# 11. Count matching values
print("\n11. Number of salaries >= 40000:",
      np.count_nonzero(salaries >= 40000))

# 12. Filter a two-dimensional array
sales = np.array([
    [100, 200, 300],
    [400, 150, 250],
    [500, 350, 100]
])

print("\n12. Sales matrix:\n", sales)
print("Sales greater than 300:", sales[sales > 300])

# 13. Select complete rows based on a condition
row_totals = sales.sum(axis=1)
print("\n13. Row totals:", row_totals)
print("Rows with total sales >= 700:\n", sales[row_totals >= 700])

# 14. Find values that are even
numbers = np.arange(1, 11)
print("\n14. Even numbers:", numbers[numbers % 2 == 0])

# 15. Find values that are multiples of 3
print("15. Multiples of 3:", numbers[numbers % 3 == 0])

print("\nAll 15 filtering examples completed!")