from dataclasses import dataclass

from app.models.greeks import Greeks


@dataclass(frozen=True, slots=True)
class OptionLeg:
    security_id: int

    ltp: float

    oi: int

    volume: int

    iv: float

    average_price: float

    previous_oi: int

    previous_volume: int

    previous_close_price: float

    top_bid_price: float

    top_bid_quantity: int

    top_ask_price: float

    top_ask_quantity: int

    greeks: Greeks
