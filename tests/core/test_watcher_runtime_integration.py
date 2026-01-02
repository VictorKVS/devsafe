import pytest
from pathlib import Path

from core.project_manager.manager import ProjectManager
from core.state_machine.controller import FailSafeStateController
from core.runtime.orchestrator import DevSafeRuntime
from core.watcher.watcher import FileSystemWatcher
from core.watcher.events import FileEventType
from core.state_machine.states import AutomationState


def test_watcher_ignored_when_not_active():
    pm = ProjectManager()
    sm = FailSafeStateController()
    rt = DevSafeRuntime(pm, sm)
    watcher = FileSystemWatcher(rt)

    pm.register_project("p1", Path("/p1"), Path("/b1"))
    rt.select_project("p1")

    # NOT started → STOPPED
    watcher.simulate_event(FileEventType.MODIFIED, Path("/p1/file.txt"))

    assert sm.state == AutomationState.STOPPED


def test_watcher_processes_only_when_active():
    pm = ProjectManager()
    sm = FailSafeStateController()
    rt = DevSafeRuntime(pm, sm)
    watcher = FileSystemWatcher(rt)

    pm.register_project("p1", Path("/p1"), Path("/b1"))
    rt.select_project("p1")
    rt.start_automation()

    watcher.simulate_event(FileEventType.MODIFIED, Path("/p1/file.txt"))

    assert sm.state == AutomationState.ACTIVE
