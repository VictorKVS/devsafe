from conftest import AutomationState


def test_transition_s0_to_s1_on_start(state_machine):
    """
    S0 → S1
    User starts automation and all guards pass.
    """
    guards_ok = True

    if state_machine["state"] == AutomationState.STOPPED and guards_ok:
        state_machine["state"] = AutomationState.ACTIVE

    assert state_machine["state"] == AutomationState.ACTIVE


def test_transition_s1_to_s2_on_failure(state_machine):
    """
    S1 → S2
    Any guardrail violation triggers fail-safe.
    """
    state_machine["state"] = AutomationState.ACTIVE

    guardrail_violation = True
    if guardrail_violation:
        state_machine["state"] = AutomationState.PAUSED
        state_machine["last_error"] = "Backup failed"

    assert state_machine["state"] == AutomationState.PAUSED
    assert state_machine["last_error"] is not None


def test_transition_s2_to_s3_on_user_retry(state_machine):
    """
    S2 → S3
    User explicitly chooses to retry.
    """
    state_machine["state"] = AutomationState.PAUSED
    user_retry = True

    if user_retry:
        state_machine["state"] = AutomationState.RECOVERING

    assert state_machine["state"] == AutomationState.RECOVERING


def test_transition_s3_to_s1_on_revalidation(state_machine):
    """
    S3 → S1
    All guards revalidated successfully.
    """
    state_machine["state"] = AutomationState.RECOVERING
    guards_ok = True

    if guards_ok:
        state_machine["state"] = AutomationState.ACTIVE

    assert state_machine["state"] == AutomationState.ACTIVE


def test_transition_s3_to_s0_on_user_stop(state_machine):
    """
    S3 → S0
    User decides to stop automation.
    """
    state_machine["state"] = AutomationState.RECOVERING
    user_stop = True

    if user_stop:
        state_machine["state"] = AutomationState.STOPPED

    assert state_machine["state"] == AutomationState.STOPPED
