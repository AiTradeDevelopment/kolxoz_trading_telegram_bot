import asyncio
from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart

from bot.initialize_bot import bot
from bot.keyboards.inline.menu import main_keyboard
from bot.utils.format_position import format_position
from bot.utils.get_decision import create_trading_agent, fetch_decision

start_command_router = Router()
BUSY_USERS = set()


@start_command_router.message(CommandStart())
async def start_handler(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>Hello, {message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )


@start_command_router.callback_query(lambda c: c.data in ["decision"])
async def crypto_choice_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id in BUSY_USERS:
        await callback_query.answer(
            text="⚠️ Analysis is already in progress. Please wait.",
            show_alert=True
        )
        return

    BUSY_USERS.add(user_id)
    try:
        # Initialize agent immediately to get the model name
        agent = create_trading_agent()
        model_name = agent.model_id

        thinking_msg = await callback_query.message.answer(
            text=f"<b>I'm thinking🤔</b>\n🤖 <b>Model:</b> {model_name}",
            reply_markup=None,
        )

        # Create a task to fetch the decision in the background
        task = asyncio.create_task(fetch_decision(agent))

        # Periodically update the message while the AI is thinking
        while not task.done():
            # Wait for either the task to complete or the timeout to trigger
            # asyncio.wait does NOT cancel the task, unlike wait_for
            done, _ = await asyncio.wait([task], timeout=15.0)

            if task in done:
                break

            # Update message to indicate that it's still processing
            try:
                await thinking_msg.edit_text(
                    text=f"<b>I'm still thinking...🤔</b>\nStill collecting data and analyzing. Please wait a bit more.\n\n🤖 <b>Model:</b> {model_name}",
                    reply_markup=None,
                )
            except TelegramBadRequest:
                # Ignore error if message content hasn't changed
                pass

        # Retrieve the final result from the task
        try:
            response_data = await task
        except Exception as e:
            # Log the exception and set response_data to None so the error message is shown
            import logging
            logging.getLogger(__name__).exception(f"AI task failed with exception: {e}")
            response_data = None

        if response_data is None or (isinstance(response_data, tuple) and response_data[0] is None):
            # Use the model name from the agent if the result is None
            final_model = response_data[1] if response_data else model_name
            await thinking_msg.edit_text(
                text=f"⚠️ <b>AI failed to provide a response after trying available models</b>\n\n🤖 <b>Model:</b> {final_model}",
                reply_markup=main_keyboard(),
            )
            return

        result_content, final_model = response_data
        await thinking_msg.edit_text(
            text=format_position(result_content, final_model),
            reply_markup=main_keyboard(),
        )
    finally:
        BUSY_USERS.remove(user_id)


@start_command_router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text=f"<b>Hello, {callback_query.message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )
    await callback_query.answer()
