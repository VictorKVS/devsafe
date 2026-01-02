from pathlib import Path

from core.runtime.orchestrator import DevSafeRuntime
from core.debounce.queue import DebounceQueue
from core.watcher.handler import WatcherEventHandler
from core.watcher.events import FileEvent, FileEventType


class FileSystemWatcher:
    """
    Filesystem watcher.
    Generates events and passes them to handler.
    """

    def __init__(self, runtime: DevSafeRuntime, queue: DebounceQueue):
        self.runtime = runtime
        self.handler = WatcherEventHandler(runtime, queue)

    def simulate_event(self, event_type: FileEventType, path: Path) -> None:
        """
        Временный метод для тестов / демо.
        Реальный watchdog подключится позже.
        """
        event = FileEvent(event_type=event_type, path=path)

        try:
            self.handler.handle(event)
        except Exception:
            # Watcher НИКОГДА не валит приложение
            # Все ошибки — через runtime.fail_safe()
            return
