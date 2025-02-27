from discord.ext import commands
from random import choice
import asyncio

active_channels = set()
with open("data/Jokes/joke.txt", "r") as file:
    pingpong_joke = file.read().split("\n")
with open("data/Jokes/snakejoke.txt", "r") as file:
    snake_joke = file.read().split("\n")

class joke(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joke")
    async def _Joke(self, ctx):

        if (ctx.channel.id in active_channels):
            await ctx.send("I'm already telling a joke, do `fbot shutup` to cancel")
            return

        await ctx.send("Ok, I've got a joke.\nDo `fbot shutup` to cancel")

        active_channels.add(ctx.channel.id)
        the_joke = choice([snake_joke, pingpong_joke])

        for line in the_joke:
            async with ctx.channel.typing():
                for i in range(0, len(line)):
                    sleep_seconds = 1 / 15
                    await asyncio.sleep(sleep_seconds)
                    if (not ctx.channel.id in active_channels):
                        return
                await ctx.send(line)

        active_channels.remove(ctx.channel.id)

    @commands.command(name="shutup")
    async def _ShutUp(self, ctx):
        if (ctx.channel.id in active_channels):
            active_channels.remove(ctx.channel.id)
            await ctx.send("Ok, but I was just getting to the best part")
        else:
            await ctx.send("You wish")

    @commands.command(name="jokeinfo")
    @commands.is_owner()
    async def _JokeInfo(self, ctx):
        await ctx.send("Active channels: " + str(active_channels))

def setup(bot):
    bot.add_cog(joke(bot))