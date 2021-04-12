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
from .config import botname, bot
from .genfunc import tblog, getpoint, setpoint, getstk, setstk, getlocale, localeerr
from discord.ext import commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_command(seemoney)
    bot.add_command(getmoney)
    bot.add_command(seeothermoney)
    bot.add_command(seestk)
    bot.add_command(seeotherstk)
    bot.add_command(sendmoney)


@commands.command(name="돈", aliases=["내돈"])  # prefix 돈 / prefix 내돈
async def seemoney(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    pnt = getpoint(ctx.author.id, guild=ctx.guild)
    if pnt == -1:
        setpoint(ctx.author.id, 0, guild=ctx.guild)
        pnt = 0
    await ctx.channel.send(
        locale["economy_seemoney_0"].format(ctx.author.mention, str(pnt))
    )
    return


@commands.command(name="돈내놔")  # prefix 돈내놔
async def getmoney(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)

    def check(m):
        return (
            m.content == botname + locale["economy_getmoney_1"]
            and m.channel == ctx.channel
            and m.author == ctx.author
        )

    i = random.randrange(1, 8)
    if i == 1:
        if getpoint(ctx.author.id, guild=ctx.guild) == -1:
            setpoint(ctx.author.id, 10, guild=ctx.guild)
        else:
            setpoint(
                ctx.author.id,
                getpoint(ctx.author.id, guild=ctx.guild) + 1000,
                guild=ctx.guild,
            )
        await ctx.channel.send(locale["economy_getmoney_2"])
    elif i == 2:
        await ctx.channel.send(locale["economy_getmoney_3"])
    elif i == 3:
        await ctx.channel.send(locale["economy_getmoney_4"])
    elif i == 4:
        if getpoint(ctx.author.id, guild=ctx.guild) == -1:
            setpoint(ctx.author.id, 1, guild=ctx.guild)
        else:
            setpoint(
                ctx.author.id,
                getpoint(ctx.author.id, guild=ctx.guild) + 100,
                guild=ctx.guild,
            )
        await ctx.channel.send(locale["economy_getmoney_5"])
    elif i == 5:
        msg = await ctx.channel.send(botname + locale["economy_getmoney_6"])
        try:
            await bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            try:
                await msg.edit(content=locale["economy_getmoney_7"])
            except Exception as e:
                await ctx.send(content=locale["economy_getmoney_7"])
        else:
            if getpoint(ctx.author.id, guild=ctx.guild) == -1:
                setpoint(ctx.author.id, 15, guild=ctx.guild)
            else:
                setpoint(
                    ctx.author.id,
                    getpoint(ctx.author.id, guild=ctx.guild) + 2500,
                    guild=ctx.guild,
                )
            await msg.edit(content=locale["economy_getmoney_8"])
    elif i == 6:
        await ctx.channel.send(locale["economy_getmoney_9"])
    elif i == 7:
        await ctx.channel.send(locale["economy_getmoney_10"])
    return


@commands.command(name="남의돈")  # prefix 남의돈 @유저
async def seeothermoney(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if len(ctx.message.mentions) == 0:
        await ctx.channel.send(locale["economy_seeothermoney_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.channel.send(locale["economy_seeothermoney_1"])
        return
    mem = ctx.message.mentions[0]
    if getpoint(mem.id, guild=ctx.guild) == -1:
        setpoint(mem.id, 0, guild=ctx.guild)
    pnt = getpoint(mem.id, guild=ctx.guild)
    await ctx.channel.send(locale["economy_seeothermoney_2"].format(str(mem), str(pnt)))
    return


@commands.command(name="내주식")  # prefix 돈 / prefix 내돈
async def seestk(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    pnt = {}
    for s in ["a", "b", "c"]:
        pnt[s] = getstk(s, ctx.author.id, guild=ctx.guild)
        if pnt[s] == -1:
            setstk(s, ctx.author.id, 0, guild=ctx.guild)
            pnt[s] = 0
    await ctx.channel.send(
        locale["economy_seestk_0"].format(
            ctx.author.mention, str(pnt["a"]), str(pnt["b"]), str(pnt["c"])
        )
    )
    return


@commands.command(name="남의주식")  # prefix 남의돈 @유저
async def seeotherstk(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if len(ctx.message.mentions) == 0:
        await ctx.channel.send(locale["economy_seeotherstk_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.channel.send(locale["economy_seeotherstk_1"])
        return
    mem = ctx.message.mentions[0]
    pnt = {}
    for s in ["a", "b", "c"]:
        pnt[s] = getstk(s, mem.id, guild=ctx.guild)
        if pnt[s] == -1:
            setstk(s, mem.id, 0, guild=ctx.guild)
            pnt[s] = 0
    await ctx.channel.send(
        locale["economy_seeotherstk_2"].format(
            str(mem), str(pnt["a"]), str(pnt["b"]), str(pnt["c"])
        )
    )
    return


@commands.command(name="선물")  # prefix 선물 (money: int) @유저
async def sendmoney(ctx: Context, money: int, *args):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if getpoint(ctx.author.id, guild=ctx.guild) == -1:
        setpoint(ctx.author.id, 0, guild=ctx.guild)
    if money <= 0 or money > getpoint(ctx.author.id, guild=ctx.guild):
        await ctx.channel.send(locale["economy_sendmoney_0"])
        return
    if len(ctx.message.mentions) == 0:
        await ctx.channel.send(locale["economy_sendmoney_1"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.channel.send(locale["economy_sendmoney_2"])
        return
    mem = ctx.message.mentions[0]
    if getpoint(mem.id, guild=ctx.guild) == -1:
        setpoint(mem.id, 0, guild=ctx.guild)
    setpoint(mem.id, getpoint(mem.id, guild=ctx.guild) + money, guild=ctx.guild)
    setpoint(
        ctx.author.id,
        getpoint(ctx.author.id, guild=ctx.guild) - money,
        guild=ctx.guild,
    )
    await ctx.channel.send(locale["economy_sendmoney_3"].format(str(mem), str(money)))
    return


@sendmoney.error
async def sendmoney_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
      if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(locale["economy_sendmoneyerror_0"])
          return
      if isinstance(error, commands.BadArgument):
          await ctx.send(locale["economy_sendmoneyerror_1"])
          return
      tblog(error)
      await ctx.send(locale["economy_sendmoneyerror_2"])
    except:
      return
