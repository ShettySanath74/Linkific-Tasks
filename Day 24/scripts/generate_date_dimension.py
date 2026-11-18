import csv
from datetime import date, timedelta
from scripts.config import SALES_CSV, get_connection

HOLIDAYS = {
    "2026-01-26": "Republic Day",
    "2026-08-15": "Independence Day",
    "2026-10-02": "Gandhi Jayanti",
}

def generate_date_dimension():
    with SALES_CSV.open(newline="", encoding="utf-8") as f:
        dates = [date.fromisoformat(r["order_date"]) for r in csv.DictReader(f)]
    if not dates:
        raise ValueError("sales.csv contains no rows")
    start, end = min(dates), max(dates)
    processed = 0
    with get_connection() as conn:
        current = start
        while current <= end:
            iso = current.isoformat()
            holiday = HOLIDAYS.get(iso)
            conn.execute("""
                INSERT OR IGNORE INTO dim_date
                (date_key,full_date,day_number,day_name,day_of_week,week_of_year,
                 month_number,month_name,quarter_number,year_number,is_weekend,is_holiday,holiday_name)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                int(current.strftime("%Y%m%d")), iso, current.day, current.strftime("%A"),
                current.isoweekday(), int(current.strftime("%V")), current.month,
                current.strftime("%B"), (current.month-1)//3+1, current.year,
                int(current.weekday() >= 5), int(holiday is not None), holiday
            ))
            processed += 1
            current += timedelta(days=1)
    print(f"Date dimension processed {processed} days: {start} to {end}.")

if __name__ == "__main__":
    generate_date_dimension()
