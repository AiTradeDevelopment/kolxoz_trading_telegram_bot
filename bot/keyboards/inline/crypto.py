from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def crypto_keyboard() -> InlineKeyboardMarkup:
    """Create the crypto inline keyboard."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Bitcoin and Etherium", callback_data="bitcoin and ethereum"
            )
        ],
        [InlineKeyboardButton(text="Back to main menu", callback_data="back_to_main")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
