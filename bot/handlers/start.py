from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.initialize_bot import bot
from bot.keyboards.inline.menu import main_keyboard
from bot.utils.get_decision import get_decision

start_command_router = Router()


@start_command_router.message(CommandStart())
async def start_handler(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>Hello, {message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )


@start_command_router.callback_query(lambda c: c.data in ["decision"])
async def crypto_choice_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        inline_message_id=str(callback_query.message.message_id),
        text="<b>I'm thinking🤔</b>",
        reply_markup=None,
    )
    result = await get_decision()
    await callback_query.message.edit_text(
        inline_message_id=str(callback_query.message.message_id),
        text=result,
        reply_markup=None,
    )


@start_command_router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text=f"<b>Hello, {callback_query.message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )
    await callback_query.answer()
