import json
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

MARKETAUX_API_KEY = os.getenv("MARKETAUX_API_KEY")
BASE_URL = "https://api.marketaux.com/v1/news/all"
SYMBOLS = "AAPL,MSFT,NVDA,TSLA,AMZN,GOOGL,META,SPY"


def fetch_news() -> list[dict]:
    params = {
        "symbols": SYMBOLS,
        "filter_entities": "true",
        "language": "en",
        "limit": 20,
        "api_token": MARKETAUX_API_KEY,
    }
    response = httpx.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    articles = response.json().get("data", [])

    result = []
    for article in articles:
        entities = article.get("entities") or []
        tickers = list({e["symbol"] for e in entities if e.get("symbol")})
        scores = [e["sentiment_score"] for e in entities if e.get("sentiment_score") is not None]
        sentiment_score = round(sum(scores) / len(scores), 2) if scores else None

        result.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "published_at": article.get("published_at"),
            "source": article.get("source"),
            "tickers": tickers,
            "sentiment_score": sentiment_score,
        })

    return result


def main():
    if not MARKETAUX_API_KEY:
        print(json.dumps({"error": "MARKETAUX_API_KEY not set in environment"}))
        sys.exit(1)

    try:
        articles = fetch_news()
    except httpx.HTTPStatusError as e:
        print(json.dumps({"error": f"HTTP {e.response.status_code}: {e.response.text}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    print(json.dumps(articles))


if __name__ == "__main__":
    main()
