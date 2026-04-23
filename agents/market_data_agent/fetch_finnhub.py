import json
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1/quote"
TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "SPY", "QQQ", "BTC"]

TICKER_ALIASES = {
    "BTC": "BINANCE:BTCUSDT",
}


def fetch_quote(ticker: str) -> dict:
    symbol = TICKER_ALIASES.get(ticker, ticker)
    params = {"symbol": symbol, "token": FINNHUB_API_KEY}
    response = httpx.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("c", 0) == 0:
        return {"error": f"no data returned for {symbol}"}
    return {
        "current": data["c"],
        "change_pct": data["dp"],
        "high": data["h"],
        "low": data["l"],
        "open": data["o"],
    }


def main():
    if not FINNHUB_API_KEY:
        print(json.dumps({"error": "FINNHUB_API_KEY not set in environment"}))
        sys.exit(1)

    result = {}
    for ticker in TICKERS:
        try:
            result[ticker] = fetch_quote(ticker)
        except Exception as e:
            result[ticker] = {"error": str(e)}

    print(json.dumps(result))


if __name__ == "__main__":
    main()
