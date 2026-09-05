import asyncio
import logging
from typing import Tuple, Optional
from bot.agents.agent import create_agent, AVAILABLE_MODELS

logger = logging.getLogger(__name__)


def create_trading_agent():
    """
    Creates and returns a trading agent.
    Primary models are selected in AVAILABLE_MODELS order.
    """
    return create_agent()


def _ordered_fallback_models(initial_model_id: str) -> list[str]:
    """Return each remaining model once, continuing from the initial model."""
    try:
        initial_index = AVAILABLE_MODELS.index(initial_model_id)
    except ValueError:
        return list(AVAILABLE_MODELS)

    return AVAILABLE_MODELS[initial_index + 1 :] + AVAILABLE_MODELS[:initial_index]


async def fetch_decision(initial_agent, symbol: str = "BTCUSDT") -> Tuple[Optional[str], str]:
    """
    Runs the agent to get a trading decision for the specified symbol.
    Implements fallback logic to try other models if the initial one fails.

    Returns:
        A tuple of (decision_content, final_model_id)
    """
    print(">>> [DEBUG_PRINT] Starting fetch_decision")
    logger.info(f"DEBUG: Starting fetch_decision. Available models: {AVAILABLE_MODELS}")
    current_agent = initial_agent
    fallback_models = iter(_ordered_fallback_models(initial_agent.model_id))
    tried_models: list[str] = []

    while True:
        model_id = current_agent.model_id # type: ignore
        tried_models.append(model_id)
        logger.info(f"DEBUG: Current iteration. Tried so far: {tried_models}")
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

            if result and result.content:
                logger.info(f"Successfully received response from model {model_id}")
                logger.info("AI market analysis from %s:\n%s", model_id, result.content)
                print(f">>> [DEBUG_PRINT] SUCCESS! Returning result from model {model_id}")
                return result.content, model_id

            logger.warning(f"DEBUG: Model {model_id} returned empty response (result exists but content is empty/None)")

        except asyncio.TimeoutError:
            print(f">>> [DEBUG_PRINT] TIMEOUT occurred for model {model_id}")
            logger.error(f"AI request timed out after 300s for {symbol} with model {model_id}")
        except Exception as e:
            print(f">>> [DEBUG_PRINT] EXCEPTION occurred: {e}")
            logger.exception(f"Error with model {model_id} for {symbol}: {e}")

        # Continue from the initial model's position and wrap around the list once.
        next_model = next(fallback_models, None)
        if next_model is None:
            print(">>> [DEBUG_PRINT] All models exhausted. Returning None")
            logger.error(f"All available models exhausted for {symbol}. No valid response obtained.")
            return None, model_id

        logger.info(f"Fallback: switching to model {next_model}")
        current_agent = create_agent(model_id=next_model)
