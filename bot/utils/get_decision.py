from bot.agents.agent import create_agent


async def get_decision(symbol: str = "BTCUSDT") -> tuple[str, str]:
    agent = create_agent()
    result = await agent.arun(
        stream=None,
        input=f"Проанализируй {symbol} используя все доступные инструменты и верни торговое решение.",
        yield_run_output=True,
    )
    return agent.model.name, result.content
