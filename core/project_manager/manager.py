from pathlib import Path
from typing import Dict, Optional

from .models import Project
from .errors import (
    ProjectAlreadyExists,
    ProjectNotFound,
    ActiveProjectExists,
)


class ProjectManager:
    """
    Single source of truth for all DevSafe projects.
    Enforces:
    - max 5 registered projects
    - exactly one active project
    """

    MAX_PROJECTS = 5

    def __init__(self):
        self._projects: Dict[str, Project] = {}

    # ---------- Queries ----------

    def list_projects(self) -> Dict[str, Project]:
        return self._projects.copy()

    def get_active_project(self) -> Optional[Project]:
        for project in self._projects.values():
            if project.active:
                return project
        return None

    # ---------- Commands ----------

    def register_project(
        self,
        name: str,
        path: Path,
        backup_path: Path,
    ) -> None:
        if name in self._projects:
            raise ProjectAlreadyExists(name)

        if len(self._projects) >= self.MAX_PROJECTS:
            raise ProjectManagerError("Maximum number of projects reached")

        self._projects[name] = Project(
            name=name,
            path=path,
            backup_path=backup_path,
            active=False,
        )

    def activate_project(self, name: str) -> None:
        if name not in self._projects:
            raise ProjectNotFound(name)

        if self.get_active_project() is not None:
            raise ActiveProjectExists(
                "Another project is already active"
            )

        project = self._projects[name]
        self._projects[name] = Project(
            name=project.name,
            path=project.path,
            backup_path=project.backup_path,
            active=True,
        )

    def deactivate_project(self) -> None:
        active = self.get_active_project()
        if not active:
            return

        self._projects[active.name] = Project(
            name=active.name,
            path=active.path,
            backup_path=active.backup_path,
            active=False,
        )
