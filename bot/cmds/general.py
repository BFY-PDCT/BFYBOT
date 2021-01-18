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

import discord, urllib.request, urllib.parse
from urllib.parse import quote
from .config import (
    invlink,
    vernum,
    botname,
    hasmusic,
    botcolor,
    bot,
    musicstr,
    helpmusicstr,
)
from .genfunc import calculate, errlog, log
from discord.ext import commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_command(ping)
    bot.add_command(version)
    bot.add_command(help)
    bot.add_command(lolsearch)
    bot.add_command(docalculate)


@commands.command(name="핑")  # prefix 핑
async def ping(ctx: Context):
    await ctx.send(f"퐁 ^^ {round(round(bot.latency, 4)*1000)}ms")


@commands.command(name="버전")  # prefix 버전
async def version(ctx: Context):
    ver = discord.Embed(title=botname + " 버전", color=botcolor)
    ver.add_field(name="현재 버전", value=vernum, inline=False)
    ver.add_field(name="discord.py version", value=discord.__version__, inline=False)
    ver.add_field(name="제작자", value="BFY Ent (jhlee@bfy.kr)", inline=False)
    ver.add_field(name="서버 상태 확인", value="https://bfy1.statuspage.io/", inline=False)
    ver.set_footer(
        text="Developed by BFY using discord.py",
        icon_url="https://www.bfy.kr/files/2020/08/BFY_LOGO_BIG.png",
    )
    if hasmusic:
        ver.add_field(
            name=botname + "의 음악 기능",
            value=musicstr,
            inline=False,
        )
    await ctx.channel.send(botname + " 버전 정보입니다", embed=ver)
    return


@commands.command(name="도움말")  # prefix 도움말
async def help(ctx: Context):
    ver = discord.Embed(title=botname + " 사용 방법", color=botcolor)
    ver.add_field(name="도움말 (온라인)", value="https://www.bfy.kr/bluebot/", inline=False)
    if hasmusic:
        ver.add_field(name="음악 도움말", value=helpmusicstr, inline=False)
    ver.add_field(
        name="문의",
        value="봇에게 DM을 보내주시면 메시지가 운영자에게 전달됩니다.\n홈페이지: https://www.bfy.kr/ 개발자이메일: jhlee@bfy.kr\n개발자 디스코드: KRMSS#9279",
        inline=False,
    )
    ver.add_field(name="초대", value=invlink, inline=False)
    await ctx.author.send(botname + "한테 명령하는 방법입니다", embed=ver)
    await ctx.add_reaction("👍")
    return


@commands.command(name="전적검색")  # prefix 전적검색 (lolid: str)
async def lolsearch(ctx: Context, *, arg):
    lolid = arg
    url = "https://www.op.gg/summoner/userName=" + quote(lolid)
    log("querying " + url)
    subres = urllib.request.urlopen(url).read().decode("utf-8")
    tmp = subres[
        subres.find('<meta name="description" content="')
        + len('<meta name="description" content="') :
    ]
    res = tmp[: tmp.find('"/>')]
    reslist = res.split(" / ")
    tmp2 = subres[subres.find('<div class="ProfileIcon">') :]
    tmp3 = tmp2[tmp2.find('<img src="') + len('<img src="') :]
    res2 = tmp3[: tmp3.find('"')]
    res3 = "https:" + res2
    log("res3: " + res3)
    msgtos = discord.Embed(color=botcolor)
    try:
        msgtos.set_author(name=reslist[0], icon_url=res3)
        msgtos.add_field(name="티어", value=reslist[1], inline=False)
        msgtos.add_field(name="최근승률", value=reslist[2], inline=False)
        msgtos.add_field(name="최근 챔피언", value=reslist[3], inline=False)
        msgtos.set_footer(text="데이터 제공: op.gg")
    except IndexError:
        errlog("failed querying " + url)
        msgtos.clear_fields()
        msgtos.set_author(name=lolid)
        msgtos.description = "검색에 실패하였습니다."
        msgtos.set_footer(text="데이터 제공: op.gg")
    else:
        pass
    await ctx.channel.send("전적 검색 결과입니다", embed=msgtos)
    return


@lolsearch.error
async def lolsearch_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("닉네임을 입력해주세요.")
        return


@commands.command(name="계산", aliases=["계산해"])  # prefix 계산해 (inputstr: str)
async def docalculate(ctx: Context, *, arg):
    inputstr = arg
    await ctx.channel.send(
        "계산 결과는 " + str(calculate(inputstr)) + "입니다! (이상하면 너가 이상한식 넣은거임)"
    )
    return


@docalculate.error
async def docalculate_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("계산할 식을 입력해주세요.")
        return
