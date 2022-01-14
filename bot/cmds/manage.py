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
    getlocale,
    tblog,
    loadsetting,
    savesetting,
    delsetting,
    localeerr,
)
from discord.errors import Forbidden, HTTPException
from discord.ext import commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_command(delwelcome)
    bot.add_command(delbye)
    bot.add_command(unsubscribe)
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
    bot.add_command(getpunishlist)
    bot.add_command(seewarning)


@commands.command(name="환영인사삭제", aliases=["delwelcome"])  # prefix 환영인사삭제
@admincheck()
async def delwelcome(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    setting_loaded = loadsetting("msgj", guild=ctx.guild)
    if setting_loaded is None:
        await ctx.send(locale["manage_delwelcome_0"])
        return
    delsetting("msgj", guild=ctx.guild)
    await ctx.send(locale["manage_delwelcome_1"])
    return


@commands.command(name="작별인사삭제", aliases=["delbye"])  # prefix 작별인사삭제
@admincheck()
async def delbye(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    setting_loaded = loadsetting("msgl", guild=ctx.guild)
    if setting_loaded is None:
        await ctx.send(locale["manage_delbye_0"])
        return
    delsetting("msgl", guild=ctx.guild)
    await ctx.send(locale["manage_delbye_1"])
    return


@commands.command(
    name="구독해제", aliases=["구독취소", "unsubscribe"]
)  # prefix 구독해제 / prefix 구독취소
@admincheck()
async def unsubscribe(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    setting_loaded = loadsetting("chnl", guild=ctx.guild)
    if setting_loaded is None:
        await ctx.send(locale["manage_unsubscribe_0"])
        return
    delsetting("chnl", guild=ctx.guild)
    await ctx.send(locale["manage_unsubscribe_1"])
    return


@commands.command(name="기본역할삭제", aliases=["deldefrole"])  # prefix 기본역할삭제
@admincheck()
async def deldefaultrole(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    setting_loaded = loadsetting("joinrole", guild=ctx.guild)
    if setting_loaded is None:
        await ctx.send(locale["manage_deldefaultrole_0"])
        return
    delsetting("joinrole", guild=ctx.guild)
    await ctx.send(locale["manage_cfrm"])
    return


@commands.command(
    name="치워", aliases=["청소", "clean"]
)  # prefix 치워 (cnt: int) / prefix 청소 (cnt: int)
async def cleanchat(ctx: Context, *args):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)

    def check(m):
        return m.channel == ctx.channel and not m == ctx

    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send(locale["manage_cleanchat_0"])
            return
    cnt = 0
    try:
        cnt = int(args[0])
    except IndexError:
        await ctx.send(locale["manage_cleanchat_1"])
        return
    except ValueError:
        await ctx.send(locale["manage_cleanchat_2"])
        return
    if cnt <= 0:
        await ctx.send(locale["manage_cleanchat_3"])
        return
    if cnt > 200:
        await ctx.send(locale["manage_cleanchat_4"])
        return
    deleted = await ctx.channel.purge(limit=cnt + 1, check=check)
    mymsg = await ctx.send(locale["manage_cleanchat_5"].format(len(deleted) - 1))
    await mymsg.delete(delay=5)
    return


@commands.command(
    name="이거로조져", aliases=["뮤트설정", "setmuterole"]
)  # prefix 이거로조져 @역할 / prefix 뮤트설정 @역할
@admincheck()
async def setmuterole(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if len(ctx.message.role_mentions) == 0:
        await ctx.send(locale["manage_setmutterole_0"])
        return
    if len(ctx.message.role_mentions) > 1:
        await ctx.send(locale["manage_setmutterole_1"])
        return
    savesetting("role", ctx.guild, ctx.message.role_mentions[0].id)
    await ctx.send(locale["manage_cfrm"])
    return


@commands.command(
    name="처벌설정", aliases=["setpunish"]
)  # prefix 처벌설정 (cnt: int) (punish: str) (pcnt: int = None)
@admincheck()
async def setpunish(ctx: Context, cnt: int, punish: str, pcnt: int = None, *args):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if cnt > 11:
        await ctx.send(locale["manage_setpunish_0"])
        return
    if cnt < 1:
        await ctx.send(locale["manage_setpunish_1"])
        return
    if not punish in [
        locale["manage_setpunish_2"],
        locale["manage_setpunish_3"],
        locale["manage_setpunish_4"],
        locale["manage_setpunish_5"],
    ]:
        await ctx.send(locale["manage_setpunish_6"])
        return
    if punish == locale["manage_setpunish_5"]:
        setting_loaded = loadsetting("punish" + str(cnt), guild=ctx.guild)
        if setting_loaded is None:
            delsetting("punish" + str(cnt), guild=ctx.guild)
            await ctx.send(locale["manage_cfrm"])
            return
        await ctx.send(locale["manage_setpunish_7"])
        return
    if punish == locale["manage_setpunish_2"]:
        if pcnt is None:
            await ctx.send(locale["manage_setpunish_8"])
            return
        savesetting("mpunish" + str(cnt), ctx.guild, pcnt)
    savesetting("punish" + str(cnt), ctx.guild, punish)
    await ctx.send(locale["manage_cfrm"])
    return


@setpunish.error
async def setpunish_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(locale["manage_error_0"])
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(locale["manage_error_1"])
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(locale["manage_error_2"])
            return
        await ctx.send(locale["manage_error_3"].format(tblog(error)))
    except Exception as e:
        return


@commands.command(name="기본역할", aliases=["setdefrole"])  # prefix 기본역할 @역할
@admincheck()
async def setdefaultrole(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if len(ctx.message.role_mentions) == 0:
        await ctx.send(locale["manage_setdefaultrole_0"])
        return
    if len(ctx.message.role_mentions) > 1:
        await ctx.send(locale["manage_setdefaultrole_1"])
        return
    savesetting("joinrole", ctx.guild, ctx.message.role_mentions[0].id)
    await ctx.send(locale["manage_cfrm"])
    return


@commands.command(name="구독", aliases=["subscribe"])  # prefix 구독 #채널
@admincheck()
async def subscribe(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if len(ctx.message.channel_mentions) == 0:
        await ctx.send(locale["manage_subscribe_0"])
        return
    if len(ctx.message.channel_mentions) > 1:
        await ctx.send(locale["manage_subscribe_1"])
        return
    savesetting("chnl", ctx.guild, ctx.message.channel_mentions[0].id)
    await ctx.send(locale["manage_cfrm"])
    return


@commands.command(name="환영인사", aliases=["setwelcome"])  # prefix 환영인사 (msgj: str)
@admincheck()
async def setwelcome(ctx: Context, *, arg):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    savesetting("msgj", ctx.guild, arg)
    await ctx.send(locale["manage_cfrm"])
    return


@setwelcome.error
async def setwelcome_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(locale["manage_error_0"])
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(locale["manage_error_1"])
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(locale["manage_error_2"])
            return
        await ctx.send(locale["manage_error_3"].format(tblog(error)))
    except Exception as e:
        return


@commands.command(name="작별인사", aliases=["setbye"])  # prefix 작별인사 (msgl: str)
@admincheck()
async def setbye(ctx: Context, *, arg):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    savesetting("msgl", ctx.guild, arg)
    await ctx.send(locale["manage_cfrm"])
    return


@setbye.error
async def setbye_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(locale["manage_error_0"])
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(locale["manage_error_1"])
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(locale["manage_error_2"])
            return
        await ctx.send(locale["manage_error_3"].format(tblog(error)))
    except Exception as e:
        return


@commands.command(name="해방", aliases=["deladmin"])  # prefix 해방 @유저
@admincheck()
async def delguildadmin(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
        return
    res = deladmin(ctx.message.mentions[0].id, ctx.guild)
    if res == 0:
        await ctx.send(
            locale["manage_delguildadmin_0"].format(ctx.message.mentions[0].mention),
            allowed_mentions=discord.AllowedMentions.all(),
        )
    elif res == 1:
        await ctx.send(locale["manage_delguildadmin_1"])
    elif res == 2:
        await ctx.send(locale["manage_delguildadmin_2"])
    elif res == 3:
        await ctx.send(locale["manage_delguildadmin_3"])
    return


@commands.command(name="새주인", aliases=["addadmin"])  # prefix 새주인 @유저
@admincheck()
async def addguildadmin(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
        return
    res = addadmin(ctx.message.mentions[0].id, ctx.guild)
    if res:
        await ctx.send(
            locale["manage_addguildadmin_4"].format(ctx.message.mentions[0].mention),
            allowed_mentions=discord.AllowedMentions.all(),
        )
    else:
        await ctx.send(locale["manage_addguildadmin_5"])
    return


@commands.command(
    name="조져", aliases=["뮤트", "mute"]
)  # prefix 조져 (time: int) @유저 (rsn: str) / prefix 뮤트 (time: int) @유저 (rsn: str)
async def execmute(ctx: Context, time: int, mention: str, *, arg):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            await ctx.send(locale["manage_error_6"])
            return
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
        return
    mem = ctx.message.mentions[0]
    currole = mem.roles
    setting_loaded = loadsetting("role", ctx.guild)
    if setting_loaded is None:
        await ctx.send(locale["manage_execmute_0"])
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
            await ctx.send(locale["manage_execmute_1"])
            return
        await mem.edit(roles=[xrole], reason="MUTE Command REASON: " + rsn)
    except Forbidden:
        await ctx.send(locale["manage_execmute_2"])
        return
    else:
        for mute in muted:
            if mem.id == mute[0] and ctx.guild.id == mute[1]:
                await ctx.send(locale["manage_execmute_3"].format(mem))
                return
        muted.append([mem.id, mem.guild.id, time, currole, ctx.channel.id])
        log("Muted " + mem.name, guild=ctx.guild)
        setting_loaded = loadsetting("chnl", ctx.guild)
        if setting_loaded is not None:
            try:
                await bot.get_channel(setting_loaded).send(
                    locale["manage_execmute_4"].format(
                        mem.mention, rsn, ctx.author.mention
                    )
                )
            except HTTPException:
                await ctx.send(
                    locale["manage_execmute_4"].format(
                        mem.mention, rsn, ctx.author.mention
                    )
                )
                await ctx.send(locale["manage_error_5"])
        else:
            await ctx.send(
                locale["manage_execmute_4"].format(mem.mention, rsn, ctx.author.mention)
            )
    return


@execmute.error
async def execmute_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(locale["manage_error_0"])
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(locale["manage_error_1"])
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(locale["manage_error_2"])
            return
        await ctx.send(locale["manage_error_3"].format(tblog(error)))
    except Exception as e:
        return


@commands.command(
    name="충분하다", aliases=["뮤트해제", "unmute"]
)  # prefix 충분하다 @유저 / prefix 뮤트해제 @유저
async def donemute(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            await ctx.send(locale["manage_error_6"])
            return
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
        return
    udmute = bot.get_cog("updatemute")
    if udmute is not None:
        res = await udmute.unmutenow(ctx)
    else:
        await ctx.send(locale["manage_execkick_0"])
        return
    if not res:
        await ctx.send(locale["manage_execkick_1"])
        return
    return


@donemute.error
async def donemute_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(locale["manage_error_0"])
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(locale["manage_error_1"])
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(locale["manage_error_2"])
            return
        await ctx.send(locale["manage_error_3"].format(tblog(error)))
    except Exception as e:
        return


@commands.command(name="킥", aliases=["kick"])  # prefix 킥 @유저 (rsn: str)
async def execkick(ctx: Context, mention: str, *, arg):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).kick_members:
            await ctx.send(locale["manage_error_6"])
            return
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
        return
    mem = ctx.message.mentions[0]
    rsn = arg
    setting_loaded = loadsetting("chnl", ctx.guild)
    try:
        await ctx.guild.kick(mem, reason="KICK Command REASON: " + rsn)
    except Forbidden:
        await ctx.send(locale["manage_error_6"])
        return
    if setting_loaded is not None:
        try:
            await bot.get_channel(setting_loaded).send(
                locale["manage_execkick_2"].format(mem.mention, rsn, ctx.author.mention)
            )
        except HTTPException:
            await ctx.send(
                locale["manage_execkick_2"].format(mem.mention, rsn, ctx.author.mention)
            )
            await ctx.send(locale["manage_error_5"])
    else:
        await ctx.send(
            locale["manage_execkick_2"].format(mem.mention, rsn, ctx.author.mention)
        )
    return


@execkick.error
async def execkick_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(locale["manage_error_0"])
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(locale["manage_error_1"])
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(locale["manage_error_2"])
            return
        await ctx.send(locale["manage_error_3"].format(tblog(error)))
    except Exception as e:
        return


@commands.command(name="밴", aliases=["ban"])
async def execban(ctx, mention: str, *, arg):  # prefix 밴 @유저 (rsn: str)
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if not isadmin(ctx.author.id, ctx.guild):
        if not ctx.author.permissions_in(ctx.channel).ban_members:
            await ctx.send(locale["manage_error_6"])
            return
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
        return
    mem = ctx.message.mentions[0]
    rsn = arg
    setting_loaded = loadsetting("chnl", ctx.guild)
    try:
        await ctx.guild.ban(mem, reason="BAN Command REASON: " + rsn)
    except Forbidden:
        await ctx.send(locale["manage_error_6"])
        return
    if setting_loaded is not None:
        try:
            await bot.get_channel(setting_loaded).send(
                locale["manage_execban_2"].format(mem.mention, rsn, ctx.author.mention)
            )
        except HTTPException:
            await ctx.send(
                locale["manage_execban_2"].format(mem.mention, rsn, ctx.author.mention)
            )
            await ctx.send(locale["manage_error_5"])
    else:
        await ctx.send(
            locale["manage_execban_2"].format(mem.mention, rsn, ctx.author.mention)
        )
    return


@execban.error
async def execban_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(locale["manage_error_0"])
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(locale["manage_error_1"])
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(locale["manage_error_2"])
            return
        await ctx.send(locale["manage_error_3"].format(tblog(error)))
    except Exception as e:
        return


@commands.command(name="경고", aliases=["warn"])  # prefix 경고 @유저 (rsn: str)
@admincheck()
async def addwarning(ctx: Context, mention: str, *, arg):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    time = 0
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
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
            await ctx.send(locale["manage_error_6"])
            return
        if setting is not None:
            try:
                await bot.get_channel(setting).send(
                    locale["manage_execkick_2"].format(
                        mem.mention, rsn, ctx.author.mention
                    )
                )
            except HTTPException:
                await ctx.send(
                    locale["manage_execkick_2"].format(
                        mem.mention, rsn, ctx.author.mention
                    )
                )
                await ctx.send(locale["manage_error_5"])
        else:
            await ctx.send(
                locale["manage_execkick_2"].format(mem.mention, rsn, ctx.author.mention)
            )
    elif ptype == "밴":
        try:
            await ctx.guild.ban(mem, reason="BAN Command REASON: " + rsn)
        except Forbidden:
            await ctx.send(locale["manage_error_6"])
            return
        if setting is not None:
            try:
                await bot.get_channel(setting).send(
                    locale["manage_execban_2"].format(
                        mem.mention, rsn, ctx.author.mention
                    )
                )
            except HTTPException:
                await ctx.send(
                    locale["manage_execban_2"].format(
                        mem.mention, rsn, ctx.author.mention
                    )
                )
                await ctx.send(locale["manage_error_5"])
        else:
            await ctx.send(
                locale["manage_execban_2"].format(mem.mention, rsn, ctx.author.mention)
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
                await ctx.send(locale["manage_execmute_1"])
                return
            await mem.edit(roles=[xrole], reason="MUTE Command REASON: " + rsn)
        except Forbidden:
            await ctx.send(locale["manage_execmute_2"])
            return
        else:
            for mute in muted:
                if mem.id == mute[0] and ctx.guild.id == mute[1]:
                    await ctx.send(locale["manage_execmute_3"].format(mem))
                    return
            muted.append([mem.id, mem.guild.id, time, currole, ctx.channel.id])
            log("Muted " + mem.name, guild=ctx.guild)
            setting_loaded = loadsetting("chnl", ctx.guild)
            if setting_loaded is not None:
                try:
                    await bot.get_channel(setting_loaded).send(
                        locale["manage_execmute_4"].format(
                            mem.mention, rsn, ctx.author.mention
                        )
                    )
                except HTTPException:
                    await ctx.send(
                        locale["manage_execmute_4"].format(
                            mem.mention, rsn, ctx.author.mention
                        )
                    )
                    await ctx.send(locale["manage_error_5"])
            else:
                await ctx.send(
                    locale["manage_execmute_4"].format(
                        mem.mention, rsn, ctx.author.mention
                    )
                )
    setting_loaded = loadsetting("chnl", ctx.guild)
    if setting_loaded is not None:
        try:
            await bot.get_channel(setting_loaded).send(
                locale["manage_warning_0"].format(
                    mem.mention, warns, rsn, ctx.author.mention
                )
            )
        except HTTPException:
            await ctx.send(
                locale["manage_warning_0"].format(
                    mem.mention, warns, rsn, ctx.author.mention
                )
            )
            await ctx.send(locale["manage_error_5"])
    else:
        await ctx.send(
            locale["manage_warning_0"].format(
                mem.mention, warns, rsn, ctx.author.mention
            )
        )
    return


@addwarning.error
async def addwarning_error(ctx: Context, error):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    try:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(locale["manage_error_0"])
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(locale["manage_error_1"])
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send(locale["manage_error_2"])
            return
        await ctx.send(locale["manage_error_3"].format(tblog(error)))
    except Exception as e:
        return


@commands.command(name="경고취소", aliases=["delwarn"])  # prefix 경고취소 @유저
async def delwarning(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if not isadmin(ctx.author.id, ctx.guild):
        await ctx.send(locale["manage_error_6"])
        return
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
        return
    mem = ctx.message.mentions[0]
    setting_loaded = loadsetting("warn" + str(mem.id), guild=ctx.guild)
    if setting_loaded is None or setting_loaded == 0:
        await ctx.send(locale["manage_delwarning_0"])
    else:
        savesetting("warn" + str(mem.id), ctx.guild, setting_loaded - 1)
        await ctx.send(locale["manage_delwarning_1"].format(str(setting_loaded - 1)))
    return


@commands.command(name="처벌정책", aliases=["punishes"])  # prefix 처벌정책
async def getpunishlist(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    strs = []
    for i in range(1, 11):
        ptype = loadsetting("punish" + str(i), ctx.guild)
        if ptype is not None:
            if ptype == locale["manage_setpunish_2"]:
                pcnt = loadsetting("mpunish" + str(i), ctx.guild)
                strs.append(locale["manage_getpunishlist_0"].format(str(i), str(pcnt)))
            elif ptype == locale["manage_setpunish_3"]:
                strs.append(locale["manage_getpunishlist_1"].format(str(i)))
            elif ptype == locale["manage_setpunish_4"]:
                strs.append(locale["manage_getpunishlist_2"].format(str(i)))
    embed = discord.Embed(title=locale["manage_getpunishlist_4"], color=botcolor)
    tmp = ""
    if len(strs) == 0:
        tmp = locale["manage_getpunishlist_3"]
    elif len(strs) == 1:
        tmp = strs[0]
    else:
        for i in range(0, len(strs) - 1):
            tmp += strs[i] + "\n"
        tmp += strs[len(strs) - 1]
    embed.description = tmp
    await ctx.send(locale["manage_getpunishlist_4"], embed=embed)
    return


@commands.command(name="경고횟수", aliases=["seewarn"])  # prefix 경고횟수 @유저
async def seewarning(ctx: Context):
    locale = getlocale(ctx)
    if locale is None:
        await localeerr(ctx)
        locale = getlocale(ctx)
    if len(ctx.message.mentions) == 0:
        await ctx.send(locale["manage_guildadmin_0"])
        return
    if len(ctx.message.mentions) > 1:
        await ctx.send(locale["manage_guildadmin_1"])
        return
    mem = ctx.message.mentions[0]
    setting_loaded = loadsetting("warn" + str(mem.id), guild=ctx.guild)
    warns = 0
    if setting_loaded is not None:
        warns = setting_loaded
    else:
        warns = 0
    await ctx.send(locale["manage_seewarning_0"].format(str(mem), str(warns)))
    return
