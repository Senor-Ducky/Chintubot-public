import discord
from discord.ext import commands
from googlesearch import search


class Google(commands.Cog):
    def __init__(self, commands):
        self.commands = commands

    @commands.command()
    async def gsearch(self, ctx):
        message = str(ctx.message.content).split()
        try:
            number_of_results = int(message[-1])
            search_string = " ".join(message[1:-1])
        except ValueError:
            number_of_results = 2
            search_string = " ".join(message[1:])
        print(search_string)
        embed = discord.Embed(title=search_string, color=discord.Color.blue())
        i = 0
        for result in search(search_string, tld='com', lang='en', start=0, stop=number_of_results):
            embed.add_field(name="Result {}".format(i + 1), value=result, inline=False)
            i += 1

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Google(bot))
