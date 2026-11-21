"""Validate sales, enrich valid rows, and route invalid rows to dead letter."""
import csv, json
from datetime import date
from pathlib import Path
from scripts.common import TRANSFORM_DIR, DEAD_LETTER_DIR, ensure_directories, get_logger
logger=get_logger(__name__)
OUTPUT_FIELDS=["sale_id","customer_id","customer_name","city","product","amount","sale_date"]
DEAD_LETTER_FIELDS=["sale_id","customer_id","product","amount","sale_date","reason"]

def validate_sale(sale, customer_ids, seen):
    sid=(sale.get("sale_id") or "").strip()
    cid=(sale.get("customer_id") or "").strip()
    amount_text=(sale.get("amount") or "").strip()
    sdate=(sale.get("sale_date") or "").strip()
    if not sid: return "Missing sale_id"
    if sid in seen: return "Duplicate sale_id"
    if cid not in customer_ids: return "Customer reference not found"
    try:
        amount=float(amount_text)
        if amount <= 0: return "Amount must be greater than zero"
    except (TypeError,ValueError): return "Amount is not numeric"
    try: date.fromisoformat(sdate)
    except (TypeError,ValueError): return "sale_date must use YYYY-MM-DD format"
    return ""

def transform_records(customers_json, sales_json, accepted_path=None, rejected_path=None):
    ensure_directories()
    with Path(customers_json).open(encoding="utf-8") as f: customers=json.load(f)
    with Path(sales_json).open(encoding="utf-8") as f: sales=json.load(f)
    lookup={c["customer_id"].strip():c for c in customers if c.get("customer_id")}
    accepted=[]; rejected=[]; seen=set(); customer_ids=set(lookup)
    for sale in sales:
        sid=(sale.get("sale_id") or "").strip()
        reason=validate_sale(sale,customer_ids,seen)
        if sid: seen.add(sid)
        if reason:
            rejected.append({k:sale.get(k,"") for k in ("sale_id","customer_id","product","amount","sale_date")}|{"reason":reason})
        else:
            c=lookup[sale["customer_id"].strip()]
            accepted.append({"sale_id":sid,"customer_id":c["customer_id"],"customer_name":c.get("name",""),
                "city":c.get("city",""),"product":(sale.get("product") or "").strip(),
                "amount":float(sale["amount"]),"sale_date":sale["sale_date"].strip()})
    ap=Path(accepted_path) if accepted_path else TRANSFORM_DIR/"accepted_sales.csv"
    rp=Path(rejected_path) if rejected_path else DEAD_LETTER_DIR/"rejected_sales.csv"
    ap.parent.mkdir(parents=True,exist_ok=True); rp.parent.mkdir(parents=True,exist_ok=True)
    with ap.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=OUTPUT_FIELDS); w.writeheader(); w.writerows(accepted)
    with rp.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=DEAD_LETTER_FIELDS); w.writeheader(); w.writerows(rejected)
    logger.info("Transformation complete: %d accepted, %d rejected",len(accepted),len(rejected))
    return str(ap)
