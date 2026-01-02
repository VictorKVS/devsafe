from pathlib import Path
from typing import Optional

from core.project_manager.models import Project


def guard_active_project_exists(project: Optional[Project]) -> None:
    if project is None:
        raise ValueError("No active project selected")


def guard_project_path_valid(project: Project) -> None:
    if not project.path:
        raise ValueError("Project path is empty")
    # В реальном коде можно проверить exists() когда дойдём до реального FS
    # if not project.path.exists(): raise ValueError("Project path does not exist")


def guard_backup_path_valid(project: Project) -> None:
    if not project.backup_path:
        raise ValueError("Backup path is empty")
    # Дополнительно: backup_path не внутри project.path
    # if str(project.backup_path).startswith(str(project.path)): raise ValueError("Backup path recursion")
