import logging
from typing import Optional
from dotenv import load_dotenv
from agno.models.nvidia import Nvidia
from agno.agent import Agent
from bot.agents.prompts.trading_strategy import PROMPT_TRADING_STRATEGY
from bot.agents.mcp_run.fetch import fetch_mcp_data
from bot.agents.mcp_tools.get_binance_candles import get_binance_candles
from bot.agents.mcp_tools.get_cryptonews import get_coindesk_news
from bot.agents.mcp_tools.get_cryptopanic_news import get_cryptopanic_news
from bot.agents.mcp_tools.get_pivot_levels import get_pivot_levels
from bot.agents.mcp_tools.get_tradingview_data import get_tradingview_data

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


AVAILABLE_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b",
    "deepseek-ai/deepseek-v4-pro-0813",
    "moonshotai/kimi-k3",
]

_next_model_index = 0


def get_next_model() -> str:
    """Return primary models in the same order as ``AVAILABLE_MODELS``."""
    global _next_model_index

    if not AVAILABLE_MODELS:
        raise RuntimeError("AVAILABLE_MODELS must contain at least one model")

    selected = AVAILABLE_MODELS[_next_model_index % len(AVAILABLE_MODELS)]
    _next_model_index = (_next_model_index + 1) % len(AVAILABLE_MODELS)
    logger.info("SELECTED_MODEL: %s", selected)
    return selected


def create_agent(model_id: str | None = None):
    if model_id is None:
        model_id = get_next_model()

    agent = Agent(
        model=Nvidia(model_id, temperature=0.2, frequency_penalty=0.0, presence_penalty=0.0),
        name="BTC Trading Agent",
        role="Professional crypto trader using ICT/SMC methodology",
        instructions=f"{PROMPT_TRADING_STRATEGY}\n Translate into Russian language",
        tools=[
            get_binance_candles,
            get_tradingview_data,
            get_cryptopanic_news,
            get_pivot_levels,
            get_coindesk_news,
            fetch_mcp_data],
    )
    # agno.Agent не объявляет model_id как штатное поле, поэтому Pylance
    # ругается на динамическое присваивание — это ожидаемо и безопасно,
    # setattr явно показывает, что мы намеренно вешаем свой атрибут.
    setattr(agent, "model_id", model_id)
    return agent
