from __future__ import annotations

import asyncio
from collections import defaultdict
from contextlib import suppress
from typing import AsyncIterator

from .schemas import StreamEvent


class EventBus:
    """Fan-out event bus per session for SSE streaming."""

    def __init__(self) -> None:
        self._subscribers: dict[str, set[asyncio.Queue[StreamEvent]]] = defaultdict(set)

    async def publish(self, event: StreamEvent) -> None:
        queues = self._subscribers.get(event.session_id)
        if not queues:
            return
        for queue in list(queues):
            with suppress(asyncio.QueueFull):
                queue.put_nowait(event)

    async def subscribe(self, session_id: str) -> AsyncIterator[StreamEvent]:
        queue: asyncio.Queue[StreamEvent] = asyncio.Queue(maxsize=100)
        self._subscribers[session_id].add(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            self._subscribers[session_id].discard(queue)
