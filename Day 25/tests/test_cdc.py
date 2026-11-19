import unittest
from scripts.db import connect
from scripts.cdc import detect_changes, record_hash, save_source_state

class CDCTests(unittest.TestCase):
    def test_insert_then_unchanged_then_update(self):
        conn = connect()
        try:
            record = {"order_id": "TEST-CDC-1", "quantity": 1}
            first = detect_changes(conn, "test", [record], "order_id")
            self.assertEqual(len(first["insert"]), 1)
            digest = record_hash(record)
            save_source_state(conn, "test", "TEST-CDC-1", digest, 0, "2026-01-01")
            conn.commit()

            same = detect_changes(conn, "test", [record], "order_id")
            self.assertEqual(len(same["unchanged"]), 1)

            changed = {"order_id": "TEST-CDC-1", "quantity": 2}
            update = detect_changes(conn, "test", [changed], "order_id")
            self.assertEqual(len(update["update"]), 1)
        finally:
            conn.close()

if __name__ == "__main__":
    unittest.main()
