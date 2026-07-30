from collections import defaultdict
from collections.abc import Iterable
from loguru import logger
from app.market_data.market_feed_client import MarketFeedClient
from app.models.instrument import Instrument
from app.models.instrument_id import InstrumentId


class SubscriptionManager:

    def __init__(
        self,
        clients: Iterable[MarketFeedClient],
    ) -> None:

        self._clients = tuple(clients)

        self._subscriptions: dict[
            InstrumentId,
            MarketFeedClient,
        ] = {}

        self._client_subscriptions : dict[
            MarketFeedClient,
            set[InstrumentId],
        ] = defaultdict(
            set
        )
        # init self._client_subscriptions with all clients
        for client in self._clients:
            self._client_subscriptions[client] = set()

    async def subscribe(
        self,
        client: MarketFeedClient,
        instruments: Iterable[Instrument],
    ) -> None:

        # Avoid duplicate subscription
        instrument_list = [
            inst for inst in instruments
            if inst.instrument_id not in self._subscriptions
        ]
        await client.subscribe(instrument_list)
        for instrument in instrument_list:
            self._subscriptions[
                instrument.instrument_id
            ] = client
            self._client_subscriptions[
                client
            ].add(
                instrument.instrument_id
            )

    async def unsubscribe(
        self,
        instruments: Iterable[Instrument],
    ) -> None:

        grouped: dict[
            MarketFeedClient,
            list[Instrument],
        ] = defaultdict(list)

        for instrument in instruments:

            client = self._subscriptions.get(
                instrument.instrument_id
            )

            if client is None:
                continue

            grouped[client].append(instrument)

        for client, values in grouped.items():

            await client.unsubscribe(values)

            for instrument in values:

                self._subscriptions.pop(
                    instrument.instrument_id,
                    None,
                )

                self._client_subscriptions[
                    client
                ].discard(
                    instrument.instrument_id
                )

    @property
    def subscription_count(self) -> int:
        return len(self._subscriptions)

    @property
    def subscription_count_per_client(self) -> dict[str, int]:
        subscription_count_per_client = {}
        for key , value in self._client_subscriptions.items():
            subscription_count_per_client[key.unique_id] = len(value)

        return subscription_count_per_client


    def subscriptions_by_client(self , client_id: str) -> list[Instrument] | None:
        logger.info("Getting subscriptions for client: {}", client_id)
        market_feed_client =   next((s for s in self._clients if s.unique_id == client_id), None)
        if market_feed_client:
            return list(self._client_subscriptions[market_feed_client])
        else:
            return list()

    def clients(self) -> tuple[MarketFeedClient, ...]:
        return self._clients

    def get_least_busy_client(self) -> MarketFeedClient | None:
        least_busy_client = min(self._client_subscriptions, key=lambda k: len(self._client_subscriptions[k]), default=None)
        if least_busy_client is None:
            return None
        elif len(self._client_subscriptions[least_busy_client])>4500:
            return None
        return least_busy_client

