from dataclasses import dataclass


@dataclass(frozen=True)
class DhanSubscriptionInstrument:
    exchange_segment: str
    security_id: str


@dataclass(frozen=True)
class DhanSubscriptionRequest:
    request_code: int
    instruments: list[DhanSubscriptionInstrument]