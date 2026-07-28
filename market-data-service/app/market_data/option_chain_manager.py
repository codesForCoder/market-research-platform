

import asyncio
from collections import deque
from typing import Tuple

from app.models.instrument import Instrument

class OptionChainManager:
    """
    Maintains active option chain subscriptions and provides
    round-robin scheduling of subscriptions.

    Internally:
        - set   : O(1) membership lookup
        - deque : O(1) round-robin rotation
    """

    def __init__(self) -> None:
        self._subscriptions: set[Instrument] = set()
        self._rotation_queue: deque[Instrument] = deque()
        self._has_subscription = asyncio.Event()
        self._lock = asyncio.Lock()

    async def subscribe(self, request: Instrument) -> bool:
        """
        Adds a subscription.

        Returns:
            True if added.
            False if it already exists.
        """
        async with self._lock:
            if request in self._subscriptions:
                return False

            self._subscriptions.add(request)
            self._rotation_queue.append(request)
            self._has_subscription.set()
            return True

    async def unsubscribe(self, request: Instrument) -> bool:
        """
        Removes a subscription.

        Returns:
            True if removed.
            False if it was not present.
        """
        async with self._lock:
            if request not in self._subscriptions:
                return False

            self._subscriptions.remove(request)
            self._rotation_queue.remove(request)
            if not self._subscriptions:
                self._has_subscription.clear()
            return True

    async def is_subscribed(self, request: Instrument) -> bool:
        """
        Returns whether the request is currently subscribed.
        """
        async with self._lock:
            return request in self._subscriptions

    async def next_subscription(self) -> Instrument | None:
        """
        Returns the next subscription to poll using
        round-robin scheduling.

        Returns:
            OptionChainRequest or None if no subscriptions exist.
        """
        async with self._lock:
            if not self._rotation_queue:
                return None

            request = self._rotation_queue[0]
            self._rotation_queue.rotate(-1)

            return request

    async def get_subscriptions(self) -> Tuple[Instrument, ...]:
        """
        Returns an immutable snapshot of all current subscriptions.

        The snapshot is created while holding the lock to prevent the
        underlying set from being modified during iteration.
        """
        async with self._lock:
            return tuple(self._subscriptions)

    async def clear(self) -> None:
        """
        Removes all subscriptions.
        """
        async with self._lock:
            self._subscriptions.clear()
            self._rotation_queue.clear()
            self._has_subscription.clear()

    async def wait_for_subscription(self) -> None:
        """
        Blocks until at least one subscription is available.
        Returns immediately if subscriptions already exist.
        """
        await self._has_subscription.wait()

    async def shutdown(self) -> None:
        self._has_subscription.set()

    async def size(self) -> int:
        """
        Returns the number of active subscriptions.
        """
        async with self._lock:
            return len(self._subscriptions)