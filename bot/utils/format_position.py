import json
import re

def format_position(content: str) -> str:
    try:
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx+1]
            else:
                json_str = content

        data = json.loads(json_str)
        decision = data.get("decision", "WAIT").upper()
        if decision == "WAIT":
            return "⏳ <b>No clear trade setup at the moment.</b>\n\n<i>AI is waiting for better confluence.</i>"

        instrument = data.get("instrument", "Unknown")
        entry = data.get("entry_price")
        tp = data.get("tp_sl", {}).get("take_profit")
        sl = data.get("tp_sl", {}).get("stop_loss")
        rr = data.get("tp_sl", {}).get("rr_ratio")
        score = data.get("score", 0)
        summary = data.get("summary", "No summary provided.")
        emoji = "🟢" if decision == "LONG" else "🔴"

        return (
            f"{emoji} <b>TRADE POSITION: {decision} {instrument}</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎯 <b>Entry:</b> {entry if entry else 'Market'}\n"
            f"🛑 <b>Stop Loss:</b> {sl if sl else 'N/A'}\n"
            f"💰 <b>Take Profit:</b> {tp if tp else 'N/A'}\n"
            f"📊 <b>Risk/Reward:</b> {rr if rr else 'N/A'}\n"
            f"⭐ <b>Confidence Score:</b> {score}/10\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📝 <b>Analysis:</b>\n{summary}"
        )
    except Exception as e:
        return f"⚠️ <b>Error parsing AI response</b>\n\n<code>{content[:200]}...</code>"
