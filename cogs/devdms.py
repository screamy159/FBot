from discord.ext import commands
import discord

class devdms(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.bot.dms = dict()
        self.bot.userdms = dict()

    @commands.command(name="opendm")
    async def _OpenDMs(self, ctx, user: discord.User, *, content):
        if ctx.channel.id in self.bot.dms:
            await ctx.send("DM already open in this channel")
        else:
            for user in self.bot.userdms:
                if ctx.author.id == user:
                    await ctx.send("DM already open with this user")
            try:
                channel = await user.create_dm()
                author = f"`{ctx.author}` "
                await channel.send(author + content)

                self.bot.dms[ctx.channel.id] = user
                self.bot.userdms[user.id] = ctx.channel

                await ctx.message.add_reaction("✅")
            except:
                await ctx.message.add_reaction("❌")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.bot.dms:
            if message.author.id in self.bot.owner_ids:
                user = self.bot.dms[message.channel.id]
                author = f"`{message.author}` "
                await user.dm_channel.send(author + message.content)
        elif message.author.id in self.bot.userdms:
            channel = self.bot.userdms[message.author.id]
            if channel.id == message.channel.id:
                author = f"`{message.author}` "
                await channel.send(author + message.content)

    @commands.command(name="closedm")
    async def _CloseDMs(self, ctx):
        if ctx.channel.id not in self.bot.dms:
            await ctx.send("No DM open in this channel")
        else:
            user = self.bot.dms[ctx.channel.id]
            del self.bot.dms[ctx.channel.id]
            del self.bot.userdms[user.id]

            await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(devdms(bot))