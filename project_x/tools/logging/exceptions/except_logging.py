"""All exceptions related to the logging system.
"""


class IsAlreadyRunning(Exception):
    """Exception thrown when the logging system is already running.
    """
    def __str__(self) -> str:
        return """The logging system has already been started.
        You cannot start the logging system twice."""


class IsNotRunning(Exception):
    """Exception thrown when the logging system is not running.
    """
    def __str__(self) -> str:
        return "The logging system has not been started. So you can't stop it."


class AddLogError(Exception):
    """Exception thrown when adding a log went wrong.
    """
