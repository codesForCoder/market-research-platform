from dataclasses import dataclass
from datetime import datetime

from app.models.canonical_data_model.option_greeks import OptionGreeks
from app.models.canonical_data_model.option_quote import OptionQuote
from app.models.canonical_data_model.option_types import OptionType


@dataclass(slots=True, frozen=True)
class OptionContract:
    instrument_id: str

    strike: float

    option_type: OptionType

    expiry: datetime

    quote: OptionQuote

    greeks: OptionGreeks | None
