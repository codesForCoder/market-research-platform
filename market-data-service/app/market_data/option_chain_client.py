
from abc import ABC, abstractmethod

from app.models.instrument import Instrument
from app.models.option_chain_snapshot import OptionChainSnapshot


class OptionChainClient(ABC):
    """
    Broker-agnostic interface for fetching an option chain.

    Implementations are responsible for:
        - Building the broker-specific request
        - Calling the broker API
        - Mapping the response into the domain model
    """

    @abstractmethod
    async def fetch(
        self,
        instrument: Instrument,
    ) -> OptionChainSnapshot:
        """
        Fetch the latest option chain for the given request.

        Args:
            instrument:
                The option chain request.

        Returns:
            A normalized OptionChainSnapshot.

        Raises:
            Exception:
                Implementations should raise a broker-specific exception
                (or wrap it into a common exception) if the fetch fails.
        """
        raise NotImplementedError