from discord.ext import commands

class ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def _Ping(self, ctx):
        ping = round((self.bot.latency * 100000) / 100)
        embed = self.bot.fn.embed(ctx.author, f"FBots Ping: `{ping}ms`")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ping(bot))