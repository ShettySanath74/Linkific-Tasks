
import json
from pathlib import Path

import requests


# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Public practice API
API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_users():
    """Fetch user records from the API."""

    try:
        response = requests.get(API_URL, timeout=10)

        # Raise an error if the server returns an unsuccessful status
        response.raise_for_status()

        # Convert the JSON response into Python objects
        users = response.json()

        if not isinstance(users, list):
            raise ValueError("Expected a list of users from the API.")

        print(f"Successfully fetched {len(users)} users.")
        return users

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        return []

    except ValueError as error:
        print(f"Invalid API response: {error}")
        return []


def process_users(users):
    """Extract only the fields required for our data pipeline."""

    processed_users = []

    for user in users:
        processed_users.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("address", {}).get("city")
        })

    return processed_users


def save_users(users):
    """Save processed records to a JSON file."""

    output_file = OUTPUT_DIR / "api_users.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

    print(f"Saved {len(users)} records to: {output_file}")


def main():
    users = fetch_users()

    if not users:
        print("No records to process.")
        return

    processed_users = process_users(users)

    print("\nFirst processed record:")
    print(json.dumps(processed_users[0], indent=4))

    save_users(processed_users)


if __name__ == "__main__":
    main()
