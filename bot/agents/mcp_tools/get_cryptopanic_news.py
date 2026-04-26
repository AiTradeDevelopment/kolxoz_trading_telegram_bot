import json
import os

from datetime import datetime, timezone

import httpx


def get_cryptopanic_news(symbol: str = "BTC", limit: int = 20) -> str:
    """Get latest crypto news from CryptoPanic Developer API v2"""
    try:
        r = httpx.get(
            "https://data-api.coindesk.com/news/v1/search",  # ✅ правильный endpoint
            params={
                "api_key": os.environ.get("COINDESK_API_KEY", ""),
                "currencies": symbol.upper(),
                "search_string": "Ethereum BTC ecosystem",
                "limit": limit,
                "lang": "en",
                "source_key": "newsbtc",
            },
            timeout=10,
        )
        data = r.json()
        results = data.get("data", [])
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
