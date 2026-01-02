import time
from pathlib import Path

from core.project_manager.manager import ProjectManager
from core.state_machine.controller import FailSafeStateController
from core.runtime.orchestrator import DevSafeRuntime
from core.debounce.queue import DebounceQueue
from core.commit_scheduler.scheduler import GitCommitScheduler
from core.watcher.events import FileEvent, FileEventType
from core.state_machine.states import AutomationState


def setup_runtime():
    pm = ProjectManager()
    sm = FailSafeStateController()
    rt = DevSafeRuntime(pm, sm)

    pm.register_project("p1", Path("/p1"), Path("/b1"))
    rt.select_project("p1")
    rt.start_automation()

    return rt, sm


def test_scheduler_no_commit_before_debounce():
    rt, sm = setup_runtime()
    queue = DebounceQueue(rt, debounce_seconds=0.2)
    scheduler = GitCommitScheduler(rt, queue)

    queue.push(FileEvent(FileEventType.MODIFIED, Path("/p1/a.txt")))

    assert scheduler.poll() is None


def test_scheduler_returns_commit_intent():
    rt, sm = setup_runtime()
    queue = DebounceQueue(rt, debounce_seconds=0.1)
    scheduler = GitCommitScheduler(rt, queue)

    queue.push(FileEvent(FileEventType.MODIFIED, Path("/p1/a.txt")))
    time.sleep(0.15)

    intent = scheduler.poll()

    assert intent is not None
    assert len(intent.events) == 1
    assert intent.reason.startswith("Filesystem stabilized")


def test_scheduler_blocked_when_paused():
    rt, sm = setup_runtime()
    queue = DebounceQueue(rt, debounce_seconds=0.1)
    scheduler = GitCommitScheduler(rt, queue)

    sm.pause("error")

    try:
        scheduler.poll()
        assert False, "Expected require_active to fail"
    except Exception:
        pass
