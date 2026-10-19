
from pathlib import Path

import pandas as pd
import numpy as np
from scipy import stats

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "ecommerce_sales.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)
df["sales"] = df["quantity"] * df["unit_price"]

sales = df["sales"].dropna()

print("\n===== DESCRIPTIVE STATISTICS =====")
print("Count:", sales.count())
print("Mean:", round(sales.mean(), 2))
print("Median:", round(sales.median(), 2))
print("Minimum:", sales.min())
print("Maximum:", sales.max())
print("Range:", sales.max() - sales.min())

print("\n===== VARIANCE AND STANDARD DEVIATION =====")
print("Sample variance:", round(sales.var(), 2))
print("Sample standard deviation:", round(sales.std(), 2))

print("\n===== QUARTILES AND PERCENTILES =====")
print(sales.quantile([0.25, 0.50, 0.75, 0.90, 0.95]))

print("\n===== SKEWNESS AND KURTOSIS =====")
print("Skewness:", round(sales.skew(), 3))
print("Excess kurtosis:", round(sales.kurtosis(), 3))

print("\n===== CORRELATION =====")
numeric_columns = ["quantity", "unit_price", "rating", "sales"]
print(df[numeric_columns].corr().round(3))

# Basic one-sample t-test
# Example question: Is the average order sales different from 1500?
test_result = stats.ttest_1samp(sales, popmean=1500)

print("\n===== ONE-SAMPLE T-TEST =====")
print("Hypothesized mean:", 1500)
print("Observed mean:", round(sales.mean(), 2))
print("T-statistic:", round(test_result.statistic, 4))
print("P-value:", round(test_result.pvalue, 4))

alpha = 0.05
if test_result.pvalue < alpha:
    print("Conclusion: Reject the null hypothesis at the 5% level.")
else:
    print("Conclusion: Do not reject the null hypothesis at the 5% level.")

# Save statistical results
summary = pd.DataFrame({
    "metric": [
        "count", "mean", "median", "minimum", "maximum",
        "range", "sample_variance", "sample_std_dev",
        "q1", "q2_median", "q3", "p90", "p95",
        "skewness", "excess_kurtosis",
        "t_statistic", "t_test_p_value"
    ],
    "value": [
        sales.count(), sales.mean(), sales.median(),
        sales.min(), sales.max(), sales.max() - sales.min(),
        sales.var(), sales.std(),
        sales.quantile(0.25), sales.quantile(0.50),
        sales.quantile(0.75), sales.quantile(0.90),
        sales.quantile(0.95), sales.skew(),
        sales.kurtosis(), test_result.statistic,
        test_result.pvalue
    ]
})

summary.to_csv(
    OUTPUT_DIR / "statistical_analysis.csv",
    index=False
)

print("\nStatistical results saved to:")
print(OUTPUT_DIR / "statistical_analysis.csv")
