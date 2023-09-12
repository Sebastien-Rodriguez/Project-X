import os
import asyncio

from .core import DiscordBot
from .exceptions import InvalidToken
from .tools import LoggingFile, ManageLoggingFile


LOOP = asyncio.new_event_loop()

manage_loggingfile = ManageLoggingFile()
logging_file = LoggingFile(manage_file=manage_loggingfile)

token = "" #os.environ.get("TOKEN")


async def main() -> None:
    await manage_loggingfile.start()

    if token is None:
        await logging_file.add_log("The token is missing or incorrect in the environment variables.")
        raise InvalidToken
    else:
        discord_bot = DiscordBot(command_prefix="!", token=token)
        await discord_bot.start_bot()


LOOP.create_task(main())
LOOP.run_forever()