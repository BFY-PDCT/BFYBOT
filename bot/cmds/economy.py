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
from .genfunc import errlog, getpoint, log, setpoint, getstk, setstk, getrecstk
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
    pnt = getpoint(ctx.author.id, guild=ctx.guild)
    if pnt == -1:
        setpoint(ctx.author.id, 0, guild=ctx.guild)
        pnt = 0
    await ctx.channel.send(
        "{.author.mention} 니가 가진 돈은 이만큼이다 알았나 `💰 ".format(ctx) + str(pnt) + "`"
    )
    return


@commands.command(name="돈내놔")  # prefix 돈내놔
async def getmoney(ctx: Context):
    def check(m):
        return (
            m.content == botname + " 형님"
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
        await ctx.channel.send("어휴 불쌍한넘 내가 특별히 1000포인트 준다 `💰+1000`")
    elif i == 2:
        await ctx.channel.send("싫은뒈~~에베ㅔㅔ")
    elif i == 3:
        await ctx.channel.send("뭐래 ㅋㅋ")
    elif i == 4:
        if getpoint(ctx.author.id, guild=ctx.guild) == -1:
            setpoint(ctx.author.id, 1, guild=ctx.guild)
        else:
            setpoint(
                ctx.author.id,
                getpoint(ctx.author.id, guild=ctx.guild) + 100,
                guild=ctx.guild,
            )
        await ctx.channel.send("가져가서 어디 써보시던가 ㅋㅋ `💰+100`")
    elif i == 5:
        msg = await ctx.channel.send(botname + " 형님 해봐")
        try:
            await bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await msg.edit(content="자존심만 높아서는 ㅉㅉ")
        else:
            if getpoint(ctx.author.id, guild=ctx.guild) == -1:
                setpoint(ctx.author.id, 15, guild=ctx.guild)
            else:
                setpoint(
                    ctx.author.id,
                    getpoint(ctx.author.id, guild=ctx.guild) + 2500,
                    guild=ctx.guild,
                )
            await msg.edit(content="옳지 잘한다 옛다 선물 `💰+2500`")
    elif i == 6:
        await ctx.channel.send("내가 니한테 돈을 왜주냐?")
    elif i == 7:
        await ctx.channel.send("ㄲㅈ")
    return


@commands.command(name="남의돈")  # prefix 남의돈 @유저
async def seeothermoney(ctx: Context):
    if len(ctx.message.mentions) == 0:
        log("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        log("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    if getpoint(mem.id, guild=ctx.guild) == -1:
        setpoint(mem.id, 0, guild=ctx.guild)
    pnt = getpoint(mem.id, guild=ctx.guild)
    await ctx.channel.send(
        "{} 이 친구가 가진 돈은 이만큼이다 알았나 `💰 ".format(str(mem)) + str(pnt) + "`"
    )
    return


@commands.command(name="내주식")  # prefix 돈 / prefix 내돈
async def seestk(ctx: Context):
    pnt = {}
    for s in ["a", "b", "c"]:
        pnt[s] = getstk(s, ctx.author.id, guild=ctx.guild)
        if pnt[s] == -1:
            setstk(s, ctx.author.id, 0, guild=ctx.guild)
            pnt[s] = 0
    await ctx.channel.send(
        "{.author.mention} 니가 가진 주식은 이만큼이다 A: {}주 / B: {}주 / C: {}주".format(
            ctx, str(pnt["a"]), str(pnt["b"]), str(pnt["c"])
        )
    )
    return


@commands.command(name="남의주식")  # prefix 남의돈 @유저
async def seeotherstk(ctx: Context):
    if len(ctx.message.mentions) == 0:
        log("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        log("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    pnt = {}
    for s in ["a", "b", "c"]:
        pnt[s] = getstk(s, mem.id, guild=ctx.guild)
        if pnt[s] == -1:
            setstk(s, mem.id, 0, guild=ctx.guild)
            pnt[s] = 0
    await ctx.channel.send(
        "{} 니가 가진 주식은 이만큼이다 A: {}주 / B: {}주 / C: {}주".format(
            str(mem), str(pnt["a"]), str(pnt["b"]), str(pnt["c"])
        )
    )
    return


@commands.command(name="선물")  # prefix 선물 (money: int) @유저
async def sendmoney(ctx: Context, money: int, *args):
    if getpoint(ctx.author.id, guild=ctx.guild) == -1:
        setpoint(ctx.author.id, 0, guild=ctx.guild)
    if money <= 0 or money > getpoint(ctx.author.id, guild=ctx.guild):
        await ctx.channel.send("선물할 수 없는 금액입니다.")
        return
    if len(ctx.message.mentions) == 0:
        await ctx.channel.send("대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.channel.send("1명의 대상자만을 멘션해주세요.")
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
    await ctx.channel.send("{0}님에게 `💰 ".format(str(mem)) + str(money) + "`을(를) 선물했습니다.")
    return


@sendmoney.error
async def sendmoney_error(ctx: Context, error):
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("금액을 올바르게 입력해주세요.")
            return
        errlog(error)
        await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    except:
        return
