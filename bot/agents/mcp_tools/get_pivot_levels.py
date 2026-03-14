import json
import httpx

from upsonic.tools import tool


@tool
def get_pivot_levels(symbol: str = "BTCUSDT") -> str:
    """Calculate classic pivot points from yesterday's daily candle"""
    r = httpx.get(
        "https://api.binance.com/api/v3/klines",
        params={"symbol": symbol.upper(), "interval": "1d", "limit": 2},
        timeout=10,
    )
    prev = r.json()[-2]
    high = float(prev[2])
    low = float(prev[3])
    close = float(prev[4])
    pp = (high + low + close) / 3
    return json.dumps({
        "PP": round(pp, 2),
        "R1": round(2 * pp - low, 2),
        "R2": round(pp + (high - low), 2),
        "S1": round(2 * pp - high, 2),
        "S2": round(pp - (high - low), 2),
    })
