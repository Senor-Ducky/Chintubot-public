import discord
from discord.ext import commands
from utilities import permission_check, system_embed
from database import warns


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        commands.has_permissions()
        return permission_check(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command(aliases=["clear", "delete"])
    async def purge(
        self, ctx: commands.Context, amount: int, member: discord.Member = None
    ):
        """
        Delete messages
        """

        def check(msg):
            if member is None:
                return True
            elif msg.author.id == member.id:
                return True

        await ctx.channel.purge(limit=amount + 1, check=check)
        await ctx.send(
            embed=system_embed(
                ctx.author, f"{amount} messages deleted by {ctx.author.mention}"
            ),
            delete_after=5,
        )

    @commands.command()
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason specified",
    ):
        """
        Kick a member
        """
        check_mod = permission_check(member)
        if check_mod:
            await ctx.send(
                embed=system_embed(ctx.author, "You can not kick a moderator")
            )
            return

        try:
            await member.send(
                embed=system_embed(
                    member,
                    f"You have been kicked from **{ctx.guild.name}** "
                    f"by {ctx.author.mention}\n\n"
                    f"Reason: {reason}",
                )
            )
        except discord.Forbidden:
            pass

        await member.kick(reason=reason)
        await ctx.send(
            embed=system_embed(
                ctx.author,
                f"{member.mention} has been kicked by {ctx.author.mention}"
                f"\n\nReason: {reason}",
            )
        )

    @commands.command()
    async def ban(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason specified",
    ):
        """
        Ban a member
        """
        check_mod = permission_check(member)
        if check_mod:
            await ctx.send(
                embed=system_embed(ctx.author, "You can not ban a moderator")
            )
            return

        try:
            await member.send(
                embed=system_embed(
                    member,
                    f"You have been banned from **{ctx.guild.name}** "
                    f"by {ctx.author.mention}\n\n"
                    f"Reason: {reason}",
                )
            )
        except discord.Forbidden:
            pass

        await member.ban(reason=reason)
        await ctx.send(
            embed=system_embed(
                ctx.author,
                f"{member.mention} has been banned by {ctx.author.mention}"
                f"\n\nReason: {reason}",
            )
        )

    @commands.command()
    async def warn(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason specified",
    ):
        """
        Warn a member
        """
        check_mod = permission_check(member)
        if check_mod:
            await ctx.send(
                embed=system_embed(ctx.author, "You can not warn a moderator")
            )
            return

        try:
            await member.send(
                embed=system_embed(
                    member,
                    f"You have been warned in **{ctx.guild.name}** "
                    f"by {ctx.author.mention}\n\n"
                    f"Reason: {reason}",
                )
            )
        except discord.Forbidden:
            pass

        await warns.add_warn(ctx.guild.id, member.id, ctx.author.id, reason)
        await ctx.send(
            embed=system_embed(
                ctx.author,
                f"{member.mention} has been warned by {ctx.author.mention}"
                f"\nReason: {reason}",
            )
        )

    @commands.command()
    async def warns(self, ctx: commands.Context, member: discord.Member):
        """
        Display a member's warn history
        """
        output = ""
        for warn in await warns.retrieve_warns(ctx.guild.id, member.id):
            output += f"{warn['time'].strftime('%d-%b-%Y')} – `{warn['reason'][0:19]}"
            if len(warn["reason"]) >= 40:
                output += "..."
            output += "`\n"
        await ctx.send(
            embed=system_embed(
                ctx.author, output, f"{member.display_name}'s last 10 warns"
            )
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
