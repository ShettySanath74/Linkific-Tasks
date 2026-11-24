import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_validation import inspect_csv

class QualityCheckTests(unittest.TestCase):
    def test_clean_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "clean.csv"
            p.write_text("id,name\n1,Ada\n2,Lin\n", encoding="utf-8")
            r = inspect_csv(p)
            self.assertEqual(r["status"], "ok")
            self.assertEqual(r["row_count"], 2)
            self.assertEqual(r["column_count"], 2)

    def test_blank_cell_is_flagged_for_review(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "blank.csv"
            p.write_text("id,name\n1,\n", encoding="utf-8")
            r = inspect_csv(p)
            self.assertEqual(r["status"], "review")
            self.assertEqual(r["blank_cells"], 1)

    def test_duplicate_row_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "dupes.csv"
            p.write_text("id\n1\n1\n", encoding="utf-8")
            r = inspect_csv(p)
            self.assertEqual(r["duplicate_rows"], 1)

if __name__ == "__main__":
    unittest.main()
