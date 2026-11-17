from datetime import datetime, timezone
import time
import requests

from config.settings import TIMEOUT, MAX_RETRIES, BACKOFF_SECONDS, PAGE_SIZE, GITHUB_TOKEN, STAGING_DIR
from scripts.common import get_logger, write_jsonl

logger = get_logger("api_ingestion")
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Linkific-Day23-Ingestion/1.0"})

def request_json(url, params=None, headers=None):
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = SESSION.get(url, params=params, headers=headers, timeout=TIMEOUT)
            if response.status_code == 429 or response.status_code >= 500:
                if attempt < MAX_RETRIES:
                    retry_after = response.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after and retry_after.isdigit() else BACKOFF_SECONDS * (2 ** attempt)
                    logger.warning("Retryable HTTP %s from %s; waiting %.1fs", response.status_code, url, delay)
                    time.sleep(delay)
                    continue
            response.raise_for_status()
            return response.json()
        except (requests.Timeout, requests.ConnectionError) as exc:
            if attempt >= MAX_RETRIES:
                raise
            delay = BACKOFF_SECONDS * (2 ** attempt)
            logger.warning("Request failed (%s); retrying in %.1fs", exc, delay)
            time.sleep(delay)
    raise RuntimeError(f"Request failed after retries: {url}")

def collect_jsonplaceholder():
    records = []
    # JSONPlaceholder supports _page and _limit pagination.
    for page in range(1, 4):
        batch = request_json("https://jsonplaceholder.typicode.com/posts",
                             {"_page": page, "_limit": PAGE_SIZE})
        if not batch:
            break
        records.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
    write_jsonl(records, STAGING_DIR / "api" / "jsonplaceholder_posts.jsonl")
    logger.info("JSONPlaceholder: collected %d posts", len(records))
    return len(records)


def collect_rest_countries():
    """Collect country information from the CountriesNow API."""

    data = request_json(
        "https://countriesnow.space/api/v0.1/countries/info",
        {
            "returns": "iso2,iso3,capital,flag,currency"
        }
    )

    if not isinstance(data, dict) or data.get("error") is True:
        raise RuntimeError(f"CountriesNow API returned an error: {data}")

    countries = data.get("data", [])

    if not isinstance(countries, list):
        raise RuntimeError("Unexpected CountriesNow API response format.")

    records = []

    for item in countries:
        records.append({
            "name": item.get("name"),
            "country_code": item.get("iso2"),
            "country_code_3": item.get("iso3"),
            "capital": item.get("capital"),
            "currency": item.get("currency"),
            "flag": item.get("flag")
        })

    write_jsonl(
        records,
        STAGING_DIR / "api" / "rest_countries.jsonl"
    )

    logger.info(
        "CountriesNow: collected %d countries",
        len(records)
    )

    return len(records)

def collect_github_repositories():
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN is missing. Add it to Day 23/.env before running the full pipeline.")
    records, page = [], 1
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
    while True:
        batch = request_json("https://api.github.com/user/repos",
                             {"per_page": PAGE_SIZE, "page": page, "sort": "updated"},
                             headers=headers)
        if not batch:
            break
        records.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        page += 1
    write_jsonl(records, STAGING_DIR / "api" / "github_repositories.jsonl")
    logger.info("GitHub: collected %d repositories", len(records))
    return len(records)

def run_api_ingestion():
    results = {}
    # Continue collecting from other APIs if one source fails.
    collectors = {
        "jsonplaceholder": collect_jsonplaceholder,
        "rest_countries": collect_rest_countries,
        "github": collect_github_repositories,
    }
    for name, collector in collectors.items():
        try:
            results[name] = {"status": "success", "records": collector()}
        except Exception as exc:
            logger.exception("%s ingestion failed: %s", name, exc)
            results[name] = {"status": "failed", "error": str(exc)}
    return results

if __name__ == "__main__":
    print(run_api_ingestion())
