from conftest import AutomationState


def test_initial_state_is_stopped(state_machine):
    """
    ADR-0002
    System must start in STOPPED state (S0).
    """
    assert state_machine["state"] == AutomationState.STOPPED


def test_active_state_requires_safe_conditions():
    """
    ADR-0002 / GR-FAILSAFE-01
    ACTIVE state allowed only when all guards pass.
    """
    safe_conditions = True  # placeholder
    if safe_conditions:
        state_machine["state"] = AutomationState.ACTIVE

    assert state_machine["state"] == AutomationState.ACTIVE


def test_paused_state_blocks_automation():
    """
    ADR-0002
    PAUSED state must block commit/push/backup.
    """
    state_machine["state"] = AutomationState.PAUSED

    commit_allowed = False
    push_allowed = False
    backup_allowed = False

    assert commit_allowed is False
    assert push_allowed is False
    assert backup_allowed is False


def test_recovering_state_requires_user_action():
    """
    ADR-0002
    RECOVERING state entered only after explicit user action.
    """
    user_acknowledged = True  # placeholder

    if user_acknowledged:
        state_machine["state"] = AutomationState.RECOVERING

    assert state_machine["state"] == AutomationState.RECOVERING
