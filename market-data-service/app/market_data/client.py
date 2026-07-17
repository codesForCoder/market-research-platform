from abc import ABC, abstractmethod


class MarketDataClient(ABC):

    @abstractmethod
    async def start(self) -> None:
        """Start receiving market data."""
        ...

    @abstractmethod
    async def stop(self) -> None:
        """Stop receiving market data."""
        ...