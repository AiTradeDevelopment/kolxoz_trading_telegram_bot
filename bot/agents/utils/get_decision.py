import re

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from bot.agents.prompts.trading_strategy import TRADING_STRATEGY
import os

load_dotenv()
llm = ChatOpenAI(
    model="qwen3.5-plus",
    base_url="https://qwen.aikit.club/v1",
    api_key=os.environ["QWEN_API_KEY"],
    temperature=0.2,
    presence_penalty=0,
    frequency_penalty=0,
    disable_streaming=True
)
agent = create_agent(model=llm)


async def get_decision():
    input_message = {"role": "user", "content": f"{TRADING_STRATEGY}\nВ поле summary текст напиши на русском"}

    result = await agent.ainvoke(
        {"messages": [input_message]}
    )

    response = result['messages'][-1].content

    cleaned = re.sub(r"(?is)<details\b[^>]*>.*?</details>\s*", "", response).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = (re.sub(r"\*\*References:\*\*.*\Z", "", cleaned, flags=re.DOTALL)
    .rstrip()
               )
    return cleaned
