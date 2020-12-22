from discord.ext import commands
from pathlib import Path


def extensions():
    files = Path("cogs").rglob("*.py")
    for file in files:
        yield file.as_posix()[:-3].replace("/", ".")


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id in [592417969666261002, 177131156028784640]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def load(self, ctx):
        for extension in extensions():
            try:
                self.bot.load_extension(extension)
            except Exception as ex:
                await ctx.send(f"Failed to load {extension}; {ex}")
        await ctx.send("Loaded")

    @commands.command()
    async def unload(self, ctx):
        for extension in extensions():
            try:
                self.bot.unload_extension(extension)
            except Exception as ex:
                await ctx.send(f"Failed to unload {extension}; {ex}")
        await ctx.send("unloaded")

    @commands.command()
    async def reload(self, ctx):
        await self.unload(ctx)
        await self.load(ctx)

    # @commands.Cog.listener()
    # async def on_guild_update(self, before, after):
    #     if after


def setup(bot):
    bot.add_cog(Owner(bot))
