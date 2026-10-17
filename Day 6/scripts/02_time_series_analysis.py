
from pathlib import Path

import numpy as np
import pandas as pd

# Keep all files inside the Day 6 folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("DAY 6: PANDAS TIME SERIES ANALYSIS")
print("=" * 60)

# 1. Create sample daily sales data
dates = pd.date_range(
    start="2026-01-01",
    periods=120,
    freq="D"
)

rng = np.random.default_rng(42)

sales = rng.integers(1000, 5000, size=len(dates))

sales_df = pd.DataFrame({
    "date": dates,
    "sales": sales
})

sales_df.to_csv(DATA_DIR / "daily_sales.csv", index=False)

# 2. Convert dates and create a DateTimeIndex
sales_df["date"] = pd.to_datetime(sales_df["date"])
sales_df = sales_df.set_index("date")

print("\n1. DAILY SALES DATA")
print(sales_df.head())

# 3. Daily data with a 7-day rolling average
daily_analysis = sales_df.copy()
daily_analysis["rolling_7_day_average"] = (
    daily_analysis["sales"].rolling(window=7, min_periods=1).mean()
)

daily_analysis.to_csv(OUTPUT_DIR / "rolling_sales.csv")

# 4. Weekly sales totals
weekly_sales = sales_df["sales"].resample("W").sum().to_frame()
weekly_sales.to_csv(OUTPUT_DIR / "weekly_sales.csv")

# 5. Monthly sales totals
monthly_sales = sales_df["sales"].resample("MS").sum().to_frame()
monthly_sales.to_csv(OUTPUT_DIR / "monthly_sales.csv")

# 6. Yearly sales totals
yearly_sales = sales_df["sales"].resample("YS").sum().to_frame()
yearly_sales.to_csv(OUTPUT_DIR / "yearly_sales.csv")

# 7. Previous-day sales (lag)
lagged_sales = sales_df.copy()
lagged_sales["previous_day_sales"] = lagged_sales["sales"].shift(1)
lagged_sales.to_csv(OUTPUT_DIR / "lagged_sales.csv")

# 8. Save the DateTimeIndex version of the daily dataset
sales_df.to_csv(OUTPUT_DIR / "daily_sales_with_datetime.csv")

# 9. Time zone conversion: UTC to India Standard Time
utc_dates = pd.date_range(
    start="2026-01-01 09:00:00",
    periods=5,
    freq="D",
    tz="UTC"
)

india_dates = utc_dates.tz_convert("Asia/Kolkata")

timezone_df = pd.DataFrame({
    "utc_time": utc_dates.astype(str),
    "india_time": india_dates.astype(str)
})

timezone_df.to_csv(OUTPUT_DIR / "timezone_demo.csv", index=False)

# 10. Display summaries
print("\n2. WEEKLY SALES TOTALS")
print(weekly_sales.head())

print("\n3. MONTHLY SALES TOTALS")
print(monthly_sales)

print("\n4. YEARLY SALES TOTALS")
print(yearly_sales)

print("\n5. ROLLING AVERAGE AND LAG")
print(lagged_sales.head(10))

print("\n6. TIME ZONE CONVERSION")
print(timezone_df)

print("\nAll time series outputs saved to:")
print(OUTPUT_DIR)
print("\nTime series analysis completed!")

