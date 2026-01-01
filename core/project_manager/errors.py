class ProjectManagerError(Exception):
    pass


class ProjectAlreadyExists(ProjectManagerError):
    pass


class ProjectNotFound(ProjectManagerError):
    pass


class ActiveProjectExists(ProjectManagerError):
    pass
