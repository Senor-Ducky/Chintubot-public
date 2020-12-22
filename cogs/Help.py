import discord
from discord.ext import commands
from utilities import system_embed, GUILD_DATA
from disputils import BotEmbedPaginator


class Help(commands.Cog):
    """
    Help command
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, command_name: str = None):
        """*Shows this message*"""
        ctx.prefix = GUILD_DATA[ctx.guild.id]["prefix"]
        if command_name is None:
            embeds = []
            for cog in self.bot.cogs:
                if cog in self.hidden_cogs:
                    continue
                cog = self.bot.get_cog(cog)
                e = discord.Embed(title=cog.qualified_name, description=cog.description)
                for command in cog.get_commands():
                    brief = command.short_doc
                    if brief == "":
                        brief = "Command help not found not"
                    if command.hidden:
                        continue
                    e.add_field(
                        name=f"{ctx.prefix}{command.name}", value=brief, inline=False
                    )
                embeds.append(e)
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
            return
        command = self.bot.get_command(command_name.casefold())
        if command is None:
            await ctx.send(embed=system_embed(ctx.author, "Command not found"))
            return
        e = discord.Embed(
            title=f"{ctx.prefix}{command.name}",
            description=f"```{command.help.format(prefix=ctx.prefix)}```",
        )
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Help(bot))
