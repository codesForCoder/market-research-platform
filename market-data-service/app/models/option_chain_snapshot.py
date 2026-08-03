from dataclasses import dataclass
from datetime import datetime

from app.models.instrument import Instrument
from app.models.option_chain_entry import OptionChainEntry


@dataclass(frozen=True, slots=True)
class OptionChainSnapshot:
    instrument: Instrument

    underlying_price: float

    timestamp: datetime

    entries: list[OptionChainEntry]
