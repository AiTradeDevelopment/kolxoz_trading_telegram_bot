import ast
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _parse_file(relative_path: str) -> ast.Module:
    file_path = PROJECT_ROOT / relative_path
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    assert isinstance(tree, ast.Module)
    return tree


def _extract_function_names(tree: ast.Module) -> set[str]:
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _extract_callback_data_values(tree: ast.Module) -> list[str]:
    callback_values: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        for keyword in node.keywords:
            if (
                keyword.arg == "callback_data"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                callback_values.append(keyword.value.value)

    return callback_values


class TestKeyboardConfig(unittest.TestCase):
    def test_main_keyboard_has_expected_callbacks(self) -> None:
        tree = _parse_file("bot/keyboards/inline/menu.py")

        self.assertIn("main_keyboard", _extract_function_names(tree))
        self.assertEqual(_extract_callback_data_values(tree), ["long", "short"])

    def test_crypto_keyboard_has_expected_callbacks(self) -> None:
        tree = _parse_file("bot/keyboards/inline/crypto.py")

        self.assertIn("crypto_keyboard", _extract_function_names(tree))
        self.assertEqual(
            _extract_callback_data_values(tree),
            ["bitcoin and ethereum", "back_to_main"],
        )


if __name__ == "__main__":
    unittest.main()
