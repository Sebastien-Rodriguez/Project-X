"""
Module containing an interface 
for the different logging systems.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any


class AbstractLogging(ABC):
    """Abstract class for logging systems.
    """

    @abstractmethod
    async def add_log(self, source, level, note: str,
                      error: Optional[str] = None,
                      speed: Optional[bool] = None,
                      other: Optional[dict[str, Any]] = None
                      ) -> None:
        """Method representing the addition of a log.
        """

    @staticmethod
    @abstractmethod
    def format_log(source: Any = None, level: Any = None,
                   note: Any = None, error: Any = None,
                   speed: Any = None, other: Any = None
                   ) -> str:
        """Method representing the formatting of a log.
        """
