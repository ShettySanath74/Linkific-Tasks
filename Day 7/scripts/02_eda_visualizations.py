
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "ecommerce_sales.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load and prepare data
df = pd.read_csv(DATA_FILE)
df["sales"] = df["quantity"] * df["unit_price"]
df["order_date"] = pd.to_datetime(df["order_date"])

# 1. Sales distribution
plt.figure(figsize=(8, 5))
plt.hist(df["sales"], bins=8, edgecolor="black")
plt.title("Distribution of Order Sales")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_distribution.png", dpi=150)
plt.close()

# 2. Outlier detection using a box plot
plt.figure(figsize=(8, 5))
plt.boxplot(df["sales"])
plt.title("Box Plot for Order Sales")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_outliers_boxplot.png", dpi=150)
plt.close()

# 3. Correlation heatmap using Matplotlib
numeric_df = df[["quantity", "unit_price", "rating", "sales"]]
correlation = numeric_df.corr()

fig, ax = plt.subplots(figsize=(7, 5))
image = ax.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(correlation.columns)))
ax.set_yticks(range(len(correlation.columns)))
ax.set_xticklabels(correlation.columns, rotation=45, ha="right")
ax.set_yticklabels(correlation.columns)

for i in range(len(correlation.columns)):
    for j in range(len(correlation.columns)):
        ax.text(j, i, f"{correlation.iloc[i, j]:.2f}",
                ha="center", va="center")

fig.colorbar(image, ax=ax, label="Correlation")
ax.set_title("Correlation Between Numerical Variables")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=150)
plt.close(fig)

# 4. Sales by category
category_sales = df.groupby("category")["sales"].mean()

plt.figure(figsize=(8, 5))
plt.bar(category_sales.index, category_sales.values,
        edgecolor="black")
plt.title("Average Order Sales by Category")
plt.xlabel("Category")
plt.ylabel("Average Sales")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_by_category.png", dpi=150)
plt.close()

# 5. Potential outliers using the IQR rule
q1 = df["sales"].quantile(0.25)
q3 = df["sales"].quantile(0.75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df[
    (df["sales"] < lower_bound) |
    (df["sales"] > upper_bound)
]

print("EDA visualizations completed.")
print("Charts saved in:", OUTPUT_DIR)
print("\nPotential outliers using the IQR rule:")
print(outliers[["order_id", "category", "sales"]])

print("\nCorrelation matrix:")
print(correlation.round(2))
