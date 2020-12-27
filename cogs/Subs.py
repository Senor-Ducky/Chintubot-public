"""Add Youtube API key in .env file with YT_API_KEY"""
import asyncio
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

load_dotenv()


def get_data(Channel_id):
    api_key = os.getenv("YT_API_KEY")
    data = requests.get(
        f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={Channel_id}&key={api_key}").json()
    subs = int(data["items"][0]["statistics"]["subscriberCount"])
    return subs


class Subscribers(commands.Cog):
    def __init__(self, commands: commands.Bot):
        self.bot = commands

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def CreateLiveSubs(self, ctx, name, yt_id: str = "UCJKYubtV1bfbhS-SxTm9Z1A", sleep=10):
        if ctx.author.guild_permissions.manage_channels is True:
            channel = await ctx.guild.create_voice_channel(name)
            await channel.set_permissions(ctx.guild.default_role, connect=False)
            self.bot.loop.create_task(self.sub_loop(channel, name, yt_id, int(sleep)))

    async def sub_loop(self, channel, name, yt_id, sleep):
        while True:
            await channel.edit(name=f"{name}: {get_data(yt_id)}")
            await asyncio.sleep(sleep)


def setup(bot):
    bot.add_cog(Subscribers(bot))
