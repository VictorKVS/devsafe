class GitAgentError(Exception):
    pass


class UnsafeGitState(GitAgentError):
    pass


class GitCommandFailed(GitAgentError):
    pass
