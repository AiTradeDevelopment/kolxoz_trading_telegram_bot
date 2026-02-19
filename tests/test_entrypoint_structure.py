import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_FILE = PROJECT_ROOT / "main.py"


class TestEntrypointStructure(unittest.TestCase):
    def test_main_has_async_main_function(self) -> None:
        tree = ast.parse(MAIN_FILE.read_text(encoding="utf-8"), filename=str(MAIN_FILE))
        async_functions = [
            node.name for node in tree.body if isinstance(node, ast.AsyncFunctionDef)
        ]
        self.assertIn("main", async_functions)

    def test_main_invokes_asyncio_run_in_module_guard(self) -> None:
        tree = ast.parse(MAIN_FILE.read_text(encoding="utf-8"), filename=str(MAIN_FILE))

        guard_found = False
        for node in tree.body:
            if not isinstance(node, ast.If):
                continue

            # if __name__ == '__main__':
            if not isinstance(node.test, ast.Compare):
                continue
            if not isinstance(node.test.left, ast.Name) or node.test.left.id != "__name__":
                continue
            if len(node.test.comparators) != 1:
                continue
            comparator = node.test.comparators[0]
            if not (
                isinstance(comparator, ast.Constant)
                and comparator.value == "__main__"
            ):
                continue

            guard_found = True

            has_asyncio_run_call = False
            for statement in node.body:
                if not isinstance(statement, ast.Expr):
                    continue
                call = statement.value
                if not isinstance(call, ast.Call):
                    continue
                if not isinstance(call.func, ast.Attribute):
                    continue
                if not (
                    isinstance(call.func.value, ast.Name)
                    and call.func.value.id == "asyncio"
                    and call.func.attr == "run"
                ):
                    continue

                has_asyncio_run_call = True

            self.assertTrue(
                has_asyncio_run_call,
                "main.py guard must call asyncio.run(...)",
            )

        self.assertTrue(guard_found, "main.py must contain module guard")


if __name__ == "__main__":
    unittest.main()
