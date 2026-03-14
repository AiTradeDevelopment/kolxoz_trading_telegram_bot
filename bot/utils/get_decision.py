from upsonic import Task

from bot.agents.agent import agent
from bot.agents.mcp_run.fetch import FetchMCP
from bot.agents.mcp_tools.get_binance_candles import get_binance_candles
from bot.agents.mcp_tools.get_cryptonews import get_coindesk_news
from bot.agents.mcp_tools.get_cryptopanic_news import get_cryptopanic_news
from bot.agents.mcp_tools.get_pivot_levels import get_pivot_levels
from bot.agents.mcp_tools.get_tradingview_data import get_tradingview_data
from bot.agents.models.trade_decision import TradeDecision


async def get_decision():
    task = Task(
        description=(
            "Perform full top-down analysis of BTCUSDT (1D→4H→1H→15m). "
            "Use ALL tools in order. Apply ICT/SMC framework strictly."
        ),
        tools=[
            get_binance_candles,
            get_tradingview_data,
            get_cryptopanic_news,
            get_pivot_levels,
            get_coindesk_news,
            FetchMCP],
        response_format=TradeDecision,
    )
    result = await agent.do_async(task)
    return result.to_text()
