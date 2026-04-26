import asyncio
import logging
from bot.agents.agent import create_agent

logger = logging.getLogger(__name__)

def create_trading_agent():
    """
    Creates and returns a trading agent.
    The model is randomly selected inside create_agent().
    """
    return create_agent()

async def fetch_decision(agent, symbol: str = "BTCUSDT") -> str:
    """
    Runs the agent to get a trading decision for the specified symbol.
    """
    logger.info(f"Fetching decision for {symbol} using model {agent.model_id}")
    try:
        result = await asyncio.wait_for(
            agent.arun(
                stream=None,
                input=f"Проанализируй {symbol} используя все доступные инструменты и верни торговое решение.",
                yield_run_output=True,
            ),
            timeout=90.0
        )

        if result is None:
            logger.error(f"Agent.arun returned None for {symbol} with model {agent.model_id}")
            return None

        if not result.content:
            logger.warning(f"Agent returned empty content for {symbol} with model {agent.model_id}")

        return result.content
    except asyncio.TimeoutError:
        logger.error(f"AI request timed out after 90 seconds for {symbol} with model {agent.model_id}")
        return None
    except Exception as e:
        logger.exception(f"Error occurred while fetching decision for {symbol} with model {agent.model_id}: {e}")
        return None
