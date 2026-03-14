import json

import httpx
from upsonic.tools import tool


@tool
def get_tradingview_data(symbol: str = "BTCUSDT") -> str:
    """Get TradingView scanner indicators for a symbol"""
    try:
        r = httpx.post(
            "https://scanner.tradingview.com/crypto/scan",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Origin": "https://www.tradingview.com",
                "Referer": "https://www.tradingview.com/",
            },
            json={
                "symbols": {"tickers": [f"BINANCE:{symbol}"]},
                "columns": [
                    "open", "high", "low", "close", "volume",
                    "change", "change_abs",
                    "Recommend.All", "Recommend.MA", "Recommend.Other",
                    "RSI", "RSI[1]",
                    "MACD.macd", "MACD.signal",
                    "BB.upper", "BB.lower", "BB.basis",
                    "EMA20", "EMA50", "EMA200",
                    "High.1M", "Low.1M",
                    "High.3M", "Low.3M",
                ]
            },
            timeout=10,
        )
        return json.dumps(r.json())
    except Exception as e:
        return json.dumps({"error": str(e)})
