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

import discord, asyncio
from .config import botcolor, using, muted, bot
from .genfunc import (
    addadmin,
    admincheck,
    deladmin,
    errlog,
    isadmin,
    loadfile,
    log,
    msglog,
    savefile,
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
    bot.add_command(execkick)
    bot.add_command(execban)
    bot.add_command(addwarning)
    bot.add_command(delwarning)
    bot.add_command(seewarning)


@commands.command(name="환영인사삭제")  # prefix 환영인사삭제
@admincheck()
async def delwelcome(ctx: Context):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if "msgj" in setting_loaded:
        del setting_loaded["msgj"]
        savefile("setting", setting_loaded, guild=ctx.guild)
        await ctx.channel.send("환영인사는 이제 없습니다.")
        return
    else:
        await ctx.channel.send("일단 설정하고 말씀하시죠?")
        return


@commands.command(name="작별인사삭제")  # prefix 작별인사삭제
@admincheck()
async def delbye(ctx: Context):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if "msgl" in setting_loaded:
        del setting_loaded["msgl"]
        savefile("setting", setting_loaded, guild=ctx.guild)
        await ctx.channel.send("작별인사는 이제 없습니다.")
        return
    else:
        await ctx.channel.send("일단 설정하고 말씀하시죠?")
        return


@commands.command(name="구독해제", aliases=["구독취소"])  # prefix 구독해제 / prefix 구독취소
@admincheck()
async def unsubscribe(ctx: Context):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if "chnl" in setting_loaded:
        del setting_loaded["chnl"]
        savefile("setting", setting_loaded, guild=ctx.guild)
        await ctx.channel.send("구독해제되었어요 힝 ㅠㅠ")
        return
    else:
        await ctx.channel.send("구독하지도 않아놓고는 ㅋㅋ")
        return


@commands.command(name="기본역할삭제")  # prefix 기본역할삭제
@admincheck()
async def deldefaultrole(ctx: Context):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if not "joinrole" in setting_loaded:
        await ctx.channel.send("기본 역할이 설정되지 않았습니다.")
        return
    del setting_loaded["joinrole"]
    savefile("setting", setting_loaded, guild=ctx.guild)
    await ctx.channel.send("넵^^7")
    return


@commands.command(
    name="치워", aliases=["청소"]
)  # prefix 치워 (cnt: int) / prefix 청소 (cnt: int)
async def cleanchat(ctx: Context, *args):
    def check(m):
        return m.channel == ctx.channel and not m == ctx

    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.channel.send("권한도 없으면서 나대긴 ㅋ")
            using.remove(ctx.author.id)
            return
    cnt = 0
    try:
        cnt = int(args[0])
    except IndexError:
        await ctx.channel.send("얼마나 치울지를 알려줘야 치우던가하지")
        using.remove(ctx.author.id)
        return
    except ValueError:
        await ctx.channel.send("숫자가 아닌걸 주시면 어쩌자는겁니까?")
        using.remove(ctx.author.id)
        return
    if cnt <= 0:
        await ctx.channel.send("정상적인 숫자를 좀 주시죠?")
        using.remove(ctx.author.id)
        return
    if cnt > 200:
        await ctx.channel.send("너무 많어 200개이상은 안치움 ㅅㄱ")
        using.remove(ctx.author.id)
        return
    deleted = await ctx.channel.purge(limit=cnt + 1, check=check)
    mymsg = await ctx.channel.send("{}개 치웠어용 히히 칭찬해조".format(len(deleted) - 1))
    log("Deleted Messages (Count: {})".format(len(deleted)), guild=ctx.guild)
    for submsg in deleted:
        msglog(submsg, guild=ctx.guild)
    log("End of Deleted Messages", guild=ctx.guild)
    await mymsg.delete(delay=5)
    return


@commands.command(name="이거로조져", aliases=["뮤트설정"])  # prefix 이거로조져 @역할 / prefix 뮤트설정 @역할
@admincheck()
async def setmuterole(ctx: Context):
    if len(ctx.message.role_mentions) == 0:
        errlog("no mentions for role", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 역할을 멘션해주세요.")
        return
    elif len(ctx.message.role_mentions) > 1:
        errlog("so many mentions for role", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 1개의 역할만을 멘션해주세요.")
        return
    else:
        setting_loaded = loadfile("setting", guild=ctx.guild)
        setting_loaded["role"] = ctx.message.role_mentions[0].id
        savefile("setting", setting_loaded, guild=ctx.guild)
        await ctx.channel.send("넵^^7")
        return


@commands.command(
    name="처벌설정"
)  # prefix 처벌설정 (cnt: int) (punish: str) (pcnt: int = None)
@admincheck()
async def setpunish(ctx: Context, cnt: int, punish: str, pcnt: int = None, *args):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if punish == "삭제":
        if "punish" + str(cnt) in setting_loaded:
            del setting_loaded["punish" + str(cnt)]
            savefile("setting", setting_loaded, guild=ctx.guild)
            await ctx.channel.send("넵^^7")
            using.remove(ctx.author.id)
            return
        else:
            await ctx.channel.send("설정이 되어있지 않습니다.")
            using.remove(ctx.author.id)
            return
    if punish == "뮤트":
        if pcnt is None:
            await ctx.send("모든 항목을 입력해주세요.")
            return
        setting_loaded["mpunish" + str(cnt)] = pcnt
    setting_loaded["punish" + str(cnt)] = punish
    savefile("setting", setting_loaded, guild=ctx.guild)
    await ctx.channel.send("넵^^7")
    return


@setpunish.error
async def setpunish_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return


@commands.command(name="기본역할")  # prefix 기본역할 @역할
@admincheck()
async def setdefaultrole(ctx: Context):
    if len(ctx.message.role_mentions) == 0:
        errlog("no mentions for role", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 역할을 멘션해주세요.")
        return
    elif len(ctx.message.role_mentions) > 1:
        errlog("so many mentions for role", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 1개의 역할만을 멘션해주세요.")
        return
    setting_loaded = loadfile("setting", guild=ctx.guild)
    setting_loaded["joinrole"] = ctx.message.role_mentions[0].id
    savefile("setting", setting_loaded, guild=ctx.guild)
    await ctx.channel.send("넵^^7")
    return


@commands.command(name="구독")  # prefix 구독 #채널
@admincheck()
async def subscribe(ctx: Context):
    if len(ctx.message.channel_mentions) == 0:
        errlog("no mentions for channel", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 채널을 멘션해주세요.")
        return
    elif len(ctx.message.channel_mentions) > 1:
        errlog("so many mentions for channel", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 1개의 채널만을 멘션해주세요.")
        return
    else:
        setting_loaded = loadfile("setting", guild=ctx.guild)
        setting_loaded["chnl"] = ctx.message.channel_mentions[0].id
        savefile("setting", setting_loaded, guild=ctx.guild)
        await ctx.channel.send("넵^^7")
        return


@commands.command(name="환영인사")  # prefix 환영인사 (msgj: str)
@admincheck()
async def setwelcome(ctx: Context, *, arg):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    setting_loaded["msgj"] = arg
    savefile("setting", setting_loaded, guild=ctx.guild)
    await ctx.channel.send("넵^^7")
    return


@setwelcome.error
async def setwelcome_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("인사말을 입력해주세요.")
        return


@commands.command(name="작별인사")  # prefix 작별인사 (msgl: str)
@admincheck()
async def setbye(ctx: Context, *, arg):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    setting_loaded["msgl"] = arg
    savefile("setting", setting_loaded, guild=ctx.guild)
    await ctx.channel.send("넵^^7")
    return


@setbye.error
async def setbye_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("인사말을 입력해주세요.")
        return


@commands.command(name="해방")  # prefix 해방 @유저
@admincheck()
async def delguildadmin(ctx: Context):
    if len(ctx.message.mentions) == 0:
        errlog("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 대상자를 멘션해주세요.")
        return
    elif len(ctx.message.mentions) > 1:
        errlog("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    else:
        res = deladmin(ctx.message.mentions[0].id, ctx.guild)
        if res == 0:
            await ctx.channel.send(
                "{.mention} 넌이제 내 주인이 아니다 ㅋㅋㅋㅋㅋㅋㅋㅋ".format(ctx.message.mentions[0]),
                allowed_mentions=discord.AllowedMentions.all(),
            )
        elif res == 1:
            await ctx.channel.send("누구세요?")
        elif res == 2:
            await ctx.channel.send("이게 서버주인을 건드리네?")
        elif res == 3:
            await ctx.channel.send("이게 아버지를 건드리네?")
        return


@commands.command(name="새주인")  # prefix 새주인 @유저
@admincheck()
async def addguildadmin(ctx: Context):
    if len(ctx.message.mentions) == 0:
        errlog("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 대상자를 멘션해주세요.")
        return
    elif len(ctx.message.mentions) > 1:
        errlog("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    else:
        res = addadmin(ctx.message.mentions[0].id, ctx.guild)
        if res:
            await ctx.channel.send(
                "작업완료 ^^7 환영합니다 {.mention} 주인님!".format(ctx.message.mentions[0]),
                allowed_mentions=discord.AllowedMentions.all(),
            )
        else:
            await ctx.channel.send("이미 주인님이십니다.")
        return


@commands.command(
    name="조져", aliases=["뮤트"]
)  # prefix 조져 (time: int) @유저 (rsn: str) / prefix 뮤트 (time: int) @유저 (rsn: str)
async def execmute(ctx: Context, time: int, mention: str, *, arg):
    def checkd(m):
        if len(m.mentions) == 0:
            return False
        return (
            m.content.startswith("이만하면 충분하다")
            and m.channel == ctx.channel
            and m.author == ctx.author
            and m.mentions[0] == ctx.message.mentions[0]
        )

    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            await ctx.channel.send("권한도 없으면서 나대긴 ㅋ")
            return
    if len(ctx.message.mentions) == 0:
        errlog("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 대상자를 멘션해주세요.")
        return
    elif len(ctx.message.mentions) > 1:
        errlog("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    currole = mem.roles
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if not "role" in setting_loaded:
        errlog("no role setted", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 역할을 지정해주세요.")
        return
    rsn = arg
    try:
        xrole: discord.Role = None
        find = False
        for rl in mem.guild.roles:
            if rl.id == setting_loaded["role"]:
                xrole = rl
                find = True
                break
        if not find:
            errlog("role not found", guild=ctx.guild)
            await ctx.channel.send("죄송합니다 역할이 잘못 지정되어 있습니다.")
            return
        await mem.edit(roles=[xrole], reason="MUTE Command REASON: " + rsn)
    except Forbidden:
        errlog("NO PERMISSION", guild=ctx.guild)
        await ctx.channel.send("죄송합니다 권한이 부족합니다.")
        return
    else:
        if mem.id in muted:
            await ctx.channel.send("이미 뮤트처리된 사용자입니다.".format(mem))
            return
        muted.append(mem.id)
        log("Muted " + mem.name, guild=ctx.guild)
        setting_loaded = loadfile("setting", guild=ctx.guild)
        if "chnl" in setting_loaded:
            try:
                await bot.get_channel(setting_loaded["chnl"]).send(
                    "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
            except HTTPException:
                await ctx.channel.send(
                    "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            except Forbidden:
                await ctx.channel.send(
                    "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        else:
            await ctx.channel.send(
                "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
        try:
            await bot.wait_for("message", timeout=time, check=checkd)
        except asyncio.TimeoutError:
            await mem.edit(roles=currole, reason="MUTE Command Timeout")
            log("Unmuted " + mem.name, guild=ctx.guild)
            if "chnl" in setting_loaded:
                try:
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "처리 종료되었습니다 - 뮤트 {.mention}".format(mem)
                    )
                except HTTPException:
                    await ctx.channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(mem))
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
                except Forbidden:
                    await ctx.channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(mem))
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            else:
                await ctx.channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(mem))
            muted.remove(mem.id)
        else:
            await mem.edit(roles=currole, reason="MUTE Command Cancel")
            log("Unmuted " + mem.name, guild=ctx.guild)
            if "chnl" in setting_loaded:
                try:
                    await ctx.channel.send("예 형님 종료하겠습니다 - 뮤트 {.mention}".format(mem))
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "처리 종료되었습니다 - 뮤트 {.mention}".format(mem)
                    )
                except HTTPException:
                    await ctx.channel.send("예 형님 종료하겠습니다 - 뮤트 {.mention}".format(mem))
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
                except Forbidden:
                    await ctx.channel.send("예 형님 종료하겠습니다 - 뮤트 {.mention}".format(mem))
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            else:
                await ctx.channel.send("예 형님 종료하겠습니다 - 뮤트 {.mention}".format(mem))
            muted.remove(mem.id)
        return


@execmute.error
async def execmute_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return


@commands.command(name="킥")  # prefix 킥 @유저 (rsn: str)
async def execkick(ctx: Context, mention: str, *, arg):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).kick_members:
            await ctx.channel.send("권한도 없으면서 나대긴 ㅋ")
            return
    if len(ctx.message.mentions) == 0:
        errlog("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("대상자를 멘션해주세요.")
        return
    elif len(ctx.message.mentions) > 1:
        errlog("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    rsn = arg
    try:
        await ctx.guild.kick(mem, reason="KICK Command REASON: " + rsn)
    except Forbidden:
        errlog("NO PERMISSION", guild=ctx.guild)
        await ctx.channel.send("권한이 부족합니다.")
        return
    if "chnl" in setting_loaded:
        try:
            await bot.get_channel(setting_loaded["chnl"]).send(
                "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
        except HTTPException:
            await ctx.channel.send(
                "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
            await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        except Forbidden:
            await ctx.channel.send(
                "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
            await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
    else:
        await ctx.channel.send(
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


@commands.command(name="밴")
async def execban(ctx, mention: str, *, arg):  # prefix 밴 @유저 (rsn: str)
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).ban_members:
            await ctx.channel.send("권한도 없으면서 나대긴 ㅋ")
            return
    if len(ctx.message.mentions) == 0:
        errlog("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("대상자를 멘션해주세요.")
        return
    elif len(ctx.message.mentions) > 1:
        errlog("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    rsn = arg
    try:
        await ctx.guild.ban(mem, reason="BAN Command REASON: " + rsn)
    except Forbidden:
        errlog("NO PERMISSION", guild=ctx.guild)
        await ctx.channel.send("권한이 부족합니다.")
        return
    if "chnl" in setting_loaded:
        try:
            await bot.get_channel(setting_loaded["chnl"]).send(
                "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
        except HTTPException:
            await ctx.channel.send(
                "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
            await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        except Forbidden:
            await ctx.channel.send(
                "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
            await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
    else:
        await ctx.channel.send(
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


@commands.command(name="경고")  # prefix 경고 @유저 (rsn: str)
@admincheck()
async def addwarning(ctx: Context, mention: str, *, arg):
    def checkd(m):
        if len(m.mentions) == 0:
            return False
        return (
            m.content.startswith("이만하면 충분하다")
            and m.channel == ctx.channel
            and m.author == ctx.author
            and m.mentions[0] == ctx.message.mentions[0]
        )

    setting_loaded = loadfile("setting", guild=ctx.guild)
    time = 0
    if len(ctx.message.mentions) == 0:
        errlog("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("대상자를 멘션해주세요.")
        return
    elif len(ctx.message.mentions) > 1:
        errlog("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    rsn = arg
    warns = 0
    currole = mem.roles
    if "warn" + str(mem.id) in setting_loaded:
        setting_loaded["warn" + str(mem.id)] += 1
        warns = setting_loaded["warn" + str(mem.id)]
    else:
        setting_loaded["warn" + str(mem.id)] = 1
        warns = 1
    savefile("setting", setting_loaded, guild=ctx.guild)
    if setting_loaded["punish" + str(warns)] == "킥":
        try:
            await ctx.guild.kick(mem, reason="KICK Command REASON: " + rsn)
        except Forbidden:
            errlog("NO PERMISSION", guild=ctx.guild)
            await ctx.channel.send("권한이 부족합니다.")
            return
        if "chnl" in setting_loaded:
            try:
                await bot.get_channel(setting_loaded["chnl"]).send(
                    "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
            except HTTPException:
                await ctx.channel.send(
                    "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            except Forbidden:
                await ctx.channel.send(
                    "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        else:
            await ctx.channel.send(
                "처리 완료되었습니다 - 킥 {.mention} / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
    elif setting_loaded["punish" + str(warns)] == "밴":
        try:
            await ctx.guild.ban(mem, reason="BAN Command REASON: " + rsn)
        except Forbidden:
            errlog("NO PERMISSION", guild=ctx.guild)
            await ctx.channel.send("권한이 부족합니다.")
            return
        if "chnl" in setting_loaded:
            try:
                await bot.get_channel(setting_loaded["chnl"]).send(
                    "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
            except HTTPException:
                await ctx.channel.send(
                    "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            except Forbidden:
                await ctx.channel.send(
                    "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
                await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        else:
            await ctx.channel.send(
                "처리 완료되었습니다 - 밴 {.mention}, 최근 1일 메시지 삭제 / 이유: {} / 처리자: {.mention}".format(
                    mem, rsn, ctx.author
                )
            )
    elif setting_loaded["punish" + str(warns)] == "뮤트":
        time = setting_loaded["mpunish" + str(warns)]
        try:
            xrole: discord.Role = None
            find = False
            for rl in mem.guild.roles:
                if rl.id == setting_loaded["role"]:
                    xrole = rl
                    find = True
                    break
            if not find:
                errlog("role not found", guild=ctx.guild)
                await ctx.channel.send("죄송합니다 역할이 잘못 지정되어 있습니다.")
                return
            await mem.edit(roles=[xrole], reason="MUTE Command REASON: " + rsn)
        except Forbidden:
            errlog("NO PERMISSION", guild=ctx.guild)
            await ctx.channel.send("죄송합니다 권한이 부족합니다.")
            return
        else:
            if mem.id in muted:
                await ctx.channel.send("이미 뮤트처리된 사용자입니다.".format(mem))
                return
            muted.append(mem.id)
            log("Muted " + mem.name, guild=ctx.guild)
            setting_loaded = loadfile("setting", guild=ctx.guild)
            if "chnl" in setting_loaded:
                try:
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                            mem, rsn, ctx.author
                        )
                    )
                except HTTPException:
                    await ctx.channel.send(
                        "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                            mem, rsn, ctx.author
                        )
                    )
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
                except Forbidden:
                    await ctx.channel.send(
                        "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                            mem, rsn, ctx.author
                        )
                    )
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            else:
                await ctx.channel.send(
                    "처리 완료되었습니다 - 뮤트 {.mention} / 이유: {} / 처리자: {.mention}".format(
                        mem, rsn, ctx.author
                    )
                )
    if "chnl" in setting_loaded:
        try:
            await bot.get_channel(setting_loaded["chnl"]).send(
                "처리 완료되었습니다 - 경고 {.mention} 누적경고수 {} / 이유: {} / 처리자: {.mention}".format(
                    mem, warns, rsn, ctx.author
                )
            )
        except HTTPException:
            await ctx.channel.send(
                "처리 완료되었습니다 - 경고 {.mention} 누적경고수 {} / 이유: {} / 처리자: {.mention}".format(
                    mem, warns, rsn, ctx.author
                )
            )
            await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
        except Forbidden:
            await ctx.channel.send(
                "처리 완료되었습니다 - 경고 {.mention} 누적경고수 {} / 이유: {} / 처리자: {.mention}".format(
                    mem, warns, rsn, ctx.author
                )
            )
            await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
    else:
        await ctx.channel.send(
            "처리 완료되었습니다 - 경고 {.mention} 누적경고수 {} / 이유: {} / 처리자: {.mention}".format(
                mem, warns, rsn, ctx.author
            )
        )
    if setting_loaded["punish" + str(warns)] == "뮤트":
        try:
            await bot.wait_for("message", timeout=time, check=checkd)
        except asyncio.TimeoutError:
            await mem.edit(roles=currole, reason="MUTE Command Timeout")
            log("Unmuted " + mem.name, guild=ctx.guild)
            if "chnl" in setting_loaded:
                try:
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "처리 종료되었습니다 - 뮤트 {.mention}".format(mem)
                    )
                except HTTPException:
                    await ctx.channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(mem))
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
                except Forbidden:
                    await ctx.channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(mem))
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            else:
                await ctx.channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(mem))
            muted.remove(mem.id)
        else:
            await mem.edit(roles=currole, reason="MUTE Command Cancel")
            log("Unmuted " + mem.name, guild=ctx.guild)
            if "chnl" in setting_loaded:
                try:
                    await ctx.channel.send("예 형님 종료하겠습니다 - 뮤트 {.mention}".format(mem))
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "처리 종료되었습니다 - 뮤트 {.mention}".format(mem)
                    )
                except HTTPException:
                    await ctx.channel.send("예 형님 종료하겠습니다 - 뮤트 {.mention}".format(mem))
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
                except Forbidden:
                    await ctx.channel.send("예 형님 종료하겠습니다 - 뮤트 {.mention}".format(mem))
                    await ctx.channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            else:
                await ctx.channel.send("예 형님 종료하겠습니다 - 뮤트 {.mention}".format(mem))
            muted.remove(mem.id)
    else:
        return
    return


@addwarning.error
async def addwarning_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("모든 항목을 입력해주세요.")
        return


@commands.command(name="경고취소")  # prefix 경고취소 @유저
async def delwarning(ctx: Context):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if not isadmin(ctx.author.id, ctx.guild):
        await ctx.channel.send("권한도 없으면서 나대긴 ㅋ")
        return
    if len(ctx.message.mentions) == 0:
        errlog("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("대상자를 멘션해주세요.")
        return
    elif len(ctx.message.mentions) > 1:
        errlog("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    if (
        "warn" + str(mem.id) in setting_loaded
        and setting_loaded["warn" + str(mem.id)] == 0
    ):
        await ctx.channel.send("경고가 없습니다.")
    elif "warn" + str(mem.id) in setting_loaded:
        setting_loaded["warn" + str(mem.id)] -= 1
        warns = setting_loaded["warn" + str(mem.id)]
        savefile("setting", setting_loaded, guild=ctx.guild)
        await ctx.channel.send("넵^^7 (누적 경고수: " + str(warns) + ")")
    else:
        await ctx.channel.send("경고가 없습니다.")
    return


@commands.command(name="처벌정책")  # prefix 처벌정책
async def getpunishlist(ctx: Context):
    strs = []
    setting_loaded = loadfile("setting", guild=ctx.guild)
    for i in range(1, 11):
        if "punish" + str(i) in setting_loaded:
            if setting_loaded["punish" + str(i)] == "뮤트":
                pcnt = setting_loaded["mpunish" + str(i)]
                strs.append("경고 " + str(i) + "회시 뮤트 " + str(pcnt) + "초")
            elif setting_loaded["punish" + str(i)] == "킥":
                strs.append("경고 " + str(i) + "회시 킥")
            elif setting_loaded["punish" + str(i)] == "밴":
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
    await ctx.channel.send("서버의 처벌 정책입니다.", embed=embed)
    return


@commands.command(name="경고횟수")  # prefix 경고횟수 @유저
async def seewarning(ctx: Context):
    setting_loaded = loadfile("setting", guild=ctx.guild)
    if len(ctx.message.mentions) == 0:
        errlog("no mentions for member", guild=ctx.guild)
        await ctx.channel.send("대상자를 멘션해주세요.")
        return
    elif len(ctx.message.mentions) > 1:
        errlog("so many mentions for member", guild=ctx.guild)
        await ctx.channel.send("1명의 대상자만을 멘션해주세요.")
        return
    mem = ctx.message.mentions[0]
    warns = 0
    if "warn" + str(mem.id) in setting_loaded:
        warns = setting_loaded["warn" + str(mem.id)]
    else:
        setting_loaded["warn" + str(mem.id)] = 0
        savefile("setting", setting_loaded, guild=ctx.guild)
        warns = 0
    await ctx.channel.send(
        "{0} 님의 현재 누적 경고 수는 ".format(str(mem)) + str(warns) + "회 입니다."
    )
    return
