import json

import httpx
from upsonic.tools import tool


@tool
def get_binance_candles(symbol: str = "BTCUSDT", interval: str = "1d", limit: int = 100) -> str:
    """Get OHLCV candles from Binance API. Intervals: 1m,5m,15m,1h,4h,1d"""
    r = httpx.get(
        "https://api.binance.com/api/v3/klines",
        params={"symbol": symbol.upper(), "interval": interval, "limit": limit},
        timeout=10,
    )
    candles = [
        {
            "time": c[0], "open": float(c[1]), "high": float(c[2]),
            "low": float(c[3]), "close": float(c[4]), "volume": float(c[5]),
        }
        for c in r.json()
    ]
    return json.dumps(candles)
