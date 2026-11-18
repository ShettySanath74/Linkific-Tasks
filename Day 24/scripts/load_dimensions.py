import csv
from datetime import date, timedelta
from scripts.config import CUSTOMERS_CSV, PRODUCTS_CSV, get_connection
OPEN_END = "9999-12-31"

def load_customers(conn):
    new_count = changed_count = 0
    with CUSTOMERS_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cid, name, city = (r[k].strip() for k in ("customer_id","customer_name","city"))
            updated = date.fromisoformat(r["updated_at"].strip()).isoformat()
            if not all((cid,name,city)):
                raise ValueError(f"Blank required customer field: {r}")
            old = conn.execute(
                "SELECT customer_key,customer_name,city,effective_start_date FROM dim_customer WHERE customer_id=? AND is_current=1",
                (cid,)
            ).fetchone()
            if old is None:
                conn.execute("INSERT INTO dim_customer(customer_id,customer_name,city,effective_start_date,effective_end_date,is_current) VALUES(?,?,?,?,?,1)",
                             (cid,name,city,updated,OPEN_END))
                new_count += 1
            elif (old[1],old[2]) != (name,city):
                if updated <= old[3]:
                    raise ValueError(f"SCD2 updated_at for {cid} must be later than {old[3]}")
                end_date = (date.fromisoformat(updated)-timedelta(days=1)).isoformat()
                conn.execute("UPDATE dim_customer SET effective_end_date=?,is_current=0 WHERE customer_key=?",
                             (end_date,old[0]))
                conn.execute("INSERT INTO dim_customer(customer_id,customer_name,city,effective_start_date,effective_end_date,is_current) VALUES(?,?,?,?,?,1)",
                             (cid,name,city,updated,OPEN_END))
                changed_count += 1
    return new_count, changed_count

def load_products(conn):
    inserted = updated = 0
    with PRODUCTS_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pid, name, category = (r[k].strip() for k in ("product_id","product_name","category"))
            if not all((pid,name,category)):
                raise ValueError(f"Blank required product field: {r}")
            old = conn.execute("SELECT product_key,product_name,category FROM dim_product WHERE product_id=?", (pid,)).fetchone()
            if old is None:
                conn.execute("INSERT INTO dim_product(product_id,product_name,category) VALUES(?,?,?)",(pid,name,category))
                inserted += 1
            elif (old[1],old[2]) != (name,category):
                conn.execute("UPDATE dim_product SET product_name=?,category=? WHERE product_id=?",(name,category,pid))
                updated += 1
    return inserted, updated

def load_dimensions():
    with get_connection() as conn:
        cn, cc = load_customers(conn)
        pn, pu = load_products(conn)
    print(f"Customers: {cn} new, {cc} new SCD2 versions.")
    print(f"Products: {pn} inserted, {pu} updated (SCD1).")

if __name__ == "__main__":
    load_dimensions()
