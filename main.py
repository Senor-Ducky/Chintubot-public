import discord
import os
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
# import praw

load_dotenv()

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.CheckFailure):
    embed = discord.Embed(title = ':x: oops! You do not have permission to use this command.', color = discord.Colour.red())
    await ctx.send(embed = embed)
  elif isinstance(error,commands.MissingRequiredArgument):
    embed = discord.Embed(title = ':x:You are missing the required arguements. Please check if your command requires an addition arguement.', color = discord.Colour.red())
    await ctx.send(embed = embed)
  elif isinstance(error, commands.CommandNotFound):
    pass

for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:3]}')



# @bot.command()
# @commands.has_permissions(kick_members=True)
# async def warn(ctx, member:  discord.Member, *, reason = 'No reason Provided'):
#     with open('warnings.json','r') as f:
#         warns = json.load(f)
#     if str(ctx.guild.id) not in warns:
#         warns[str(ctx.guild.id)] = {}
#     if str(member.id) not in warns[str(ctx.guild.id)]:
#         warns[str(ctx.guild.id)][str(member.id)] = {}
#         warns[str(ctx.guild.id)][str(member.id)]["warns"] = 1
#         warns[str(ctx.guild.id)][str(member.id)]["warnings"] = [reason]
#     else:
#         warns[str(ctx.guild.id)][str(member.id)]["warnings"].append(reason)
#     with open('warnings.json','w') as f:
#         json.dump(warns , f)
#         #await ctx.send(f"{member.mention} was warned for: {reason}")
        
#         embed = discord.Embed(title='You have been warned ', description=f'You received a warning from {member}')
#         embed.add_field(name='Reason:', value=f'{reason}')
#         await member.send(embed=embed)
    #print(reason)
    #embed = discord.Embed(
    #    description=str(member + " is warned | Reason = " + reason),
    #    colour=discord.Colour.blue()
    #)
    #await send_messeage_to_general(ctx, embed)
@bot.command()
async def warns(ctx , member : discord.Member ):
    with open('warnings.json', 'r') as f:
        warns = json.load(f)
    num = 1
    warnings = discord.Embed(title = f'{member}\'s warns ')
    for warn in warns[str(ctx.guild.id)][str(member.id)]["warnings"]:
        warnings.add_field(name = f"Warn {num}" , value = warn)
        num += 1
    await ctx.send(embed = warnings)

@bot.command()
@commands.has_permissions(manage_guild=True)
async def removewarn(ctx, member: discord.Member, num: int, *, reason='No reason provided.'):
    with open('warnings.json' , 'r') as f:
        warns = json.load(f)
    num -= 1
    warns[str(ctx.guild.id)][str(member.id)]["warns"] -= 1
    warns[str(ctx.guild.id)][str(member.id)]["warnings"].pop(num)
    with open('warnings.json' , 'w') as f:
        json.dump(warns , f)
        await ctx.send('Warn has been removed!')
        embed = discord.Embed(title='Your warn has been removed', description=f'Your warning was removed by {ctx.author}')
        await member.send(embed=embed)
        

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason):
    print(reason)
    embed = discord.Embed(
        description=str(
            str(member) + " is Kicked | reason = " + reason),
        colour=discord.Colour.green()
    )
    await member.kick(reason=reason)
    await member.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason):
    print(reason)
    embed = discord.Embed(
        description=str(
            str(member) + " is banned | reason = " + reason),
        colour=discord.Colour.green()
    )
    await member.ban(reason=reason)
    await member.send(embed=embed)


@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason):
    print(reason)
    Muted = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(Muted)
    embed = discord.Embed(
        description=str(
            str(member) + " is Muted | reason = " + reason),
        colour=discord.Colour.red()
    )
    await member.send(embed=embed)


@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member, *, reason = "No reason specified"):
    print(reason)
    Muted = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(Muted)
    embed = discord.Embed(
        description=str(
            str(member) + " is Unmuted | reason = " + reason),
        colour=discord.Colour.green()
    )
    await member.send(embed=embed)



bot.run(os.getenv("TOKEN"))