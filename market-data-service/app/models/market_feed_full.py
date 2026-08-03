from dataclasses import dataclass, field


@dataclass(slots=True)
class DepthLevel:
    level: int

    bid_price: float
    bid_quantity: int
    bid_orders: int

    ask_price: float
    ask_quantity: int
    ask_orders: int


@dataclass(slots=True)
class QuoteUpdate:
    event_id: str

    event_time: int
    receive_time: int

    source: str

    exchange: str
    segment: str

    instrument_id: str
    symbol: str | None

    last_traded_price: float
    last_traded_quantity: int
    last_trade_time: int

    average_trade_price: float

    volume: int

    total_buy_quantity: int
    total_sell_quantity: int

    open_interest: int | None
    day_high_open_interest: int | None
    day_low_open_interest: int | None

    open: float
    high: float
    low: float
    close: float | None

    market_depth: list[DepthLevel] = field(default_factory=list)
