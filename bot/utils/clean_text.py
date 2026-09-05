import html
import re


def clean_text(text: str) -> str:
    # Убираем служебные теги агента
    text = re.sub(r'｜\w+｜.*?(?=｜|$)', '', text, flags=re.DOTALL)
    # Убираем HTML теги кроме разрешённых Telegram
    text = re.sub(r'<(?!/?(?:b|i|u|s|code|pre|a)\b)[^>]+>', '', text)
    return text.strip()


def markdown_to_telegram_html(text: str) -> str:
    """
    Конвертирует ответ LLM в Markdown-подобном формате (###, **, -)
    в HTML, который умеет рендерить Telegram (parse_mode=HTML).

    Telegram поддерживает только <b>, <i>, <u>, <s>, <code>, <pre>, <a>,
    поэтому заголовки уровня ### превращаются в жирный текст, а не в
    отдельный тег заголовка (его в Telegram просто нет).
    """
    if not text:
        return ""

    text = clean_text(text)
    # Экранируем спецсимволы HTML, чтобы Telegram не сломался на "<" / ">" / "&"
    text = html.escape(text, quote=False)

    # Заголовки ### / ## / # -> жирная строка
    text = re.sub(r'^#{1,6}\s*(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    # **жирный** и __жирный__
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text, flags=re.DOTALL)

    # *курсив* (не трогая уже вставленные <b>)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text, flags=re.DOTALL)

    # Маркеры списков "- пункт" -> "• пункт"
    text = re.sub(r'^\s*-\s+', '• ', text, flags=re.MULTILINE)

    # Схлопываем более двух пустых строк подряд
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()
