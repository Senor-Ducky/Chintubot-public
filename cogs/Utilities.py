import sys
from utilities import GUILD_DATA
from discord.ext import commands
import discord
import datetime


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")


def setup(bot):
    bot.add_cog(Utilities(bot))
