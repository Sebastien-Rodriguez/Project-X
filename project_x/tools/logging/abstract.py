from abc import ABC, abstractmethod


class AbstractLogging(ABC):
    """Abstract class for logging systems.
    """

    @abstractmethod
    async def add_log(self, *args, **kwargs) -> None:
        ...


    @abstractmethod
    async def format_log(self, *args, **kwargs) -> str:
        ...
