import asyncio

from aiogram import Router, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from bot.initialize_bot import dp, bot

router = Router()
load_dotenv('bot/.env')


@router.message(CommandStart())
async def handle_start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Hello! I'm your bot.")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
