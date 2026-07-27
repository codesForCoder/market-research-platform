from pathlib import Path
from loguru import logger

import httpx

from app.core.config import get_settings
from app.exceptions.instrument_exceptions import (
    InstrumentDownloadException,
)



class InstrumentDownloader:
    """
    Downloads the latest Dhan instrument master CSV.

    Responsibilities:
        - Download CSV from Dhan
        - Save it atomically
        - Return the downloaded file path

    Does NOT:
        - Retry
        - Fallback to seed data
        - Parse CSV
        - Build repository
    """

    def __init__(
        self,
        http_client: httpx.AsyncClient,
    ) -> None:
        self._client = http_client
        self._settings = get_settings()

    async def download(self) -> Path:

        output_directory = self._settings.INSTRUMENT_DIRECTORY
        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            output_directory
            / self._settings.INSTRUMENT_MASTER_FILE
        )

        temp_file = destination.with_suffix(".tmp")

        logger.info(
            "Downloading Dhan instrument master from {}",self._settings.DHAN_INSTRUMENT_MASTER_URL
        )

        try:

            async with self._client.stream(
                "GET",
                self._settings.DHAN_INSTRUMENT_MASTER_URL,
            ) as response:

                response.raise_for_status()

                with temp_file.open("wb") as file:

                    async for chunk in response.aiter_bytes():

                        file.write(chunk)

            # Atomic replace
            temp_file.replace(destination)

            logger.info(
                "Instrument master downloaded successfully: {}",destination
            )

            return destination

        except Exception as ex:

            if temp_file.exists():
                temp_file.unlink()

            logger.error(
                "Failed to download instrument master. {}", str(ex)
            )

            raise InstrumentDownloadException(
                "Unable to download Dhan instrument master."
            ) from ex