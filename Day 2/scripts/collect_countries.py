
import json
from pathlib import Path

import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://api.restcountries.com/countries/v5"
HEADERS = {
    "Authorization": "Bearer rc_live_demo"
}
PARAMS = {
    "limit": 100,
    "response_fields": (
        "names.common,codes.alpha_3,capitals,region,population"
    ),
}

try:
    print("Connecting to REST Countries v5 API...")

    response = requests.get(
        API_URL,
        headers=HEADERS,
        params=PARAMS,
        timeout=20,
    )

    print("HTTP status:", response.status_code)
    response.raise_for_status()

    payload = response.json()

    # Validate the API response structure.
    if "errors" in payload:
        raise ValueError(f"API error: {payload['errors']}")

    countries = payload.get("data", {}).get("objects", [])

    if not isinstance(countries, list) or not countries:
        raise ValueError(
            f"No country records returned: {str(payload)[:500]}"
        )

    records = []

    for country in countries:
        names = country.get("names") or {}
        codes = country.get("codes") or {}

        records.append({
            "country": names.get("common", "Unknown"),
            "country_code": codes.get("alpha_3", ""),
           "capital": ", ".join(
    str(capital.get("name", ""))
    if isinstance(capital, dict)
    else str(capital)
    for capital in (country.get("capitals") or [])
),
            "region": country.get("region", "Unknown"),
            "population": country.get("population", 0),
        })

    df = pd.DataFrame(records)

    csv_path = OUTPUT_DIR / "countries.csv"
    json_path = OUTPUT_DIR / "countries.json"

    df.to_csv(csv_path, index=False)

    json_path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Success! Collected {len(records)} country records.")
    print(f"CSV saved: {csv_path}")
    print(f"JSON saved: {json_path}")

except (requests.RequestException, ValueError, TypeError, KeyError) as error:
    print(f"Country collection failed: {error}")
