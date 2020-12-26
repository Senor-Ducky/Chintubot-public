import discord
from discord.ext import commands

class Suggestions(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['poll'])
	async def suggest(self, ctx, *,suggestion):
		suggestion_channel = 775789016842764303

		await ctx.channel.purge(limit=1)
		em = discord.Embed(title=f'Suggestion by {ctx.message.author}', description=suggestion, colour=discord.Color.dark_blue())
		em.set_thumbnail(url=ctx.message.author.avatar_url)
		bot_message = await ctx.send(embed=em)
		await bot_message.add_reaction('👍')
		await bot_message.add_reaction('👎')


def setup(bot):
	bot.add_cog(Suggestions(bot))

