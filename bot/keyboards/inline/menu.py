from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard() -> InlineKeyboardMarkup:
    """Create the main inline keyboard."""
    buttons = [
        [InlineKeyboardButton(text="🟢When long🟢", callback_data="long")],
        [InlineKeyboardButton(text="🔴When short🔴", callback_data="short")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
