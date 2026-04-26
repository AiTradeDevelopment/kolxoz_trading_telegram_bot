import asyncio
from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.initialize_bot import bot
from bot.keyboards.inline.menu import main_keyboard
from bot.utils.format_position import format_position
from bot.utils.get_decision import create_trading_agent, fetch_decision

start_command_router = Router()


@start_command_router.message(CommandStart())
async def start_handler(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>Hello, {message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )


@start_command_router.callback_query(lambda c: c.data in ["decision"])
async def crypto_choice_handler(callback_query: types.CallbackQuery):
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
    result = None
    while not task.done():
        try:
            # Wait for a short interval (15 seconds) before updating the status
            result = await asyncio.wait_for(task, timeout=15.0)
            break  # Task completed successfully
        except asyncio.TimeoutError:
            # Update message to indicate that it's still processing
            await thinking_msg.edit_text(
                text=f"<b>I'm still thinking...🤔</b>\nStill collecting data and analyzing. Please wait a bit more.\n\n🤖 <b>Model:</b> {model_name}",
                reply_markup=None,
            )

    if result is None:
        await thinking_msg.edit_text(
            text=f"⚠️ <b>AI failed to provide a response</b>\n\n🤖 <b>Model:</b> {model_name}",
            reply_markup=main_keyboard(),
        )
        return

    await thinking_msg.edit_text(
        text=format_position(result, model_name),
        reply_markup=main_keyboard(),
    )


@start_command_router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text=f"<b>Hello, {callback_query.message.chat.full_name}! Please choose option below:</b>",
        reply_markup=main_keyboard(),
    )
    await callback_query.answer()
