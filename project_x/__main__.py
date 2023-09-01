import discord
from discord.ext import commands
from configparser import ConfigParser

from .config import ConfigPath
from .token import TOKEN


class ProjectX(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = "!", intents = discord.Intents.all())
        
        self.config = ConfigParser()
        self.config.read(ConfigPath.ALLCONFIG.value)


    async def on_ready(self) -> None:
        pass


    def running(self) -> None:
        self.run(TOKEN)


ProjectX().running()