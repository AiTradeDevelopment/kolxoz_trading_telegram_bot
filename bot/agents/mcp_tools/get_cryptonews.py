import json

import httpx
from upsonic.tools import tool


@tool
async def get_coindesk_news(query: str = "Bitcoin BTC") -> str:
    """Fetches news articles from the Coindesk News API based on a search query."""
    url = "https://data-api.coindesk.com/news/v1/search"
    params = {
        "search_string": query,
        "lang": "EN",
        "source_key": "coindesk",
        "limit": 20,
        "api_key": "53db396ee2768bb37a95e93775ada602774a24f8ab01e66db8871d8d9a68ca89",
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        data = r.json()

    return json.dumps(data, ensure_ascii=False, indent=2)
