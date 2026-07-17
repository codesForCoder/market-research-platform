from collections import defaultdict
from typing import Iterable

from app.models.instrument import Instrument
from app.models.instrument_id import InstrumentId


class InstrumentRepository:

    def __init__(self):

        # Primary index
        self._by_instrument_id: dict[
            InstrumentId,
            Instrument
        ]= {}
        # One-to-many indexes
        #key = (instrument.exchange, instrument.segment)
        # Secondary indexes (1 -> many)
        self._by_exchange_segment: dict[
            tuple[str, str],
            list[Instrument]
        ] = defaultdict(list)

    def add(self, instrument: Instrument) -> None:
        """Add an instrument and update all indexes."""

        instrument_id = instrument.instrument_id

        if instrument_id in self._by_instrument_id:
            raise ValueError(
                f"Duplicate instrument: {instrument_id}"
            )

        # Primary index
        self._by_instrument_id[instrument_id] = instrument

        # Composite index
        exchange_segment  = (instrument.exchange, instrument.segment)
        self._by_exchange_segment[exchange_segment ].append(instrument)

    def get_by_instrument_id(
            self,
            instrument_id: InstrumentId
    ) -> Instrument | None:
        return self._by_instrument_id.get(
           instrument_id
        )

    def get_by_exchange_segment(
            self,
            exchange: str,
            segment: str,
    ) -> list[Instrument]:
        return self._by_exchange_segment.get(
            (exchange, segment),
            [],
        )

    def __len__(self) -> int:
        return len(self._by_instrument_id)

    def __iter__(self) -> Iterable[Instrument]:
        return iter(self._by_instrument_id.values())

    def all(self) -> Iterable[Instrument]:
        return self._by_instrument_id.values()
