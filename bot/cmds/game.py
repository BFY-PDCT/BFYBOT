#######################################################
#                                                     #
#      BFY Entertainment                              #
#      Written-by: J.H.Lee                            #
#      (jhlee@bfy.kr)                                 #
#                                                     #
#######################################################

import sys

if __name__ == "__main__":
    print("Please execute bot.py")
    sys.exit(0)

import asyncio, random
from .config import using, bot
from .genfunc import getpoint, log, setpoint
from discord.ext import commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_command(gamble)


@commands.command(name="도박")  # prefix 도박 / prefix 도박 올인 / prefix 도박 (num: int)
async def gamble(ctx: Context, *args):
    using.append(ctx.author.id)
    if len(args) == 0:

        def check(m):
            base: bool = m.channel == ctx.channel and m.author == ctx.author
            if not base:
                return False
            try:
                int(m.content)
            except ValueError:
                return False
            return True

        pnt = getpoint(ctx.author.id, guild=ctx.guild)
        if pnt == -1:
            setpoint(ctx.author.id, 0, guild=ctx.guild)
            pnt = 0
        if pnt == 0:
            await ctx.channel.send(content="돈도없으면서 도박같은 소리하네")
            using.remove(ctx.author.id)
            return
        msg = await ctx.channel.send("얼마걸건데? 잔액: `💰 " + str(pnt) + "`")
        try:
            reply = await bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await msg.edit(content="안할거면 ㄲㅈ")
            using.remove(ctx.author.id)
            return
        num = int(reply.content)
        if pnt < num or num == 0:
            await msg.edit(content="돈도없으면서 도박같은 소리하네")
            using.remove(ctx.author.id)
            return
        await msg.edit(content=str(num) + "포인트로 게임을 시작하지")
        await asyncio.sleep(1)
    elif args[0] == "올인":
        pnt = getpoint(ctx.author.id, guild=ctx.guild)
        if pnt == -1:
            setpoint(ctx.author.id, 0, guild=ctx.guild)
            pnt = 0
        if pnt == 0:
            await ctx.channel.send(content="돈도없으면서 도박같은 소리하네")
            using.remove(ctx.author.id)
            return
        num = getpoint(ctx.author.id, guild=ctx.guild)
        if pnt < num or num == 0:
            await ctx.channel.send(content="돈도없으면서 도박같은 소리하네")
            using.remove(ctx.author.id)
            return
        msg = await ctx.channel.send(content=str(num) + "포인트로 게임을 시작하지")
        await asyncio.sleep(1)
    else:
        pnt = getpoint(ctx.author.id, guild=ctx.guild)
        if pnt == -1:
            setpoint(ctx.author.id, 0, guild=ctx.guild)
            pnt = 0
        if pnt == 0:
            await ctx.channel.send(content="돈도없으면서 도박같은 소리하네")
            using.remove(ctx.author.id)
            return
        try:
            num = int(args[0])
        except ValueError:
            await ctx.channel.send(content="제대로 된 숫자를 좀 주시죠?")
            using.remove(ctx.author.id)
            return
        if num <= 0:
            await ctx.channel.send(content="제대로 된 숫자를 좀 주시죠?")
            using.remove(ctx.author.id)
            return
        if pnt < num or num == 0:
            await ctx.channel.send(content="돈도없으면서 도박같은 소리하네")
            using.remove(ctx.author.id)
            return
        msg = await ctx.channel.send(content=str(num) + "포인트로 게임을 시작하지")
        await asyncio.sleep(1)
    i = random.randrange(1, 257)
    if i >= 1 and i <= 96:
        await msg.edit(content="꿀--꺼억 `💰-" + str(num) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) - num,
            guild=ctx.guild,
        )
        log("Taking " + str(num) + " Points from " + str(ctx.author), guild=ctx.guild)
    elif i >= 97 and i <= 144:
        await msg.edit(content="꿀--꺼억하려다 참았다... 후... `💰+0`")
    elif i >= 145 and i <= 224:
        await msg.edit(content="2배...ㅋ `💰+" + str(num) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num,
            guild=ctx.guild,
        )
        log("Giving " + str(num) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 225 and i <= 240:
        await msg.edit(content="3배... 나쁘지 않지? `💰+" + str(num * 2) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 2,
            guild=ctx.guild,
        )
        log("Giving " + str(num * 2) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 241 and i <= 248:
        await msg.edit(content="올 4배 ㅊㅊ `💰+" + str(num * 3) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 3,
            guild=ctx.guild,
        )
        log("Giving " + str(num * 3) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 249 and i <= 252:
        await msg.edit(content="이야 이걸 5배로 가져가네 `💰+" + str(num * 4) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 4,
            guild=ctx.guild,
        )
        log("Giving " + str(num * 4) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 253 and i <= 254:
        await msg.edit(content="8배면 와... `💰+" + str(num * 7) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 7,
            guild=ctx.guild,
        )
        log("Giving " + str(num * 7) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 255 and i <= 255:
        await msg.edit(content="15배라니 너 운 좀 좋다? `💰+" + str(num * 14) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 14,
            guild=ctx.guild,
        )
        log(
            "Giving " + str(num * 14) + " Points to " + str(ctx.author), guild=ctx.guild
        )
    elif i >= 256 and i <= 256:
        await msg.edit(content="뭔 나 거지되겠네 30배는 너무한거아니냐 `💰+" + str(num * 29) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 29,
            guild=ctx.guild,
        )
        log(
            "Giving " + str(num * 29) + " Points to " + str(ctx.author), guild=ctx.guild
        )
    using.remove(ctx.author.id)
    return