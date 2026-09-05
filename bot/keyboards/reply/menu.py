from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BTN_ANALYSIS = "📈 Анализ BTC/USDT"
BTN_HISTORY = "📜 История"
BTN_HELP = "ℹ️ Помощь"


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    """
    Постоянная клавиатура рядом с полем ввода (не в теле сообщения).
    Остаётся на экране, пока не будет заменена или убрана.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ANALYSIS)],
            [KeyboardButton(text=BTN_HISTORY), KeyboardButton(text=BTN_HELP)],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )
