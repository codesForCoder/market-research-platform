from pydantic import BaseModel

from app.models.exchange import Exchange
from app.models.segment import Segment


class OptionChainRequest(BaseModel):
    exchange: Exchange
    segment: Segment
    security_id: int
