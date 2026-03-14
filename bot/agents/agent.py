from dotenv import load_dotenv
from upsonic.agent import Agent
from pydantic_ai import ModelSettings
from bot.agents.prompts.trading_strategy import TRADING_STRATEGY

load_dotenv()

SELECTED_MODEL = "mistral/codestral-latest"

agent = Agent(
    settings=ModelSettings(
        temperature=0.2,
        presence_penalty=0.0,
        frequency_penalty=0.0,
    ),
    model=SELECTED_MODEL,
    name="BTC Trading Agent",
    role="Professional crypto trader using ICT/SMC methodology",
    goal="Analyze BTCUSDT and produce LONG/SHORT/WAIT decision",
    instructions=f"{TRADING_STRATEGY}\n Translate into Russian language"
)
