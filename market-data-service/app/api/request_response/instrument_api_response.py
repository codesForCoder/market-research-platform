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


class SubscriptionStatus(BaseModel):
    instrument: InstrumentElement
    is_subscribed: bool
    feedback: str | None = None


class DepthSubscriptionStatus(BaseModel):
    instrument: InstrumentElement
    depth: int
    is_subscribed: bool
    feedback: str | None = None


class MarketFeedResponse(BaseModel):
    subscription_status: list[SubscriptionStatus]


class MarketDepthResponse(BaseModel):
    subscription_status: list[DepthSubscriptionStatus]


class SubscribedInstrumentsResponse(BaseModel):
    instruments: list[InstrumentElement]
    total_count: int
