from abc import ABC, abstractmethod
from collections.abc import Iterable

from app.models.instrument import Instrument
from app.market_data.connection_state import ConnectionState


class MarketFeedClient(ABC):

    @abstractmethod
    async def start(self) -> None:
        """Start the market feed."""
        ...

    @abstractmethod
    async def stop(self) -> None:
        """Stop the market feed."""
        ...

    @abstractmethod
    async def subscribe(
        self,
        instruments: Iterable[Instrument],
    ) -> None:
        """Subscribe to instruments."""
        ...

    @abstractmethod
    async def unsubscribe(
        self,
        instruments: Iterable[Instrument],
    ) -> None:
        """Unsubscribe from instruments."""
        ...

    @property
    @abstractmethod
    def state(self) -> ConnectionState:
        ...

    @property
    @abstractmethod
    def debug(self) -> None:
        ...

    @property
    @abstractmethod
    def unique_id(self) -> str:
        ...

    @property
    def is_connected(self) -> bool:
        return self.state == ConnectionState.CONNECTED

    @property
    def is_running(self) -> bool:
        return self.state in {
            ConnectionState.CONNECTING,
            ConnectionState.CONNECTED,
        }