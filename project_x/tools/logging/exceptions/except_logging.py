class IsAlreadyRunning(Exception):
    def __str__(self) -> str:
        return "The logging system has already been started. You cannot start the logging system twice."
    

class IsNotRunning(Exception):
    def __str__(self) -> str:
        return "The logging system has not been started. So you can't stop it."