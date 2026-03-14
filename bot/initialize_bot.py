from __future__ import annotations

import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Load environment variables: try project root first, then fallback to bot/.env
load_dotenv()
load_dotenv("bot/.env")


def _get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN")
    if token is None or not token.strip():
        raise RuntimeError(
            "Environment variable BOT_TOKEN is not set. "
            "Please set BOT_TOKEN in the environment or in a .env file "
            "(project root or bot/.env)."
        )
    return token


BOT_TOKEN: str = _get_bot_token()

bot: Bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(storage=storage)
