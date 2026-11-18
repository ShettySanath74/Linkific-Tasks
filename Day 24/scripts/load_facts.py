import csv
from scripts.config import SALES_CSV, get_connection

def load_facts():
    inserted = skipped = 0
    with get_connection() as conn:
        with SALES_CSV.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                order, line = r["order_id"].strip(), int(r["line_number"])
                order_date, cid, pid = r["order_date"].strip(), r["customer_id"].strip(), r["product_id"].strip()
                qty, price = int(r["quantity"]), float(r["unit_price"])
                if qty <= 0 or price < 0:
                    raise ValueError(f"Invalid quantity/price: {r}")
                exists = conn.execute("SELECT 1 FROM fact_sales WHERE order_id=? AND line_number=?",(order,line)).fetchone()
                if exists:
                    skipped += 1
                    continue
                d = conn.execute("SELECT date_key FROM dim_date WHERE full_date=?",(order_date,)).fetchone()
                c = conn.execute("""
                    SELECT customer_key FROM dim_customer
                    WHERE customer_id=? AND effective_start_date<=? AND effective_end_date>=?
                    ORDER BY effective_start_date DESC LIMIT 1
                """,(cid,order_date,order_date)).fetchone()
                p = conn.execute("SELECT product_key FROM dim_product WHERE product_id=?",(pid,)).fetchone()
                if not d: raise ValueError(f"Missing date dimension row: {order_date}")
                if not c: raise ValueError(f"No effective customer version: {cid} on {order_date}")
                if not p: raise ValueError(f"Missing product dimension row: {pid}")
                amount = round(qty*price,2)
                conn.execute("""
                    INSERT INTO fact_sales(order_id,line_number,date_key,customer_key,product_key,quantity,unit_price,sales_amount)
                    VALUES(?,?,?,?,?,?,?,?)
                """,(order,line,d[0],c[0],p[0],qty,price,amount))
                inserted += 1
    print(f"Facts: {inserted} inserted, {skipped} already loaded/skipped.")

if __name__ == "__main__":
    load_facts()
