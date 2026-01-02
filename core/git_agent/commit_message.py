from core.commit_scheduler.models import CommitIntent


def build_commit_message(intent: CommitIntent) -> str:
    files = {e.path.name for e in intent.events}

    header = f"chore(devsafe): auto-commit ({len(files)} files changed)"
    body = [
        "",
        f"Reason: {intent.reason}",
        "Actor: DevSafe Git Agent",
    ]

    return "\n".join([header] + body)
