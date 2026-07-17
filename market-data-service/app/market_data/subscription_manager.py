from collections.abc import Iterable

from app.models.instrument_id import InstrumentId


class SubscriptionManager:

    def __init__(self) -> None:
        self._subscriptions: set[InstrumentId] = set()

    def add(self, instrument: InstrumentId) -> None:
        self._subscriptions.add(instrument)

    def add_all(
        self,
        instruments: Iterable[InstrumentId],
    ) -> None:
        self._subscriptions.update(instruments)

    def remove(self, instrument: InstrumentId) -> None:
        self._subscriptions.discard(instrument)

    def clear(self) -> None:
        self._subscriptions.clear()

    @property
    def subscriptions(self) -> frozenset[InstrumentId]:
        return frozenset(self._subscriptions)