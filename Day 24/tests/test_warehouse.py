import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.config import get_connection
from scripts.main import main

class WarehouseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main()

    def test_fact_count(self):
        with get_connection() as c:
            self.assertEqual(c.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0],11)

    def test_foreign_keys(self):
        with get_connection() as c:
            self.assertEqual(c.execute("PRAGMA foreign_key_check").fetchall(),[])

    def test_sales_calculation(self):
        with get_connection() as c:
            row = c.execute("SELECT quantity,unit_price,sales_amount FROM fact_sales WHERE order_id='O1001' AND line_number=2").fetchone()
            self.assertEqual(row,(2,750.0,1500.0))

    def test_dimensions(self):
        with get_connection() as c:
            self.assertEqual(c.execute("SELECT COUNT(*) FROM dim_product").fetchone()[0],5)
            self.assertEqual(c.execute("SELECT COUNT(DISTINCT customer_id) FROM dim_customer").fetchone()[0],5)

if __name__ == "__main__":
    unittest.main()
