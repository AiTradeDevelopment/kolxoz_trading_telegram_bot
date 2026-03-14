# Kolxoz Trading Telegram Bot

Telegram bot for trading workflow automation.

## Requirements

- `uv` installed (`uv --version`)
- Python `>=3.13`
- Telegram bot token from BotFather

## Environment variables

Create `.env` in the project root (or `bot/.env`):

BOT_TOKEN=your_telegram_bot_token

## Setup and run with uv

### 1) Create project virtual environment

uv venv

By default, `uv` creates `.venv` in the project root.

### 2) Install/sync dependencies

uv sync

### 3) Run bot

uv run main.py

## Running tests

Run all tests:

uv run python -m unittest discover -s tests -p "test_*.py" -v

Run handler regression tests only:

uv run python -m unittest tests.handlers.test_start_handler_behavior -v

## Optional: force Python version for venv

If you need a specific Python version:

uv venv --python 3.13 .venv
uv sync

## Useful commands

Check active interpreter used by `uv run`:

uv run python -c "import sys; print(sys.executable)"

Quick import check:

uv run python -c "import aiogram, dotenv; print('imports_ok')"

---

All rights reserved © 2026 AiTrade Development
