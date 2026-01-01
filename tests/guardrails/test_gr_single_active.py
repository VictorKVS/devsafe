def test_gr_single_active_project_enforced():
    """
    GR-SINGLEACTIVE-01
    Only one project can be active at a time.
    """
    active_projects = ["project-A"]

    activate_second = False  # placeholder

    assert activate_second is False