"""
DevSafe application entry point.
Composition root: wires all core components together.
"""

from core.project_manager.manager import ProjectManager
from core.state_machine.controller import FailSafeStateController
from core.runtime.orchestrator import DevSafeRuntime
from core.debounce.queue import DebounceQueue
from core.watcher.watcher import FileSystemWatcher


def build_runtime():
    """
    Builds and wires DevSafe runtime components.

    Returns:
        runtime: DevSafeRuntime
        watcher: FileSystemWatcher
        queue: DebounceQueue
    """
    # 1️⃣ Core state & project control
    pm = ProjectManager()
    sm = FailSafeStateController()
    runtime = DevSafeRuntime(pm, sm)

    # 2️⃣ Event buffering
    queue = DebounceQueue(runtime, debounce_seconds=5.0)

    # 3️⃣ Filesystem watcher (event source)
    watcher = FileSystemWatcher(runtime, queue)

    return runtime, watcher, queue
