import asyncio
import logging
from typing import Tuple, Optional
from bot.agents.agent import create_agent, AVAILABLE_MODELS

logger = logging.getLogger(__name__)

# Agno иногда не выбрасывает исключение при ошибке модели/провайдера, а
# кладёт текст ошибки прямо в result.content. Такие ответы нельзя считать
# успехом, иначе пользователь получит "200 OK" с текстом "404 page not found"
# вместо реального фолбэка на следующую модель.
KNOWN_ERROR_MARKERS = (
    "unknown model error",
    "error code:",
    "has reached its end of life",
    "model not found",
    "page not found",
    "not found",
    "bad gateway",
    "internal server error",
    "service unavailable",
    "unauthorized",
    "rate limit",
)

# HTTP-коды, которые иногда прилетают как открытый текст в content
_ERROR_STATUS_CODES = ("400", "401", "403", "404", "410", "429", "500", "502", "503", "504")


def _looks_like_error(content: str) -> bool:
    stripped = content.strip()
    if not stripped:
        return True

    lowered = stripped.lower()
    if any(marker in lowered for marker in KNOWN_ERROR_MARKERS):
        return True

    # Реальный анализ рынка — это длинный текст (десятки-сотни слов) и/или
    # JSON с решением. Короткая строка с HTTP-кодом внутри почти наверняка
    # техническая ошибка провайдера, а не торговое решение.
    if len(stripped) < 200 and "{" not in stripped:
        if any(code in stripped for code in _ERROR_STATUS_CODES):
            return True

    return False


def create_trading_agent():
    """
    Creates and returns a trading agent.
    The model is randomly selected inside create_agent().
    """
    return create_agent()

async def fetch_decision(initial_agent, symbol: str = "BTCUSDT") -> Tuple[Optional[str], str]:
    """
    Runs the agent to get a trading decision for the specified symbol.
    Implements fallback logic to try other models if the initial one fails.

    Returns:
        A tuple of (decision_content, final_model_id)
    """
    logger.debug("Starting fetch_decision. Available models: %s", AVAILABLE_MODELS)
    tried_models = set()
    current_agent = initial_agent

    while True:
        model_id = current_agent.model_id # type: ignore
        tried_models.add(model_id)
        logger.info(f"Fetching decision for {symbol} using model {model_id}")

        try:
            # Use a hard timeout of 300 seconds to prevent hanging on unresponsive models
            result = await asyncio.wait_for(
                current_agent.arun(
                    stream=None, # type: ignore
                    input=f"Проанализируй {symbol} используя все доступные инструменты и верни торговое решение.",
                    yield_run_output=True,
                ), # type: ignore
                timeout=300.0
            )

            if result and result.content and not _looks_like_error(result.content):
                logger.info(f"Successfully received response from model {model_id}")
                logger.info("AI market analysis from %s:\n%s", model_id, result.content)
                return result.content, model_id

            logger.warning(
                "Model %s returned no usable response (empty or error-like content): %r",
                model_id,
                result.content if result else None,
            )

        except asyncio.TimeoutError:
            logger.error(f"AI request timed out after 300s for {symbol} with model {model_id}")
        except Exception as e:
            logger.exception(f"Error with model {model_id} for {symbol}: {e}")

        # Try to find a fallback model from the available list
        remaining_models = [m for m in AVAILABLE_MODELS if m not in tried_models]
        if not remaining_models:
            logger.error(f"All available models exhausted for {symbol}. No valid response obtained.")
            return None, model_id

        next_model = remaining_models[0]
        logger.info(f"Fallback: switching to model {next_model}")
        current_agent = create_agent(model_id=next_model)
