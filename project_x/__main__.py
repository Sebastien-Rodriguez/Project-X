import os
import asyncio

from .core import DiscordBot
from .exceptions import InvalidToken
from .tools.logging import Logging, LoggingSource, LoggingLevel


LOOP = asyncio.new_event_loop()

logging = Logging()

token = "" #os.environ.get("TOKEN")


async def main() -> None:
    await logging.start()
    await logging.add_log(source = LoggingSource.ACCOUNT,
                          level = LoggingLevel.CRITICAL,
                          note = "test"
                          )
    return

    if token is None:
        await logging.add_log("The token is missing or incorrect in the environment variables.")
        raise InvalidToken
    else:
        discord_bot = DiscordBot(command_prefix="!", token=token)
        await discord_bot.start_bot()


LOOP.create_task(main())
LOOP.run_forever()