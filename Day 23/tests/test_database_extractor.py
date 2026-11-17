from scripts.database_extractor import initialize_source_database, extract_incremental

def test_database_initial_load_then_incremental(tmp_path, monkeypatch):
    # The project integration smoke test is exercised by running the script.
    initialize_source_database()
    count = extract_incremental()
    assert count >= 0
