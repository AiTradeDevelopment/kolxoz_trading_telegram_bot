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
