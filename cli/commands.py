"""
DevSafe CLI commands.

This module provides user-facing commands to control
DevSafe runtime, projects, and automation lifecycle.

CLI DOES NOT execute automation logic.
It only manipulates runtime state.
"""

from pathlib import Path

from core.app import build_runtime
from core.state_machine.states import AutomationState
from core.project_manager.errors import ProjectNotFoundError
from core.runtime.errors import RuntimeError as DevSafeRuntimeError


# -------------------------------------------------
# Runtime bootstrap (v0.1: in-memory, process-local)
# -------------------------------------------------

_runtime, _watcher, _queue = build_runtime()


# -------------------------------------------------
# Commands
# -------------------------------------------------

def cmd_init() -> None:
    """
    Initialize DevSafe runtime (noop in v0.1).
    """
    print("DevSafe initialized")


def cmd_project_add(args) -> None:
    """
    Register a new project.
    """
    try:
        _runtime.pm.register_project(
            name=args.name,
            path=Path(args.path),
            backup_path=Path(args.backup),
        )
        print(f"Project '{args.name}' registered")
    except Exception as e:
        print(f"ERROR: failed to register project: {e}")


def cmd_project_list() -> None:
    """
    List registered projects.
    """
    projects = _runtime.pm.list_projects()

    if not projects:
        print("No projects registered")
        return

    for project in projects.values():
        marker = "*" if project.active else " "
        print(f"{marker} {project.name}")
        print(f"    path:   {project.path}")
        print(f"    backup: {project.backup_path}")


def cmd_project_activate(args) -> None:
    """
    Activate a project.
    """
    try:
        _runtime.select_project(args.name)
        print(f"Project '{args.name}' activated")
    except ProjectNotFoundError:
        print(f"ERROR: project '{args.name}' not found")
    except Exception as e:
        print(f"ERROR: failed to activate project: {e}")


def cmd_start() -> None:
    """
    Start DevSafe automation.
    """
    try:
        _runtime.start_automation()
        print("Automation started")
    except DevSafeRuntimeError as e:
        print(f"ERROR: cannot start automation: {e}")


def cmd_stop() -> None:
    """
    Stop DevSafe automation.
    """
    try:
        _runtime.stop_automation()
        print("Automation stopped")
    except DevSafeRuntimeError as e:
        print(f"ERROR: cannot stop automation: {e}")


def cmd_status() -> None:
    """
    Show current runtime status.
    """
    state = _runtime.sm.state
    project = _runtime.get_active_project()

    print(f"State: {state.value}")

    if project:
        print(f"Active project: {project.name}")
        print(f"Path:   {project.path}")
        print(f"Backup: {project.backup_path}")
    else:
        print("No active project")

    if state == AutomationState.PAUSED:
        reason = _runtime.sm.last_error or "unknown"
        print(f"Paused reason: {reason}")
