import re


def clean_text(text: str) -> str:
    # Убираем служебные теги агента
    text = re.sub(r'｜\w+｜.*?(?=｜|$)', '', text, flags=re.DOTALL)
    # Убираем HTML теги кроме разрешённых Telegram
    text = re.sub(r'<(?!/?(?:b|i|u|s|code|pre|a)\b)[^>]+>', '', text)
    return text.strip()
