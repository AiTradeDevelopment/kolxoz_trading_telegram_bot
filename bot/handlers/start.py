import asyncio
import logging
from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart

from bot.initialize_bot import bot
from bot.keyboards.inline.menu import main_keyboard
from bot.utils.format_position import format_position
from bot.utils.get_decision import create_trading_agent, fetch_decision

start_command_router = Router()
BUSY_USERS = set()
logger = logging.getLogger(__name__)


@start_command_router.message(CommandStart())
async def start_handler(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>Hello, {message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )


async def send_trading_analysis(chat_id: int) -> None:
    if chat_id in BUSY_USERS:
        logger.info("Market analysis is already in progress for chat %s", chat_id)
        return

    BUSY_USERS.add(chat_id)
    try:
        agent = create_trading_agent()
        model_name = agent.model_id

        thinking_msg = await bot.send_message(
            chat_id=chat_id,
            text=f"<b>I'm thinking🤔</b>\n🤖 <b>Model:</b> {model_name}",
            reply_markup=None,
        )

        task = asyncio.create_task(fetch_decision(agent))

        while not task.done():
            done, _ = await asyncio.wait([task], timeout=15.0)

            if task in done:
                break

            try:
                await thinking_msg.edit_text(
                    text=f"<b>I'm still thinking...🤔</b>\nStill collecting data and analyzing. Please wait a bit more.\n\n🤖 <b>Model:</b> {model_name}",
                    reply_markup=None,
                )
            except TelegramBadRequest:
                pass

        try:
            response_data = await task
        except Exception as e:
            logger.exception("AI task failed with exception: %s", e)
            response_data = None

        if response_data is None or (isinstance(response_data, tuple) and response_data[0] is None):
            final_model = response_data[1] if response_data else model_name
            await thinking_msg.edit_text(
                text=f"⚠️ <b>AI failed to provide a response after trying available models</b>\n\n🤖 <b>Model:</b> {final_model}",
                reply_markup=main_keyboard(),
            )
            return

        result_content, final_model = response_data
        await thinking_msg.edit_text(
            text=format_position(result_content, final_model),
            reply_markup=main_keyboard(),
        )
    finally:
        BUSY_USERS.discard(chat_id)


@start_command_router.callback_query(lambda c: c.data in ["decision"])
async def crypto_choice_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    if chat_id in BUSY_USERS:
        await callback_query.answer(
            text="⚠️ Analysis is already in progress. Please wait.",
            show_alert=True
        )
        return

    await callback_query.answer()
    await send_trading_analysis(chat_id)


@start_command_router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text=f"<b>Hello, {callback_query.message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )
    await callback_query.answer()
