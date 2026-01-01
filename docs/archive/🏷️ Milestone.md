🏷️ Milestone

Название: v0.2 — Functional MVP

Описание:

Functional MVP of DevSafe:
file watching, debounce logic, git automation,
local backup, and basic GUI integration.

Focus: correctness, stability, and reproducibility.

🧩 ISSUES (COPY–PASTE)
Issue 1

Title:

Implement Project Manager (persistent config & state)


Description:

Implement Project Manager responsible for:
- storing up to 5 projects
- persisting configuration between restarts
- ensuring exactly one active project
- activate / deactivate project logic

Config format: JSON
Config location: data/devsafe.json


Acceptance Criteria:

project list persists after restart

max 5 projects enforced

only one project can be active

Labels:
core, project-manager, v0.2

Issue 2

Title:

Add file watcher for active project


Description:

Implement filesystem watcher for the active project.

Watcher must:
- detect file modifications
- work recursively
- ignore system directories:
  .git, .venv, __pycache__, node_modules


Acceptance Criteria:

modifying a file triggers an event

ignored directories do not trigger events

Labels:
core, watcher, v0.2

Issue 3

Title:

Implement debounce logic for file change events


Description:

Aggregate multiple rapid file changes into a single action.

Debounce logic must:
- prevent commit storms
- be configurable (default 5–10 seconds)


Acceptance Criteria:

multiple saves create one commit

no excessive commits during rapid edits

Labels:
watcher, debounce, v0.2

Issue 4

Title:

Implement git auto-commit for active project


Description:

When file changes are detected:
- run git add
- create commit with timestamp message
- respect .gitignore


Acceptance Criteria:

commit created on file change

ignored files are not committed

Labels:
git, core, v0.2

Issue 5

Title:

Implement git auto-push to configured remote


Description:

After successful commit:
- push to configured GitHub remote and branch
- handle push failures gracefully
- local commits must succeed even if push fails


Acceptance Criteria:

commits are pushed when network is available

push failures are logged

application continues running

Labels:
git, network, v0.2

Issue 6

Title:

Implement local backup mirror for active project


Description:

Mirror project contents to local backup directory.

Backup must:
- exclude .git and runtime directories
- reflect file deletions
- work without internet


Acceptance Criteria:

backup matches project state

recovery possible via file copy

Labels:
backup, core, v0.2

Issue 7

Title:

Wire core logic into GUI


Description:

Connect GUI controls to core logic:
- project manager
- watcher start / stop
- status updates and basic logs

UI polish is not required.


Acceptance Criteria:

user can start/stop protection

active project is visible

errors are shown in status/log

Labels:
gui, integration, v0.2

Issue 8

Title:

Add logging and error handling


Description:

Implement basic logging for:
- git commits
- push failures
- backup operations
- watcher errors

Errors must not crash the application.


Acceptance Criteria:

errors are logged

application remains stable

last actions are visible to user

Labels:
logging, stability, v0.2