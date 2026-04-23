# Macro Agent Skills

## Tool: fetch_fred.py

This script fetches the latest macroeconomic data from the FRED API.

### What it does
- Connects to `https://api.stlouisfed.org/fred/series/observations`
- Fetches the last 3 observations for each of the following series:
  - `GDP` — Gross Domestic Product
  - `CPIAUCSL` — Consumer Price Index (All Urban Consumers)
  - `FEDFUNDS` — Federal Funds Effective Rate
  - `UNRATE` — Unemployment Rate
- Prints a JSON object to stdout with the following shape:
```json
{
  "GDP": [{"date": "...", "value": "..."}, ...],
  "CPIAUCSL": [...],
  "FEDFUNDS": [...],
  "UNRATE": [...]
}
```

### When to create it
Create this script only if `agents/macro_agent/fetch_fred.py` does not exist.

### Script spec (use when creating fetch_fred.py)
- Language: Python 3
- Dependencies: `httpx`, `python-dotenv` (both in requirements.txt)
- Reads `FRED_API_KEY` from `.env` via `python-dotenv`
- Uses `httpx.get()` for HTTP requests
- Query params: `series_id`, `api_key`, `file_type=json`, `sort_order=desc`, `limit=3`
- On error: print `{"error": "description"}` and exit with code 1
- No print statements other than the final JSON output (so the agent can parse stdout cleanly)

## Tool: research/macro_research.md

Output file. Written by the agent after analyzing the fetched data.
Location is always `research/macro_research.md` relative to project root.
