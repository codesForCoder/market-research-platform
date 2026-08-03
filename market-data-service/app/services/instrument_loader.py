import csv
from loguru import logger

from app.brokers.dhan.instrument_data_source import InstrumentDataSource
from app.brokers.dhan.instrument_mapper import DhanInstrumentMapper
from app.repository import RepositoryManager, RepositoryBuilder


class InstrumentLoader:
    """
    Loads the instrument master into the in-memory repository.

    Workflow:
        InstrumentDataSource
                ↓
            CSV Path
                ↓
          csv.DictReader
                ↓
       DhanInstrumentMapper
                ↓
           Instrument objects
                ↓
        RepositoryBuilder
                ↓
      InstrumentRepository
                ↓
      RepositoryManager.replace()
    """

    def __init__(
        self,
        data_source: InstrumentDataSource,
        mapper: DhanInstrumentMapper,
        repository_builder: RepositoryBuilder,
        repository_manager: RepositoryManager,
    ) -> None:
        self._data_source = data_source
        self._mapper = mapper
        self._repository_builder = repository_builder
        self._repository_manager = repository_manager

    async def load(self) -> None:
        logger.info("Loading instrument master...")

        csv_path = await self._data_source.get_csv()

        logger.info("Reading instrument master: {}", csv_path)

        with csv_path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            instruments = (self._mapper.map(row) for row in reader)

            repository = self._repository_builder.build(instruments)

        self._repository_manager.replace(repository)

        logger.info(
            "Instrument repository loaded successfully ({} instruments).",
            len(repository),
        )
