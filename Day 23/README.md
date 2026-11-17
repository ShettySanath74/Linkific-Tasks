# Day 23 – Multi-Source Data Collection and Ingestion Pipeline

## 1. Overview
A Python-based ingestion project that collects raw data from REST APIs, a public website, local CSV/Excel/JSON files, and a SQLite source database, then stores source outputs in a staging area.

## 2. Objectives
- Connect to three APIs and collect records.
- Demonstrate GitHub token authentication and API pagination.
- Apply timeouts, retries, exponential backoff and a polite scraping delay.
- Scrape product data from Books to Scrape.
- Process CSV in chunks and process Excel/JSON in bounded batches.
- Extract database rows incrementally using an ID watermark.
- Orchestrate collectors and maintain logs and a pipeline summary.

## 3. Technologies
Python, Requests, python-dotenv, BeautifulSoup, Pandas, OpenPyXL, SQLite, JSONL, pytest.

## 4. Folder structure
- `scripts/`: source collectors and pipeline orchestrator.
- `config/`: environment-based configuration.
- `data/input/`: sample CSV, Excel and JSON inputs.
- `data/source_database/`: generated SQLite source database.
- `staging/`: raw collected data, separated by source.
- `logs/`: execution log.
- `state/`: incremental extraction watermark.
- `tests/`: basic automated checks.

## 5. Architecture / workflow
APIs, website, local files and SQLite source database → Python source-specific collectors → JSONL raw staging files → pipeline summary and logs.

## 6. Implementation details
- JSONPlaceholder: paginated public posts API.
- REST Countries: country reference data API.
- GitHub: authenticated user repositories endpoint with page-based pagination.
- API requests use configurable timeouts, retry handling for timeouts, connection errors, HTTP 429 and server errors, and exponential backoff. The server `Retry-After` header is respected when it contains a numeric delay.
- Books to Scrape: static HTML extraction using Requests and BeautifulSoup; a one-second delay is applied between pages. Browser automation is not needed for this static site.
- CSV: Pandas chunked reading. Excel and JSON: sequential batches are written to raw JSONL.
- SQLite: source orders are extracted using `order_id > last_successful_id`; the state file advances only when rows are extracted.
- The orchestrator continues to later sources if one source fails and records source-level outcomes.

## 7. Setup (Windows PowerShell)
1. Open this folder in PowerShell.
2. Create a virtual environment (recommended): `py -3.14 -m venv .venv`
3. Activate it: `.\.venv\Scripts\Activate.ps1`
4. Install dependencies: `python -m pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add a GitHub token to `GITHUB_TOKEN`.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again. You can also use `.venv\Scripts\python.exe` without activation.

## 8. Execution
From the `Day 23` directory:
- Full pipeline: `python -m scripts.main_pipeline`
- API collectors only: `python -m scripts.api_ingestion`
- Scraper only: `python -m scripts.web_scraper`
- File processor only: `python -m scripts.file_processor`
- Database extractor only: `python -m scripts.database_extractor`

## 9. Testing and validation
Run `python -m pytest -q`. Inspect JSONL outputs under `staging/`, pipeline outcomes in `staging/pipeline_summary.json`, and logs in `logs/ingestion.log`. Actual record counts and pass/fail results must be recorded after execution; they are not assumed in advance.

## 10. Results
Results are generated at runtime. No live API or scraping execution is claimed by this starter project.

## 11. Limitations and future improvements
- GitHub token is required for the GitHub collector.
- The API clients are intentionally small examples; production systems should add source-specific schema validation and secrets management.
- Excel processing reads a worksheet into memory before iterating batches; CSV is streamed in chunks.
- The SQLite incremental example uses an increasing numeric primary key. Real systems may require update timestamps, deletes/CDC, composite watermarks, and transactional checkpoints.
- Add persistent retry queues, metrics, data quality rules, and scheduling for production use.
