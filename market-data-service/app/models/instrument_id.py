from typing import NamedTuple


class InstrumentId(NamedTuple):
    exchange: str
    segment: str
    security_id: int