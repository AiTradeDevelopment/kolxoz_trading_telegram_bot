<div align="center">

# 🚀 Kolxoz Trading Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.25.0-4CAF50?logo=telegram)](https://docs.aiogram.dev/)
[![Agno](https://img.shields.io/badge/Agno-2.6+-orange)](https://docs.agno.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Logo -->
<br>
<a href="https://github.com/AiTradeDevelopment/kolxoz_trading_telegram_bot">
  <img src="docs/assets/logo.jpg" alt="Kolxoz Trading Bot" width="300" />
</a>

**AI-Powered Cryptocurrency Trading Assistant for Telegram**  
Real-time market analysis using ICT/SMC methodology with LLM-driven trade decisions

</div>

---

## 🎯 Overview

Kolxoz Trading Bot is a Telegram bot that provides intelligent cryptocurrency trading analysis and signals

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **uv** — Ultra-fast Python package manager
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Telegram Bot Token** from [@BotFather](https://t.me/Botfather)
- **NVIDIA API Key** from [NVIDIA NIM](https://build.nvidia.com/)

### Installation

```bash
# Clone the repository
git clone https://github.com/AiTradeDevelopment/kolxoz_trading_telegram_bot.git
cd kolxoz_trading_telegram_bot

# Install dependencies
uv sync
```

### Configuration

Copy the example environment file and fill in your keys:

```bash
cp .env.example .env
```

Then edit `.env` with your credentials:

```properties
# Required
BOT_TOKEN=your_telegram_bot_token_from_botfather
NVIDIA_API_KEY=your-nvidia-api-key-here

# Optional
MCP_TIMEOUT=60
OPENAI_API_URL=https://integrate.api.nvidia.com/v1/
COINDESK_API_KEY=your-coindesk-api-key-here
CRYPTOPANIC_TOKEN=your-cryptopanic-token-here
AGNO_TELEMETRY=false
```

### Running the Bot

```bash
# Run with uv (recommended)
uv run main.py

# Or activate venv first
source .venv/bin/activate
python main.py
```

> 💡 **Tip:** The bot will start polling Telegram for messages. Make sure your `BOT_TOKEN` is valid and the bot is not blocked.

---

## 📄 License

Distributed under the MIT License.

```
MIT License

Copyright (c) 2024-2026 Kolxoz Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<div align="center">

**Made with ❤️ by the Kolxoz Team**

_AI-Powered Trading for the Next Generation_

</div>
