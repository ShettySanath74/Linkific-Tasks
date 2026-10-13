
import json
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

# Find the Day 2 project folder
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load optional environment variables from the project folder
load_dotenv(BASE_DIR / ".env")

# Public GitHub repository API
API_URL = "https://api.github.com/repos/python/cpython"

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Add authentication only if a token is configured
github_token = os.getenv("GITHUB_TOKEN")
if github_token:
    headers["Authorization"] = f"Bearer {github_token}"


def main():
    try:
        print("Connecting to GitHub API...")

        response = requests.get(
            API_URL,
            headers=headers,
            timeout=20,
        )

        print("HTTP status:", response.status_code)
        response.raise_for_status()

        repository = response.json()

        # Select useful fields from the response
        record = {
            "name": repository.get("name"),
            "full_name": repository.get("full_name"),
            "description": repository.get("description"),
            "stars": repository.get("stargazers_count"),
            "forks": repository.get("forks_count"),
            "open_issues": repository.get("open_issues_count"),
            "language": repository.get("language"),
            "html_url": repository.get("html_url"),
            "default_branch": repository.get("default_branch"),
        }

        output_file = OUTPUT_DIR / "github_repository.json"
        output_file.write_text(
            json.dumps(record, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print("Success! Repository information collected.")
        print("Repository:", record["full_name"])
        print("Stars:", record["stars"])
        print("Saved to:", output_file)

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again.")

    except requests.exceptions.HTTPError as error:
        print("GitHub returned an HTTP error:", error)
        if response.status_code == 403:
            print("You may have reached the API rate limit.")
        elif response.status_code == 404:
            print("The repository was not found.")

    except requests.exceptions.RequestException as error:
        print("Network or request error:", error)

    except (ValueError, TypeError) as error:
        print("Could not process the API response:", error)


if __name__ == "__main__":
    main()
