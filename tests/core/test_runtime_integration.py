import pytest
from pathlib import Path

from core.project_manager.manager import ProjectManager
from core.state_machine.controller import FailSafeStateController
from core.state_machine.states import AutomationState
from core.runtime.orchestrator import DevSafeRuntime
from core.runtime.errors import GuardViolation


def test_start_requires_active_project():
    pm = ProjectManager()
    sm = FailSafeStateController()
    rt = DevSafeRuntime(pm, sm)

    with pytest.raises(GuardViolation):
        rt.start_automation()

    assert sm.state == AutomationState.PAUSED


def test_start_ok_when_project_selected():
    pm = ProjectManager()
    sm = FailSafeStateController()
    rt = DevSafeRuntime(pm, sm)

    pm.register_project("p1", Path("/p1"), Path("/b1"))
    rt.select_project("p1")

    rt.start_automation()
    assert sm.state == AutomationState.ACTIVE


def test_cannot_switch_project_while_active():
    pm = ProjectManager()
    sm = FailSafeStateController()
    rt = DevSafeRuntime(pm, sm)

    pm.register_project("p1", Path("/p1"), Path("/b1"))
    pm.register_project("p2", Path("/p2"), Path("/b2"))

    rt.select_project("p1")
    rt.start_automation()

    with pytest.raises(GuardViolation):
        rt.select_project("p2")
