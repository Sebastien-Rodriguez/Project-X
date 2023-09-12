import os
import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union

from . import config_logging

from discord.ext import commands
import aiofiles


class AbstractLogging(ABC):
    """Abstract class for logging systems.
    """

    @abstractmethod
    async def add_log(self, *args, **kwargs) -> None:
        ...


    @abstractmethod
    async def _format_log(self, *args, **kwargs) -> str:
        ...


class ManageLoggingFile:
    """Singleton class that manages the file system. 
    Once the system starts a file is open for the lifetime of the application.
    
    Notes:
        - The file is closed then reopened every X time 
        in order to change the file.

        - This class should only be used with the Logging system.

        - The class only implements and supports JSON files.
    """

    _instance: Union["ManageLoggingFile", None] = None

    def __new__(cls, *args, **kwargs) -> "ManageLoggingFile":
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self) -> None:
        max_queue_size = config_logging.getint("MANAGE_FILE", "MAX_PENDING")

        self.running = asyncio.Event()
        self.queue: asyncio.Queue[str] = asyncio.Queue(max_queue_size)
        self.file: aiofiles.threadpool.text.AsyncTextIOWrapper


    def start(self) -> None:
        """Start the file system.
        """

        asyncio.create_task(self.rotate_file())
        asyncio.create_task(self.infinity_loop_write())
        self.running.set()


    async def stop(self) -> None:
        """Wait until all messages waiting,
          to be written are written then stop the file system.
        """

        await self.queue.join()
        self.running.clear()
        await self.file.close()


    async def rotate_file(self) -> None:
        """Close the old file 
        then create a new JSON file every X time infinitely.
        """

        # Use os path here ?
        PATH = config_logging.get("MANAGE_FILE", "PATH")
        TIME_ROTATE = config_logging.getint("MANAGE_FILE", "TIME_ROTATE")
        
        while await self.running.wait():
            filename = datetime.now()

            await self.file.close()
            self.file = await aiofiles.open(f"{PATH}{filename}.json", "w")
            await asyncio.sleep(TIME_ROTATE)


    async def write(self, message: str) -> None:
        """Add a new pending message to write to the file.

        Args:
            message (str): Message needs to be added.
        
        Notes:
            - The message must be valid for JSON format. 
            No verification is done by the system,
            you must ensure that the message is correctly formatted
            otherwise it can introduce bugs.
        """
        await self.queue.put(message)

    
    async def infinity_loop_write(self) -> None:
        """The main system is located here. 
        Recovery of pending messages then flush every X time the messages in the file.

        Notes:
            - If no message is pending, the get method simply waits, 
            blocking the loop until a message is pending again.
        """

        counter = 0

        while await self.running.wait():
            counter += 1

            if counter >= config_logging.getint("MANAGE_FILE", "MIN_FLUSH"):
                await self.file.flush()

            await self.file.write(await self.queue.get() + "\n")
            self.queue.task_done()
            await asyncio.sleep(0)


class LoggingFile(AbstractLogging):
    def __init__(self, manage_file: ManageLoggingFile) -> None:
        self.manage_file = manage_file


    async def add_log(self, message: str) -> None:
        ...


    async def _format_log(self, message: str) -> str:
        return ""


class LoggingDiscord(AbstractLogging):
    def __init__(self, bot: commands.Bot, channel_id: int) -> None:
        self.bot = bot
        self.channel = channel_id
    

    async def add_log(self, message: str) -> None:
        ...


    async def _format_log(self, message: str) -> str:
        return ""
    

def protect_log() -> int:
    """
    Returns:
        - Return 0 if log is send in < Log File >.
        - Return 1 if log is send in < Log Channel >.
    """ 
    ...
    return 0