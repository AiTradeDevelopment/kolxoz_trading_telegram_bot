"""
Простое in-memory хранилище состояния бота.

Важно: это не персистентное хранилище — при перезапуске бота подписчики
и история сигналов обнуляются. Для продакшена стоит заменить на Redis
или БД, но для текущего масштаба (один процесс, polling) этого достаточно.
"""
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, Set

SUBSCRIBERS: Set[int] = set()

HISTORY_MAX_SIZE = 10


@dataclass
class SignalRecord:
    chat_id: int
    text: str
    created_at: datetime = field(default_factory=datetime.utcnow)


HISTORY: Deque[SignalRecord] = deque(maxlen=HISTORY_MAX_SIZE)


def subscribe(chat_id: int) -> None:
    SUBSCRIBERS.add(chat_id)


def unsubscribe(chat_id: int) -> None:
    SUBSCRIBERS.discard(chat_id)


def add_signal_to_history(chat_id: int, text: str) -> None:
    HISTORY.append(SignalRecord(chat_id=chat_id, text=text))


def get_history(limit: int = 5):
    return list(HISTORY)[-limit:]
