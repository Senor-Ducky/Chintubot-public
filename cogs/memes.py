import redditapi
import discord
import io
import asyncio
from discord.ext import commands
from PIL import Image
from io import BytesIO

class Meme(commands.Cog):
    def __init__(self , commands) :
        self.commands = commands


    @commands.command()
    async def csmeme(self , ctx):
        title , url = redditapi.memes('ProgrammerHumor')
        em = discord.Embed(title = title, color = discord.Colour.red())
        em.set_image(url = url)
        await ctx.send(embed=em)

    @commands.command()
    async def coffin(self, ctx, member: discord.Member = None):

    	if member is None:
    		member = ctx.author

    	print('command received')
    	img = Image.open('coffin.jpg')
    	print('opened Image')

    	asset = member.avatar_url_as(size = 256)
    	print('asset resized')

    	data = BytesIO(await asset.read())
    	print('data done')

    	pfp = Image.open(data)
    	print('pfp opened')

    	pfp.resize((400, 400))
    	print('pfp resized')

    	img.paste(pfp, (1097, 71))
    	print('pasted')

    	img.save('ded.jpg')
    	print('saved edited img')

    	await ctx.send(file = discord.File('ded.jpg'))
    	print('senf')

def setup(bot):
    bot.add_cog(Meme(bot))