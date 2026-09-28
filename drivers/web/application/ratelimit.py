import threading
import time
from collections import defaultdict, deque
from typing import Callable, Deque, Dict


class RateLimiter:
    """Allows at most `max_events` per key (e.g. a client address) within
    any `window_seconds`. Thread-safe; state lives in this process."""

    def __init__(self,
                 max_events: int,
                 window_seconds: float,
                 clock: Callable[[], float] = time.monotonic
                 ):
        self.max_events = max_events
        self.window_seconds = window_seconds
        self._clock = clock
        self._events: Dict[str, Deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, key: str) -> bool:
        now = self._clock()
        with self._lock:
            events = self._events[key]
            while events and events[0] <= now - self.window_seconds:
                events.popleft()
            if len(events) >= self.max_events:
                return False
            events.append(now)
            return True
