import unittest
from scripts.quality_checks import check_required_fields, check_ranges, check_duplicates, check_date_format

class QualityTests(unittest.TestCase):
    def test_null_check(self):
        self.assertTrue(check_required_fields({"id": "", "name": "A"}, ["id", "name"]))

    def test_range_check(self):
        self.assertTrue(check_ranges({"quantity": -1, "unit_price": 10}))

    def test_duplicate_detection(self):
        rows = [{"id": "A"}, {"id": "A"}, {"id": "B"}]
        self.assertEqual(check_duplicates(rows, "id"), ["A"])

    def test_date_format(self):
        self.assertEqual(check_date_format("2026-01-01"), [])
        self.assertTrue(check_date_format("01/01/2026"))

if __name__ == "__main__":
    unittest.main()
