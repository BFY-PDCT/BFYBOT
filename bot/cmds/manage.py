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

import discord
from .config import botcolor, muted, bot
from .genfunc import (
    addadmin,
    admincheck,
    deladmin,
    errlog,
    isadmin,
    log,
    dbglog,
    tblog,
    loadsetting,
    savesetting,
    delsetting,
)
from discord.errors import Forbidden, HTTPException
from discord.ext import commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_command(delwelcome)
    bot.add_command(delbye)
    bot.add_command(unsubscribe)
    bot.add_command(getpunishlist)
    bot.add_command(deldefaultrole)
    bot.add_command(cleanchat)
    bot.add_command(setmuterole)
    bot.add_command(setpunish)
    bot.add_command(setdefaultrole)
    bot.add_command(subscribe)
    bot.add_command(setwelcome)
    bot.add_command(setbye)
    bot.add_command(delguildadmin)
    bot.add_command(addguildadmin)
    bot.add_command(execmute)
    bot.add_command(donemute)
    bot.add_command(execkick)
    bot.add_command(execban)
    bot.add_command(addwarning)
    bot.add_command(delwarning)
    bot.add_command(seewarning)


@commands.command(name="환영인사삭제")  # prefix 환영인사삭제
@admincheck()
async def delwelcome(ctx: Context):
    setting_loaded = loadsetting("msgj", guild=ctx.guild)
    if setting_loaded is None:
        await ctx.send("일단 설정하고 말씀하시죠?")
        return
    delsetting("msgj", guild=ctx.guild)
    await ctx.send("환영인사는 이제 없습니다.")
    return


@commands.command(name="작별인사삭제")  # prefix 작별인사삭제
@admincheck()
async def delbye(ctx: Context):
    setting_loaded = loadsetting("msgl", guild=ctx.guild)
    if setting_loaded is None:
        await ctx.send("일단 설정하고 말씀하시죠?")
        return
    delsetting("msgl", guild=ctx.guild)
    await ctx.send("작별인사는 이제 없습니다.")
    return


@commands.command(name="구독해제", aliases=["구독취소"])  # prefix 구독해제 / prefix 구독취소
@admincheck()
async def unsubscribe(ctx: Context):
    setting_loaded = loadsetting("chnl", guild=ctx.guild)
    if setting_loaded is None:
        await ctx.send("구독하지도 않아놓고는 ㅋㅋ")
        return
    delsetting("chnl", guild=ctx.guild)
    await ctx.send("구독해제되었어요 힝 ㅠㅠ")
    return


@commands.command(name="기본역할삭제")  # prefix 기본역할삭제
@admincheck()
async def deldefaultrole(ctx: Context):
    setting_loaded = loadsetting("joinrole", guild=ctx.guild)
    if setting_loaded is None:
        await ctx.send("기본 역할이 설정되지 않았습니다.")
        return
    delsetting("joinrole", guild=ctx.guild)
    await ctx.send("넵^^7")
    return


@commands.command(
    name="치워", aliases=["청소"]
)  # prefix 치워 (cnt: int) / prefix 청소 (cnt: int)
async def cleanchat(ctx: Context, *args):
    def check(m):
        return m.channel == ctx.channel and not m == ctx

    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send("권한도 없으면서 나대긴 ㅋ")
            return
    cnt = 0
    try:
        cnt = int(args[0])
    except IndexError:
        await ctx.send("얼마나 치울지를 알려줘야 치우던가하지")
        return
    except ValueError:
        await ctx.send("숫자가 아닌걸 주시면 어쩌자는겁니까?")
        return
    if cnt <= 0:
        await ctx.send("정상적인 숫자를 좀 주시죠?")
        return
    if cnt > 200:
        await ctx.send("너무 많어 200개이상은 안치움 ㅅㄱ")
        return
    deleted = await ctx.channel.purge(limit=cnt + 1, check=check)
    mymsg = await ctx.send("{}개 치웠어용 히히 칭찬해조".format(len(deleted) - 1))
    """
    log("Deleted Messages (Count: {})".format(len(deleted)), guild=ctx.guild)
    for submsg in deleted:
        dbglog(submsg.content, guild=ctx.guild)
    log("End of Deleted Messages", guild=ctx.guild)
    """
    await mymsg.delete(delay=5)
    return


