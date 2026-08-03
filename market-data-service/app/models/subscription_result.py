from dataclasses import dataclass

from app.api.request_response.instrument_api_response import InstrumentElement, SubscriptionStatus
from app.models.instrument import Instrument


@dataclass(slots=True)
class SubscriptionResult:
    instrument: Instrument
    success: bool
    error: str | None
    depth: int = 5

    def to_status(self) -> SubscriptionStatus:
        return SubscriptionStatus(
            instrument=InstrumentElement(
                segment=self.instrument.segment,
                exchange=self.instrument.exchange,
                security_id=self.instrument.security_id,
                custom_symbol_name=self.instrument.custom_symbol,
            ),
            is_subscribed=self.success,
            feedback=self.error,
        )
