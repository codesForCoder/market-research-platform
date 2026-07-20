
import asyncio
from typing import Iterable
from uuid import uuid4
import json
import collections
from dhanhq import DhanContext, FullDepth ,MarketFeed
from loguru import logger
from app.brokers.dhan.dhan_exchange_segment import ExchangeSegment
from app.brokers.dhan.exchange_segment_mapper import ExchangeSegmentMapper
from app.brokers.dhan.feed_type import FeedType
from app.market_data.connection_state import ConnectionState
from app.market_data.market_feed_client import MarketFeedClient
from app.models.instrument import Instrument


class DhanMarketFeedFullDepthClient(MarketFeedClient):

    def __init__(
        self,
        client_id: str,
        access_token: str,
        depth_level: int
    ) -> None:
        self._unique_id = uuid4()
        self._state = ConnectionState.STOPPED
        self._reader_task : asyncio.Task | None = None
        self._client_id = client_id
        self._access_token = access_token
        self._depth_level = depth_level
        self._dhan_context: DhanContext = DhanContext(
            client_id=client_id,
            access_token=access_token,
        )
        # For temporary debug
        instruments = [(MarketFeed.NSE, "1333"),(MarketFeed.NSE, "1334"),(MarketFeed.NSE, "1335"),(MarketFeed.NSE, "1336")]
        self._market_feed: FullDepth = FullDepth(
            dhan_context=self._dhan_context,
            # For temporary debug
            instruments=instruments,
            # instruments=[],
            depth_level=self._depth_level
        )

    async def start(self) -> None:

        if self._state != ConnectionState.STOPPED:
            logger.info("Dhan full depth market data websocket client is already running.")
            return

        logger.info("Starting full depath Dhan market data websocket client.")

        self._state = ConnectionState.CONNECTING
        # Connect to the WebSocket
        await self._market_feed.connect()
        self._state = ConnectionState.CONNECTED

        self._reader_task = asyncio.create_task(
            self._consume_market_events()
        )
        logger.info("Dhan full depth market data websocket client started.")

    async def stop(self) -> None:

        if self._state == ConnectionState.STOPPED:
            logger.info("Dhan full depth market data websocket client is not running.")
            return

        logger.info("Stopping full depth Dhan market data websocket client.")

        self._state = ConnectionState.STOPPING

        if self._reader_task:
            self._reader_task.cancel()

            try:
                await self._reader_task
            except asyncio.CancelledError:
                logger.warning("Dhan full depth market data websocket reader cancelled.")

        if self._market_feed is not None:
            await self._market_feed.disconnect()
            self._market_feed = None
        self._state = ConnectionState.STOPPED
        logger.info("Dhan full depth market data client stopped.")


    async def _consume_market_events(self) -> None:

        logger.info("Receive loop started for full depth. State: {}", self._state)

        while self._state == ConnectionState.CONNECTED:
            try:
                logger.info("Waiting for instrument data in full depth {}",self.unique_id)
                # Use get_instrument_data() which is async
                message = await self._get_instrument_data()
                logger.info("Client {} Received message full depth: {}",self.unique_id,  message)

            except asyncio.CancelledError:
                logger.info("Client full depth {} Receive loop cancelled due to task cancellation", self.unique_id)
                raise
            except Exception as ex:
                logger.error("Client full depth {}  Receive loop failed: {}", self.unique_id, ex)
        logger.info("Receive loop stopped for full depth. Final state: {}", self._state)

    async def subscribe(self, instruments: Iterable[Instrument]) -> None:
        """Subscribe to market full depth data for the given instruments. """
        logger.info(f"Subscribe to Dhan market full depth feed client. elements {len(instruments)}")
        for instrument in instruments:
            exchange_segment = ExchangeSegmentMapper.to_exchange_segment(
                exchange = instrument.instrument_id.exchange,
                segment=instrument.instrument_id.segment,
            )
            internal_instrument = (exchange_segment.value, str(instrument.security_id), FeedType.SUBSCRIBE_FULL_5_DEPTH.value)
            await self._subscribe_symbol_async(internal_instrument)

        for instrument in self._market_feed.instruments:
            logger.info(f"Instrument: {instrument}")

    async def unsubscribe(self, instruments: Iterable[Instrument]) -> None:
        logger.info(f"Unsubscribe to Dhan market feed client elements {len(instruments)}")

        for instrument in instruments:
            exchange_segment = ExchangeSegmentMapper.to_exchange_segment(
                exchange = instrument.instrument_id.exchange,
                segment=instrument.instrument_id.segment,
            )
            internal_instrument = (exchange_segment.value, str(instrument.security_id), FeedType.UNSUBSCRIBE_FULL_5_DEPTH.value)
            await self._unsubscribe_symbol_async(internal_instrument)

        for instrument in self._market_feed.instruments:
            logger.info(f"Instrument: {instrument}")

    # Temporarily added as dhan sdk is not working
    async def _subscribe_symbol_async(
            self,
            instrument: tuple[str, str, int]
    ) -> None:
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

        await self._market_feed.ws.send(
            json.dumps(subscription_message)
        )

        # Keep SDK's internal instrument list in sync
        exchange_segment_str, *rest = instrument
        dhan_internal_instrument = (list(ExchangeSegment).index(exchange_segment_str), *rest)
        if dhan_internal_instrument not in self._market_feed.instruments:
            self._market_feed.instruments.append(dhan_internal_instrument)

    # Temporarily added as dhan sdk is not working
    async def _unsubscribe_symbol_async(
            self,
            instrument: tuple[str, str, int]
    ) -> None:

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
        await self._market_feed.ws.send(
            json.dumps(unsubscription_message)
        )
        # Keep SDK's internal instrument list in sync
        exchange_segment_str, *rest = instrument
        dhan_internal_instrument = (list(ExchangeSegment).index(exchange_segment_str), security_id, FeedType.SUBSCRIBE_FULL_5_DEPTH.value) # for removing from dhan sdk internal list tuple signature need to match of what inserted during subscription
        if dhan_internal_instrument in self._market_feed.instruments:
            self._market_feed.instruments.remove(dhan_internal_instrument)

    # Temporarily added as dhan sdk is not working
    async def _get_instrument_data(self):
        response = await self._market_feed.ws.recv()
        remaining_data = response
        # Initialize as a defaultdict so "depth" defaults to an empty list automatically
        results = collections.defaultdict(list)
        while remaining_data:
            update = self._market_feed.process_data(remaining_data)
            if not update:
                break
            remaining_data = update.pop("remaining_data", None)
            if remaining_data:
                logger.info(f"raw_update---------: {update}")
                logger.info(f"remaining_data---------: {remaining_data}")
            # 1. Process market depth if it exists in the payload
            if "depth" in update:
                results["depth"].extend(update["depth"])
            # 2. Safely merge metadata fields without modifying the source dict layout
            for key, value in update.items():
                if key != "depth":
                    results[key] = value
        return json.dumps(results)


    @property
    def state(self) -> ConnectionState:
        return self._state

    @property
    def unique_id(self) -> str:
        return self._unique_id

    def debug(self) -> None:
        logger.info("Dhan market feed client debug:")
        logger.info("Instruments: {}", self._market_feed.instruments)