class BackupError(Exception):
    pass


class BackupPathInvalid(BackupError):
    pass


class BackupFailed(BackupError):
    pass
