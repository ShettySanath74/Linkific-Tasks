import unittest
from scripts.transform import transform_sources
from scripts.config import CUSTOMERS_FILE, PRODUCTS_FILE, SALES_FILE

class PipelineIntegrationTests(unittest.TestCase):
    def test_sample_sources_transform_without_rejects(self):
        records, rejects = transform_sources(CUSTOMERS_FILE, PRODUCTS_FILE, SALES_FILE)
        self.assertGreater(len(records), 0)
        self.assertEqual(rejects, [])
        self.assertTrue(all(row["revenue"] == row["quantity"] * row["unit_price"] for row in records))

if __name__ == "__main__":
    unittest.main()
