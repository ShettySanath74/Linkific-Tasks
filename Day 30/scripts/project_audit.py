"""Audit expected Day 28–30 project artifacts without modifying the repository."""
from __future__ import annotations

import argparse
from pathlib import Path

EXPECTED = [
    "Day 28/README.md",
    "Day 28/data/customers.csv",
    "Day 28/data/orders.csv",
    "Day 28/data/order_items.csv",
    "Day 28/data/products.csv",
    "Day 28/sql/analytical_queries.sql",
    "Day 28/python/exploratory_analysis.ipynb",
    "Day 28/powerbi/Day28_Business_Intelligence_Dashboard.pbix",
    "Day 29/README.md",
    "Day 29/scripts/run_validation.py",
    "Day 29/tests/test_quality_checks.py",
    "Day 29/tests/test_edge_cases.py",
    "Day 29/outputs/data_quality_report.json",
    "Day 29/outputs/sql_optimization_report.json",
    "Day 30/README.md",
    "Day 30/docs/FINAL_PROJECT_REPORT.md",
    "Day 30/presentation/Linkific_BI_Analytics_Final_Presentation.pptx",
]

def audit(root: Path) -> tuple[list[str], list[str]]:
    present, missing = [], []
    for relative in EXPECTED:
        (present if (root / relative).is_file() else missing).append(relative)
    return present, missing

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root directory")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    present, missing = audit(root)

    print(f"Repository root: {root}")
    print(f"Present: {len(present)} / {len(EXPECTED)}")
    for item in present:
        print(f"[OK]      {item}")
    for item in missing:
        print(f"[MISSING] {item}")

    print("\nThis is a path-existence audit only; it does not execute or validate the artifacts.")
    return 0 if not missing else 1

if __name__ == "__main__":
    raise SystemExit(main())
