
import json
import time
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://api.github.com/repos/python/cpython/commits"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

PER_PAGE = 10
MAX_PAGES = 3
MAX_RETRIES = 3


def fetch_page(page):
    """Fetch one page, retrying temporary failures."""
    params = {"per_page": PER_PAGE, "page": page}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                API_URL,
                headers=HEADERS,
                params=params,
                timeout=20,
            )

            if response.status_code == 429 or response.status_code >= 500:
                if attempt < MAX_RETRIES - 1:
                    retry_after = response.headers.get("Retry-After")
                    try:
                        delay = float(retry_after) if retry_after else 2 ** attempt
                    except ValueError:
                        delay = 2 ** attempt

                    print(f"Temporary error {response.status_code}; retrying in {delay}s...")
                    time.sleep(min(delay, 30))
                    continue

            response.raise_for_status()
            data = response.json()

            if not isinstance(data, list):
                raise ValueError("Expected a list of commits from GitHub.")

            return data

        except (requests.Timeout, requests.ConnectionError) as error:
            if attempt == MAX_RETRIES - 1:
                raise

            delay = 2 ** attempt
            print(f"Network error: {error}. Retrying in {delay}s...")
            time.sleep(delay)

    return []


def main():
    all_commits = []

    try:
        for page in range(1, MAX_PAGES + 1):
            print(f"Fetching page {page}...")

            commits = fetch_page(page)

            if not commits:
                print("No more commits returned; stopping pagination.")
                break

            for item in commits:
                commit_info = item.get("commit", {})
                author_info = commit_info.get("author") or {}

                all_commits.append({
                    "sha": item.get("sha"),
                    "author": author_info.get("name"),
                    "date": author_info.get("date"),
                    "message": commit_info.get("message"),
                    "url": item.get("html_url"),
                })

            print(f"Collected {len(commits)} commits from page {page}.")

            if len(commits) < PER_PAGE:
                print("Last page reached.")
                break

            # Small delay to avoid sending requests too quickly.
            time.sleep(1)

        output_file = OUTPUT_DIR / "github_commits.json"
        output_file.write_text(
            json.dumps(all_commits, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print(f"\nTotal commits collected: {len(all_commits)}")
        print(f"Saved to: {output_file}")

    except requests.HTTPError as error:
        print(f"GitHub returned an HTTP error: {error}")
        if error.response is not None and error.response.status_code == 403:
            print("Check GitHub's rate-limit headers or try again later.")

    except (requests.RequestException, ValueError, TypeError) as error:
        print(f"Could not collect commit data: {error}")


if __name__ == "__main__":
    main()
