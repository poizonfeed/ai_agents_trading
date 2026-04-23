# News Agent Skills

## Tool: fetch_marketaux.py

This script fetches the latest financial news from Marketaux API.

### What it does
Calls:
`GET https://api.marketaux.com/v1/news/all`

With params:
- `symbols` — comma-separated watchlist: `AAPL,MSFT,NVDA,TSLA,AMZN,GOOGL,META,SPY`
- `filter_entities` — `true`
- `language` — `en`
- `limit` — `20`
- `api_token` — from `MARKETAUX_API_KEY` env variable

Prints a JSON array to stdout with simplified article objects:
```json
[
  {
    "title": "...",
    "description": "...",
    "published_at": "...",
    "source": "...",
    "tickers": ["AAPL", "MSFT"],
    "sentiment_score": 0.75
  },
  ...
]
```

Fields to extract from Marketaux response:
- `title` from `data[].title`
- `description` from `data[].description`
- `published_at` from `data[].published_at`
- `source` from `data[].source`
- `tickers` from `data[].entities[].symbol` (collect all unique symbols)
- `sentiment_score` from `data[].entities[].sentiment_score`
  (average across all entities in the article, round to 2 decimals)

### When to create it
Create this script only if `agents/news_agent/fetch_marketaux.py`
does not exist.

### Script spec (use when creating fetch_marketaux.py)
- Language: Python 3
- Dependencies: `httpx`, `python-dotenv` (already in requirements.txt)
- Reads `MARKETAUX_API_KEY` from `.env` via `python-dotenv`
- On empty response: print `[]` and exit with code 0
- On HTTP error: print `{"error": "description"}` and exit with code 1
- No print statements other than the final JSON output

## Tool: research/news_research.md

Output file. Written by the agent after analyzing the fetched articles.
Location is always `research/news_research.md` relative to project root.
