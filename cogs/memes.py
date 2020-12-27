import discord
from discord.ext import commands
import redditapi


class Meme(commands.Cog):
    def __init__(self , commands) :
        self.commands = commands
    @commands.command()
    async def csmeme(self , ctx):
        title , url = redditapi.memes('ProgrammerHumor')
        em = discord.Embed(title = title, color = discord.Colour.red())
        em.set_image(url = url)
        await ctx.send('works!')

def setup(bot):
    bot.add_cog(Meme(bot))