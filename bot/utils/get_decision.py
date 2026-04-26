from bot.agents.agent import create_agent

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
    result = await agent.arun(
        stream=None,
        input=f"Проанализируй {symbol} используя все доступные инструменты и верни торговое решение.",
        yield_run_output=True,
    )
    return result.content
