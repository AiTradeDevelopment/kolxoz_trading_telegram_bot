from pydantic import BaseModel


class TpSl(BaseModel):
    take_profit: float | None = None
    stop_loss: float | None = None
    rr_ratio: float | None = None
