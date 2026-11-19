import tempfile
import unittest
from pathlib import Path
from scripts.transform import transform_sources, aggregate_daily_category

class TransformTests(unittest.TestCase):
    def test_transform_join_and_revenue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "customers.csv").write_text(
                "customer_id,customer_name,city,updated_at\nC1, Alice ,Mysuru,2026-01-01T10:00:00\n",
                encoding="utf-8"
            )
            (root / "products.csv").write_text(
                "product_id,product_name,category,updated_at\nP1,Mouse,Electronics,2026-01-01T10:00:00\n",
                encoding="utf-8"
            )
            (root / "sales.csv").write_text(
                "order_id,customer_id,product_id,order_date,quantity,unit_price,updated_at,is_deleted\nO1,C1,P1,2026-01-01,2,500,2026-01-01T11:00:00,false\n",
                encoding="utf-8"
            )
            rows, rejects = transform_sources(root/"customers.csv", root/"products.csv", root/"sales.csv")
            self.assertEqual(rejects, [])
            self.assertEqual(rows[0]["customer_name"], "Alice")
            self.assertEqual(rows[0]["revenue"], 1000.0)
            summary = aggregate_daily_category(rows)
            self.assertEqual(summary[0]["revenue"], 1000.0)

    def test_invalid_foreign_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "customers.csv").write_text("customer_id,customer_name,city,updated_at\nC1,A,M,2026-01-01T10:00:00\n")
            (root / "products.csv").write_text("product_id,product_name,category,updated_at\nP1,Mouse,Electronics,2026-01-01T10:00:00\n")
            (root / "sales.csv").write_text("order_id,customer_id,product_id,order_date,quantity,unit_price,updated_at,is_deleted\nO1,C999,P1,2026-01-01,1,10,2026-01-01T11:00:00,false\n")
            rows, rejects = transform_sources(root/"customers.csv", root/"products.csv", root/"sales.csv")
            self.assertEqual(rows, [])
            self.assertEqual(len(rejects), 1)

if __name__ == "__main__":
    unittest.main()
