from typing import Optional

from core.runtime.orchestrator import DevSafeRuntime
from core.debounce.queue import DebounceQueue
from core.commit_scheduler.models import CommitIntent


class GitCommitScheduler:
    """
    Decides WHEN a commit should be performed
    based on debounced filesystem events.
    """

    def __init__(self, runtime: DevSafeRuntime, queue: DebounceQueue):
        self.runtime = runtime
        self.queue = queue

    def poll(self) -> Optional[CommitIntent]:
        """
        Called periodically (timer / loop / tick).

        Returns:
            CommitIntent if commit should be performed,
            None otherwise.
        """
        # 1️⃣ Fail-safe gate
        self.runtime.require_active()

        # 2️⃣ Check debounce condition
        if not self.queue.is_ready():
            return None

        # 3️⃣ Flush events
        events = self.queue.flush()
        if not events:
            return None

        # 4️⃣ Return DECISION, not action
        return CommitIntent(
            events=events,
            reason="Filesystem stabilized after debounce window"
        )
