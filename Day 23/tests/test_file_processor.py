from scripts.file_processor import process_files

def test_file_processor_returns_all_formats():
    result = process_files()
    assert set(result) == {"csv", "excel", "json"}
    assert result["csv"] > 0
    assert result["excel"] > 0
    assert result["json"] > 0
