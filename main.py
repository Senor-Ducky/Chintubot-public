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
    await member.ban(reason="BC")
    await ctx.send(embed=embed)


@bot.command()
async def kick(ctx, member: discord.Member, *reason):
    print(reason)
    embed = discord.Embed(
        description=str(
            str(member) + " is Kicked | reason = " + " ".join(reason)),
        colour=discord.Colour.green()
    )
    await member.kick(reason=" ".join(reason))
    await ctx.send(embed=embed)


@bot.command()
async def ban(ctx, member: discord.Member, *reason):
    print(reason)
    embed = discord.Embed(
        description=str(
            str(member) + " is banned | reason = " + " ".join(reason)),
        colour=discord.Colour.green()
    )
    await member.ban(reason=" ".join(reason))
    await ctx.send(embed=embed)

bot.run('NzkwOTAwOTUwODg1MjAzOTc4.X-HV6A.VBQd4nfGOFXSkYdDvmBBGXn-aiw')
