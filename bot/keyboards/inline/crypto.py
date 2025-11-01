from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def crypto_keyboard() -> InlineKeyboardMarkup:
    """Create the crypto inline keyboard."""
    buttons = [
        [InlineKeyboardButton(text="Bitcoin", callback_data="bitcoin")],
        [InlineKeyboardButton(text="Ethereum", callback_data="ethereum")],
        [InlineKeyboardButton(text="BNB", callback_data="bnb")],
        [InlineKeyboardButton(text="SOL", callback_data="solana")],
        [InlineKeyboardButton(text="Back to main menu", callback_data="back_to_main")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
