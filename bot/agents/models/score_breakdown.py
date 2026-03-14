from pydantic import BaseModel


class ScoreBreakdown(BaseModel):
    bias_1d: int = 0
    poi_confluence: int = 0
    sweep: int = 0
    choch_retest: int = 0
    candle_confirmation: int = 0
    impulse_or_fvg: int = 0
    news_penalty: int = 0
    structure_penalty: int = 0
