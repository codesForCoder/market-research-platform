from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import get_settings
from app.services.instrument_loader import InstrumentLoader


class InstrumentScheduler:

    def __init__(
        self,
        instrument_loader: InstrumentLoader,
    ) -> None:

        self._loader = instrument_loader
        self._settings = get_settings()
        self._scheduler = AsyncIOScheduler(  timezone=self._settings.TIMEZONE,)

    async def start(self) -> None:

        self._scheduler.add_job(
            self._loader.load,
            trigger=CronTrigger(
                hour=self._settings.INSTRUMENT_REFRESH_HOUR,
                minute=self._settings.INSTRUMENT_REFRESH_MINUTE,
            ),
            id="instrument_master_refresh",
            replace_existing=True, #replace existing job
            max_instances=1, #never run two refreshes concurrently
            coalesce=True, #if a refresh is already running, skip the next one
        )

        self._scheduler.start()

    async def stop(self) -> None:
        self._scheduler.shutdown(wait=True)