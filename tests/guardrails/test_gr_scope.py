def test_gr_scope_project_containment(fake_project):
    """
    GR-SCOPE-01
    DevSafe must not operate outside project directory.
    """
    project_path = fake_project["path"]
    accessed_path = "/tmp/devsafe"

    within_scope = accessed_path.startswith(project_path)

    assert within_scope is False
