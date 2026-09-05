import html
import json
import re

from bot.utils.clean_text import markdown_to_telegram_html


def format_position(content: str, model_name: str = "") -> str:
    if content is None:
        return f"⚠️ <b>AI вернул пустой ответ</b>\n\n🤖 <b>Модель:</b> {html.escape(model_name)}"
    try:
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx + 1]
            else:
                json_str = content

        data = json.loads(json_str)
        decision = str(data.get("decision", "WAIT")).upper()
        summary_raw = data.get("summary") or "Нет описания."
        summary = markdown_to_telegram_html(str(summary_raw))
        if decision == "WAIT":
            return (
                f"⏳ <b>Сейчас нет чёткой точки входа.</b>\n\n"
                f"📝 <b>Анализ:</b>\n{summary}\n\n"
                f"🤖 <b>Модель:</b> {html.escape(model_name)}"
            )

        instrument = html.escape(str(data.get("instrument", "Unknown")))
        entry = data.get("entry_price")
        tp_sl = data.get("tp_sl", {}) or {}
        tp = tp_sl.get("take_profit")
        sl = tp_sl.get("stop_loss")
        rr = tp_sl.get("rr_ratio")
        score = data.get("score", 0)
        try:
            score_int = max(0, min(10, int(score)))
        except (TypeError, ValueError):
            score_int = 0
        score_bar = "⭐" * score_int + "☐" * (10 - score_int)

        emoji = "🟢" if decision == "LONG" else "🔴"

        return (
            f"{emoji} <b>ТОРГОВАЯ ПОЗИЦИЯ: {decision} {instrument}</b>\n\n"
            f"📝 <b>Анализ:</b>\n{summary}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎯 <b>Вход:</b> {entry if entry else 'По рынку'}\n"
            f"🛑 <b>Стоп-лосс:</b> {sl if sl else 'N/A'}\n"
            f"💰 <b>Тейк-профит:</b> {tp if tp else 'N/A'}\n"
            f"📊 <b>Risk/Reward:</b> {rr if rr else 'N/A'}\n"
            f"⭐ <b>Уверенность:</b> {score_bar} {score_int}/10\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🤖 <b>Модель:</b> {html.escape(model_name)}"
        )
    except Exception:
        preview = html.escape((content or "Пустой ответ")[:300])
        return (
            f"⚠️ <b>Не удалось разобрать ответ ИИ</b>\n\n"
            f"<code>{preview}...</code>\n\n"
            f"🤖 <b>Модель:</b> {html.escape(model_name)}"
        )
