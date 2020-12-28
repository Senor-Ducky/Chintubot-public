import discord
from discord.ext import commands
import requests
import json


class GitHub(commands.Cog):
    def __init__(self, commands):
        self.commands = commands

    @commands.command(aliases=["repositories", "github"])
    async def repos(self, ctx, username):
        user_image = requests.get(f"https://api.github.com/users/{username}").json()
        if "message" in user_image:
            em = discord.Embed(title=f"User {username} not found! Please check the username.",
                               color=discord.Color.red())
            await ctx.send(embed=em)
            return
        results = requests.get(f"https://api.github.com/users/{username}/repos").json()
        embed = discord.Embed(title=f"Top 5 repositories of {username}", color=discord.Color.blue())
        embed.set_thumbnail(url=user_image["avatar_url"])
        embed.set_footer(text=f"{username} has {user_image['public_repos']} repositories!")
        if len(results) > 5:
            results = results[:5]
        for result in results:
            embed.add_field(name=result["name"], value=result["html_url"], inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["gitmember"])
    async def gituser(self, ctx, username):
        user = requests.get(f"https://api.github.com/users/{username}").json()
        if "message" in user:
            em = discord.Embed(title=f"User {username} not found! Please check the username.",
                               color=discord.Color.red())
            await ctx.send(embed=em)
            return
        embed = discord.Embed(title=username, color=discord.Color.blue())
        embed.set_thumbnail(url=user["avatar_url"])
        embed.add_field(name="URL", value=user["html_url"])
        attributes = {"name":"Name", "company":"Company", "blog":"Website", "location":"Location", "bio":"Github Bio", "twitter_username":"Twitter Handle", "public_repos":"Total Repos"}
        for attribute in attributes:
            if user[attribute] is not None:
                if user[attribute] != "":
                    embed.add_field(name=attributes[attribute], value=user[attribute], inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def contributors(self, ctx):
    	url = 'https://api.github.com/repos/soulless-404/chintubot/contributors'
    	response = requests.get(url)
    	data = json.loads(response.text)
    	embed = discord.Embed(title='People who have contributed in making the Chintu Bot')
    	for contributor in data:
    		embed.add_field(name=str(contributor['login']) + ' (' + contributor['html_url'] + ')', value = str(contributor['contributions'])+ ' commits', inline=False)

    	embed.set_thumbnail(url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
    	await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GitHub(bot))
