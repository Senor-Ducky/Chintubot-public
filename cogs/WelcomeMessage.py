import discord
from discord.ext import commands
from utilities import GUILD_DATA, permission_check, system_embed
from typing import Union

from database import guild


class WelcomeMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = member.guild.get_channel(
            GUILD_DATA[member.guild.id].get("welcome_channel")
        )
        welcome_message = GUILD_DATA[member.guild.id].get("welcome_message")
        if not welcome_message or not welcome_channel:
            return
        welcome_message = welcome_message.replace("{user}", member.mention).replace(
            "{server}", f"**{member.guild.name}**"
        )
        roles = GUILD_DATA[member.guild.id].get("welcome_roles")
        if roles is not None:
            for role in roles:
                role = member.guild.get_role(role)
                await member.add_roles(role)
        try:
            await welcome_channel.send(welcome_message)
        except discord.Forbidden:
            pass
        if GUILD_DATA[member.guild.id].get("dm") is True:
            try:
                await member.send(welcome_message)
            except discord.Forbidden:
                pass

    @commands.check(permission_check)
    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx: commands.Context):
        welcome_channel = ctx.guild.get_channel(
            GUILD_DATA[ctx.guild.id].get("welcome_channel")
        )
        welcome_message = GUILD_DATA[ctx.guild.id].get("welcome_message")
        if not welcome_message or not welcome_channel:
            await ctx.send(
                embed=system_embed(
                    ctx.author,
                    f"Welcome messages has not been setup!\nType ``{ctx.prefix}help welcome`` for more info",
                )
            )
            return
        embed = discord.Embed(title="Welcome Settings")
        embed.add_field(
            name="Welcome_Channel", value=str(welcome_channel.mention), inline=False
        )
        embed.add_field(name="Message", value=welcome_message)
        await ctx.send(embed=embed)

    @commands.check(permission_check)
    @welcome.command()
    async def channel(self, ctx: commands.Context, channel: Union[discord.TextChannel]):
        past_channel = ctx.guild.get_channel(
            GUILD_DATA[ctx.guild.id].get("welcome_channel")
        )
        await guild.set_variable(ctx.guild.id, "welcome_channel", channel.id)
        await ctx.send(
            embed=system_embed(
                ctx.author, f"Channel changed from {past_channel} to {channel.mention}"
            )
        )

    @commands.check(permission_check)
    @welcome.command()
    async def message(self, ctx: commands.Context, *, message: str):
        await guild.set_variable(ctx.guild.id, "welcome_message", message)
        await ctx.send(embed=system_embed(ctx.author, f"Welcome message set!"))

    @commands.check(permission_check)
    @welcome.command()
    async def disable(self, ctx: commands.Context, dm: str = ""):
        if dm.lower() == "dm":
            message = f"""Welcome DMs has been disabled.
            To enable them back use command ``{ctx.prefix}welcome dm``"""
            await guild.unset_variable(ctx.guild.id, "dm")
            await ctx.send(embed=system_embed(ctx.author, message))
        else:
            message = f"""Welcome Messages has been disabled.
            To enable them back use command ``{ctx.prefix}welcome channel #channel``"""
            await guild.unset_variable(ctx.guild.id, "welcome_channel")
            await ctx.send(
                embed=system_embed(
                    ctx.author,
                    message,
                )
            )

    @commands.check(permission_check)
    @welcome.command()
    async def dm(self, ctx: commands.Context):
        await guild.set_variable(ctx.guild.id, "dm", True)
        await ctx.send(embed=system_embed(ctx.author, "DMs have been enabled!"))

    @commands.check(permission_check)
    @commands.group(invoke_without_command=True)
    async def welcome_roles(self, ctx: commands.Context):
        roles = GUILD_DATA[ctx.guild.id].get("welcome_roles")
        print(roles)
        if not roles:
            message = f"""No roles set
            To set welcome roles use the command ``{ctx.prefix}welcome_roles add @role``"""
        else:
            message = ""
            for role in roles:
                role = ctx.guild.get_role(role)
                message += f"{role.mention}\n"
        await ctx.send(embed=system_embed(ctx.author, message, "Welcome Roles"))

    @commands.check(permission_check)
    @welcome_roles.command()
    async def add(self, ctx: commands.Context, role: discord.Role):
        if not await guild.welcome_role(ctx.guild.id, role.id):
            message = f"{role.mention} is already added"
            await ctx.send(embed=system_embed(ctx.author, message))
        else:
            message = f"{role.mention} is has been added"
            await ctx.send(embed=system_embed(ctx.author, message))

    @commands.check(permission_check)
    @welcome_roles.command()
    async def remove(self, ctx: commands.Context, role: discord.Role):
        if not await guild.welcome_role(ctx.guild.id, role.id, "remove"):
            message = f"{role.mention} is not on the list"
            await ctx.send(embed=system_embed(ctx.author, message))
        else:
            message = f"{role.mention} is has been removed"
            await ctx.send(embed=system_embed(ctx.author, message))


def setup(bot):
    bot.add_cog(WelcomeMessage(bot))
