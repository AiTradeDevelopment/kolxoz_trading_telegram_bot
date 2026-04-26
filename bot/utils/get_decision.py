from bot.agents.agent import agent


async def get_decision(symbol: str = "BTCUSDT") -> str:
    result = await agent.arun(
        stream=None,
        input=f"Проанализируй {symbol} используя все доступные инструменты и верни торговое решение.",
        yield_run_output=True,
    )
    return result.content
