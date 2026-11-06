
import requests
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

API_URL = "https://countriesnow.space/api/v0.1/countries/positions"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_FILE = OUTPUT_DIR / "api2_countries.json"


def collect_countries():

    print("Connecting to CountriesNow API...")

    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()

        result = response.json()

        if result.get("error"):
            raise ValueError(result.get("msg", "API returned an error"))

        countries = result.get("data", [])

        if not isinstance(countries, list) or not countries:
            raise ValueError("No country records received.")

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(countries, file, indent=4, ensure_ascii=False)

        print("\nCountry collection successful!")
        print(f"HTTP Status: {response.status_code}")
        print(f"Countries collected: {len(countries)}")
        print(f"Saved to: {JSON_FILE}")

        print("\nSample country:")
        print(json.dumps(countries[0], indent=4))

    except (requests.exceptions.RequestException, ValueError) as error:
        print(f"API collection failed: {error}")


if __name__ == "__main__":
    collect_countries()
