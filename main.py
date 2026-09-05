import asyncio
import logging

from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from bot.handlers.start import start_command_router
from bot.initialize_bot import dp, bot
from bot.utils.format_position import format_position
from bot.utils.get_decision import create_trading_agent, fetch_decision
from bot.utils.state import SUBSCRIBERS, add_signal_to_history, unsubscribe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


AUTO_ANALYSIS_INTERVAL_SECONDS = 30 * 60


async def auto_analysis_loop():
    while True:
        await asyncio.sleep(AUTO_ANALYSIS_INTERVAL_SECONDS)

        if not SUBSCRIBERS:
            logger.info("No subscribers yet, skipping scheduled analysis cycle")
            continue

        logger.info("Starting scheduled market analysis cycle")
        try:
            agent = create_trading_agent()
            content, model_id = await fetch_decision(agent)
        except Exception:
            logger.exception("Scheduled market analysis cycle failed")
            continue

        if content is None:
            logger.warning("Scheduled market analysis returned no decision. Last model: %s", model_id)
            continue

        formatted = format_position(content, model_id)
        logger.info("Scheduled market analysis completed with model %s", model_id)

        for chat_id in list(SUBSCRIBERS):
            try:
                await bot.send_message(chat_id=chat_id, text=f"🔔 <b>Авто-сигнал</b>\n\n{formatted}")
                add_signal_to_history(chat_id, formatted)
            except TelegramForbiddenError:
                # Пользователь заблокировал бота — убираем из подписчиков
                unsubscribe(chat_id)
            except TelegramBadRequest:
                logger.exception("Failed to send scheduled signal to chat %s", chat_id)


async def main():
    dp.include_router(start_command_router)
    asyncio.create_task(auto_analysis_loop())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