@commands.command(name="이거로조져", aliases=["뮤트설정"])  # prefix 이거로조져 @역할 / prefix 뮤트설정 @역할
@admincheck()
async def setmuterole(ctx: Context):
    if len(ctx.message.role_mentions) == 0:
        await ctx.send("죄송합니다 역할을 멘션해주세요.")
        return
    if len(ctx.message.role_mentions) > 1:
        await ctx.send("죄송합니다 1개의 역할만을 멘션해주세요.")
        return
    savesetting("role", ctx.guild, ctx.message.role_mentions[0].id)
    await ctx.send("넵^^7")
    return


@commands.command(
    name="처벌설정"
)  # prefix 처벌설정 (cnt: int) (punish: str) (pcnt: int = None)
@admincheck()
async def setpunish(ctx: Context, cnt: int, punish: str, pcnt: int = None, *args):
    if cnt > 11:
        await ctx.send("경고는 최대 10개까지에요.")
        return
    if not punish in ["뮤트", "킥", "밴", "삭제"]:
        await ctx.send("뮤트, 킥, 밴, 삭제 중에서만 선택 가능해요.")
        return
    if punish == "삭제":
        setting_loaded = loadsetting("punish" + str(cnt), guild=ctx.guild)
        if setting_loaded is None:
            delsetting("punish" + str(cnt), guild=ctx.guild)
            await ctx.send("넵^^7")
            return
        await ctx.send("설정이 되어있지 않습니다.")
        return
    if punish == "뮤트":
        if pcnt is None:
            await ctx.send("모든 항목을 입력해주세요.")
            return
        savesetting("mpunish" + str(cnt), ctx.guild, pcnt)
    savesetting("punish" + str(cnt), ctx.guild, punish)
    await ctx.send("넵^^7")
    return


@setpunish.error
async def setpunish_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("관리자가 아니면 못써요 흥")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("뭔가 잘못 입력하신것 같아요,,")
        return
    tblog(error)
    await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    return


@commands.command(name="기본역할")  # prefix 기본역할 @역할
@admincheck()
async def setdefaultrole(ctx: Context):
    if len(ctx.message.role_mentions) == 0:
        await ctx.send("죄송합니다 역할을 멘션해주세요.")
        return
    if len(ctx.message.role_mentions) > 1:
        await ctx.send("죄송합니다 1개의 역할만을 멘션해주세요.")
        return
    savesetting("joinrole", ctx.guild, ctx.message.role_mentions[0].id)
    await ctx.send("넵^^7")
    return


@commands.command(name="구독")  # prefix 구독 #채널
@admincheck()
async def subscribe(ctx: Context):
    if len(ctx.message.channel_mentions) == 0:
        await ctx.send("죄송합니다 채널을 멘션해주세요.")
        return
    if len(ctx.message.channel_mentions) > 1:
        await ctx.send("죄송합니다 1개의 채널만을 멘션해주세요.")
        return
    savesetting("chnl", ctx.guild, ctx.message.channel_mentions[0].id)
    await ctx.send("넵^^7")
    return


@commands.command(name="환영인사")  # prefix 환영인사 (msgj: str)
@admincheck()
async def setwelcome(ctx: Context, *, arg):
    savesetting("msgj", ctx.guild, arg)
    await ctx.send("넵^^7")
    return


