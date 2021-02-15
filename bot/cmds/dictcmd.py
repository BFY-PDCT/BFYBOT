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
from .config import prefix, pending, using, bot, owner, botcolor
from .genfunc import (
    deldict,
    errlog,
    getpoint,
    isowner,
    loaddict,
    savedict,
    setpoint,
    tblog,
)
from discord.ext import commands


def initcmd():
    bot.add_cog(CommandErrorHandler(bot))


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("관리자 아니면 안해줄건뎅")
            return
        else:
            tblog(error)
            await ctx.send("오류가 있었어요.. :( 자동으로 리포트가 생성되었어요")
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        if ctx.author.id in using:
            using.remove(ctx.author.id)

        if ctx.message.content.startswith(prefix):  # prefix *

            # reply: [replystr: str, editable: bool, author: int]
            kwd = " ".join(ctx.message.content.split(" ")[1:])
            reply = loaddict(kwd)

            def checka(m):
                return (
                    m.content == "지워"
                    and m.channel == ctx.message.channel
                    and ctx.message.author == m.author
                )

            def checkb(m):
                return (
                    (m.content == "어" or m.content == "아니")
                    and m.channel == ctx.message.channel
                    and ctx.message.author == m.author
                )

            def checkc(m):
                return (
                    m.channel == ctx.message.channel and ctx.message.author == m.author
                )

            def checkd(m):
                return (
                    (m.content.startswith("신고") or m.content == "바꿔")
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
                            content="주인님 지웠읍니다.",
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        return
                try:
                    msg = await bot.wait_for("message", check=checkd, timeout=10.0)
                except asyncio.TimeoutError:
                    return
                if msg.content == "바꿔":
                    if not reply[1]:
                        await mymsg.edit(content="이건 못바꿔줘")
                        return
                    if getpoint(ctx.message.author.id, guild=ctx.guild) >= 100000:
                        await mymsg.edit(
                            content="100000포인트를 사용해서 대답을 바꿔줄래?",
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        try:
                            msg = await bot.wait_for(
                                "message", check=checkb, timeout=10.0
                            )
                        except asyncio.TimeoutError:
                            await mymsg.edit(content="...")
                            return
                        if msg.content == "어":
                            if ctx.message.content in pending:
                                await mymsg.edit(content="누군가 수정중인것 같아요 ;)")
                                return
                            if ctx.message.author.id in using:
                                await mymsg.edit(content="이미 사용중이에요 ;)")
                                return
                            pending.append(ctx.message.content)
                            using.append(ctx.message.author.id)
                            await mymsg.edit(
                                content="머라고할건데",
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
                                    content="이걸 어케등록하란겨",
                                    allowed_mentions=discord.AllowedMentions.all(),
                                )
                                pending.remove(ctx.message.content)
                                using.remove(ctx.message.author.id)
                                return
                            savedict(kwd, [msg.content, True, msg.author.id])
                            await mymsg.edit(
                                content="ㅇㅋ `💰-100000`",
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
                        if msg.content == "아니":
                            await mymsg.edit(content="ㅇㅋ 싫음말고")
                            return
                    else:
                        await mymsg.edit(content="100000포인트 벌고와")
                        return
                else:
                    ver = discord.Embed(
                        title="새 신고",
                        description="by: "
                        + str(msg.author)
                        + "\nid: "
                        + str(msg.author.id),
                        color=botcolor,
                    )
                    ver.add_field(name="질문", value=kwd)
                    ver.add_field(name="답변", value=reply[0])
                    ver.add_field(
                        name="사유", value=" ".join(ctx.message.content.split()[1:])
                    )
                    ver.add_field(name="작성자", value=reply[2], inline=False)
                    await bot.get_user(owner[0]).send("새 신고", embed=ver)
                    await mymsg.edit(
                        content="해당 답변을 신고하였습니다. 신고된 답변은 관리자가 검토 후 조치할 예정입니다."
                    )
                    return
            if isowner(ctx.message.author.id):
                mymsg = await ctx.message.channel.send(
                    "주인님 새 명령어가 필요하십니까", allowed_mentions=discord.AllowedMentions.all()
                )
            elif getpoint(ctx.message.author.id, guild=ctx.guild) >= 50000:
                mymsg = await ctx.message.channel.send("50000포인트를 사용해서 대답을 알려줄래?")
            else:
                await ctx.message.channel.send(
                    "뭐래 ㅋ", allowed_mentions=discord.AllowedMentions.all()
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
                        await mymsg.edit(content="누군가 수정중인것 같아요 ;)")
                        return
                    if ctx.message.author.id in using:
                        await mymsg.edit(content="이미 사용중이에요 ;)")
                        return
                    pending.append(ctx.message.content)
                    using.append(ctx.message.author.id)
                    await mymsg.edit(
                        content="주인님 무엇을 원하십니까.",
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
                            content="주인님 이건좀...",
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                    else:
                        savedict(kwd, [msg.content, True, msg.author.id])
                        await mymsg.edit(
                            content="주인님 등록하였읍니다.",
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                else:
                    if ctx.message.content in pending:
                        await mymsg.edit(content="누군가 수정중인것 같아요 ;)")
                        return
                    if ctx.message.author.id in using:
                        await mymsg.edit(content="이미 사용중이에요 ;)")
                        return
                    pending.append(ctx.message.content)
                    using.append(ctx.message.author.id)
                    await mymsg.edit(
                        content="머라고할건데",
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
                            content="이걸 어케등록하란겨",
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
                    else:
                        savedict(kwd, [msg.content, True, msg.author.id])
                        await mymsg.edit(
                            content="ㅇㅋ `💰-50000`",
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        setpoint(
                            ctx.message.author.id,
                            getpoint(ctx.message.author.id, guild=ctx.guild) - 50000,
                            guild=ctx.guild,
                        )
                        pending.remove(ctx.message.content)
                        using.remove(ctx.message.author.id)
            elif msg.content == "아니":
                if isowner(ctx.message.author.id):
                    await mymsg.edit(content="알겠습니다 주인님")
                else:
                    await mymsg.edit(content="ㅇㅋ 싫음말고")
            return
