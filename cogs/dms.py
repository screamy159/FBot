from discord.ext import commands

class dms(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dms")
    async def _DMs(self, ctx):
        channel = await ctx.author.create_dm()
        await channel.send("What do you want from me?!?")
        await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(dms(bot))