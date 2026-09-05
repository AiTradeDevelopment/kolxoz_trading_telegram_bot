import asyncio
import logging
from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart

from bot.initialize_bot import bot
from bot.keyboards.inline.menu import main_keyboard
from bot.keyboards.reply.menu import main_reply_keyboard, BTN_ANALYSIS, BTN_HISTORY, BTN_HELP
from bot.utils.format_position import format_position
from bot.utils.get_decision import create_trading_agent, fetch_decision
from bot.utils.state import add_signal_to_history, get_history, subscribe

start_command_router = Router()
BUSY_USERS = set()
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "<b>👋 Привет, {name}!</b>\n\n"
    "Я — торговый ИИ-ассистент по BTC/USDT. Анализирую рынок по методологии "
    "ICT/SMC на 4 таймфреймах и выдаю решение LONG/SHORT/WAIT со Stop-Loss "
    "и Take-Profit.\n\n"
    "Жми кнопки внизу 👇"
)

HELP_TEXT = (
    "<b>ℹ️ Как это работает</b>\n\n"
    "📈 <b>Анализ BTC/USDT</b> — запускает ИИ-агента: он собирает свечи с "
    "Binance (1D/4H/1H/15m), данные TradingView и новости, затем выдаёт "
    "торговое решение.\n\n"
    "📜 <b>История</b> — последние сигналы, которые ты получал в этом чате "
    "(хранится только пока бот запущен, после перезапуска обнуляется).\n\n"
    "⏳ Анализ занимает 30–90 секунд — модель реально считает уровни, а не "
    "выдаёт готовый шаблон.\n\n"
    "⚠️ Это не финансовый совет — решения принимает LLM на основе публичных "
    "данных, всегда проверяй сигнал сам перед сделкой."
)

ANALYSIS_STEPS = [
    "📊 Загружаю свечи 1D / 4H / 1H / 15m с Binance...",
    "📉 Запрашиваю индикаторы и pivot-уровни TradingView...",
    "📰 Читаю свежие новости по BTC...",
    "🧠 Считаю структуру рынка и точки входа (ICT/SMC)...",
    "✍️ Формирую итоговое решение...",
]


@start_command_router.message(CommandStart())
async def start_handler(message: types.Message):
    subscribe(message.chat.id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=WELCOME_TEXT.format(name=message.chat.full_name),
        reply_markup=main_reply_keyboard(),
    )


@start_command_router.message(Command("help"))
@start_command_router.message(F.text == BTN_HELP)
async def help_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT)


@start_command_router.message(Command("history"))
@start_command_router.message(F.text == BTN_HISTORY)
async def history_handler(message: types.Message):
    await send_history(message.chat.id)


async def send_history(chat_id: int) -> None:
    records = [r for r in get_history(limit=10) if r.chat_id == chat_id][-5:]
    if not records:
        text = "📜 <b>История пуста</b>\n\nЗапроси анализ, и он появится здесь."
    else:
        lines = ["<b>📜 Последние сигналы:</b>\n"]
        for r in reversed(records):
            timestamp = r.created_at.strftime("%d.%m %H:%M UTC")
            preview = r.text.split("\n")[0]
            lines.append(f"🕒 <i>{timestamp}</i>\n{preview}\n")
        text = "\n".join(lines)

    await bot.send_message(chat_id=chat_id, text=text)


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
            text=f"<b>🤖 Начинаю анализ...</b>\n\n{ANALYSIS_STEPS[0]}\n\n<i>Модель: {model_name}</i>",
        )

        task = asyncio.create_task(fetch_decision(agent))
        step_index = 0

        while not task.done():
            done, _ = await asyncio.wait([task], timeout=15.0)

            if task in done:
                break

            step_index = min(step_index + 1, len(ANALYSIS_STEPS) - 1)
            try:
                await thinking_msg.edit_text(
                    text=f"<b>🤖 Анализирую рынок...</b>\n\n{ANALYSIS_STEPS[step_index]}\n\n<i>Модель: {model_name}</i>",
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
                text=(
                    "⚠️ <b>Не удалось получить решение ни от одной модели.</b>\n"
                    "Попробуй ещё раз чуть позже.\n\n"
                    f"🤖 <b>Модель:</b> {final_model}"
                ),
                reply_markup=main_keyboard(),
            )
            return

        result_content, final_model = response_data
        formatted = format_position(result_content, final_model)
        add_signal_to_history(chat_id, formatted)
        await thinking_msg.edit_text(
            text=formatted,
            reply_markup=main_keyboard(),
        )
    finally:
        BUSY_USERS.discard(chat_id)


@start_command_router.message(F.text == BTN_ANALYSIS)
async def analysis_button_handler(message: types.Message):
    chat_id = message.chat.id
    if chat_id in BUSY_USERS:
        await bot.send_message(chat_id=chat_id, text="⚠️ Анализ уже выполняется, подожди немного.")
        return
    await send_trading_analysis(chat_id)


@start_command_router.callback_query(lambda c: c.data == "decision")
async def crypto_choice_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    if chat_id in BUSY_USERS:
        await callback_query.answer(
            text="⚠️ Анализ уже выполняется, подожди немного.",
            show_alert=True,
        )
        return

    await callback_query.answer()
    await send_trading_analysis(chat_id)
