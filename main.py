import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def warn(ctx, member, *reason):
    print(reason)
    embed = discord.Embed(
        description=str(member + " is warned | Reason = " + " ".join(reason)),
        colour=discord.Colour.blue()
    )
    await ctx.send(embed=embed)

bot.run('NzkwOTAwOTUwODg1MjAzOTc4.X-HV6A.VBQd4nfGOFXSkYdDvmBBGXn-aiw')

@bot.command()
async def ban(ctx, member, *reason):
    print (reason)
    embed = discord.Embed(
        description = str(member + " is banned | reason = " + " ".join(reason)),
        colour=discord.Colour.green()
    )
    await member.ban(reason=" ".join(reason))
    await ctx.send(embed=embed)
