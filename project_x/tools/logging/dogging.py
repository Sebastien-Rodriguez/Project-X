from discord.ext import commands

from .abstract import AbstractLogging


class Dogging(AbstractLogging):
    def __init__(self, bot: commands.Bot, channel_id: int) -> None:
        self.bot = bot
        self.channel = channel_id
    

    async def add_log(self, message: str) -> None:
        ...


    def format_log(self, message: str) -> str:
        return ""
    