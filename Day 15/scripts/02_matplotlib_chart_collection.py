
import matplotlib.pyplot as plt
import numpy as np

# Sample sales dataset
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12000, 15000, 13500, 18000, 22000, 25000]
categories = ["Electronics", "Furniture", "Clothing", "Food"]
category_sales = [45000, 30000, 22000, 15000]

# Create output folder if it doesn't exist
from pathlib import Path
Path("outputs/matplotlib").mkdir(parents=True, exist_ok=True)

# 1. Line plot
plt.figure()
plt.plot(months, sales, marker="o")
plt.title("1. Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/matplotlib/02_line_plot.png", dpi=150)
plt.close()

# 2. Bar chart
plt.figure()
plt.bar(categories, category_sales)
plt.title("2. Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("outputs/matplotlib/03_bar_chart.png", dpi=150)
plt.close()

# 3. Scatter plot
plt.figure()
plt.scatter([10, 20, 30, 40, 50], [100, 180, 160, 260, 300])
plt.title("3. Advertising Spend vs Sales")
plt.xlabel("Advertising Spend (units)")
plt.ylabel("Sales (units)")
plt.tight_layout()
plt.savefig("outputs/matplotlib/04_scatter_plot.png", dpi=150)
plt.close()

# 4. Histogram
plt.figure()
plt.hist(sales, bins=5, edgecolor="black")
plt.title("4. Distribution of Monthly Sales")
plt.xlabel("Sales (₹)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("outputs/matplotlib/05_histogram.png", dpi=150)
plt.close()

# 5. Pie chart
plt.figure()
plt.pie(category_sales, labels=categories, autopct="%1.1f%%", startangle=90)
plt.title("5. Sales Share by Category")
plt.tight_layout()
plt.savefig("outputs/matplotlib/06_pie_chart.png", dpi=150)
plt.close()

# 6. Box plot
plt.figure()
plt.boxplot(sales)
plt.title("6. Monthly Sales Spread")
plt.ylabel("Sales (₹)")
plt.tight_layout()
plt.savefig("outputs/matplotlib/07_box_plot.png", dpi=150)
plt.close()

# 7. Area chart
plt.figure()
plt.fill_between(months, sales, alpha=0.4)
plt.plot(months, sales, marker="o")
plt.title("7. Monthly Sales Area Chart")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.tight_layout()
plt.savefig("outputs/matplotlib/08_area_chart.png", dpi=150)
plt.close()

# 8. Horizontal bar chart
plt.figure()
plt.barh(categories, category_sales)
plt.title("8. Horizontal Category Comparison")
plt.xlabel("Sales (₹)")
plt.tight_layout()
plt.savefig("outputs/matplotlib/09_horizontal_bar.png", dpi=150)
plt.close()

# 9. Stem plot
plt.figure()
plt.stem(months, sales)
plt.title("9. Monthly Sales Stem Plot")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.tight_layout()
plt.savefig("outputs/matplotlib/10_stem_plot.png", dpi=150)
plt.close()

# 10. Stacked bar chart
online = [20000, 15000, 12000, 8000]
store = [25000, 15000, 10000, 7000]

plt.figure()
plt.bar(categories, online, label="Online")
plt.bar(categories, store, bottom=online, label="In-store")
plt.title("10. Sales by Category and Channel")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=20)
plt.legend()
plt.tight_layout()
plt.savefig("outputs/matplotlib/11_stacked_bar.png", dpi=150)
plt.close()

print("Successfully generated 10 Matplotlib chart types.")
print("Check the outputs/matplotlib/ folder.")
