import asyncio
import logging

from bot.handlers.start import start_command_router
from bot.initialize_bot import dp, bot

logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_router(start_command_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
