import time
from typing import List, Optional
from threading import Lock

from core.runtime.orchestrator import DevSafeRuntime
from core.watcher.events import FileEvent


class DebounceQueue:
    """
    Collects filesystem events and emits a single
    'stable' signal after quiet period.

    Does NOT perform commits.
    """

    def __init__(self, runtime: DevSafeRuntime, debounce_seconds: float = 5.0):
        self.runtime = runtime
        self.debounce_seconds = debounce_seconds

        self._events: List[FileEvent] = []
        self._last_event_ts: Optional[float] = None
        self._lock = Lock()

    # ---------- Input ----------

    def push(self, event: FileEvent) -> None:
        """
        Called by Watcher.
        """
        self.runtime.require_active()

        with self._lock:
            self._events.append(event)
            self._last_event_ts = time.time()

    # ---------- Processing ----------

    def is_ready(self) -> bool:
        """
        True if quiet window elapsed.
        """
        if not self._events or self._last_event_ts is None:
            return False

        return (time.time() - self._last_event_ts) >= self.debounce_seconds

    def flush(self) -> List[FileEvent]:
        """
        Returns aggregated events and clears queue.
        """
        self.runtime.require_active()

        with self._lock:
            events = list(self._events)
            self._events.clear()
            self._last_event_ts = None
            return events

    # ---------- Fail-safe ----------

    def clear(self) -> None:
        """
        Used when runtime enters PAUSED/STOPPED.
        """
        with self._lock:
            self._events.clear()
            self._last_event_ts = None
