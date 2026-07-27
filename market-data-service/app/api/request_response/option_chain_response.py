from pydantic import BaseModel

from app.models.exchange import Exchange
from app.models.instrument import Instrument
from app.models.segment import Segment


class SubscriptionInstrumentResponse(BaseModel):
    security_id: int
    exchange: Exchange
    segment: Segment
    custom_symbol_name: str

class OptionChainSubscriptionResponse(BaseModel):
    instrument: SubscriptionInstrumentResponse
    status: str = "Unknown"

class OptionChainUnSubscribeResponse(BaseModel):
    instrument: SubscriptionInstrumentResponse
    status: str = "Unknown"