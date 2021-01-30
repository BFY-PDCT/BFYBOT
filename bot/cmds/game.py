"""
    Copyright (C) 2021 BFY Entertainment
    All right reserved

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    import sys

    print("Please execute bot.py")
    sys.exit(0)

import asyncio
import random
import discord
from .config import using, bot, prefix, botcolor
from .genfunc import getpoint, log, setpoint, getstk, setstk
from discord.ext import commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_command(gamble)
    bot.add_command(stock)


@commands.command(name="도박")  # prefix 도박 / prefix 도박 올인 / prefix 도박 (num: int)
async def gamble(ctx: Context, *args):
    using.append(ctx.author.id)
    if len(args) == 0:

        def check(m):
            base: bool = m.channel == ctx.channel and m.author == ctx.author
            if not base:
                return False
            try:
                if int(m.content) < 0:
                    return False
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
    if i >= 1 and i <= 80:
        await msg.edit(content="꿀--꺼억 `💰-" + str(num) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) - num,
            guild=ctx.guild,
        )
        log("Taking " + str(num) + " Points from " + str(ctx.author), guild=ctx.guild)
    elif i >= 81 and i <= 128:
        await msg.edit(content="0.5배 다먹기엔 배불러 ㅋㅋ `💰-" + str(num // 2) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) - num // 2,
            guild=ctx.guild,
        )
        log(
            "Taking " + str(num // 2) + " Points from " + str(ctx.author),
            guild=ctx.guild,
        )
    elif i >= 128 and i <= 224:
        await msg.edit(content="꿀--꺼억하려다 참았다... 후... `💰+0`")
    elif i >= 225 and i <= 240:
        await msg.edit(content="2배... 나쁘지 않지? `💰+" + str(num) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num,
            guild=ctx.guild,
        )
        log("Giving " + str(num) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 241 and i <= 248:
        await msg.edit(content="올 4배 ㅊㅊ `💰+" + str(num * 3) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 3,
            guild=ctx.guild,
        )
        log("Giving " + str(num * 3) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 249 and i <= 252:
        await msg.edit(content="이야 이걸 6배로 가져가네 `💰+" + str(num * 5) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 5,
            guild=ctx.guild,
        )
        log("Giving " + str(num * 5) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 253 and i <= 254:
        await msg.edit(content="8배면 와... `💰+" + str(num * 7) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 7,
            guild=ctx.guild,
        )
        log("Giving " + str(num * 7) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 255 and i <= 255:
        await msg.edit(content="10배라니 너 운 좀 좋다? `💰+" + str(num * 9) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 9,
            guild=ctx.guild,
        )
        log("Giving " + str(num * 9) + " Points to " + str(ctx.author), guild=ctx.guild)
    elif i >= 256 and i <= 256:
        await msg.edit(content="뭔 나 거지되겠네 50배는 너무한거아니냐 `💰+" + str(num * 29) + "`")
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 49,
            guild=ctx.guild,
        )
        log(
            "Giving " + str(num * 49) + " Points to " + str(ctx.author), guild=ctx.guild
        )
    using.remove(ctx.author.id)
    return


@commands.command(name="주식")  # prefix 주식 / prefix 도박 올인 / prefix 도박 (num: int)
async def stock(ctx: Context, *args):
    def check(m):
        base: bool = m.channel == ctx.channel and m.author == ctx.author
        if not base:
            return False
        try:
            if int(m.content) < 0:
                return False
        except ValueError:
            return False
        return True

    if (len(args)) != 2:
        await ctx.send("`" + prefix + " 주식 (그래프|매수|매도) (A|B|ENT|CORP)` 이 올바른 사용법이에요 ^^")
        return
    if not args[0] in ["그래프", "매수", "매도"]:
        await ctx.send("`" + prefix + " 주식 (그래프|매수|매도) (A|B|ENT|CORP)` 이 올바른 사용법이에요 ^^")
        return
    if args[1] in ["A", "A주식", "주식A", "ENT", "BFYENT"]:
        stktype = 0
    elif args[1] in ["B", "B주식", "주식B", "CORP", "BFYCORP"]:
        stktype = 1
    else:
        await ctx.send("`" + prefix + " 주식 (그래프|매수|매도) (A|B|ENT|CORP)` 이 올바른 사용법이에요 ^^")
        return
    using.append(ctx.author.id)
    if args[0] == "그래프":
        if stktype == 0:
            stka = bot.get_cog("updatestka")
            if stka is not None:
                res = stka.getprice()
            else:
                await ctx.send("ERROR")
                using.remove(ctx.author.id)
                return
            msg = discord.Embed(
                title="현재 가격: " + str(res),
                color=botcolor,
                description="BFY ENT(A)의 그래프입니다.",
            )
            await ctx.send(embed=msg, file=discord.File("./bbdata/stock_a.png"))
        elif stktype == 1:
            stkb = bot.get_cog("updatestkb")
            if stkb is not None:
                res = stkb.getprice()
            else:
                await ctx.send("ERROR")
                using.remove(ctx.author.id)
                return
            msg = discord.Embed(
                title="현재 가격: " + str(res),
                color=botcolor,
                description="BFY CORP(B)의 그래프입니다.",
            )
            await ctx.send(embed=msg, file=discord.File("./bbdata/stock_b.png"))
    elif args[0] == "매수":
        if stktype == 0:
            stka = bot.get_cog("updatestka")
            if stka is not None:
                res = stka.getprice()
            else:
                await ctx.send("ERROR")
                using.remove(ctx.author.id)
                return
            pnt = getpoint(ctx.author.id, guild=ctx.guild)
            if pnt == -1:
                setpoint(ctx.author.id, 0, guild=ctx.guild)
                pnt = 0
            stk = getstk("stka", ctx.author.id, ctx.guild)
            if stk == -1:
                setstk("stka", ctx.author.id, 0, ctx.guild)
                stk = 0
            if pnt <= res:
                await ctx.channel.send(content="돈도없으면서 주식같은 소리하네")
                using.remove(ctx.author.id)
                return
            msg = await ctx.channel.send(
                "얼마나 구매하시겠어요? 잔액: `💰 "
                + str(pnt)
                + "`, 현재가격: "
                + str(res)
                + ", 구매가능수량: "
                + str(pnt // res)
                + "주"
            )
            try:
                reply = await bot.wait_for("message", check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await msg.edit(content="안살거면 가세요")
                using.remove(ctx.author.id)
                return
            num = int(reply.content)
            if pnt // res < num or num == 0:
                await msg.edit(content="정확한 수량을 입력하십쇼")
                using.remove(ctx.author.id)
                return
            await msg.edit(content=str(num) + "주를 구매하셨습니다. `💰-" + str(res * num) + "`")
            setpoint(ctx.author.id, pnt - res * num, guild=ctx.guild)
            log(
                "Taking " + str(res * num) + " Points from " + str(ctx.author),
                guild=ctx.guild,
            )
            setstk("stka", ctx.author.id, stk + num, ctx.guild)
            stka.buy(num)
            log(
                "Giving " + str(num) + " A Stocks to " + str(ctx.author),
                guild=ctx.guild,
            )
        elif stktype == 1:
            stkb = bot.get_cog("updatestkb")
            if stkb is not None:
                res = stkb.getprice()
            else:
                await ctx.send("ERROR")
                using.remove(ctx.author.id)
                return
            pnt = getpoint(ctx.author.id, guild=ctx.guild)
            if pnt == -1:
                setpoint(ctx.author.id, 0, guild=ctx.guild)
                pnt = 0
            stk = getstk("stkb", ctx.author.id, ctx.guild)
            if stk == -1:
                setstk("stkb", ctx.author.id, 0, ctx.guild)
                stk = 0
            if pnt <= res:
                await ctx.channel.send(content="돈도없으면서 주식같은 소리하네")
                using.remove(ctx.author.id)
                return
            msg = await ctx.channel.send(
                "얼마나 구매하시겠어요? 잔액: `💰 "
                + str(pnt)
                + "`, 현재가격: "
                + str(res)
                + ", 구매가능수량: "
                + str(pnt // res)
                + "주"
            )
            try:
                reply = await bot.wait_for("message", check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await msg.edit(content="안살거면 가세요")
                using.remove(ctx.author.id)
                return
            num = int(reply.content)
            if pnt // res < num or num == 0:
                await msg.edit(content="정확한 수량을 입력하십쇼")
                using.remove(ctx.author.id)
                return
            await msg.edit(content=str(num) + "주를 구매하셨습니다. `💰-" + str(res * num) + "`")
            setpoint(ctx.author.id, pnt - res * num, guild=ctx.guild)
            log(
                "Taking " + str(res * num) + " Points from " + str(ctx.author),
                guild=ctx.guild,
            )
            setstk("stkb", ctx.author.id, stk + num, ctx.guild)
            stkb.buy(num)
            log(
                "Giving " + str(num) + " B Stocks to " + str(ctx.author),
                guild=ctx.guild,
            )
    elif args[0] == "매도":
        if stktype == 0:
            stka = bot.get_cog("updatestka")
            if stka is not None:
                res = stka.getprice()
            else:
                await ctx.send("ERROR")
                using.remove(ctx.author.id)
                return
            pnt = getpoint(ctx.author.id, guild=ctx.guild)
            if pnt == -1:
                setpoint(ctx.author.id, 0, guild=ctx.guild)
                pnt = 0
            stk = getstk("stka", ctx.author.id, guild=ctx.guild)
            if stk == -1:
                setstk("stka", ctx.author.id, 0, guild=ctx.guild)
                stk = 0
            if stk == 0:
                await ctx.channel.send(content="주식도 없으면서 매도같은 소리하네")
                using.remove(ctx.author.id)
                return
            msg = await ctx.channel.send(
                "얼마나 판매하시겠어요? 현재가격: " + str(res) + ", 판매가능수량: " + str(stk) + "주"
            )
            try:
                reply = await bot.wait_for("message", check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await msg.edit(content="안팔거면 가세요")
                using.remove(ctx.author.id)
                return
            num = int(reply.content)
            if stk < num or num == 0:
                await msg.edit(content="정확한 수량을 입력하십쇼")
                using.remove(ctx.author.id)
                return
            await msg.edit(content=str(num) + "주를 판매하셨습니다. `💰+" + str(res * num) + "`")
            setpoint(ctx.author.id, pnt + res * num, guild=ctx.guild)
            log(
                "Giving " + str(res * num) + " Points to " + str(ctx.author),
                guild=ctx.guild,
            )
            setstk("stka", ctx.author.id, stk - num, ctx.guild)
            stka.sell(num)
            log(
                "Taking " + str(num) + " A Stocks from " + str(ctx.author),
                guild=ctx.guild,
            )
        elif stktype == 1:
            stkb = bot.get_cog("updatestkb")
            if stkb is not None:
                res = stkb.getprice()
            else:
                await ctx.send("ERROR")
                using.remove(ctx.author.id)
                return
            pnt = getpoint(ctx.author.id, guild=ctx.guild)
            if pnt == -1:
                setpoint(ctx.author.id, 0, guild=ctx.guild)
                pnt = 0
            stk = getstk("stkb", ctx.author.id, guild=ctx.guild)
            if stk == -1:
                setstk("stkb", ctx.author.id, 0, guild=ctx.guild)
                stk = 0
            if stk == 0:
                await ctx.channel.send(content="주식도 없으면서 매도같은 소리하네")
                using.remove(ctx.author.id)
                return
            msg = await ctx.channel.send(
                "얼마나 판매하시겠어요? 현재가격: " + str(res) + ", 판매가능수량: " + str(stk) + "주"
            )
            try:
                reply = await bot.wait_for("message", check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await msg.edit(content="안팔거면 가세요")
                using.remove(ctx.author.id)
                return
            num = int(reply.content)
            if stk < num or num == 0:
                await msg.edit(content="정확한 수량을 입력하십쇼")
                using.remove(ctx.author.id)
                return
            await msg.edit(content=str(num) + "주를 판매하셨습니다. `💰+" + str(res * num) + "`")
            setpoint(ctx.author.id, pnt + res * num, guild=ctx.guild)
            log(
                "Giving " + str(res * num) + " Points to " + str(ctx.author),
                guild=ctx.guild,
            )
            setstk("stkb", ctx.author.id, stk - num, ctx.guild)
            stkb.sell(num)
            log(
                "Taking " + str(num) + " B Stocks from " + str(ctx.author),
                guild=ctx.guild,
            )
    using.remove(ctx.author.id)
    return
