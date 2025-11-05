import os

from aiogram import Bot, types, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Load environment variables: try project root first, then fallback to bot/.env
load_dotenv()
load_dotenv("bot/.env")

# Validate BOT_TOKEN before creating the Bot instance
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "Environment variable BOT_TOKEN is not set. Please set BOT_TOKEN in the environment or in a .env file (project root or bot/.env)."
    )

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
