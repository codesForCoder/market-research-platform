from app.market_data.client import MarketDataClient


class WebSocketManager:

    def __init__(
        self,
        clients: list[MarketDataClient],
    ) -> None:
        self._clients: list[MarketDataClient] = clients

    async def start(self) -> None:

        # await self._client.start()
        for client in self._clients:
            await client.start()

    async def stop(self) -> None:

        # await self._client.stop()
        for client in self._clients:
            await client.stop()
