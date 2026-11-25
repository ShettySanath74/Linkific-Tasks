import sys
import tempfile
import unittest
from pathlib import Path

# Make the Day 30 folder importable when unittest is launched from the repo root.
DAY30_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DAY30_ROOT))

from scripts.project_audit import audit

class ProjectAuditTests(unittest.TestCase):
    def test_reports_existing_and_missing_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Day 28").mkdir()
            (root / "Day 28" / "README.md").write_text("# demo", encoding="utf-8")
            present, missing = audit(root)
            self.assertIn("Day 28/README.md", present)
            self.assertIn("Day 28/data/customers.csv", missing)

if __name__ == "__main__":
    unittest.main()
