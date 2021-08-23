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
import asyncio
from .config import prefix, pending, using, bot, owner, botcolor, report
from .genfunc import (
    deldict,
    getlocale,
    getpoint,
    isowner,
    loaddict,
    savedict,
    setpoint,
    tblog,
    localeerr,
)
from discord.ext import commands


def initcmd():
    bot.add_cog(CommandErrorHandler(bot))


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        locale = getlocale(ctx)
        if locale is None:
            await localeerr(ctx)
        locale = getlocale(ctx)

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(locale["dictcmd_error_notadmin"])
            return
        else:
            tblog(error)
            await ctx.send(locale["dictcmd_error_err"])
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        if ctx.author.id in using:
            using.remove(ctx.author.id)

        if ctx.message.content.startswith(tuple(prefix)):  # prefix *

            # reply: [replystr: str, editable: bool, author: int]
            kwd = " ".join(ctx.message.content.split(" ")[1:])
            reply = loaddict(kwd)

            def checka(m):
                return (
                    m.content == locale["dictcmd_checka_delete"]
                    and m.channel == ctx.message.channel
                    and ctx.message.author == m.author
                )

            def checkb(m):
                return (
                    (
                        m.content == locale["dictcmd_checkb_yes"]
                        or m.content == locale["dictcmd_checkb_no"]
                    )
                    and m.channel == ctx.message.channel
                    and ctx.message.author == m.author
                )

            def checkc(m):
                return (
                    m.channel == ctx.message.channel and ctx.message.author == m.author
                )

            def checkd(m):
                return (
                    (
                        m.content.startswith(locale["dictcmd_checkd_report"])
                        or m.content == locale["dictcmd_checkd_change"]
                    )
                    and m.channel == ctx.message.channel
                    and ctx.message.author == m.author
                )

            if reply is not False:
                mymsg = await ctx.message.channel.send(reply[0])
                if isowner(ctx.message.author.id):
                    try:
                        msg = await bot.wait_for("message", check=checka, timeout=10.0)
                    except asyncio.TimeoutError:
                        return
                    else:
                        deldict(kwd)
                        await mymsg.edit(
                            content=locale["dictcmd_general_deleted"],
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        return
                try:
                    msg = await bot.wait_for("message", check=checkd, timeout=10.0)
                except asyncio.TimeoutError:
                    return
                if msg.content == locale["dictcmd_general_reqedit"]:
                    if not reply[1]:
                        await mymsg.edit(content=locale["dictcmd_general_rejedit"])
                        return
                    if getpoint(ctx.message.author.id, guild=ctx.guild) >= 100000:
                        await mymsg.edit(
                            content=locale["dictcmd_general_cfmedit"],
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        try:
                            msg = await bot.wait_for(
                                "message", check=checkb, timeout=10.0
                            )
                        except asyncio.TimeoutError:
                            await mymsg.edit(content="...")
                            return
                        if msg.content == locale["dictcmd_general_yes"]:
                            if ctx.message.content in pending:
                                await mymsg.edit(
                                    content=locale["dictcmd_general_editing"]
                                )
                                return
                            if ctx.message.author.id in using:
                                await mymsg.edit(
                                    content=locale["dictcmd_general_using"]
                                )
                                return
                            pending.append(ctx.message.content)
                            using.append(ctx.message.author.id)
                            await mymsg.edit(
                                content=locale["dictcmd_general_question"],
                                allowed_mentions=discord.AllowedMentions.all(),
                            )
                            try:
                                msg = await bot.wait_for(
                                    "message", check=checkc, timeout=30.0
                                )
                            except asyncio.TimeoutError:
                                await mymsg.edit(content="...")
                                pending.remove(ctx.message.content)
                                using.remove(ctx.message.author.id)
                                return
                            if msg.content == "":
                                await mymsg.edit(
                                    content=locale["dictcmd_general_emptyerr"],
                                    allowed_mentions=discord.AllowedMentions.all(),
                                )
                                pending.remove(ctx.message.content)
                                using.remove(ctx.message.author.id)
                                return
                            if len(msg.content) > 100:
                                await mymsg.edit(
                                    content=locale["dictcmd_general_limiterr"],
                                    allowed_mentions=discord.AllowedMentions.all(),
                                )
                                pending.remove(ctx.message.content)
                                using.remove(ctx.message.author.id)
                                return
                            savedict(kwd, [msg.content, True, msg.author.id])
                            await mymsg.edit(
                                content=locale["dictcmd_general_acpedit"],
                                allowed_mentions=discord.AllowedMentions.all(),
                            )
                            setpoint(
                                ctx.message.author.id,
                                getpoint(
                                    ctx.message.author.id,
                                    guild=ctx.guild,
                                )
                                - 50000,
                                guild=ctx.guild,
                            )
                            pending.remove(ctx.message.content)
                            using.remove(ctx.message.author.id)
                            return
                        if msg.content == locale["dictcmd_general_no"]:
                            await mymsg.edit(content=locale["dictcmd_general_cancel"])
                            return
                    else:
                        await mymsg.edit(content=locale["dictcmd_general_npntedit"])
                        return
                else:
                    if report:
                        ver = discord.Embed(
                            title=locale["dictcmd_report_title"],
                            description="by: "
                            + str(msg.author)
                            + "\nid: "
                            + str(msg.author.id),
                            color=botcolor,
                        )
                        ver.add_field(name=locale["dictcmd_report_cmd"], value=kwd)
                        ver.add_field(
                            name=locale["dictcmd_report_reply"], value=reply[0]
                        )
                        ver.add_field(
                            name=locale["dictcmd_report_reason"],
                            value=" ".join(ctx.message.content.split()[1:]),
                        )
                        ver.add_field(
                            name=locale["dictcmd_report_author"],
                            value=reply[2],
                            inline=False,
                        )
                        await bot.get_user(owner[0]).send(
                            locale["dictcmd_report_title"], embed=ver
                        )
                        await mymsg.edit(content=locale["dictcmd_report_reported"])
                    return
            if isowner(ctx.message.author.id):
                mymsg = await ctx.message.channel.send(
                    locale["dictcmd_general_ownercfmnew"],
                    allowed_mentions=discord.AllowedMentions.all(),
                )
            elif getpoint(ctx.message.author.id, guild=ctx.guild) >= 50000:
                mymsg = await ctx.message.channel.send(locale["dictcmd_general_cfmnew"])
            else:
                await ctx.message.channel.send(
                    locale["dictcmd_general_cancel2"],
                    allowed_mentions=discord.AllowedMentions.all(),
                )
                return
            try:
                msg = await bot.wait_for("message", check=checkb, timeout=10.0)
            except asyncio.TimeoutError:
                await mymsg.edit(content="...")
                return
            if msg.content == "어":
                if isowner(ctx.message.author.id):
                    if ctx.message.content in pending:
                        await mymsg.edit(content=locale["dictcmd_general_editing"])
                        return
                    if ctx.message.author.id in using:
                        await mymsg.edit(content=locale["dictcmd_general_using"])
                        return
                    pending.append(ctx.message.content)
                    using.append(ctx.message.author.id)
                    await mymsg.edit(
                        content=locale["dictcmd_general_ownerquestion"],
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                    try:
                        msg = await bot.wait_for("message", check=checkc, timeout=30.0)
                    except asyncio.TimeoutError:
                        await mymsg.edit(content="...")
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                        return
                    if msg.content == "":
                        await mymsg.edit(
                            content=locale["dictcmd_general_emptyerr"],
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                        return
                    if len(msg.content) > 100:
                        await mymsg.edit(
                            content=locale["dictcmd_general_limiterr"],
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                        return
                    savedict(kwd, [msg.content, True, msg.author.id])
                    await mymsg.edit(
                        content=locale["dictcmd_general_owneracpnew"],
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                    pending.remove(ctx.message.content)
                    using.remove(ctx.message.author.id)
                else:
                    if ctx.message.content in pending:
                        await mymsg.edit(content=locale["dictcmd_general_editing"])
                        return
                    if ctx.message.author.id in using:
                        await mymsg.edit(content=locale["dictcmd_general_using"])
                        return
                    pending.append(ctx.message.content)
                    using.append(ctx.message.author.id)
                    await mymsg.edit(
                        content=locale["dictcmd_general_question"],
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                    try:
                        msg = await bot.wait_for("message", check=checkc, timeout=30.0)
                    except asyncio.TimeoutError:
                        await mymsg.edit(content="...")
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                        return
                    if msg.content == "":
                        await mymsg.edit(
                            content=locale["dictcmd_general_emptyerr"],
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                        return
                    if len(msg.content) > 100:
                        await mymsg.edit(
                            content=locale["dictcmd_general_limiterr"],
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                        return
                    savedict(kwd, [msg.content, True, msg.author.id])
                    await mymsg.edit(
                        content=locale["dictcmd_general_acpnew"],
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                    setpoint(
                        ctx.message.author.id,
                        getpoint(ctx.message.author.id, guild=ctx.guild) - 50000,
                        guild=ctx.guild,
                    )
                    pending.remove(ctx.message.content)
                    using.remove(ctx.message.author.id)
            elif msg.content == locale["dictcmd_general_no"]:
                if isowner(ctx.message.author.id):
                    await mymsg.edit(content=locale["dictcmd_general_ownercancel"])
                else:
                    await mymsg.edit(content=locale["dictcmd_general_cancel"])
            return
