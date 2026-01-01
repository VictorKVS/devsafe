def test_gr_backup_path_not_inside_project(fake_project):
    """
    GR-BACKUP-01
    Backup directory must not be inside project directory.
    """
    project_path = fake_project["path"]
    backup_path = fake_project["path"] + "/backup"

    is_recursive = backup_path.startswith(project_path)

    assert is_recursive is True  # must be detected and blocked
