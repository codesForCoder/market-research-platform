from pydantic import BaseModel

from app.models.exchange import Exchange
from app.models.segment import Segment


class InstrumentElement(BaseModel):
    security_id: int
    exchange: Exchange
    segment: Segment
    custom_symbol_name: str


class InstrumentResponseByExchangeSegment(BaseModel):
    instruments: list[InstrumentElement]
    total_count: int
    exchange: Exchange
    segment: Segment
    limit: int
    offset: int

class InstrumentResponseById(BaseModel):
    instrument: InstrumentElement