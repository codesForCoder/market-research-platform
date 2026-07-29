from pydantic import BaseModel

from app.brokers.dhan.dedicated_feed_depth import MarketDepthType
from app.models.exchange import Exchange
from app.models.segment import Segment


class InstrumentInput(BaseModel):
    security_id: int
    exchange: Exchange
    segment: Segment

class DepthInput(BaseModel):
    instrument: InstrumentInput
    depth: MarketDepthType

class MarketFeedRequest(BaseModel):
    instruments: list[InstrumentInput]

class MarketDepthRequest(BaseModel):
    instruments: list[DepthInput]
