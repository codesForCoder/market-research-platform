from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class OptionQuote:
    ltp: float

    close: float | None

    open: float | None

    high: float | None

    low: float | None

    volume: int

    oi: int

    oi_change: int | None

    bid_price: float | None

    bid_qty: int | None

    ask_price: float | None

    ask_qty: int | None

    last_trade_time: datetime | None
