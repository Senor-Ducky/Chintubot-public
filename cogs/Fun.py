import discord
from discord.ext import commands
from utilities import system_embed


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def say(self, ctx: commands.Context):
        message = f"""The help command is being worked!
        If you have any questions please feel free to dm my owner"""
        await ctx.send(embed=system_embed(ctx.author.role, message))


def setup(bot):
    bot.add_cog(Fun(bot))
