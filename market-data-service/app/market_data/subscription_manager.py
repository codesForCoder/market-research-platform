import asyncio
from collections import defaultdict
from collections.abc import Iterable
from typing import List

from loguru import logger

from app.market_data.market_feed_client import MarketFeedClient
from app.models.instrument import Instrument
from app.models.instrument_id import InstrumentId
from app.models.subscription_result import SubscriptionResult


class SubscriptionManager:
    def __init__(self, clients: Iterable[MarketFeedClient], per_client_limit: int, market_depth: int) -> None:

        self._clients = tuple(clients)
        self._per_client_limit = per_client_limit
        self._market_depth = market_depth
        self._subscriptions: dict[
            InstrumentId,
            MarketFeedClient,
        ] = {}

        self._client_subscriptions: dict[
            MarketFeedClient,
            set[InstrumentId],
        ] = defaultdict(set)
        # init self._client_subscriptions with all clients
        self._lock = asyncio.Lock()
        for client in self._clients:
            self._client_subscriptions[client] = set()

    async def subscribe(
        self,
        instruments: Iterable[Instrument],
    ) -> list[SubscriptionResult]:
        results: list[SubscriptionResult] = []
        for instrument in instruments:
            async with self._lock:
                # Check if instrument is already subscribed
                if instrument.instrument_id in self._subscriptions:
                    results.append(SubscriptionResult(instrument, False, "Already subscribed", self._market_depth))
                    continue
                client = self.get_least_busy_client()
                if client is None:
                    results.append(SubscriptionResult(instrument, False, "No available client", self._market_depth))
                    continue
                self._subscriptions[instrument.instrument_id] = client
                self._client_subscriptions[client].add(instrument.instrument_id)
            try:
                await client.subscribe([instrument])
                results.append(SubscriptionResult(instrument, True, None, self._market_depth))
            except Exception as e:
                results.append(SubscriptionResult(instrument, False, str(e), self._market_depth))
                # Remove from tracking if subscription failed
                async with self._lock:
                    self._subscriptions.pop(instrument.instrument_id, None)
                    self._client_subscriptions[client].discard(instrument.instrument_id)
                logger.error(f"Failed to subscribe {instrument}: {e}")
        return results

    async def unsubscribe(
        self,
        instruments: Iterable[Instrument],
    ) -> list[SubscriptionResult]:
        results: list[SubscriptionResult] = []
        for instrument in instruments:
            async with self._lock:
                client = self._subscriptions.get(instrument.instrument_id)
                if client is None:
                    results.append(SubscriptionResult(instrument, False, "Not subscribed", self._market_depth))
                    continue
                # Reserve removal
                self._subscriptions.pop(instrument.instrument_id, None)
                self._client_subscriptions[client].discard(instrument.instrument_id)
            try:
                await client.unsubscribe([instrument])
                results.append(SubscriptionResult(instrument, True, None, self._market_depth))
            except Exception as e:
                # Rollback
                async with self._lock:
                    self._subscriptions[instrument.instrument_id] = client
                    self._client_subscriptions[client].add(instrument.instrument_id)
                results.append(SubscriptionResult(instrument, False, str(e), self._market_depth))
                logger.error(f"Failed to unsubscribe {instrument}: {e}")
        return results

    @property
    def subscription_count_per_client(self) -> dict[str, int]:
        subscription_count_per_client = {}
        for key, value in self._client_subscriptions.items():
            subscription_count_per_client[key.unique_id] = len(value)
        return subscription_count_per_client

    def subscriptions_by_client(self, client_id: str) -> list[Instrument] | None:
        logger.info("Getting subscriptions for client: {}", client_id)
        market_feed_client = next((s for s in self._clients if s.unique_id == client_id), None)
        if market_feed_client:
            return list(self._client_subscriptions[market_feed_client])
        else:
            return list()

    def get_least_busy_client(self) -> MarketFeedClient | None:
        least_busy_client = min(self._client_subscriptions, key=lambda k: len(self._client_subscriptions[k]))
        if len(self._client_subscriptions[least_busy_client]) < self._per_client_limit:
            return least_busy_client
        else:
            logger.warning("all clients have reached max threshold")
            return None
