"""Generate reproducible normal, edge-case and volume test datasets."""
import csv, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CUSTOMERS=ROOT/"data/test_data/customers.csv"
OUT=ROOT/"data/test_data"

def generate(size, seed=42):
    rng=random.Random(seed)
    OUT.mkdir(parents=True,exist_ok=True)
    customers=[{"customer_id":f"C{i:05d}","name":f"Customer {i}","city":rng.choice(["Mysuru","Bengaluru","Mangaluru","Hubballi"])} for i in range(1,101)]
    with CUSTOMERS.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=customers[0].keys()); w.writeheader(); w.writerows(customers)
    path=OUT/f"sales_{size}.csv"
    with path.open("w",newline="",encoding="utf-8") as f:
        fields=["sale_id","customer_id","product","amount","sale_date"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for i in range(size):
            # About 2% deliberate invalid cases; valid rows are deterministic.
            case=i%50
            row={"sale_id":f"T{i:08d}","customer_id":rng.choice(customers)["customer_id"],
                 "product":rng.choice(["Laptop","Mouse","Keyboard","Monitor"]),
                 "amount":round(rng.uniform(100,80000),2),"sale_date":"2026-11-21"}
            if case==1: row["amount"]=-10
            elif case==2: row["amount"]="not-a-number"
            elif case==3: row["customer_id"]="C99999"
            elif case==4: row["sale_date"]="21-11-2026"
            elif case==5: row["sale_id"]=""
            w.writerow(row)
    return path

def generate_all():
    return [str(generate(n)) for n in (100,1000,10000,100000)]

if __name__=="__main__":
    for p in generate_all(): print("Generated:",p)
