# core/runtime/orchestrator.py

class DevSafeRuntime:
    def __init__(self, project_manager, state_machine):
        self.pm = project_manager
        self.sm = state_machine

    def require_active(self):
        self.sm.require_active()

    def start_automation(self):
        self.sm.start()

    def stop_automation(self):
        self.sm.stop()

    def fail_safe(self, reason: str):
        self.sm.pause(reason)

    def select_project(self, name: str):
        self.pm.activate(name)

    def get_active_project(self):
        return self.pm.get_active()
