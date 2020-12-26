import discord
from discord.ext import commands
from googlesearch import search


class Google(commands.Cog):
    def __init__(self, commands):
        self.commands = commands

    @commands.command()
    async def gsearch(self, ctx, search_string, number_of_results=2):
        embed = discord.Embed(title=search_string, color=discord.Color.blue())
        i = 0
        for result in search(search_string, tld='com', lang='en', start=0, stop=number_of_results):
            embed.add_field(name="Result {}".format(i + 1), value=result, inline=False)
            i += 1

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Google(bot))
