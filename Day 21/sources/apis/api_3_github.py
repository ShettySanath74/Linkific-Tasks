
import requests
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

API_URL = "https://api.github.com/repos/python/cpython"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "api3_github.json"


def collect_github_data():

    print("Connecting to GitHub API...")

    # Optional authentication token
    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"
        print("Authenticated request.")
    else:
        print("Using unauthenticated public API access.")

    try:
        response = requests.get(
            API_URL,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        repository = response.json()

        # Save repository data
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(repository, file, indent=4)

        print("\nGitHub collection successful!")
        print(f"HTTP Status: {response.status_code}")
        print(f"Repository: {repository['full_name']}")
        print(f"Stars: {repository['stargazers_count']}")
        print(f"Forks: {repository['forks_count']}")
        print(f"Language: {repository['language']}")
        print(f"Saved to: {OUTPUT_FILE}")

        # API rate limit information
        print("\nRemaining API requests:",
              response.headers.get("X-RateLimit-Remaining", "Unknown"))

    except requests.exceptions.RequestException as error:
        print(f"GitHub API collection failed: {error}")


if __name__ == "__main__":
    collect_github_data()
