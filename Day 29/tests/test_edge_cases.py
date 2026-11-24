import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_validation import inspect_csv

class EdgeCaseTests(unittest.TestCase):
    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "empty.csv"
            p.write_bytes(b"")
            r = inspect_csv(p)
            self.assertEqual(r["status"], "failed")
            self.assertIn("empty", r["issues"][0].lower())

    def test_inconsistent_row_width(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "width.csv"
            p.write_text("id,name\n1,A\n2,B,extra\n", encoding="utf-8")
            r = inspect_csv(p)
            self.assertEqual(r["inconsistent_rows"], 1)
            self.assertEqual(r["status"], "review")

    def test_duplicate_headers(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "headers.csv"
            p.write_text("id,id\n1,2\n", encoding="utf-8")
            r = inspect_csv(p)
            self.assertIn("Duplicate column names detected.", r["issues"])

if __name__ == "__main__":
    unittest.main()
