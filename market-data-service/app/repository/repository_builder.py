from collections.abc import Iterable

from app.models.instrument import Instrument
from app.repository.instrument_repository import InstrumentRepository


class RepositoryBuilder:
    """
    Builds an InstrumentRepository from a collection
    of Instrument objects.
    """

    def build(
        self,
        instruments: Iterable[Instrument],
    ) -> InstrumentRepository:

        repository = InstrumentRepository()
        count = 0
        for instrument in instruments:
            repository.add(instrument)
            count += 1
        if count == 0:
            raise ValueError("No instruments were provided to build the repository.")

        return repository