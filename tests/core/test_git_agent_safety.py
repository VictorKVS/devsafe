import pytest

from core.git_agent.errors import UnsafeGitState
from core.git_agent.git_checks import check_git_safe


def test_git_checks_fail_on_non_repo(tmp_path):
    with pytest.raises(Exception):
        check_git_safe(str(tmp_path))
