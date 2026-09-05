"""
Запусти этот скрипт из папки проекта командой:
uv run python list_models.py

Он спросит у NVIDIA API реальный список доступных моделей твоим ключом.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
)

models = client.models.list()
ids = sorted(m.id for m in models.data)

# Показываем только то, что похоже на крупные чат-модели с tool calling
keywords = ["nemotron", "deepseek", "minimax", "gpt-oss", "qwen", "kimi", "mistral", "llama"]
filtered = [i for i in ids if any(k in i.lower() for k in keywords)]

print(f"Всего моделей в каталоге: {len(ids)}\n")
print("Подходящие для торгового агента (чат + tool calling):")
for i in filtered:
    print(" -", i)
