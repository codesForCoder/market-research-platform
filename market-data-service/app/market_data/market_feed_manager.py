from typing import Iterable

from app.market_data.market_feed_client import MarketFeedClient


class MarketFeedManager:
    def __init__(
        self,
        clients: Iterable[MarketFeedClient],
    ) -> None:
        self._clients: tuple[MarketFeedClient, ...] = tuple(clients)

    async def start(self) -> None:

        # await self._client.start()
        for client in self._clients:
            await client.start()

    async def stop(self) -> None:

        # await self._client.stop()
        for client in self._clients:
            await client.stop()
