from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "marketing_campaign_synthetic.csv"
OUT = ROOT / "outputs" / "campaign_comparison.csv"
BUDGET = 300.0

with DATA.open(newline="", encoding="utf-8") as f:
    customers = list(csv.DictReader(f))
for r in customers:
    r["p"] = float(r["response_probability"])
    r["cost"] = float(r["contact_cost"])
    r["revenue"] = float(r["revenue_if_response"])
    r["expected_revenue"] = r["p"] * r["revenue"]

def choose(ranked, positive_value_only=False):
    chosen, spent = [], 0.0
    for r in ranked:
        if positive_value_only and r["expected_revenue"] <= r["cost"]:
            continue
        if spent + r["cost"] <= BUDGET:
            chosen.append(r)
            spent += r["cost"]
    return chosen

def summary(label, chosen):
    cost = sum(r["cost"] for r in chosen)
    rev = sum(r["expected_revenue"] for r in chosen)
    return {"approach": label, "customers_selected": len(chosen),
            "campaign_cost": round(cost, 2),
            "expected_responses": round(sum(r["p"] for r in chosen), 2),
            "expected_revenue": round(rev, 2),
            "expected_net_value": round(rev-cost, 2)}

results = [
    summary("Prediction-based", choose(sorted(customers, key=lambda r: r["p"], reverse=True))),
    summary("Decision-oriented (greedy heuristic)", choose(
        sorted(customers, key=lambda r: (r["expected_revenue"]-r["cost"])/r["cost"], reverse=True),
        positive_value_only=True))
]
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
for result in results:
    print(result)
print(f"Saved: {OUT}")
