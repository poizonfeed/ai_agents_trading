# Market Data Agent Skills

## Tool: fetch_finnhub.py

This script fetches current market data for a list of tickers from Finnhub API.

### What it does
For each ticker in the watchlist, it calls:
`GET https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}`

Response fields used:
- `c` — current price
- `d` — change (absolute)
- `dp` — change percent
- `h` — high of the day
- `l` — low of the day
- `o` — open price
- `v` — volume (if available)

Prints a JSON object to stdout:
```json
{
  "AAPL": {"current": 182.5, "change_pct": 1.2, "high": 183.0, "low": 180.1, "open": 181.0},
  "MSFT": {...},
  ...
}
```

### When to create it
Create this script only if `agents/market_data_agent/fetch_finnhub.py`
does not exist.

### Script spec (use when creating fetch_finnhub.py)
- Language: Python 3
- Dependencies: `httpx`, `python-dotenv` (already in requirements.txt)
- Reads `FINNHUB_API_KEY` from `.env` via `python-dotenv`
- Watchlist hardcoded in script as a list:
  `TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "SPY", "QQQ", "BTC"]`
  Note: for crypto Finnhub uses symbol `BINANCE:BTCUSDT` — handle this alias
- On error for a single ticker: include `{"error": "reason"}` for that ticker,
  continue with the rest
- On complete failure: print `{"error": "description"}` and exit with code 1
- No print statements other than the final JSON output

## Tool: research/market_research.md

Output file. Written by the agent after analyzing the fetched data.
Location is always `research/market_research.md` relative to project root.
