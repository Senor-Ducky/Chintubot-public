import discord
from discord.ext import commands
from database import guild
from utilities import system_embed, permission_check, GUILD_DATA
from typing import Union


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    async def cog_check(self, ctx):
        commands.has_permissions()
        return permission_check(ctx)

    @commands.command()
    async def prefix(self, ctx: commands.Context, new_prefix: str = None):
        if new_prefix is None:
            await ctx.send(
                embed=system_embed(
                    ctx.author,
                    f"The current prefix is `{GUILD_DATA[ctx.guild.id]['prefix']}`",
                )
            )
            return
        await guild.set_variable(ctx.guild.id, "prefix", new_prefix)
        await ctx.send(
            embed=system_embed(
                ctx.author,
                f"Prefix changed from `{GUILD_DATA[ctx.guild.id]['prefix']}` to `{new_prefix}`",
            )
        )

    @commands.group(invoke_without_command=True)
    async def moderators(self, ctx: commands.Context):

        no = f"No moderators found you can add moderators by ``{GUILD_DATA[ctx.guild.id]['prefix']}" \
             f"moderators add user/role``"

        mods = GUILD_DATA[ctx.guild.id].get("moderation_permissions")
        print(mods)
        if mods is None:
            await ctx.send(
                embed=system_embed(
                    ctx.author,
                    no,
                )
            )
            return
        out = ""
        for mod in mods:
            role = ctx.guild.get_role(mod)
            user = ctx.guild.get_member(mod)
            if role and user is None:
                # await guild.moderation()
                continue
            out += f"{role.mention if role is not None else user.mention}\n"

        await ctx.send(
            embed=system_embed(ctx.author, out if out != "" else no, "Moderators")
        )

    @commands.has_permissions(administrator=True)
    @moderators.command()
    async def add(
        self, ctx: commands.Context, mod: Union[discord.Member, discord.Role]
    ):
        if await guild.moderation(ctx.guild.id, mod.id) is False:
            await ctx.send(
                embed=system_embed(
                    ctx.author, f"{mod.mention} is already part of moderators"
                )
            )
        else:
            await ctx.send(
                embed=system_embed(ctx.author, f"{mod.mention} is added to moderators")
            )

    @commands.has_permissions(administrator=True)
    @moderators.command()
    async def remove(
        self, ctx: commands.Context, mod: Union[discord.Member, discord.Role]
    ):
        if await guild.moderation(ctx.guild.id, mod.id, "remove") is False:
            await ctx.send(
                embed=system_embed(ctx.author, f"{mod.mention} not  part of moderators")
            )
        else:
            await ctx.send(
                embed=system_embed(
                    ctx.author, f"{mod.mention} is removed from moderators"
                )
            )


def setup(bot):
    bot.add_cog(Settings(bot))
