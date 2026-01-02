from pathlib import Path

from core.project_manager.manager import ProjectManager
from core.state_machine.controller import FailSafeStateController
from core.runtime.orchestrator import DevSafeRuntime
from core.backup.engine import BackupEngine


def test_backup_copies_files(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "backup"

    src.mkdir()
    dst.mkdir()

    file = src / "a.txt"
    file.write_text("data")

    pm = ProjectManager()
    sm = FailSafeStateController()
    rt = DevSafeRuntime(pm, sm)

    pm.register_project("p1", src, dst)
    rt.select_project("p1")
    rt.start_automation()

    backup = BackupEngine(rt)
    backup.run()

    assert (dst / "a.txt").exists()
