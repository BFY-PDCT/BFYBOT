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
from .genfunc import (
    getpoint,
    setpoint,
    getstk,
    setstk,
    recstk,
    getrecstk,
    getlocale,
    localeerr,
)
from discord.ext import commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_command(gamble)
    bot.add_command(stock)


@commands.command(
    name="도박", aliases=["gamble"]
)  # prefix 도박 / prefix 도박 올인 / prefix 도박 (num: int)
async def gamble(ctx: Context, *args):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
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
            await ctx.channel.send(content=locale["game_gamble_0"])
            using.remove(ctx.author.id)
            return
        msg = await ctx.channel.send(locale["game_gamble_1"].format(str(pnt)))
        try:
            reply = await bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await msg.edit(content=locale["game_gamble_2"])
            using.remove(ctx.author.id)
            return
        num = int(reply.content)
        if pnt < num or num == 0:
            await msg.edit(content=locale["game_gamble_4"])
            using.remove(ctx.author.id)
            return
        await msg.edit(content=locale["game_gamble_3"].format(str(num)))
        await asyncio.sleep(1)
    elif args[0] == "올인" or args[0] == "allin":
        pnt = getpoint(ctx.author.id, guild=ctx.guild)
        if pnt == -1:
            setpoint(ctx.author.id, 0, guild=ctx.guild)
            pnt = 0
        if pnt == 0:
            await ctx.channel.send(content=locale["game_gamble_4"])
            using.remove(ctx.author.id)
            return
        num = getpoint(ctx.author.id, guild=ctx.guild)
        if pnt < num or num == 0:
            await ctx.channel.send(content=locale["game_gamble_4"])
            using.remove(ctx.author.id)
            return
        msg = await ctx.channel.send(content=locale["game_gamble_3"].format(str(num)))
        await asyncio.sleep(1)
    else:
        pnt = getpoint(ctx.author.id, guild=ctx.guild)
        if pnt == -1:
            setpoint(ctx.author.id, 0, guild=ctx.guild)
            pnt = 0
        if pnt == 0:
            await ctx.channel.send(content=locale["game_gamble_4"])
            using.remove(ctx.author.id)
            return
        try:
            num = int(args[0])
        except ValueError:
            await ctx.channel.send(content=locale["game_gamble_5"])
            using.remove(ctx.author.id)
            return
        if num <= 0:
            await ctx.channel.send(content=locale["game_gamble_5"])
            using.remove(ctx.author.id)
            return
        if pnt < num or num == 0:
            await ctx.channel.send(content=locale["game_gamble_4"])
            using.remove(ctx.author.id)
            return
        msg = await ctx.channel.send(content=locale["game_gamble_3"].format(str(num)))
        await asyncio.sleep(1)
    i = random.randrange(1, 257)
    if i >= 1 and i <= 80:
        await msg.edit(content=locale["game_gamble_6"].format(str(num)))
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) - num,
            guild=ctx.guild,
        )
    elif i >= 81 and i <= 128:
        await msg.edit(content=locale["game_gamble_7"].format(str(num // 2)))
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) - num // 2,
            guild=ctx.guild,
        )
    elif i >= 128 and i <= 224:
        await msg.edit(content=locale["game_gamble_8"])
    elif i >= 225 and i <= 240:
        await msg.edit(content=locale["game_gamble_9"].format(str(num)))
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num,
            guild=ctx.guild,
        )
    elif i >= 241 and i <= 248:
        await msg.edit(content=locale["game_gamble_10"].format(str(num * 3)))
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 3,
            guild=ctx.guild,
        )
    elif i >= 249 and i <= 252:
        await msg.edit(content=locale["game_gamble_11"].format(str(num * 5)))
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 5,
            guild=ctx.guild,
        )
    elif i >= 253 and i <= 254:
        await msg.edit(content=locale["game_gamble_12"].format(str(num * 7)))
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 7,
            guild=ctx.guild,
        )
    elif i >= 255 and i <= 255:
        await msg.edit(content=locale["game_gamble_13"].format(str(num * 9)))
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 9,
            guild=ctx.guild,
        )
    elif i >= 256 and i <= 256:
        await msg.edit(content=locale["game_gamble_14"].format(str(num * 49)))
        setpoint(
            ctx.author.id,
            getpoint(ctx.author.id, guild=ctx.guild) + num * 49,
            guild=ctx.guild,
        )
    using.remove(ctx.author.id)
    return


@gamble.error
async def gamble_error(ctx: Context, error):
    using.remove(ctx.author.id)
    return


