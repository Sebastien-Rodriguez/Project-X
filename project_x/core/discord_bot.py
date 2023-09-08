import discord
from discord.ext import commands


class DiscordBot(commands.Bot):
    def __init__(self, command_prefix: str, token: str) -> None:
        super().__init__(command_prefix=command_prefix, intents=discord.Intents.all())
        self.token = token


    async def setup_hook(self) -> None:
        await self.tree.sync()


    async def on_ready(self) -> None:
        print("Bot is ready !")


    async def start_bot(self) -> None:
        await self.start(self.token)
