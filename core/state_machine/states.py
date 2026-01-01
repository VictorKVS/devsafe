from enum import Enum


class AutomationState(Enum):
    """
    Fail-Safe Automation States (ADR-0002)
    """

    STOPPED = "S0_STOPPED"
    ACTIVE = "S1_ACTIVE"
    PAUSED = "S2_PAUSED"
    RECOVERING = "S3_RECOVERING"
