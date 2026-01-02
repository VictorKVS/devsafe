import subprocess

from core.runtime.orchestrator import DevSafeRuntime
from core.commit_scheduler.models import CommitIntent
from core.git_agent.git_checks import check_git_safe
from core.git_agent.commit_message import build_commit_message
from core.git_agent.errors import GitAgentError


class GitAgent:
    """
    Executes git commits safely.
    """

    def __init__(self, runtime: DevSafeRuntime):
        self.runtime = runtime

    def execute(self, intent: CommitIntent) -> None:
        # 1️⃣ Fail-safe gate
        self.runtime.require_active()

        project = self.runtime.get_active_project()
        if project is None:
            self.runtime.fail_safe("No active project for git execution")
            return

        repo_path = str(project.path)

        try:
            # 2️⃣ Git safety checks
            check_git_safe(repo_path)

            # 3️⃣ Stage all changes
            self._run_git(["add", "-A"], repo_path)

            # 4️⃣ Commit
            message = build_commit_message(intent)
            self._run_git(["commit", "-m", message], repo_path)

        except GitAgentError as e:
            # 5️⃣ HARD FAIL-SAFE
            self.runtime.fail_safe(f"GitAgent failure: {e}")

    def _run_git(self, cmd: list, cwd: str) -> None:
        subprocess.run(
            ["git"] + cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
