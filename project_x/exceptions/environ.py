class InvalidToken(Exception):
    def __str__(self) -> str:
        return "The token is missing or incorrect in the environment variables."