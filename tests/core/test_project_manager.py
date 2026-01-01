from pathlib import Path
import pytest

from core.project_manager.manager import ProjectManager
from core.project_manager.errors import ActiveProjectExists


def test_only_one_project_can_be_active():
    pm = ProjectManager()

    pm.register_project(
        "proj1", Path("/p1"), Path("/b1")
    )
    pm.register_project(
        "proj2", Path("/p2"), Path("/b2")
    )

    pm.activate_project("proj1")

    with pytest.raises(ActiveProjectExists):
        pm.activate_project("proj2")
