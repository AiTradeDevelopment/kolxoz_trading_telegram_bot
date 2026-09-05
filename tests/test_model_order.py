import unittest
from types import SimpleNamespace
from unittest.mock import patch

from bot.agents import agent as agent_module
from bot.utils import get_decision


class _FakeAgent:
    def __init__(self, model_id: str, content: str | None = None) -> None:
        self.model_id = model_id
        self._content = content

    async def arun(self, **_kwargs):
        return SimpleNamespace(content=self._content)


class TestModelOrder(unittest.IsolatedAsyncioTestCase):
    async def test_valid_response_is_returned_without_fallback(self) -> None:
        model_id = agent_module.AVAILABLE_MODELS[0]
        content = '{"decision": "WAIT", "summary": "News source returned error: unavailable"}'
        agent = _FakeAgent(model_id, content)

        with patch.object(get_decision, "create_agent") as create_fallback:
            result = await get_decision.fetch_decision(agent)

        self.assertEqual(result, (content, model_id))
        create_fallback.assert_not_called()

    async def test_error_response_falls_back_to_valid_response(self) -> None:
        first, second = agent_module.AVAILABLE_MODELS[:2]
        valid_content = '{"decision": "WAIT"}'
        error_responses = (
            "  ERROR: service unavailable",
            "Error code: 429 - rate limit exceeded",
            "Ошибка: сервис недоступен",
            '{"error": {"message": "rate limit exceeded", "code": 429}}',
            " \n\t",
        )

        for error_content in error_responses:
            with self.subTest(content=error_content):
                initial_agent = _FakeAgent(first, error_content)
                fallback_agent = _FakeAgent(second, valid_content)

                with patch.object(
                    get_decision, "create_agent", return_value=fallback_agent
                ) as create_fallback:
                    result = await get_decision.fetch_decision(initial_agent)

                self.assertEqual(result, (valid_content, second))
                create_fallback.assert_called_once_with(model_id=second)

    def test_primary_models_are_selected_in_list_order(self) -> None:
        expected = agent_module.AVAILABLE_MODELS + [agent_module.AVAILABLE_MODELS[0]]

        with patch.object(agent_module, "_next_model_index", 0):
            actual = [agent_module.get_next_model() for _ in expected]

        self.assertEqual(actual, expected)

    async def test_fallback_continues_in_list_order_and_wraps_once(self) -> None:
        first, second, third = agent_module.AVAILABLE_MODELS
        agents = {
            first: _FakeAgent(first),
            second: _FakeAgent(second),
            third: _FakeAgent(third),
        }
        created_models: list[str] = []

        def create_fake_agent(model_id: str):
            created_models.append(model_id)
            return agents[model_id]

        with patch.object(get_decision, "create_agent", side_effect=create_fake_agent):
            content, final_model = await get_decision.fetch_decision(agents[second])

        self.assertIsNone(content)
        self.assertEqual(final_model, first)
        self.assertEqual(created_models, [third, first])


if __name__ == "__main__":
    unittest.main()
