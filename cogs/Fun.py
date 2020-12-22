import discord
from discord.ext import commands
from utilities import system_embed


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")



def setup(bot):
    bot.add_cog(Fun(bot))
