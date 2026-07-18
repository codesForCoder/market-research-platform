from typing import NamedTuple

from app.models.exchange import Exchange
from app.models.segment import Segment


class InstrumentId(NamedTuple):
    exchange: Exchange
    segment: Segment
    security_id: int