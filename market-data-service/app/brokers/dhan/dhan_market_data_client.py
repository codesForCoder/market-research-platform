from __future__ import annotations

from app.brokers.dhan.websocket_url_builder import DhanWebSocketUrlBuilder
from app.core.config import get_settings
from app.market_data.connection_state import ConnectionState
import asyncio

from loguru import logger
from websockets.asyncio.client import ClientConnection, connect

from app.market_data.client import MarketDataClient



class DhanMarketDataClient(MarketDataClient):

    def __init__(
        self
    ) -> None:

        self._websocket_url = DhanWebSocketUrlBuilder.build()
        self._websocket: ClientConnection | None = None
        self._receive_task: asyncio.Task | None = None
        self._state  : ConnectionState = ConnectionState.STOPPED

    async def start(self) -> None:

        if self._state != ConnectionState.STOPPED:
            logger.info("Dhan market data websocket client is already running.")
            return

        logger.info("Starting Dhan market data websocket client.")

        self._state = ConnectionState.CONNECTING

        await self._connect()

        self._state = ConnectionState.CONNECTED

        self._start_receive_task()
        logger.info("Dhan market data websocket client started.")

    async def stop(self) -> None:

        if self._state == ConnectionState.STOPPED:
            logger.info("Dhan market data websocket client is not running.")
            return

        logger.info("Stopping Dhan market data websocket client.")

        self._state = ConnectionState.STOPPING

        await self._stop_receive_task()

        if self._websocket is not None:
            await self._websocket.close()
            self._websocket = None
        self._state = ConnectionState.STOPPED
        logger.info("Dhan market data client stopped.")

    async def _connect(self) -> None:

        logger.info(
            "Connecting to {}",
            get_settings().DHAN_MARKET_DATA_WS_URL,
        )

        self._websocket = await connect(
            self._websocket_url,
        )

        logger.info("WebSocket connected.")

    async def _receive_loop(self) -> None:

        logger.info("Receive loop started.")

        while self._state == ConnectionState.CONNECTED:
            await asyncio.sleep(1)


        logger.info("Receive loop stopped.")

    def _start_receive_task(self) -> None:
        self._receive_task = asyncio.create_task(
            self._receive_loop(),
            name="dhan-receive-loop",
        )

    async def _stop_receive_task(self) -> None:

        if self._receive_task is None:
            return

        self._receive_task.cancel()

        try:
            await self._receive_task
        except asyncio.CancelledError:
            pass

        self._receive_task = None

    @property
    def is_connected(self) -> bool:
        return self._state == ConnectionState.CONNECTED

    @property
    def is_running(self) -> bool:
        return self._state in {
            ConnectionState.CONNECTING,
            ConnectionState.CONNECTED,
            ConnectionState.RECONNECTING,
        }

    @property
    def state(self) -> ConnectionState:
        return self._state