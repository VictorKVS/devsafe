from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Project:
    name: str
    path: Path
    backup_path: Path
    active: bool = False
