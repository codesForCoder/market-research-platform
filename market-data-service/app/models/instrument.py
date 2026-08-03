from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field

from app.models.exchange import Exchange
from app.models.segment import Segment
from app.models.instrument_id import InstrumentId
from app.models.instrument_type import InstrumentType


class Instrument(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    security_id: int

    exchange: Exchange
    segment: Segment

    trading_symbol: str
    custom_symbol: str
    symbol_name: str

    instrument_type: InstrumentType

    expiry_date: datetime | None

    strike_price: float | None

    option_type: str | None

    lot_size: int

    tick_size: float

    # --- 1. Custom Hash Method for Sets ---
    def __hash__(self) -> int:
        # Generate a unique hash integer based on the structural ID components
        return hash((self.security_id, self.exchange, self.segment))

    # --- 2. Custom Equality Method for Sets ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Instrument):
            return NotImplemented

        # Two instruments are identical if their core ID values match
        return (
            self.security_id == other.security_id and self.exchange == other.exchange and self.segment == other.segment
        )

    @computed_field
    def instrument_id(self) -> InstrumentId:
        return InstrumentId(
            exchange=self.exchange,
            segment=self.segment,
            security_id=self.security_id,
        )
