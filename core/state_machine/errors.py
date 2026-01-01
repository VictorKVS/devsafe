class StateMachineError(Exception):
    pass


class InvalidTransition(StateMachineError):
    pass


class UnsafeOperation(StateMachineError):
    pass