@setwelcome.error
async def setwelcome_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("인사말을 입력해주세요.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("관리자가 아니면 못써요 흥")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("뭔가 잘못 입력하신것 같아요,,")
        return
    tblog(error)
    await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    return


@commands.command(name="작별인사")  # prefix 작별인사 (msgl: str)
@admincheck()
async def setbye(ctx: Context, *, arg):
    savesetting("msgl", ctx.guild, arg)
    await ctx.send("넵^^7")
    return


@setbye.error
async def setbye_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("인사말을 입력해주세요.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("관리자가 아니면 못써요 흥")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("뭔가 잘못 입력하신것 같아요,,")
        return
    tblog(error)
    await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    return


@commands.command(name="해방")  # prefix 해방 @유저
@admincheck()
async def delguildadmin(ctx: Context):
    if len(ctx.message.mentions) == 0:
        await ctx.send("죄송합니다 대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    res = deladmin(ctx.message.mentions[0].id, ctx.guild)
    if res == 0:
        await ctx.send(
            "{.mention} 넌이제 내 주인이 아니다 ㅋㅋㅋㅋㅋㅋㅋㅋ".format(ctx.message.mentions[0]),
            allowed_mentions=discord.AllowedMentions.all(),
        )
    elif res == 1:
        await ctx.send("누구세요?")
    elif res == 2:
        await ctx.send("이게 서버주인을 건드리네?")
    elif res == 3:
        await ctx.send("이게 아버지를 건드리네?")
    return


@commands.command(name="새주인")  # prefix 새주인 @유저
@admincheck()
async def addguildadmin(ctx: Context):
    if len(ctx.message.mentions) == 0:
        await ctx.send("죄송합니다 대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    res = addadmin(ctx.message.mentions[0].id, ctx.guild)
    if res:
        await ctx.send(
            "작업완료 ^^7 환영합니다 {.mention} 주인님!".format(ctx.message.mentions[0]),
            allowed_mentions=discord.AllowedMentions.all(),
        )
    else:
        await ctx.send("이미 주인님이십니다.")
    return


@commands.command(
    name="조져", aliases=["뮤트"]
)  # prefix 조져 (time: int) @유저 (rsn: str) / prefix 뮤트 (time: int) @유저 (rsn: str)
async def execmute(ctx: Context, time: int, mention: str, *, arg):
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            await ctx.send("권한도 없으면서 나대긴 ㅋ")
            return
    if len(ctx.message.mentions) == 0:
        await ctx.send("죄송합니다 대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    currole = mem.roles
    setting_loaded = loadsetting("role", ctx.guild)
    if setting_loaded is None:
        await ctx.send("죄송합니다 역할을 지정해주세요.")
        return
    rsn = arg
    try:
        xrole: discord.Role = None
        find = False
        for rl in mem.guild.roles:
            if rl.id == setting_loaded:
                xrole = rl
                find = True
                break
        if not find:
            errlog("role not found", guild=ctx.guild)
            await ctx.send("죄송합니다 역할이 잘못 지정되어 있습니다.")
            return
        await mem.edit(roles=[xrole], reason="MUTE Command REASON: " + rsn)
    except Forbidden:
        errlog("NO PERMISSION", guild=ctx.guild)
        await ctx.send("죄송합니다 권한이 부족합니다.")
        return
    else:
        for mute in muted:
            if mem.id == mute[0] and ctx.guild.id == mute[1]:
                await ctx.send("이미 뮤트처리된 사용자입니다.".format(mem))
                return
        muted.append([mem.id, mem.guild.id, time, currole, ctx.channel.id])
        log("Muted " + mem.name, guild=ctx.guild)
        setting_loaded = loadsetting("chnl", ctx.guild)
        if setting_loaded is not None:
            try:
                await bot.get_channel(setting_loaded).send(
                    "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
            except HTTPException:
                await ctx.send(
                    "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            except Forbidden:
                await ctx.send(
                    "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        else:
            await ctx.send(
                "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
    return


@execmute.error
async def execmute_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("관리자가 아니면 못써요 흥")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("뭔가 잘못 입력하신것 같아요,,")
        return
    tblog(error)
    await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    return


@commands.command(name="충분하다", aliases=["뮤트해제"])  # prefix 충분하다 @유저 / prefix 뮤트해제 @유저
async def donemute(ctx: Context):
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            await ctx.send("권한도 없으면서 나대긴 ㅋ")
            return
    if len(ctx.message.mentions) == 0:
        await ctx.send("죄송합니다 대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    udmute = bot.get_cog("updatemute")
    if udmute is not None:
        res = await udmute.unmutenow(ctx)
    else:
        await ctx.send("문제가 있었어요,, 관리자한테 문의해주세요 ㅠㅠ")
        return
    if not res:
        await ctx.send("문제가 있었어요,, 아마 뮤트를 한적이 없는거 아닐까요..?")
        return
    return


@donemute.error
async def donemute_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("관리자가 아니면 못써요 흥")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("뭔가 잘못 입력하신것 같아요,,")
        return
    tblog(error)
    await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    return


@commands.command(name="킥")  # prefix 킥 @유저 (rsn: str)
async def execkick(ctx: Context, mention: str, *, arg):
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).kick_members:
            await ctx.send("권한도 없으면서 나대긴 ㅋ")
            return
    if len(ctx.message.mentions) == 0:
        await ctx.send("대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    rsn = arg
    setting_loaded = loadsetting("chnl", ctx.guild)
    try:
        await ctx.guild.kick(mem, reason="KICK Command REASON: " + rsn)
    except Forbidden:
        errlog("NO PERMISSION", guild=ctx.guild)
        await ctx.send("권한이 부족합니다.")
        return
    if setting_loaded is not None:
        try:
            await bot.get_channel(setting_loaded).send(
                "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
        except HTTPException:
            await ctx.send(
                "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
            await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        except Forbidden:
            await ctx.send(
                "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
            await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
    else:
        await ctx.send(
            "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                mem, rsn, ctx.author
            )
        )
    return


@execkick.error
async def execkick_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("관리자가 아니면 못써요 흥")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("뭔가 잘못 입력하신것 같아요,,")
        return
    tblog(error)
    await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    return


@commands.command(name="밴")
async def execban(ctx, mention: str, *, arg):  # prefix 밴 @유저 (rsn: str)
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).ban_members:
            await ctx.send("권한도 없으면서 나대긴 ㅋ")
            return
    if len(ctx.message.mentions) == 0:
        await ctx.send("대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    rsn = arg
    setting_loaded = loadsetting("chnl", ctx.guild)
    try:
        await ctx.guild.ban(mem, reason="BAN Command REASON: " + rsn)
    except Forbidden:
        errlog("NO PERMISSION", guild=ctx.guild)
        await ctx.send("권한이 부족합니다.")
        return
    if setting_loaded is not None:
        try:
            await bot.get_channel(setting_loaded).send(
                "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
        except HTTPException:
            await ctx.send(
                "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
            await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        except Forbidden:
            await ctx.send(
                "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
            await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
    else:
        await ctx.send(
            "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                mem, rsn, ctx.author
            )
        )
    return


@execban.error
async def execban_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("관리자가 아니면 못써요 흥")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("뭔가 잘못 입력하신것 같아요,,")
        return
    tblog(error)
    await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    return


@commands.command(name="경고")  # prefix 경고 @유저 (rsn: str)
@admincheck()
async def addwarning(ctx: Context, mention: str, *, arg):
    time = 0
    if len(ctx.message.mentions) == 0:
        await ctx.send("대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    rsn = arg
    warns = 0
    currole = mem.roles
    setting = loadsetting("chnl", ctx.guild)
    mutes = loadsetting("warn" + str(mem.id), ctx.guild)
    if mutes is not None:
        savesetting("warn" + str(mem.id), ctx.guild, mutes + 1)
        warns = mutes + 1
    else:
        savesetting("warn" + str(mem.id), ctx.guild, 1)
        warns = 1
    ptype = loadsetting("punish" + str(warns), ctx.guild)
    if ptype == "킥":
        try:
            await ctx.guild.kick(mem, reason="KICK Command REASON: " + rsn)
        except Forbidden:
            errlog("NO PERMISSION", guild=ctx.guild)
            await ctx.send("권한이 부족합니다.")
            return
        if setting is not None:
            try:
                await bot.get_channel(setting).send(
                    "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
            except HTTPException:
                await ctx.send(
                    "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            except Forbidden:
                await ctx.send(
                    "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        else:
            await ctx.send(
                "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
    elif ptype == "밴":
        try:
            await ctx.guild.ban(mem, reason="BAN Command REASON: " + rsn)
        except Forbidden:
            errlog("NO PERMISSION", guild=ctx.guild)
            await ctx.send("권한이 부족합니다.")
            return
        if setting is not None:
            try:
                await bot.get_channel(setting).send(
                    "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
            except HTTPException:
                await ctx.send(
                    "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            except Forbidden:
                await ctx.send(
                    "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        else:
            await ctx.send(
                "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
    elif ptype == "뮤트":
        time = loadsetting("mpunish" + str(warns), ctx.guild)
        try:
            xrole: discord.Role = None
            find = False
            for rl in mem.guild.roles:
                if rl.id == loadsetting("role" + str(warns), ctx.guild):
                    xrole = rl
                    find = True
                    break
            if not find:
                errlog("role not found", guild=ctx.guild)
                await ctx.send("죄송합니다 역할이 잘못 지정되어 있습니다.")
                return
            await mem.edit(roles=[xrole], reason="MUTE Command REASON: " + rsn)
        except Forbidden:
            errlog("NO PERMISSION", guild=ctx.guild)
            await ctx.send("죄송합니다 권한이 부족합니다.")
            return
        else:
            for mute in muted:
                if mem.id == mute[0] and ctx.guild.id == mute[1]:
                    await ctx.send("이미 뮤트처리된 사용자입니다.".format(mem))
                    return
            muted.append([mem.id, mem.guild.id, time, currole, ctx.channel.id])
            log("Muted " + mem.name, guild=ctx.guild)
            setting_loaded = loadsetting("chnl", ctx.guild)
            if setting_loaded is not None:
                try:
                    await bot.get_channel(setting_loaded).send(
                        "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                            mem, rsn, ctx.author
                        )
                    )
                except HTTPException:
                    await ctx.send(
                        "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                            mem, rsn, ctx.author
                        )
                    )
                    await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
                except Forbidden:
                    await ctx.send(
                        "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                            mem, rsn, ctx.author
                        )
                    )
                    await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            else:
                await ctx.send(
                    "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
    setting_loaded = loadsetting("chnl", ctx.guild)
    if setting_loaded is not None:
        try:
            await bot.get_channel(setting_loaded).send(
                "처리 완료되었습니다 - 경고 {.mention} 누적경고수 {} / 이유: {} / 처리자: {.mention}".format(
                    mem, warns, rsn, ctx.author
                )
            )
        except HTTPException:
            await ctx.send(
                "처리 완료되었습니다 - 경고 {.mention} 누적경고수 {} / 이유: {} / 처리자: {.mention}".format(
                    mem, warns, rsn, ctx.author
                )
            )
            await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        except Forbidden:
            await ctx.send(
                "처리 완료되었습니다 - 경고 {.mention} 누적경고수 {} / 이유: {} / 처리자: {.mention}".format(
                    mem, warns, rsn, ctx.author
                )
            )
            await ctx.send("구독 설정에 오류가 있습니다. 수정해주세요.")
    else:
        await ctx.send(
            "처리 완료되었습니다 - 경고 {.mention} 누적경고수 {} / 이유: {} / 처리자: {.mention}".format(
                mem, warns, rsn, ctx.author
            )
        )
    return


@addwarning.error
async def addwarning_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send("관리자가 아니면 못써요 흥")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("뭔가 잘못 입력하신것 같아요,,")
        return
    tblog(error)
    await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
    return


@commands.command(name="경고취소")  # prefix 경고취소 @유저
async def delwarning(ctx: Context):
    if not isadmin(ctx.author.id, ctx.guild):
        await ctx.send("권한도 없으면서 나대긴 ㅋ")
        return
    if len(ctx.message.mentions) == 0:
        await ctx.send("대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    setting_loaded = loadsetting("warn" + str(mem.id), guild=ctx.guild)
    if setting_loaded is None or setting_loaded == 0:
        await ctx.send("경고가 없습니다.")
    else:
        savesetting("warn" + str(mem.id), ctx.guild, setting_loaded - 1)
        await ctx.send("넵^^7 (누적 경고수: " + str(setting_loaded - 1) + ")")
    return


@commands.command(name="처벌정책")  # prefix 처벌정책
async def getpunishlist(ctx: Context):
    strs = []
    for i in range(1, 11):
        ptype = loadsetting("punish" + str(i), ctx.guild)
        if ptype is not None:
            if ptype == "뮤트":
                pcnt = loadsetting("mpunish" + str(i), ctx.guild)
                strs.append("경고 " + str(i) + "회시 뮤트 " + str(pcnt) + "초")
            elif ptype == "킥":
                strs.append("경고 " + str(i) + "회시 킥")
            elif ptype == "밴":
                strs.append("경고 " + str(i) + "회시 밴")
    embed = discord.Embed(title="처벌 정책", color=botcolor)
    tmp = ""
    if len(strs) == 0:
        tmp = "처벌 정책이 없습니다."
    elif len(strs) == 1:
        tmp = strs[0]
    else:
        for i in range(0, len(strs) - 1):
            tmp += strs[i] + "\n"
        tmp += strs[len(strs) - 1]
    embed.description = tmp
    await ctx.send("서버의 처벌 정책입니다.", embed=embed)
    return


@commands.command(name="경고횟수")  # prefix 경고횟수 @유저
async def seewarning(ctx: Context):
    if len(ctx.message.mentions) == 0:
        await ctx.send("대상자를 멘션해주세요.")
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    setting_loaded = loadsetting("warn" + str(mem.id), guild=ctx.guild)
    warns = 0
    if setting_loaded is not None:
        warns = setting_loaded
    else:
        warns = 0
    await ctx.send("{0} 님의 현재 누적 경고 수는 ".format(str(mem)) + str(warns) + "회 입니다.")
    return
