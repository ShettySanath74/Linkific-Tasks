
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Create output folder
Path("outputs/seaborn").mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

# Sample sales dataset
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "Sales": [12000, 15000, 13500, 18000, 22000, 25000,
              24000, 28000, 26000, 31000, 34000, 38000],
    "Profit": [2000, 2800, 2200, 3500, 4600, 5200,
               5000, 6200, 5700, 7200, 8100, 9500],
    "Advertising": [1000, 1200, 1100, 1500, 1800, 2000,
                    1900, 2300, 2200, 2600, 2900, 3200],
    "Orders": [80, 95, 90, 110, 130, 145,
               140, 160, 155, 180, 195, 220],
    "Category": ["Electronics", "Clothing", "Furniture"] * 4,
    "Region": ["North", "South", "East", "West"] * 3
})

# 1. Histogram with KDE
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Sales", kde=True)
plt.title("1. Sales Distribution")
plt.tight_layout()
plt.savefig("outputs/seaborn/01_histogram_kde.png", dpi=150)
plt.close()

# 2. Box plot
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Category", y="Sales")
plt.title("2. Sales by Category")
plt.tight_layout()
plt.savefig("outputs/seaborn/02_boxplot.png", dpi=150)
plt.close()

# 3. Violin plot
plt.figure(figsize=(8, 5))
sns.violinplot(data=df, x="Category", y="Profit")
plt.title("3. Profit Distribution by Category")
plt.tight_layout()
plt.savefig("outputs/seaborn/03_violinplot.png", dpi=150)
plt.close()

# 4. Bar plot
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Region", y="Sales", errorbar=None)
plt.title("4. Average Sales by Region")
plt.tight_layout()
plt.savefig("outputs/seaborn/04_barplot.png", dpi=150)
plt.close()

# 5. Scatter plot with category hue
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Advertising", y="Sales", hue="Category", s=90)
plt.title("5. Advertising vs Sales")
plt.tight_layout()
plt.savefig("outputs/seaborn/05_scatterplot.png", dpi=150)
plt.close()

# 6. Regression plot
plt.figure(figsize=(8, 5))
sns.regplot(data=df, x="Advertising", y="Sales")
plt.title("6. Advertising and Sales Relationship")
plt.tight_layout()
plt.savefig("outputs/seaborn/06_regression.png", dpi=150)
plt.close()

# 7. Count plot
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Category")
plt.title("7. Number of Records by Category")
plt.tight_layout()
plt.savefig("outputs/seaborn/07_countplot.png", dpi=150)
plt.close()

# 8. Heatmap of numerical correlations
numeric_df = df[["Sales", "Profit", "Advertising", "Orders"]]
correlations = numeric_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlations, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("8. Sales Dataset Correlation Heatmap")
plt.tight_layout()
plt.savefig("outputs/seaborn/08_heatmap.png", dpi=150)
plt.close()

# 9. Pair plot
pair_grid = sns.pairplot(
    df[["Sales", "Profit", "Advertising", "Orders"]],
    diag_kind="hist"
)
pair_grid.figure.suptitle("9. Pairwise Relationships", y=1.02)
pair_grid.savefig("outputs/seaborn/09_pairplot.png", dpi=150)
plt.close("all")

# 10. Strip plot
plt.figure(figsize=(8, 5))
sns.stripplot(data=df, x="Category", y="Orders", jitter=True)
plt.title("10. Orders by Category")
plt.tight_layout()
plt.savefig("outputs/seaborn/10_stripplot.png", dpi=150)
plt.close()

print("Successfully generated 10 Seaborn visualizations.")
print("Check the outputs/seaborn/ folder.")
