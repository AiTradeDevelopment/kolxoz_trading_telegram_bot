import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = PROJECT_ROOT / "bot" / "agents" / "prompts"


class TestPromptModules(unittest.TestCase):
    def test_prompt_files_exist(self) -> None:
        prompt_files = sorted(PROMPTS_DIR.glob("*.py"))
        self.assertGreaterEqual(len(prompt_files), 1)

    def test_each_prompt_file_has_non_empty_prompt_constant(self) -> None:
        prompt_files = sorted(PROMPTS_DIR.glob("*.py"))

        for prompt_file in prompt_files:
            source = prompt_file.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(prompt_file))

            prompt_constants: list[tuple[str, str]] = []
            for node in tree.body:
                if not isinstance(node, ast.Assign):
                    continue

                for target in node.targets:
                    if not (
                        isinstance(target, ast.Name)
                        and target.id.startswith("PROMPT_")
                    ):
                        continue

                    self.assertIsInstance(
                        node.value,
                        ast.Constant,
                        f"{prompt_file} has non-literal prompt value",
                    )
                    self.assertIsInstance(
                        node.value.value,
                        str,
                        f"{prompt_file} prompt constant must be a string",
                    )
                    prompt_constants.append((target.id, node.value.value))

            self.assertGreaterEqual(
                len(prompt_constants),
                1,
                f"{prompt_file} does not define a PROMPT_* constant",
            )

            for constant_name, prompt_text in prompt_constants:
                self.assertGreater(
                    len(prompt_text.strip()),
                    100,
                    f"{prompt_file}:{constant_name} is unexpectedly short",
                )


if __name__ == "__main__":
    unittest.main()
