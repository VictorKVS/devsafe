import pytest
from enum import Enum

class AutomationState(Enum):
    STOPPED = "S0_STOPPED"
    ACTIVE = "S1_ACTIVE"
    PAUSED = "S2_PAUSED"
    RECOVERING = "S3_RECOVERING"


@pytest.fixture
def state_machine():
    """
    Fail-Safe State Machine placeholder.
    Real implementation must respect these states and transitions.
    """
    return {
        "state": AutomationState.STOPPED,
        "last_error": None,
    }
