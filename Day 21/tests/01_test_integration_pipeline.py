
import unittest
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

OUTPUT_FILE = (
    BASE_DIR / "outputs" / "files" /
    "pipeline_integrated_data.csv"
)


class TestIntegrationPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not OUTPUT_FILE.exists():
            raise FileNotFoundError(
                "Pipeline output not found. Run the pipeline first."
            )

        cls.df = pd.read_csv(OUTPUT_FILE)

    def test_output_file_contains_four_records(self):
        self.assertEqual(len(self.df), 4)

    def test_required_columns_exist(self):
        required = [
            "customer_key",
            "customer_name",
            "customer_city",
            "sale_id",
            "sale_amount",
            "match_status",
            "source_system",
            "processed_at"
        ]

        for column in required:
            self.assertIn(column, self.df.columns)

    def test_all_customers_are_present(self):
        self.assertEqual(
            set(self.df["customer_key"]),
            {"C001", "C002", "C003"}
        )

    def test_sales_amounts_are_correct(self):
        rahul_total = self.df.loc[
            self.df["customer_key"] == "C001",
            "sale_amount"
        ].sum()

        self.assertEqual(rahul_total, 7000)

    def test_customer_without_sales_is_retained(self):
        arjun = self.df[
            self.df["customer_key"] == "C003"
        ]

        self.assertEqual(len(arjun), 1)
        self.assertEqual(
            arjun.iloc[0]["match_status"],
            "Customer without sales"
        )

    def test_data_lineage_is_present(self):
        self.assertTrue(
            (self.df["source_system"] == "company.db").all()
        )

        self.assertTrue(
            self.df["processed_at"].notna().all()
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
