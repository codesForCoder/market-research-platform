import asyncio
from typing import Iterable
from uuid import uuid4
import json
from dhanhq import DhanContext, MarketFeed
from loguru import logger
from app.brokers.dhan.dhan_exchange_segment import ExchangeSegment
from app.brokers.dhan.exchange_segment_mapper import ExchangeSegmentMapper
from app.brokers.dhan.feed_type import FeedType
from app.market_data.connection_state import ConnectionState
from app.market_data.market_feed_client import MarketFeedClient
from app.models.instrument import Instrument


class DhanMarketFeedClient(MarketFeedClient):
    def __init__(
        self,
        client_id: str,
        access_token: str,
    ) -> None:
        self._unique_id = str(uuid4())
        self._state = ConnectionState.STOPPED
        self._reader_task: asyncio.Task | None = None
        self._client_id = client_id
        self._access_token = access_token
        self._dhan_context: DhanContext = DhanContext(
            client_id=client_id,
            access_token=access_token,
        )
        # For temporary debug
        # instruments = [(MarketFeed.NSE, "1333", MarketFeed.Ticker),
        #                (MarketFeed.NSE, "1333", MarketFeed.Quote),
        #                (MarketFeed.NSE, "1333", MarketFeed.Full),
        #                (MarketFeed.NSE, "11915", MarketFeed.Ticker),
        #                (MarketFeed.NSE, "11915", MarketFeed.Full)]
        self._market_feed: MarketFeed = MarketFeed(
            dhan_context=self._dhan_context,
            # For temporary debug
            # instruments=instruments,
            instruments=[],
        )

    async def start(self) -> None:

        if self._state != ConnectionState.STOPPED:
            logger.info("Dhan market data websocket client is already running.")
            return

        logger.info("Starting Dhan market data websocket client.")

        self._state = ConnectionState.CONNECTING
        # Connect to the WebSocket
        await self._market_feed.connect()
        self._state = ConnectionState.CONNECTED

        self._reader_task = asyncio.create_task(self._consume_market_events())
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

        logger.info("Receive loop started. State: {}", self._state)

        while self._state == ConnectionState.CONNECTED:
            try:
                logger.info("Waiting for instrument data in {}", self.unique_id)
                # Use get_instrument_data() which is async
                message = await self._market_feed.get_instrument_data()
                logger.info("Client {} Received message: {}", self.unique_id, message)

            except asyncio.CancelledError:
                logger.info(
                    "Client {} Receive loop cancelled due to task cancellation",
                    self.unique_id,
                )
                raise
            except Exception as ex:
                logger.error("Client {}  Receive loop failed: {}", self.unique_id, ex)
        logger.info("Receive loop stopped. Final state: {}", self._state)

    async def subscribe(self, instruments: Iterable[Instrument]) -> None:
        """Subscribe to market data for the given instruments."""
        logger.info(f"Subscribe to Dhan market feed client. elements {len(instruments)}")
        for instrument in instruments:
            exchange_segment = ExchangeSegmentMapper.to_exchange_segment(
                exchange=instrument.instrument_id.exchange,
                segment=instrument.instrument_id.segment,
            )
            internal_instrument = (
                exchange_segment.value,
                str(instrument.security_id),
                FeedType.SUBSCRIBE_FULL_5_DEPTH.value,
            )
            await self._subscribe_symbol_async(internal_instrument)

        for instrument in self._market_feed.instruments:
            logger.info(f"Instrument: {instrument}")

    async def unsubscribe(self, instruments: Iterable[Instrument]) -> None:
        logger.info(f"Unsubscribe to Dhan market feed client elements {len(instruments)}")

        for instrument in instruments:
            exchange_segment = ExchangeSegmentMapper.to_exchange_segment(
                exchange=instrument.instrument_id.exchange,
                segment=instrument.instrument_id.segment,
            )
            internal_instrument = (
                exchange_segment.value,
                str(instrument.security_id),
                FeedType.UNSUBSCRIBE_FULL_5_DEPTH.value,
            )
            await self._unsubscribe_symbol_async(internal_instrument)

        for instrument in self._market_feed.instruments:
            logger.info(f"Instrument: {instrument}")

    # Temporarily added as dhan sdk is not working
    async def _subscribe_symbol_async(self, instrument: tuple[str, str, int]) -> None:
        exchange_segment, security_id, request_code = instrument
        subscription_message = {
            "RequestCode": request_code,
            "InstrumentCount": 1,
            "InstrumentList": [
                {
                    "ExchangeSegment": exchange_segment,
                    "SecurityId": security_id,
                }
            ],
        }

        logger.info("Sending subscription: {}", subscription_message)

        await self._market_feed.ws.send(json.dumps(subscription_message))

        # Keep SDK's internal instrument list in sync
        exchange_segment_str, *rest = instrument
        dhan_internal_instrument = (
            list(ExchangeSegment).index(exchange_segment_str),
            *rest,
        )
        if dhan_internal_instrument not in self._market_feed.instruments:
            self._market_feed.instruments.append(dhan_internal_instrument)

    # Temporarily added as dhan sdk is not working
    async def _unsubscribe_symbol_async(self, instrument: tuple[str, str, int]) -> None:

        exchange_segment, security_id, request_code = instrument

        unsubscription_message = {
            "RequestCode": request_code,
            "InstrumentCount": 1,
            "InstrumentList": [
                {
                    "ExchangeSegment": exchange_segment,
                    "SecurityId": security_id,
                }
            ],
        }
        logger.info("Sending unsubscription: {}", unsubscription_message)
        await self._market_feed.ws.send(json.dumps(unsubscription_message))
        # Keep SDK's internal instrument list in sync
        exchange_segment_str, *rest = instrument
        dhan_internal_instrument = (
            list(ExchangeSegment).index(exchange_segment_str),
            security_id,
            FeedType.SUBSCRIBE_FULL_5_DEPTH.value,
        )  # for removing from dhan sdk internal list tuple signature need to match of what inserted during subscription
        if dhan_internal_instrument in self._market_feed.instruments:
            self._market_feed.instruments.remove(dhan_internal_instrument)

    @property
    def state(self) -> ConnectionState:
        return self._state

    @property
    def unique_id(self) -> str:
        return self._unique_id

    def debug(self) -> None:
        logger.info("Dhan market feed client debug:")
        logger.info("Instruments: {}", self._market_feed.instruments)
