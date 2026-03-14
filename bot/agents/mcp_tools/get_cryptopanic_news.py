import json
import os

from datetime import datetime, timezone

import httpx
from upsonic.tools import tool


@tool
def get_cryptopanic_news(symbol: str = "BTC", limit: int = 20) -> str:
    """Get latest crypto news from CryptoPanic Developer API v2"""
    try:
        r = httpx.get(
            "https://cryptopanic.com/api/developer/v2/posts/",  # ✅ правильный endpoint
            params={
                "auth_token": os.environ.get("CRYPTOPANIC_TOKEN", ""),
                "currencies": symbol.upper(),
                "kind": "news",
                "public": "true",
                "regions": "en",
                "filter": "important",
            },
            timeout=10,
        )
        data = r.json()
        results = data.get("results", [])[:limit]
        now = datetime.now(timezone.utc)

        news = []
        for n in results:
            published = n.get("published_at", "")

            try:
                pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                hours_ago = (now - pub_dt).total_seconds() / 3600
                freshness = "≤24h" if hours_ago <= 24 else ("24-72h" if hours_ago <= 72 else ">72h")
            except:
                freshness = "unknown"

            votes = n.get("votes", {})
            positive = votes.get("positive", 0)
            negative = votes.get("negative", 0)
            important = votes.get("important", 0)

            if positive > negative * 1.5:
                sentiment = "bullish"
            elif negative > positive * 1.5:
                sentiment = "bearish"
            else:
                sentiment = "neutral"

            if important > 10 or (positive + negative) > 20:
                impact = "high"
            elif important > 3 or (positive + negative) > 5:
                impact = "medium"
            else:
                impact = "low"

            news.append({
                "title": n.get("title"),
                "published_at": published,
                "freshness": freshness,
                "sentiment": sentiment,
                "impact": impact,
                "source": n.get("source", {}).get("domain"),
                "url": n.get("original_url"),
                "votes": {
                    "positive": positive,
                    "negative": negative,
                    "important": important,
                }
            })

        return json.dumps(news, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
