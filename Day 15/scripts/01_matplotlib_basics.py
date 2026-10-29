
import matplotlib.pyplot as plt

# Sample monthly sales data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12000, 15000, 13500, 18000, 22000, 25000]

# Create a figure with two side-by-side charts
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Chart 1: Line plot
axes[0].plot(
    months,
    sales,
    marker="o",
    linewidth=2,
    label="Monthly Sales"
)
axes[0].set_title("Monthly Sales Trend")
axes[0].set_xlabel("Month")
axes[0].set_ylabel("Sales (₹)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Chart 2: Bar chart
axes[1].bar(months, sales)
axes[1].set_title("Monthly Sales Comparison")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Sales (₹)")

# Add a main title and adjust spacing
fig.suptitle("Sales Visualization Dashboard")
fig.tight_layout()

# Save the chart
fig.savefig(
    "outputs/matplotlib/01_sales_basics.png",
    dpi=150,
    bbox_inches="tight"
)

print("Charts saved to outputs/matplotlib/01_sales_basics.png")

# Display the chart
plt.show()
