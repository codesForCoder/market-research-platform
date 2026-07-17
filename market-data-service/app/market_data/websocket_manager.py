from app.market_data.client import MarketDataClient


class WebSocketManager:

    def __init__(
        self,
        client: MarketDataClient,
    ) -> None:

        self._client = client

    async def start(self) -> None:

        await self._client.start()

    async def stop(self) -> None:

        await self._client.stop()
