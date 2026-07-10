import asyncio
import logging

from bot.handlers.start import start_command_router
from bot.initialize_bot import dp, bot
from bot.utils.get_decision import create_trading_agent, fetch_decision

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


AUTO_ANALYSIS_INTERVAL_SECONDS = 30 * 60


async def auto_analysis_loop():
    while True:
        await asyncio.sleep(AUTO_ANALYSIS_INTERVAL_SECONDS)

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

        logger.info("Scheduled market analysis completed with model %s: %s", model_id, content)


async def main():
    dp.include_router(start_command_router)
    asyncio.create_task(auto_analysis_loop())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
