from dataclasses import dataclass
from typing import List
from core.watcher.events import FileEvent


@dataclass(frozen=True)
class CommitIntent:
    """
    Decision to perform a git commit.
    This is NOT the commit itself.
    """
    events: List[FileEvent]
    reason: str
