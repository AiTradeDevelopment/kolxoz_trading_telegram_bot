from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard() -> InlineKeyboardMarkup:
    """Create the main inline keyboard."""
    buttons = [
        [InlineKeyboardButton(text="Make decision BTC/USDT", callback_data="decision", style="primary")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
