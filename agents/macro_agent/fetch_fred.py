import json
import sys

import httpx
from dotenv import load_dotenv
import os

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
SERIES = ["GDP", "CPIAUCSL", "FEDFUNDS", "UNRATE"]


def fetch_series(series_id: str) -> list[dict]:
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 3,
    }
    response = httpx.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    observations = response.json().get("observations", [])
    return [{"date": o["date"], "value": o["value"]} for o in observations]


def main():
    if not FRED_API_KEY:
        print(json.dumps({"error": "FRED_API_KEY not set in environment"}))
        sys.exit(1)

    result = {}
    for series_id in SERIES:
        try:
            result[series_id] = fetch_series(series_id)
        except Exception as e:
            print(json.dumps({"error": f"Failed to fetch {series_id}: {e}"}))
            sys.exit(1)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
