from discord.ext import commands
import asyncio

ongoing_purges = set()

class purge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", aliases=["thanos"])
    async def _Purge(self, ctx, *args):

        if not ctx.message.author.guild_permissions.manage_messages:
            await ctx.send("**`You do not have the manage_messages permissions.`**")
            return

        if ctx.channel.id in ongoing_purges:
            msg = await ctx.send("**A purge is already in progress, calm yoself.**")
            await asyncio.sleep(1)
            try:
                await msg.delete()
            except: pass
            return

        if len(args) != 0:
            limit = "".join(args)
            if limit.isdigit():
                limit = int(limit)
                if limit > 1000:
                    await ctx.send("`The purge limit is currently 1000 messages`")
                    return
                ongoing_purges.add(ctx.channel.id)
                await ctx.channel.purge(limit=limit + 1)
                ongoing_purges.remove(ctx.channel.id)
                msg = await ctx.send(f"`Purged {limit} messages.`")
                await asyncio.sleep(1)
                await msg.delete()
            else:
                await ctx.send("You must specify how many messages to purge!")
        else:
            await ctx.send("You must specify how many messages to purge!")

def setup(bot):
    bot.add_cog(purge(bot))