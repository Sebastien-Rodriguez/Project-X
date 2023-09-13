"""
This is a module containing an asynchronous logging system. 
No dependency is necessary apart from the configuration .ini, 
the configuration instance is defined in the package. 
This logging system is based on files.
"""

import asyncio
from datetime import datetime
from typing import Optional, Any, Union
from enum import Enum

from .utils import CONFIG
from .abstract import AbstractLogging
from .exceptions import IsAlreadyRunning, IsNotRunning

import aiofiles


class LoggingLevel(Enum):
    DEBUG = "debug"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"


class LoggingSource(Enum):
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
        MAX_PENDING = CONFIG.getint("MANAGE_FILE", "MAX_PENDING")
    
        self.running = asyncio.Event()
        self.queue: asyncio.Queue[str] = asyncio.Queue(MAX_PENDING)
        self.file: aiofiles.threadpool.text.AsyncTextIOWrapper
        self.file_create_at: int


    async def start(self) -> None:
        """Start the logging file system.

        Raises:
            - < IsAlreadyRunning > Raised if the logging system
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
            - < IsNotRunning > Raised if The logging system
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
                      error: Optional[Any] = None, 
                      speed: Optional[int] = None, 
                      other: Optional[dict[str, Any]] = None
                      ) -> None:
        
        """Add a new pending message to write to the file.

        Args:
            message (str): Message needs to be added.
        
        Notes:
            - The message must be valid for JSON format. 
            No verification is done by the system,
            you must ensure that the message is correctly formatted
            otherwise it can introduce bugs.

        - "timestamp" (str): Current timestamp in string format.
        - "level" (str): Log level: "info" for general information, "warn" for warning error,
            "critical" for critical error, "success" for success actions.
        - "source_system" (str) Indicates the source system or person responsible for adding the log entry.
        - "error" (str): Any encountered error (if applicable).
        - "message" (str): Additional information.
        - "speed" (str): Execution speed.
        - "data" (dict): Other data in the form of a dictionary object.

        """

        if not isinstance(level, LoggingLevel):
            raise ...
        
        elif not isinstance(source, LoggingSource):
            raise ...
        
        timestamp = datetime.now()

        await self.queue.put("")


    async def format_log(self, message: Any) -> str:
        """_summary_

        Args:
            message (str): _description_

        Returns:
            str: _description_
        """

        return ""
    

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
            await asyncio.sleep(2)