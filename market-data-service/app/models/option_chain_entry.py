from dataclasses import dataclass

from app.models.option_leg import OptionLeg


@dataclass(frozen=True, slots=True)
class OptionChainEntry:
    strike_price: float

    call: OptionLeg

    put: OptionLeg
