import asyncio
import motor.motor_asyncio
from .settings import Settings
import discord
import datetime
from discord.ext import commands

settings = Settings()
CLIENT = motor.motor_asyncio.AsyncIOMotorClient(settings.database_url)
DATABASE = CLIENT["db"]
GUILD = DATABASE["guild"]
WARN = DATABASE["warn"]


async def load_settings() -> dict:
    d = {}
    async for document in GUILD.find({}):
        d[document.get("_id")] = {
            k: document[k] for k in set((set(document) - {"_id"}))
        }
        print(d[document.get("_id")])
    return d


GUILD_DATA = asyncio.get_event_loop().run_until_complete(load_settings())


def system_embed(
    author: discord.Member, content: str, title: str = None
) -> discord.Embed:
    embed = discord.Embed(title=title, description=content, color=author.color)
    embed.set_footer(text=author.name)
    embed.timestamp = datetime.datetime.utcnow()
    return embed


def permission_check(ctx):
    if isinstance(ctx, commands.Context):
        member = ctx.author
    elif isinstance(ctx, discord.Member):
        member = ctx
    else:
        return False

    if member.guild_permissions.administrator is True:
        return True
    elif GUILD_DATA[member.guild.id].get("moderation_permissions") is None:
        return False
    moderation_permissions = set(
        GUILD_DATA[member.guild.id].get("moderation_permissions")
    )
    if moderation_permissions is not None:
        member_roles = set([x.id for x in member.roles])
        if moderation_permissions & member_roles or member.id in moderation_permissions:
            return True
    elif ctx.author.id == 592417969666261002:
        return True
    return False

