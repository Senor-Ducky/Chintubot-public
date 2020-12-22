from pathlib import Path

import aiohttp
import discord
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands

from database import guild
from utilities import settings, GUILD_DATA, system_embed

intents = discord.Intents.all()


async def fetch_prefix(_bot, message):
    prefix = settings.prefix
    if not isinstance(message.channel, discord.DMChannel):
        await guild.query_guild(message.guild.id)
        prefix = GUILD_DATA[message.guild.id]["prefix"]
    return commands.when_mentioned_or(prefix)(_bot, message)


bot = commands.AutoShardedBot(
    command_prefix=fetch_prefix, help_command=None, intents=intents
)


@bot.event
async def on_ready():
    print("Ready")
    guilds = bot.guilds
    members = [member for member in bot.get_all_members()]
    await bot.change_presence(
        activity=discord.Game(
            name=f"Serving {len(members)} people in {len(guilds)} servers"
        )
    )
    bot.session = aiohttp.ClientSession()


def extensions():
    files = Path("cogs").rglob("*.py")
    for file in files:
        yield file.as_posix()[:-3].replace("/", ".")


for extension in extensions():
    try:
        bot.load_extension(extension)
        print(f"Loading {extension}")
    except Exception as ex:
        print(f"Failed to load {extension}; {ex}")


async def command_log(ctx: commands.Context):
    log_channel = GUILD_DATA[ctx.guild.id].get("log_channel")
    if log_channel is None:
        return
    webhook = Webhook.from_url(log_channel, adapter=AsyncWebhookAdapter(bot.session))
    try:
        await webhook.send(
            embed=system_embed(
                ctx.author,
                f"`{ctx.command}` used by {ctx.author.mention} in "
                f"{ctx.channel.mention}",
            ),
            username="Epsilon",
        )
    except discord.NotFound:
        await guild.unset_variable(ctx.guild.id, "log_channel")


bot.after_invoke(command_log)

bot.run(settings.token)
