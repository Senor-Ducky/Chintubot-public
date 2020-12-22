import discord
from discord.ext import commands
from utilities import system_embed


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        if hasattr(ctx.cog, f"_{ctx.cog.__class__.__name__}__error"):
            return

        ignored = ()

        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f"{ctx.command} has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f"{ctx.command} can not be used in Private Messages."
                )
            except discord.HTTPException:
                pass

        elif isinstance(
            error, (commands.MissingRequiredArgument, commands.BadArgument)
        ):
            await ctx.send(
                embed=system_embed(
                    ctx.author,
                    f"Invalid Command usage. To get additional information"
                    f" about the following command "
                    f"``{ctx.prefix}help {ctx.command}``",
                )
            )

        elif isinstance(error, commands.MissingPermissions) or isinstance(
            error, commands.CheckFailure
        ):
            await ctx.send(
                embed=system_embed(
                    ctx.author,
                    f"You do not have the permission to use "
                    f"``{ctx.prefix}{ctx.command}``",
                )
            )


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
