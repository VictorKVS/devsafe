from dataclasses import dataclass
from pathlib import Path
from enum import Enum


class FileEventType(Enum):
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"


@dataclass(frozen=True)
class FileEvent:
    event_type: FileEventType
    path: Path
