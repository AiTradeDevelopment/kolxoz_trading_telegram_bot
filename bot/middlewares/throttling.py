import time
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 2.0):
        self.limit = limit
        self.users: Dict[int, float] = {}
        self.warnings: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            # For other event types, just let them through
            return await handler(event, data)

        now = time.time()
        last_time = self.users.get(user_id, 0)

        if now - last_time < self.limit:
            # Send a warning message only once every 5 seconds to avoid further flooding
            last_warn = self.warnings.get(user_id, 0)
            if now - last_warn > 5.0:
                warning_text = "⚠️ Too many requests! Please slow down."
                if isinstance(event, Message):
                    await event.answer(warning_text, parse_mode="HTML")
                elif isinstance(event, CallbackQuery):
                    await event.answer(warning_text, show_alert=True)
                self.warnings[user_id] = now
            return # Block the handler from executing

        self.users[user_id] = now
        return await handler(event, data)
