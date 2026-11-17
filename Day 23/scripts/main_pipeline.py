import json
from datetime import datetime, timezone

from scripts.common import get_logger, write_json
from scripts.api_ingestion import run_api_ingestion
from scripts.web_scraper import scrape_books
from scripts.file_processor import process_files
from scripts.database_extractor import extract_incremental

logger = get_logger("main_pipeline")

def run_pipeline():
    started = datetime.now(timezone.utc).isoformat()
    summary = {"started_at": started, "sources": {}}

    summary["sources"]["apis"] = run_api_ingestion()
    for name, function in [
        ("web_scraping", scrape_books),
        ("file_processing", process_files),
        ("database_extraction", extract_incremental),
    ]:
        try:
            result = function()
            summary["sources"][name] = {"status": "success", "records": result}
        except Exception as exc:
            logger.exception("%s failed: %s", name, exc)
            summary["sources"][name] = {"status": "failed", "error": str(exc)}

    summary["finished_at"] = datetime.now(timezone.utc).isoformat()
    source_statuses = []
    for source_name, source_result in summary["sources"].items():
        if source_name == "apis":
            source_statuses.extend(
                item.get("status") for item in source_result.values()
                if isinstance(item, dict)
            )
        elif isinstance(source_result, dict):
            source_statuses.append(source_result.get("status"))
    summary["overall_status"] = (
        "success" if source_statuses and all(status == "success" for status in source_statuses)
        else "partial_failure"
    )
    write_json(summary, __import__("pathlib").Path(__file__).resolve().parents[1] / "staging" / "pipeline_summary.json")
    logger.info("Pipeline finished with status: %s", summary["overall_status"])
    print(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    run_pipeline()
