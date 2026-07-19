from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.exchange import Exchange
from app.models.segment import Segment
from app.models.instrument_id import InstrumentId
from app.models.instrument_type import InstrumentType



class Instrument(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid"
    )

    security_id: int

    exchange: Exchange
    segment: Segment

    @property
    def instrument_id(self) -> InstrumentId:
        return InstrumentId(
            exchange=self.exchange,
            segment=self.segment,
            security_id=self.security_id,
        )

    trading_symbol: str
    custom_symbol: str
    symbol_name: str

    instrument_type: InstrumentType

    expiry_date: datetime | None

    strike_price: float | None

    option_type: str | None

    lot_size: int

    tick_size: float