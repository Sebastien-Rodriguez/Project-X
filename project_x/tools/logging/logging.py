"""
This is a module containing an asynchronous logging system. 
No dependency is necessary apart from the configuration .ini, 
the configuration instance is defined in the package. 
This logging system is based on files.
"""

import asyncio
from datetime import datetime
from typing import Optional, Any
from enum import Enum
import json

import aiofiles

from .utils import CONFIG
from .abstract import AbstractLogging
from .exceptions import IsAlreadyRunning, IsNotRunning, AddLogError


class LoggingLevel(Enum):
    """Enum class logging levels.

    Members:     
        - INFO: To record general information about the application, 
            such as actions taken, progress steps, and important events.

        - WARNING: To record warnings about potentially problematic 
            situations, such as an unhandled exception or any 
            behavior that is not managed but does not threaten
            the proper functioning of the application.

        - CRITICAL: To record critical errors that can lead to significant 
            malfunctions of the application.

        - SUCCESS: To record successful events or actions.
    """

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"


class LoggingSource(Enum):
    """Enum class source categories for logging.

    Members:
        - DATABASE: For database-related logs.
        - DOGGING: For dogging-related logs.
        - WEBSITE: For website-related logs.
        - ACCOUNT: For account-related logs.
        - COMPRETEUR: For compreteur-related logs.
        - MODERATION: For moderation-related logs.
        - PROMOTE: For promote-related logs.
        - SUPPORT: For support-related logs.
        - VOICE: For voice-related logs.
        - CORE: For core system-related logs.
    """
    DATABASE = "database"
    DOGGING = "dogging"
    WEBSITE = "website"
    ACCOUNT = "account"
    COMPRETEUR = "compreteur"
    MODERATION = "moderation"
    PROMOTE = "promote"
    SUPPORT = "support"
    VOICE = "voice"
    CORE = "core"


class Logging(AbstractLogging):
    """Asynchronous and singleton logging system,
       supporting only JSON file type.
       The logging system remains running once launched
       for the duration of the application.

    Notes:
        - The file is closed then reopened every X time 
        in order to change the file.

        - Start method to start the system, 
        and stop method to stop the system.
    """

    _instance: Optional["Logging"] = None


    def __new__(cls) -> "Logging":
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self) -> None:
        MAX_PENDING = CONFIG.getint("LOGGING", "MAX_PENDING")

        self.running = asyncio.Event()
        self.queue: asyncio.Queue[str] = asyncio.Queue(MAX_PENDING)
        self.file: aiofiles.threadpool.text.AsyncTextIOWrapper
        self.file_create_at: int


    async def start(self) -> None:
        """Start the logging file system.

        Raises:
            - IsAlreadyRunning: Raised if the logging system
              has already been started.
        """

        if self.running.is_set():
            raise IsAlreadyRunning

        await self.create_file()

        asyncio.create_task(self._infinity_loop_write())
        self.running.set()


    async def stop(self) -> None:
        """Wait until all messages waiting,
          to be written are written then stop the logging file system.

        Raises:
            - IsNotRunning: Raised if The logging system
              has not been started. 
        """

        if not self.running.is_set():
            raise IsNotRunning

        await self.queue.join()
        self.running.clear()
        await self.file.close()


    async def add_log(self,
                      source: LoggingSource,
                      level: LoggingLevel,
                      note: str,
                      error: Optional[str] = None,
                      speed: Optional[bool] = None,
                      other: Optional[dict[str, Any]] = None,
                      ) -> None:

        """Add a log to the queue.

        Notes:
            - If a lot of logs are in the queue, 
            the log may not be immediately processed.

        Raises:
            AddLogError: Raised if an 
            argument type is invalid.

        Args:
            - source: Information defining approximately 
            where the logo comes from (From which service).

            - level: Information defining the log level. 
            (CRITICAL, SUCCESS etc)

            - note: A small description of some character 
            about the reason for the log.

            - error: Argument indicating the exception 
            generated if there is one.

            - speed: Argument indicating how quickly 
            something executes. (To be used as often as possible).

            - other: Argument to use for data that is not 
            categorized by the other arguments.
        """

        arguments = (source, level, note, error, speed, other)

        match arguments:
            case (LoggingSource(), LoggingLevel(), str(),
                  str() | None, bool() | None, dict() | None):

                log_formated = Logging.format_log(
                    source.value, level.value, note, error, speed, other)

            case invalid:
                raise AddLogError(
                    f"{invalid} An invalid argument type was detected.")

        await self.queue.put(log_formated)


    @staticmethod
    def format_log(source: Any = None, level: Any = None,
                   note: Any = None, error: Any = None,
                   speed: Any = None, other: Any = None
                   ) -> str:
        """Format the log in an X format 
        then serialize it in a valid JSON format.

        Returns:
            - Return the log format if the serialization
              in JSON format was successful.
        Raises:
            - TypeError: Raised If log 
            serialization fail.
        Notes:
            - If log serialization fail, it is because 
            of a type not supported by JSON.
        """

        log_formated = {
            "timestamp": str(datetime.now()),
            "source": source,
            "level": level,
            "note": note,
            "error": error,
            "speed": speed,
            "other": other
        }

        return json.dumps(log_formated)


    async def create_file(self) -> None:
        """Create a new log file with the current date, 
        and the full path of the folder where the file was saved.

        Notes:
            - The re method assigns the self.file attribute
            with a file object in write mode.

            - A JSON file extension is automatically assigned.
        """

        PATH = CONFIG.get("MANAGE_FILE", "PATH")
        filename = datetime.now()

        self.file = await aiofiles.open(f"{PATH}{filename}.json", "w")
        self.file_create_at = int(datetime.now().timestamp())


    async def rotate_file(self) -> None:
        """Rotates the log file by closing and creating a new file.
        """
        await self.file.close()
        await self.create_file()


    async def _infinity_loop_write(self) -> None:
        """The main system is located here. 
        Recovery of pending logs then flush every X time the logs in the file.

        Notes:
            - Manages the launch of log file rotation. 
            When the maximum time for each log file has expired, 
            a rotation is performed.

            - If no message is pending, the get method simply waits, 
            blocking the loop until a message is pending again.
        """

        TIME_ROTATE = CONFIG.getint("MANAGE_FILE", "TIME_ROTATE")
        MIN_FLUSH = CONFIG.getint("MANAGE_FILE", "MIN_FLUSH")

        counter_logs = 0

        while await self.running.wait():
            counter_logs += 1

            if int(datetime.now().timestamp()) - self.file_create_at > TIME_ROTATE:
                await self.rotate_file()

            elif counter_logs >= MIN_FLUSH:
                await self.file.flush()

            await self.file.write(await self.queue.get() + "\n")
            self.queue.task_done()
            await asyncio.sleep(0)
