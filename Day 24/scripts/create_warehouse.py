from scripts.config import SCHEMA_SQL, get_connection

def create_warehouse():
    with get_connection() as conn:
        conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
    print("Warehouse schema created/verified.")

if __name__ == "__main__":
    create_warehouse()
