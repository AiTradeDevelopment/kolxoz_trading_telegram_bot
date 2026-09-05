from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard() -> InlineKeyboardMarkup:
    """Кнопка повтора анализа, показывается под карточкой сигнала."""
    buttons = [
        [InlineKeyboardButton(text="🔄 Повторить анализ", callback_data="decision")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
