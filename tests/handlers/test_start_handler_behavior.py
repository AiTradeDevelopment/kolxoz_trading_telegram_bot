from __future__ import annotations

import importlib
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from aiogram import types


def _make_chat(chat_id: int = 123, full_name: str = "Test User") -> types.Chat:
    return types.Chat(id=chat_id, type="private", first_name=full_name)


def _make_callback_query(
    data: str,
    message: object,
) -> SimpleNamespace:
    callback_query = SimpleNamespace()
    callback_query.data = data
    callback_query.message = message
    callback_query.answer = AsyncMock()
    return callback_query


class TestStartHandlerBehavior(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.start_module = importlib.import_module("bot.handlers.start")

    async def test_start_handler_sends_main_keyboard(self) -> None:
        message = SimpleNamespace()
        message.chat = SimpleNamespace(id=123, full_name="Alice")
        message.answer = AsyncMock()

        await self.start_module.start_handler(message)

        message.answer.assert_awaited_once()
        await_args = message.answer.await_args
        assert await_args is not None
        kwargs = await_args.kwargs
        self.assertIn("Hello, Alice!", kwargs["text"])
        self.assertEqual(
            kwargs["reply_markup"].inline_keyboard[0][0].callback_data, "long"
        )
        self.assertEqual(
            kwargs["reply_markup"].inline_keyboard[1][0].callback_data, "short"
        )

    async def test_menu_handler_long_shows_crypto_keyboard(self) -> None:
        editable_message = SimpleNamespace()
        editable_message.chat = SimpleNamespace(full_name="Test User")
        editable_message.edit_text = AsyncMock()

        callback_query = _make_callback_query(data="long", message=editable_message)

        with patch(
            "bot.handlers.start._get_editable_message", return_value=editable_message
        ):
            await self.start_module.menu_handler(callback_query)

        callback_query.answer.assert_awaited_once_with(text="long")
        editable_message.edit_text.assert_awaited_once()
        await_args = editable_message.edit_text.await_args
        assert await_args is not None
        kwargs = await_args.kwargs
        self.assertEqual(kwargs["text"], "Please choose another option:")
        self.assertEqual(
            kwargs["reply_markup"].inline_keyboard[0][0].callback_data,
            "bitcoin and ethereum",
        )
        self.assertEqual(
            kwargs["reply_markup"].inline_keyboard[1][0].callback_data,
            "back_to_main",
        )

    async def test_crypto_choice_handler_shows_wait_message(self) -> None:
        editable_message = SimpleNamespace()
        editable_message.chat = SimpleNamespace(full_name="Test User")
        editable_message.edit_text = AsyncMock()

        callback_query = _make_callback_query(
            data="bitcoin and ethereum",
            message=editable_message,
        )

        with patch(
            "bot.handlers.start._get_editable_message", return_value=editable_message
        ):
            await self.start_module.crypto_choice_handler(callback_query)

        callback_query.answer.assert_awaited_once_with(
            text="You selected BITCOIN AND ETHEREUM!"
        )
        editable_message.edit_text.assert_awaited_once_with(text="Wait for updates...")

    async def test_back_to_main_handler_restores_main_keyboard(self) -> None:
        editable_message = SimpleNamespace()
        editable_message.chat = SimpleNamespace(full_name="Test User")
        editable_message.edit_text = AsyncMock()

        callback_query = _make_callback_query(
            data="back_to_main",
            message=editable_message,
        )

        with patch(
            "bot.handlers.start._get_editable_message", return_value=editable_message
        ):
            await self.start_module.back_to_main_handler(callback_query)

        editable_message.edit_text.assert_awaited_once()
        await_args = editable_message.edit_text.await_args
        assert await_args is not None
        kwargs = await_args.kwargs
        self.assertIn("Hello, Test User!", kwargs["text"])
        self.assertEqual(
            kwargs["reply_markup"].inline_keyboard[0][0].callback_data, "long"
        )
        self.assertEqual(
            kwargs["reply_markup"].inline_keyboard[1][0].callback_data, "short"
        )
        callback_query.answer.assert_awaited_once_with()

    async def test_callback_with_inaccessible_message_is_handled_gracefully(
        self,
    ) -> None:
        inaccessible = types.InaccessibleMessage(
            chat=_make_chat(), message_id=777, date=0
        )
        callback_query = _make_callback_query(data="long", message=inaccessible)

        await self.start_module.menu_handler(callback_query)

        callback_query.answer.assert_awaited_once_with()
