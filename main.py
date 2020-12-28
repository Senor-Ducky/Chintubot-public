import os
from itertools import cycle
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import requests
import json
# import praw

load_dotenv()

api_key = 'YOUR PERSPECTIVE API KEY HERE'
url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
    '?key=' + api_key)

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    change_status.start()


status = cycle(['WhiteHatJr SEO', ' with wolf gupta', 'with Lana Rhoades'])


def toxicity_checker():
    @bot.event
    async def on_message(message):
        data_dict = {
            'comment': {'text': message.content},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}
        }

        response = requests.post(url=url, data=json.dumps(data_dict)) 
        response_dict = json.loads(response.content)
        results = json.dumps(response_dict, indent=2)
        json_results = json.loads(results)
        toxicity = json_results['attributeScores']['TOXICITY']['summaryScore']['value']
        if toxicity > 0.95:
            await message.channel.purge(limit=1)
            await message.author.send(f'{message.author.mention} watch your language.')

        else:
            pass

        await bot.process_commands(message)



@tasks.loop(seconds=300)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title=':x: oops! You do not have permission to use this command.',
                              color=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title=':x:You are missing the required arguements. Please check if your command requires an addition arguement.',
            color=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        pass


for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')

#toxicity_checker()
bot.run(os.getenv("TOKEN"))
