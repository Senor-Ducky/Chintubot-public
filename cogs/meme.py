import redditapi
import discord
import io
import asyncio
from discord.ext import commands

class Meme(commands.cog):
    def  __init__(self, commands):
        self.commands = commands

    @commands.command()
    async def csmeme(self, ctx):
        title,image = redditapi.memes("ProgrammerHumor")
        embed = discord.Embed(title = title)
        embed.set_image(url=image)
        await ctx.send(embed = embed) 

    @client.command()
    async def ping(self , ctx):
        before = time.monotonic()
        before_ws = int(round(bot.latency * 1000, 1))
        message = await ctx.send(":ping_pong: Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f":ping_pong: WS: {before_ws}ms  |  REST: {int(ping)}ms")

def setup(bot):
    bot.add_cog(Meme(bot))