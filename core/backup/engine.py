import shutil
from pathlib import Path

from core.runtime.orchestrator import DevSafeRuntime
from core.backup.errors import BackupFailed, BackupPathInvalid
from core.backup.filters import should_exclude


class BackupEngine:
    """
    Post-commit backup engine.
    Copies project working tree to backup location.
    """

    def __init__(self, runtime: DevSafeRuntime):
        self.runtime = runtime

    def run(self) -> None:
        # 1️⃣ Fail-safe gate
        self.runtime.require_active()

        project = self.runtime.get_active_project()
        if project is None:
            self.runtime.fail_safe("Backup failed: no active project")
            return

        src = Path(project.path)
        dst = Path(project.backup_path)

        if not src.exists():
            self.runtime.fail_safe("Backup failed: source path missing")
            return

        if not dst.exists():
            raise BackupPathInvalid("Backup path does not exist")

        try:
            self._copy_tree(src, dst)
        except Exception as e:
            self.runtime.fail_safe(f"Backup failed: {e}")

    def _copy_tree(self, src: Path, dst: Path) -> None:
        for item in src.rglob("*"):
            if should_exclude(item):
                continue

            rel = item.relative_to(src)
            target = dst / rel

            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
