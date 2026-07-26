from pydantic import BaseModel

from app.models.exchange import Exchange
from app.models.instrument import Instrument
from app.models.segment import Segment


class OptionChainSubscriptionResponse(BaseModel):
    instrument: Instrument
    status: str

class OptionChainUnSubscribeResponse(BaseModel):
    instrument: Instrument
    status: str