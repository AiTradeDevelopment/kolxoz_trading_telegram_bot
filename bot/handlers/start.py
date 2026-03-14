from aiogram import F, Router, types
from aiogram.filters import CommandStart

from bot.keyboards.inline.crypto import crypto_keyboard
from bot.keyboards.inline.menu import main_keyboard
from bot.utils.get_decision import get_decision

start_command_router = Router()


def _get_editable_message(
    callback_query: types.CallbackQuery,
) -> types.Message | None:
    message = callback_query.message
    if isinstance(message, types.Message):
        return message
    return None


@start_command_router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    await message.answer(
        text=f"<b>Hello, {message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )


@start_command_router.callback_query(F.data.in_(["long", "short"]))
async def menu_handler(callback_query: types.CallbackQuery) -> None:
    message = _get_editable_message(callback_query)
    if message is None:
        await callback_query.answer()
        return

    choice = callback_query.data or ""
    await callback_query.answer(text=choice)
    await message.edit_text(
        text="Please choose another option:",
        reply_markup=crypto_keyboard(),
    )


@start_command_router.callback_query(F.data == "bitcoin and ethereum")
async def crypto_choice_handler(callback_query: types.CallbackQuery) -> None:
    message = _get_editable_message(callback_query)
    if message is None:
        await callback_query.answer()
        return

    crypto = (callback_query.data or "").upper()
    await callback_query.answer(text=f"You selected {crypto}!")
    await message.edit_text(text="Wait for updates...")


@start_command_router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback_query: types.CallbackQuery) -> None:
    message = _get_editable_message(callback_query)
    if message is None:
        await callback_query.answer()
        return

    await message.edit_text(
        text=f"<b>Hello, {message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )
    await callback_query.answer()