@commands.command(
    name="주식", aliases=["stock"]
)  # prefix 주식
async def stock(ctx: Context, *args):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)

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
        await ctx.send(locale["game_stock_0"].format(prefix))
        return
    if not args[0] in ["그래프", "매수", "매도", "통계", "graph", "buy", "sell", "record"]:
        await ctx.send(locale["game_stock_0"].format(prefix))
        return
    if args[1] in [
        "A",
        "ENT",
        "BFYENT",
        "a",
        "ent",
        "bfyent",
    ]:
        types = "a"
        names = "BFY ENT(A)"
    elif args[1] in [
        "B",
        "CORP",
        "BFYCORP",
        "b",
        "corp",
        "bfycorp",
    ]:
        types = "b"
        names = "BFY CORP(B)"
    elif args[1] in [
        "C",
        "AT7",
        "AT7GROUP",
        "c",
        "at7",
        "at7group",
    ]:
        types = "c"
        names = "AT7 GROUP(C)"
    else:
        await ctx.send(locale["game_stock_0"].format(prefix))
        return
    using.append(ctx.author.id)
    if args[0] == "그래프" or args[0] == "graph":
        stk = bot.get_cog("updatestk" + types)
        if stk is not None:
            res = stk.getprice()
        else:
            await ctx.send("ERROR")
            using.remove(ctx.author.id)
            return
        msg = discord.Embed(
            title=locale["game_stock_1"].format(str(res)),
            color=botcolor,
            description=locale["game_stock_2"].format(names),
        )
        await ctx.send(embed=msg, file=discord.File("./bbdata/stock_" + types + ".png"))
    elif args[0] == "매수" or args[0] == "buy":
        stkx = bot.get_cog("updatestk" + types)
        if stkx is not None:
            res = stkx.getprice()
        else:
            await ctx.send("ERROR")
            using.remove(ctx.author.id)
            return
        pnt = getpoint(ctx.author.id, guild=ctx.guild)
        if pnt == -1:
            setpoint(ctx.author.id, 0, guild=ctx.guild)
            pnt = 0
        stk = getstk(types, ctx.author.id, ctx.guild)
        if stk == -1:
            setstk(types, ctx.author.id, 0, ctx.guild)
            stk = 0
        if pnt <= res:
            await ctx.channel.send(content=locale["game_stock_3"])
            using.remove(ctx.author.id)
            return
        msg = await ctx.channel.send(
            locale["game_stock_4"].format(str(pnt), str(res), str(pnt // res))
        )
        try:
            reply = await bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await msg.edit(content=locale["game_stock_5"])
            using.remove(ctx.author.id)
            return
        num = int(reply.content)
        if pnt // res < num or num == 0:
            await msg.edit(content=locale["game_stock_6"])
            using.remove(ctx.author.id)
            return
        stknow = getstk(types, ctx.author.id, ctx.guild)
        if stknow + num > 100000:
            await msg.edit(content=locale["game_stock_7"])
            using.remove(ctx.author.id)
            return
        await msg.edit(content=locale["game_stock_8"].format(str(num), str(res * num)))
        setpoint(ctx.author.id, pnt - res * num, guild=ctx.guild)
        setstk(types, ctx.author.id, stk + num, ctx.guild)
        stkx.buy(num)
        recstk(types, ctx.author.id, ctx.guild, True, num, res)
    elif args[0] == "매도" or args[0] == "sell":
        stkx = bot.get_cog("updatestk" + types)
        if stkx is not None:
            res = stkx.getprice()
        else:
            await ctx.send("ERROR")
            using.remove(ctx.author.id)
            return
        pnt = getpoint(ctx.author.id, ctx.guild)
        stk = getstk(types, ctx.author.id, ctx.guild)
        if stk == 0:
            await ctx.channel.send(content=locale["game_stock_9"])
            using.remove(ctx.author.id)
            return
        msg = await ctx.channel.send(locale["game_stock_10"].format(str(res), str(stk)))
        try:
            reply = await bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await msg.edit(content=locale["game_stock_11"])
            using.remove(ctx.author.id)
            return
        num = int(reply.content)
        if stk < num or num == 0:
            await msg.edit(content=locale["game_stock_6"])
            using.remove(ctx.author.id)
            return
        await msg.edit(content=locale["game_stock_12"].format(str(num), str(res * num)))
        setpoint(ctx.author.id, pnt + res * num, guild=ctx.guild)
        setstk(types, ctx.author.id, stk - num, ctx.guild)
        stkx.sell(num)
        recstk(types, ctx.author.id, ctx.guild, False, num, res)
    elif args[0] == "통계" or args[0] == "record":
        stk = getrecstk(types, ctx.author.id, guild=ctx.guild)
        if len(stk) == 0:
            await ctx.channel.send(content=locale["game_stock_13"])
            using.remove(ctx.author.id)
            return
        desc = ""
        for substk in stk:
            if substk[0]:
                substk[0] = "매수"
            else:
                substk[0] = "매도"
        for substk in stk:
            desc = (
                desc
                + locale["game_stock_16"].format(
                    substk[0], substk[2], substk[1], substk[1] * substk[2]
                )
                + "\n"
            )
        msg = discord.Embed(
            title=locale["game_stock_17"].format(names),
            color=botcolor,
            description=desc,
        )
        await ctx.send(embed=msg)
    using.remove(ctx.author.id)
    return


@stock.error
async def stock_error(ctx: Context, error):
    using.remove(ctx.author.id)
    return
