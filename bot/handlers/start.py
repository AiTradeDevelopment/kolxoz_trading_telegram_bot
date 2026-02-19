from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.initialize_bot import bot
from bot.keyboards.inline.crypto import crypto_keyboard
from bot.keyboards.inline.menu import main_keyboard

start_command_router = Router()


@start_command_router.message(CommandStart())
async def start_handler(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>Hello, {message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )


@start_command_router.callback_query(lambda c: c.data in ["long", "short"])
async def menu_handler(callback_query: types.CallbackQuery):
    choice = callback_query.data

    await callback_query.answer(chat_id=callback_query.message.chat.id, text=choice)
    await callback_query.message.edit_reply_markup(
        inline_message_id=str(callback_query.message.message_id),
        text="Please choose another option:",
        reply_markup=crypto_keyboard(),
    )


@start_command_router.callback_query(lambda c: c.data in ["bitcoin and ethereum"])
async def crypto_choice_handler(callback_query: types.CallbackQuery):
    crypto = callback_query.data.upper()

    await callback_query.answer(
        chat_id=callback_query.message.chat.id, text=f"You selected {crypto}!"
    )

    await callback_query.message.edit_text(
        inline_message_id=str(callback_query.message.message_id),
        text="Wait for updates...",
        reply_markup=None,
    )


@start_command_router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text=f"<b>Hello, {callback_query.message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )
    await callback_query.answer()
