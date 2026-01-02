import subprocess
from typing import Tuple

from core.git_agent.errors import UnsafeGitState, GitCommandFailed


def _run_git(cmd: list, cwd: str) -> str:
    try:
        result = subprocess.run(
            ["git"] + cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise GitCommandFailed(e.stderr.strip())


def check_git_safe(cwd: str) -> None:
    """
    Enforce:
    - not in rebase / merge
    - no conflicts
    - not detached HEAD
    """
    status = _run_git(["status", "--porcelain"], cwd)

    # Conflicts
    if any(line.startswith("UU") for line in status.splitlines()):
        raise UnsafeGitState("Git has unresolved conflicts")

    # Rebase / merge detection
    if _run_git(["rev-parse", "--git-path", "rebase-apply"], cwd):
        raise UnsafeGitState("Rebase in progress")

    # Detached HEAD
    branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)
    if branch == "HEAD":
        raise UnsafeGitState("Detached HEAD state")
