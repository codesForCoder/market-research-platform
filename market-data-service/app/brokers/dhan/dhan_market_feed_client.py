
import asyncio
from typing import Iterable
from uuid import uuid4

from dhanhq import DhanContext, MarketFeed
from loguru import logger
from app.market_data.connection_state import ConnectionState
from app.market_data.market_feed_client import MarketFeedClient
from app.models.instrument import Instrument


class DhanMarketFeedClient(MarketFeedClient):

    async def subscribe(self, instruments: Iterable[Instrument]) -> None:
        if len(instruments) != 0 :
            logger.info(f"Subscribe to Dhan market feed client. elements {len(instruments)}")
        else:
            logger.info("Nothing Subscribe to Dhan market feed client.")

    async def unsubscribe(self, instruments: Iterable[Instrument]) -> None:
        logger.info(f"Unsubscribe to Dhan market feed client. elements {len(instruments)}")

    def __init__(
        self,
        client_id: str,
        access_token: str,
    ) -> None:
        self._unique_id = uuid4()
        self._state = ConnectionState.STOPPED
        self._reader_task : asyncio.Task | None = None
        self._client_id = client_id
        self._access_token = access_token
        self._dhan_context: DhanContext = DhanContext(
            client_id=client_id,
            access_token=access_token,
        )
        self._market_feed: MarketFeed = MarketFeed(
            dhan_context=self._dhan_context,
            instruments=[]
        )

    async def start(self) -> None:

        if self._state != ConnectionState.STOPPED:
            logger.info("Dhan market data websocket client is already running.")
            return

        logger.info("Starting Dhan market data websocket client.")

        self._state = ConnectionState.CONNECTING
        await self._market_feed.connect()
        self._state = ConnectionState.CONNECTED

        self._reader_task = asyncio.create_task(
            self._consume_market_events()
        )
        logger.info("Dhan market data websocket client started.")

    async def stop(self) -> None:

        if self._state == ConnectionState.STOPPED:
            logger.info("Dhan market data websocket client is not running.")
            return

        logger.info("Stopping Dhan market data websocket client.")

        self._state = ConnectionState.STOPPING

        if self._reader_task:
            self._reader_task.cancel()

            try:
                await self._reader_task
            except asyncio.CancelledError:
                logger.warning("Dhan market data websocket reader cancelled.")

        if self._market_feed is not None:
            await self._market_feed.disconnect()
            self._market_feed = None
        self._state = ConnectionState.STOPPED
        logger.info("Dhan market data client stopped.")


    async def _consume_market_events(self) -> None:

        logger.info("Receive loop started.")

        while self._state == ConnectionState.CONNECTED:
            try:
                message = await self._market_feed.get_instrument_data()

                logger.info(message)

            except Exception as ex:
                logger.error("Receive loop failed {}",ex)


        logger.info("Receive loop stopped.")

    @property
    def state(self) -> ConnectionState:
        return self._state

    @property
    def unique_id(self) -> str:
        return self._unique_id