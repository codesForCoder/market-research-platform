from abc import ABC, abstractmethod

class OptionChainPublisher(ABC):

    @abstractmethod
    async def publish(self, snapshot):
        ...