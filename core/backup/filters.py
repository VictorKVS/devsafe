from pathlib import Path


def should_exclude(path: Path) -> bool:
    """
    Files / directories NEVER included in backup.
    """
    return (
        ".git" in path.parts
        or path.name.endswith(".lock")
    )
