import redditapi
import discord
import io
import asyncio
from discord.ext import commands

class Meme(commands.Cog):
    def __init__(self , commands) :
        self.commands = commands
    @commands.command()
    async def csmeme(self , ctx):
        title , url = redditapi.memes('ProgrammerHumor')
        print(title , url)
        em = discord.Embed(title = title, color = discord.Colour.red())
        em.set_image(url = url)
        await ctx.send(embed= em)

def setup(bot):
    bot.add_cog(Meme(bot))