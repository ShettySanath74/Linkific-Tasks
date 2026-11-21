import csv, json, tempfile, unittest, sqlite3
from pathlib import Path
from contextlib import closing
from scripts.transform import transform_records, validate_sale
from scripts.load import load_sales
from scripts.quality_check import run_quality_checks

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.customers=self.root/"customers.json"; self.sales=self.root/"sales.json"
        self.customers.write_text(json.dumps([{"customer_id":"C1","name":"Asha","city":"Mysuru"}]))
    def tearDown(self): self.tmp.cleanup()
    def read_rows(self, path):
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    def transform(self, rows):
        self.sales.write_text(json.dumps(rows))
        accepted=self.root/"accepted.csv"; rejected=self.root/"rejected.csv"
        transform_records(self.customers,self.sales,accepted,rejected)
        return accepted,rejected
    def test_valid_row_accepted(self):
        a,r=self.transform([{"sale_id":"S1","customer_id":"C1","product":"Pen","amount":"10","sale_date":"2026-11-21"}])
        self.assertEqual(len(self.read_rows(a)),1); self.assertEqual(len(self.read_rows(r)),0)
    def test_unknown_customer_rejected(self):
        _,r=self.transform([{"sale_id":"S1","customer_id":"BAD","amount":"10","sale_date":"2026-11-21"}])
        self.assertIn("Customer reference not found",self.read_rows(r)[0]["reason"])
    def test_zero_and_negative_rejected(self):
        for amount in ("0","-2"):
            _,r=self.transform([{"sale_id":"S1","customer_id":"C1","amount":amount,"sale_date":"2026-11-21"}])
            self.assertEqual(len(self.read_rows(r)),1)
    def test_non_numeric_rejected(self):
        _,r=self.transform([{"sale_id":"S1","customer_id":"C1","amount":"abc","sale_date":"2026-11-21"}])
        self.assertIn("not numeric",self.read_rows(r)[0]["reason"])
    def test_bad_date_rejected(self):
        _,r=self.transform([{"sale_id":"S1","customer_id":"C1","amount":"10","sale_date":"21/11/2026"}])
        self.assertIn("YYYY-MM-DD",self.read_rows(r)[0]["reason"])
    def test_duplicate_rejected(self):
        row={"sale_id":"S1","customer_id":"C1","amount":"10","sale_date":"2026-11-21"}
        _,r=self.transform([row,row])
        self.assertEqual(self.read_rows(r)[0]["reason"],"Duplicate sale_id")
    def test_missing_id_rejected(self):
        _,r=self.transform([{"sale_id":"","customer_id":"C1","amount":"10","sale_date":"2026-11-21"}])
        self.assertIn("Missing sale_id",self.read_rows(r)[0]["reason"])
    def test_missing_source_raises(self):
        with self.assertRaises(FileNotFoundError): transform_records(self.customers,self.root/"absent.json")
    def test_incremental_upsert_is_idempotent(self):
        a,_=self.transform([{"sale_id":"S1","customer_id":"C1","amount":"10","sale_date":"2026-11-21"}])
        db=self.root/"warehouse.db"; load_sales(a,db); load_sales(a,db)
        with closing(sqlite3.connect(db)) as c: self.assertEqual(c.execute("select count(*) from sales").fetchone()[0],1)
    def test_quality_check_passes_for_batch(self):
        a,_=self.transform([{"sale_id":"S1","customer_id":"C1","amount":"10","sale_date":"2026-11-21"}])
        db=self.root/"warehouse.db"; load_sales(a,db)
        self.assertTrue(Path(run_quality_checks(a,db)).exists())

if __name__=="__main__": unittest.main(verbosity=2)
