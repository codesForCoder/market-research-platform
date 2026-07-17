from pathlib import Path
from loguru import logger

from app.core.config import get_settings
from app.exceptions.instrument_exceptions import (
    SeedInstrumentNotFoundException,
)




class SeedCsvLoader:
    """
    Returns the bundled seed instrument master CSV.

    Responsibilities:
        - Locate bundled CSV
        - Validate it exists
        - Return Path

    Does NOT:
        - Parse CSV
        - Download
        - Retry
    """

    def __init__(self):
        self._settings = get_settings()

    def load(self) -> Path:

        seed_file = (
            self._settings.SEED_DIRECTORY
            / self._settings.SEED_INSTRUMENT_MASTER_FILE
        )

        if not seed_file.exists():

            logger.error(
                "Seed instrument master not found: {}",seed_file
            )

            raise SeedInstrumentNotFoundException(
                "Seed instrument master not found: {}",seed_file
            )

        logger.info(
            "Using bundled seed instrument master: {}",seed_file
        )

        return seed_file