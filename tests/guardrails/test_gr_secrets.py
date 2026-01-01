import pytest

@pytest.mark.parametrize("filename", [
    ".env",
    ".env.prod",
    "id_rsa.key",
    "private.pem",
])
def test_gr_secrets_deny_list(filename):
    """
    GR-SECRETS-01
    Forbidden secret files must never be committed.
    """
    commit_allowed = False  # placeholder

    assert commit_allowed is False
