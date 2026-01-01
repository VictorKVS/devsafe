from typing import Optional

from .states import AutomationState
from .errors import InvalidTransition, UnsafeOperation


class FailSafeStateController:
    """
    Central authority controlling DevSafe automation state.

    Enforces:
    - explicit state transitions
    - fail-safe behavior
    - no silent continuation on errors
    """

    def __init__(self):
        self._state: AutomationState = AutomationState.STOPPED
        self._last_error: Optional[str] = None

    # ---------- Queries ----------

    @property
    def state(self) -> AutomationState:
        return self._state

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    # ---------- State transitions ----------

    def start(self) -> None:
        if self._state != AutomationState.STOPPED:
            raise InvalidTransition("Can only start from STOPPED")

        self._state = AutomationState.ACTIVE

    def pause(self, reason: str) -> None:
        """
        Fail-safe entry point.
        Can be triggered from ANY state.
        """
        self._state = AutomationState.PAUSED
        self._last_error = reason

    def recover(self) -> None:
        if self._state != AutomationState.PAUSED:
            raise InvalidTransition("Recover allowed only from PAUSED")

        self._state = AutomationState.RECOVERING
        self._last_error = None

    def resume(self, guards_ok: bool) -> None:
        if self._state != AutomationState.RECOVERING:
            raise InvalidTransition("Resume allowed only from RECOVERING")

        if not guards_ok:
            self.pause("Guard re-validation failed")
            return

        self._state = AutomationState.ACTIVE

    def stop(self) -> None:
        self._state = AutomationState.STOPPED
        self._last_error = None

    # ---------- Enforcement helpers ----------

    def require_active(self) -> None:
        """
        Used by subsystems (watcher, git, backup).
        """
        if self._state != AutomationState.ACTIVE:
            raise UnsafeOperation(
                f"Operation not allowed in state {self._state.value}"
            )
