import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

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


@bot.command()
async def mute(ctx, member: discord.Member, *reason):
    print(reason)
    Muted = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(Muted)
    embed = discord.Embed(
        description=str(
            str(member) + " is Muted | reason = " + " ".join(reason)),
        colour=discord.Colour.red()
    )
    await ctx.send(embed=embed)


@ bot.command()
async def unmute(ctx, member: discord.Member, *reason):
    print(reason)
    Muted = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(Muted)
    embed = discord.Embed(
        description=str(
            str(member) + " is Unmuted | reason = " + " ".join(reason)),
        colour=discord.Colour.green()
    )
    await ctx.send(embed=embed)



bot.run(os.getenv("TOKEN"))