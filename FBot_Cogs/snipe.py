import discord
from discord.ext import commands
from functions import fn

snipes = dict()

class snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild: snipes[message.channel.id] = message

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild: snipes[before.channel.id] = before
    

    @commands.command(name='snipe')
#    @commands.is_owner()
    async def do_snipe(self, ctx):
        try:
            embed = fn.embed("FBot Snipe",
                f"```Sender: {snipes[ctx.channel.id].author.display_name}\n"
                f"Message: {snipes[ctx.channel.id].content}```")
            await ctx.send(embed=embed)
        except KeyError:
            embed = fn.embed("FBot Snipe", "```No recently deleted/edited messages to snipe```")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(snipe(bot))
