# Kolxoz Trading Telegram Bot

Telegram bot for trading workflow automation.

## Requirements

- Python `>=3.13`
- Telegram bot token from BotFather

## Environment variables

Create `.env` in the project root (or `bot/.env`):

BOT_TOKEN=your_telegram_bot_token

## Local run (venv + pip)

### Linux / macOS (Fish)

1) Create venv:
python3 -m venv venv

2) Activate:
source venv/bin/activate.fish

3) Install dependencies:
pip install -r requirements.txt

4) Run bot:
python main.py

### Linux / macOS (Bash/Zsh)

1) Create venv:
python3 -m venv venv

2) Activate:
source venv/bin/activate

3) Install dependencies:
pip install -r requirements.txt

4) Run bot:
python main.py

### Windows (PowerShell)

1) Create venv:
py -3 -m venv venv

2) Activate:
.\venv\Scripts\Activate.ps1

3) Install dependencies:
pip install -r requirements.txt

4) Run bot:
python main.py

### Windows (CMD)

1) Create venv:
py -3 -m venv venv

2) Activate:
venv\Scripts\activate.bat

3) Install dependencies:
pip install -r requirements.txt

4) Run bot:
python main.p# Kolxoz Trading Telegram Bot

Telegram bot for trading workflow automation.

## Requirements

- Python `>=3.13`
- Telegram bot token from BotFather

## Environment variables

Create `.env` in the project root (or `bot/.env`):

BOT_TOKEN=your_telegram_bot_token

Run all tests:
python -m unittest discover -s tests -p "test_*.py" -v

Run handler regression tests only:
python -m unittest tests.handlers.test_start_handler_behavior -v

## Notes

- `.env` is ignored by git and must not be committed.
- If editor shows unresolved imports, make sure it uses your project interpreter:
  `/home/user/.../kolxoz_trading_telegram_bot/venv/bin/python`.

---

All rights reserved © 2026 AiTrade Development
