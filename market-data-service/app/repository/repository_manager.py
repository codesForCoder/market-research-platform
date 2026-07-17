from loguru import logger

from app.repository.instrument_repository import InstrumentRepository


class RepositoryManager:
    """
    Owns the current active InstrumentRepository.

    This class allows us to atomically replace the repository
    without affecting existing readers.
    """

    def __init__(self):
        self._repository: InstrumentRepository | None = None

    def get(self) -> InstrumentRepository:
        """
        Returns the currently active repository.

        Raises:
            RuntimeError: if repository has not been loaded yet.
        """
        if self._repository is None:
            raise RuntimeError("Instrument repository has not been loaded.")

        return self._repository

    def replace(self, repository: InstrumentRepository) -> None:
        """
        Atomically replaces the current repository.
        """
        logger.info("Replaced instrument repository")
        self._repository = repository

    def is_loaded(self) -> bool:
        return self._repository is not None