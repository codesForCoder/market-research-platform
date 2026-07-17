from pathlib import Path
import asyncio
from loguru import logger

from app.brokers.dhan.instrument_downloader import InstrumentDownloader
from app.brokers.dhan.seed_csv_loader import SeedCsvLoader
from app.core.config import get_settings
from app.exceptions.instrument_exceptions import (
    InstrumentDownloadException,
)


class InstrumentDataSource:

    def __init__(
            self,
            downloader: InstrumentDownloader,
            seed_loader: SeedCsvLoader,
    ) -> None:

        self._downloader = downloader
        self._seed_loader = seed_loader
        self._settings = get_settings()

    async def get_csv(self) -> Path:

        for attempt in range(
                1,
                self._settings.INSTRUMENT_DOWNLOAD_RETRIES + 1,
        ):

            try:

                logger.info(
                    "Downloading instrument master (attempt {}/{})",attempt ,self._settings.INSTRUMENT_DOWNLOAD_RETRIES
                )

                return await self._downloader.download()

            except InstrumentDownloadException:

                logger.warning("Download attempt {} failed." ,attempt)

                if attempt < self._settings.INSTRUMENT_DOWNLOAD_RETRIES:
                    await asyncio.sleep(
                        self._settings.INSTRUMENT_RETRY_DELAY_SECONDS
                    )

        logger.warning(
            "Falling back to bundled seed instrument master."
        )

        return self._seed_loader.load()
