
import asyncio
from loguru import logger

from app.market_data.option_chain_client import OptionChainClient
from app.market_data.option_chain_manager import OptionChainManager



class OptionChainScheduler:
    """
    Periodically polls all subscribed option chains.

    Responsibilities:
      - Wake up every polling interval.
      - Get a snapshot of current subscriptions.
      - Fetch the latest option chain for each subscription.

    It does not manage subscriptions or publish results.
    """

    def __init__(
        self,
        option_chain_manager: OptionChainManager,
        option_chain_client: OptionChainClient,
        polling_interval_seconds: float,
    ) -> None:
        self._manager = option_chain_manager
        self._client = option_chain_client
        self._polling_interval_seconds = polling_interval_seconds

        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        """
        Starts the scheduler.
        """
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._run())

        logger.info("Option Chain Scheduler started.")

    async def stop(self) -> None:
        """
        Stops the scheduler gracefully.
        """
        self._running = False
        await self._manager.shutdown()
        if self._task:
            await self._task

        logger.info("Option Chain Scheduler stopped.")

    async def _run(self) -> None:
        """
        Main polling loop.
        """
        while self._running:
            await self._manager.wait_for_subscription()
            option_chain_req = await self._manager.next_subscription()

            if option_chain_req is not None:

                try:
                    snapshot = await self._client.fetch(option_chain_req)
                    # TODO
                    # Publish snapshot to Kafka

                except Exception as e:
                    logger.error(
                        "Failed to fetch option chain for {} with error {}",
                        option_chain_req.custom_symbol,str(e)
                    )

            await asyncio.sleep(self._polling_interval_seconds)