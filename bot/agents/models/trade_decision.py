from pydantic import BaseModel

from bot.agents.models.score_breakdown import ScoreBreakdown
from bot.agents.models.tpsl import TpSl


class TradeDecision(BaseModel):
    instrument: str = "BTCUSDT"
    decision: str = "WAIT"
    score: int = 0
    score_breakdown: ScoreBreakdown = ScoreBreakdown()
    tp_sl: TpSl = TpSl()
    entry_price: float | None = None
    summary: str = ""

    def to_text(self) -> str:
        decision_emoji = {"LONG": "🟢", "SHORT": "🔴", "WAIT": "🟡"}.get(self.decision, "⚪")

        sb = self.score_breakdown
        breakdown = (
            f"  1D Bias:        {'+' if sb.bias_1d >= 0 else ''}{sb.bias_1d}\n"
            f"  POI Confluence: {'+' if sb.poi_confluence >= 0 else ''}{sb.poi_confluence}\n"
            f"  Sweep:          {'+' if sb.sweep >= 0 else ''}{sb.sweep}\n"
            f"  CHOCH Retest:   {'+' if sb.choch_retest >= 0 else ''}{sb.choch_retest}\n"
            f"  Candle Confirm: {'+' if sb.candle_confirmation >= 0 else ''}{sb.candle_confirmation}\n"
            f"  Impulse/FVG:    {'+' if sb.impulse_or_fvg >= 0 else ''}{sb.impulse_or_fvg}\n"
            f"  News Penalty:   {sb.news_penalty}\n"
            f"  Structure:      {sb.structure_penalty}"
        )

        tp_sl_text = (
            f"  TP:    {self.tp_sl.take_profit or 'N/A'}\n"
            f"  SL:    {self.tp_sl.stop_loss or 'N/A'}\n"
            f"  RR:    {self.tp_sl.rr_ratio or 'N/A'}"
        )

        return (
            f"{'=' * 25}\n"
            f"<b>{decision_emoji} DECISION: {self.decision} | {self.instrument}</b>\n"
            f"{'=' * 25}\n"
            f"📊 Score: {self.score}/10\n\n"
            f"Score Breakdown:\n{breakdown}\n\n"
            f"💰 Entry: {self.entry_price or 'N/A'}\n"
            f"{tp_sl_text}\n\n"
            f"<b>📝 Summary:\n{self.summary}</b>\n"
            f"{'=' * 25}"
        )
