import os
os.environ["MAGICK_OCL_DEVICE"] = "OFF"

from wand.image import Image as wand_image
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord import File
import requests
import re

black = (0, 0, 0)
white = (255, 255, 255)
nogodfont = ImageFont.truetype("arial.ttf", 30)
godfont = ImageFont.truetype("arial.ttf", 50)

bigpp_img = wand_image(filename="data/imgs/bigpp.png")
bonk_img = wand_image(filename="data/imgs/bonk.png")
triggered_img = wand_image(filename="data/imgs/triggered.png")
sneak_img = wand_image(filename="data/imgs/sneak.png")
url = "https://cdn.filestackcontent.com/AWM47Q1KrQqWAvDUZduCYz/resize=width:512,height:512,fit:scale/"
is_img_url = re.compile("(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?")

class image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def save_image(self, path, member, attachments, to_process, author):
        if not os.path.exists("data/Temp/"):
            os.makedirs("data/Temp/")
        if member:
            await member.avatar_url_as(format="png", static_format="png", size=512).save(path)
        elif attachments:
            await attachments[0].save(path)
        elif (is_img_url.match(to_process)):
            r = requests.get(url + to_process, allow_redirects=True)
            if r.status_code == 400: raise Exception()
            with open(path, "wb") as file:
                file.write(r.content)
        else:
            await author.avatar_url_as(format="png", static_format="png", size=512).save(path)

        resized_path = path.replace("to_", "resized_to_")
        with Image.open(path) as img:
            resized_img = img.resize((512, 512))
            pixels = resized_img.load()

            if len(pixels[0, 0]) == 4:
                for y in range(512):
                    for x in range(512): 
                        if pixels[x, y][3] < 255:
                            pixels[x, y] = (255, 255, 255, 255)
            resized_img.convert("RGB").save(resized_path, "JPEG")

    async def get_member(self, guild, obj):

        if obj.isdigit():
            member = await self.bot.fetch_user(int(obj))
            if member: return member

        if guild:
            member = guild.get_member_named(obj)
            if member: return member

        obj = obj.split("<@")[-1].split("!")[-1].split(">")[0]
        if obj.isdigit():
            member = await self.bot.fetch_user(int(obj))
            if member: return member
        return None

    async def clean_up(self, ctx, path, process, success):
        if success:
            if process in ["blur"]: filename = process + "red.jpg"
            else: filename = process + "ed.jpg"

            file = File(fp=path + filename)
            await ctx.send(file=file)

            os.remove(path + "to_" + process)
            os.remove(path + "resized_to_" + process)
            try: os.remove(path + "zoom_to_" + process)
            except: pass
            os.remove(path + filename)
        else:
            await ctx.send("That image is too big to " + process)

    @commands.command(name="bigpp")
    async def _BigPP(self, ctx, *to_bigpp):

        async with ctx.channel.typing():

            to_bigpp = " ".join(to_bigpp)
            path = "data/Temp/" + str(ctx.author.id) + "_"
            member = await self.get_member(ctx.guild, to_bigpp)

            try:
                await self.save_image(path + "to_bigpp", member,
                                      ctx.message.attachments,
                                      to_bigpp, ctx.author)
            except:
                success = False
            else:
                with wand_image(filename=path + "resized_to_bigpp") as img:
                    img.implode(amount=-7)
                    img.composite(bigpp_img)
                    img.save(filename=path + "bigpped.jpg")
                success = True

        await self.clean_up(ctx, path, "bigpp", success)

    @commands.command(name="bonk")
    async def _Bonk(self, ctx, *to_bonk):

        async with ctx.channel.typing():

            to_bonk = " ".join(to_bonk)
            path = "data/Temp/" + str(ctx.author.id) + "_"
            member = await self.get_member(ctx.guild, to_bonk)

            try:
                await self.save_image(path + "to_bonk", member,
                                      ctx.message.attachments,
                                      to_bonk, ctx.author)
            except:
                success = False
            else:
                with wand_image(filename=path + "resized_to_bonk") as img:
                    img.swirl(degree=-45)
                    img.implode(amount=0.4)
                    img.composite(bonk_img)
                    img.save(filename=path + "bonked.jpg")
                success = True

        await self.clean_up(ctx, path, "bonk", success)

    @commands.command(name="blur")
    async def _Blur(self, ctx, amount: int=25, *to_blur):

        if type(amount) is not int:
            await ctx.send("Amount must be a number")
            return
        elif amount > 200:
            await ctx.send("Whoa! That number is like, bigger than 200 bro")
            return

        async with ctx.channel.typing():

            to_blur = " ".join(to_blur)
            path = "data/Temp/" + str(ctx.author.id) + "_"
            member = await self.get_member(ctx.guild, to_blur)

            try:
                await self.save_image(path + "to_blur", member,
                                      ctx.message.attachments,
                                      to_blur, ctx.author)
            except:
                success = False
            else:
                with wand_image(filename=path + "resized_to_blur") as img:
                    angle = amount * 5 / 9
                    img.rotational_blur(angle=angle)
                    img.save(filename=path + "blurred.jpg")
                success = True

        await self.clean_up(ctx, path, "blur", success)

    @commands.command(name="trigger")
    async def _Trigger(self, ctx, *to_trigger):

        async with ctx.channel.typing():

            to_trigger = " ".join(to_trigger)
            path = "data/Temp/" + str(ctx.author.id) + "_"
            member = await self.get_member(ctx.guild, to_trigger)

            try:
                await self.save_image(path + "to_trigger", member,
                                      ctx.message.attachments,
                                      to_trigger, ctx.author)
            except:
                success = False
            else:
                with wand_image(filename=path + "resized_to_trigger") as img:
                    img.rotational_blur(angle=30)
                    img.composite(triggered_img)
                    img.rotational_blur(angle=10)
                    img.save(filename=path + "triggered.jpg")
                success = True

        await self.clean_up(ctx, path, "trigger", success)

    @commands.command(name="sneak")
    async def _Sneak(self, ctx, *to_sneak):

        async with ctx.channel.typing():

            to_sneak = " ".join(to_sneak)
            path = "data/Temp/" + str(ctx.author.id) + "_"
            member = await self.get_member(ctx.guild, to_sneak)

            try:
                await self.save_image(path + "to_sneak", member,
                                      ctx.message.attachments,
                                      to_sneak, ctx.author)
            except:
                success = False
            else:
                with wand_image(filename=path + "resized_to_sneak") as img:
                    img.composite(sneak_img)
                    img.save(filename=path + "sneaked.jpg")
                success = True

        await self.clean_up(ctx, path, "sneak", success)

    @commands.command(name="god")
    async def _God(self, ctx, *to_god):

        async with ctx.channel.typing():

            to_god = " ".join(to_god)
            path = "data/Temp/" + str(ctx.author.id) + "_"
            member = await self.get_member(ctx.guild, to_god)

            try:
                await self.save_image(path + "to_god", member,
                                      ctx.message.attachments,
                                      to_god, ctx.author)
            except:
                success = False
            else:
                with Image.open(path + "resized_to_god") as img:
                    img.resize((511, 255)).save(path + "resized_to_god", "JPEG")

                with wand_image(filename=path + "resized_to_god") as zoomed_img:
                    zoomed_img.crop(127, 63, 383, 191)
                    zoomed_img.resize(511, 255)
                    zoomed_img.colorize(color="red", alpha="rgb(20%, 20%, 20%)")
                    zoomed_img.save(filename=path + "zoom_to_god")

                top = Image.open(path + "resized_to_god")
                bottom = Image.open(path + "zoom_to_god")
                back = Image.new("RGB", (511, 511), (0,0,0))

                back.paste(top, (0,0))
                back.paste(bottom, (0, 256))
                draw = ImageDraw.Draw(back)

                x, y = 20, 20
                text = "i see no god up here"
                for i in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
                    coords = (x + i[0], y + i[1])
                    draw.text(coords, text, font=nogodfont, fill=black)
                draw.text((x, y), text, font=nogodfont, fill=white)

                x, y = 100, 460
                text = "OTHER THAN ME"
                for i in [(2, 2), (2, -2), (-2, -2), (-2, 2)]:
                    coords = (x + i[0], y + i[1])
                    draw.text(coords, text, font=godfont, fill=black)
                draw.text((x, y), text, font=godfont, fill=white)

                back.save(path + "goded.jpg")

                top.close()
                bottom.close()
                back.close()

                success = True

        await self.clean_up(ctx, path, "god", success)

def setup(bot):
    bot.add_cog(image(bot))