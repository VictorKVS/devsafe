import pytest

from core.state_machine.controller import FailSafeStateController
from core.state_machine.states import AutomationState
from core.state_machine.errors import InvalidTransition, UnsafeOperation


def test_initial_state_is_stopped():
    sm = FailSafeStateController()
    assert sm.state == AutomationState.STOPPED


def test_start_only_from_stopped():
    sm = FailSafeStateController()
    sm.start()
    assert sm.state == AutomationState.ACTIVE

    with pytest.raises(InvalidTransition):
        sm.start()


def test_pause_from_active_sets_error():
    sm = FailSafeStateController()
    sm.start()
    sm.pause("backup failed")

    assert sm.state == AutomationState.PAUSED
    assert sm.last_error == "backup failed"


def test_recover_only_from_paused():
    sm = FailSafeStateController()

    with pytest.raises(InvalidTransition):
        sm.recover()

    sm.pause("error")
    sm.recover()
    assert sm.state == AutomationState.RECOVERING


def test_resume_with_failed_guards_returns_to_paused():
    sm = FailSafeStateController()
    sm.pause("error")
    sm.recover()
    sm.resume(guards_ok=False)

    assert sm.state == AutomationState.PAUSED


def test_require_active_blocks_operations():
    sm = FailSafeStateController()

    with pytest.raises(UnsafeOperation):
        sm.require_active()

    sm.start()
    sm.require_active()  # should not raise
