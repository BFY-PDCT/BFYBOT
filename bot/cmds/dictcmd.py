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

import discord, asyncio
from .config import owner, prefix, botcolor, pending, using, bot
from .genfunc import errlog, getpoint, isowner, loadfile, log, savefile, setpoint
from discord.ext import commands


def initcmd():
    bot.add_cog(CommandErrorHandler(bot))


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        log("PROCESS COMMAND ERROR : " + str(error))

        if ctx.message.content.startswith(prefix):  # prefix *

            new_dict = loadfile("dict")

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
                    m.content == "바꿔"
                    and m.channel == ctx.message.channel
                    and ctx.message.author == m.author
                )

            if ctx.message.content in new_dict:
                if new_dict.get(ctx.message.content) == "":
                    errlog(
                        "Error found, automatic fix process will be started",
                        guild=ctx.message.guild,
                    )
                    await ctx.message.channel.send(
                        "죄송합니다 에러가 발견되어 수정되었습니다.",
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                    del new_dict[ctx.message.content]
                    if "id" + ctx.message.content in new_dict:
                        del new_dict["id" + ctx.message.content]
                    savefile("dict", new_dict, guild=ctx.message.guild)
                    return
                mymsg = await ctx.message.channel.send(
                    new_dict.get(ctx.message.content)
                )
                if isowner(ctx.message.author.id):
                    try:
                        msg = await bot.wait_for("message", check=checka, timeout=10.0)
                    except asyncio.TimeoutError:
                        return
                    else:
                        del new_dict[ctx.message.content]
                        if "id" + ctx.message.content in new_dict:
                            del new_dict["id" + ctx.message.content]
                        savefile("dict", new_dict, guild=ctx.message.guild)
                        await mymsg.edit(
                            content="주인님 지웠읍니다.",
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        return
                else:
                    try:
                        msg = await bot.wait_for("message", check=checkd, timeout=10.0)
                    except asyncio.TimeoutError:
                        return
                    else:
                        if msg.content == "바꿔":
                            if "editable" + ctx.message.content in new_dict:
                                if not new_dict["editable" + ctx.message.content]:
                                    await mymsg.edit(content="이건 못바꿔줘")
                                    return
                            if getpoint(ctx.message.author.id, guild=ctx.guild) >= 500:
                                await mymsg.edit(
                                    content="500포인트를 사용해서 대답을 바꿔줄래?",
                                    allowed_mentions=discord.AllowedMentions.all(),
                                )
                                try:
                                    msg = await bot.wait_for(
                                        "message", check=checkb, timeout=10.0
                                    )
                                except asyncio.TimeoutError:
                                    await mymsg.edit(content="...")
                                    return
                                else:
                                    if msg.content == "어":
                                        if ctx.message.content in pending:
                                            await mymsg.edit(content="누군가 수정중인것 같아요 ;)")
                                            return
                                        pending.append(ctx.message.content)
                                        using.append(ctx.message.author.id)
                                        await mymsg.edit(
                                            content="머라고할건데",
                                            allowed_mentions=discord.AllowedMentions.all(),
                                        )
                                        try:
                                            msg = await bot.wait_for(
                                                "message", check=checkc
                                            )
                                        except asyncio.TimeoutError:
                                            await mymsg.edit(content="...")
                                            pending.remove(ctx.message.content)
                                            using.remove(ctx.message.author.id)
                                            return
                                        else:
                                            if msg.content == "":
                                                errlog(
                                                    "Cannot store empty message",
                                                    guild=ctx.message.guild,
                                                )
                                                await mymsg.edit(
                                                    content="이걸 어케등록하란겨",
                                                    allowed_mentions=discord.AllowedMentions.all(),
                                                )
                                                pending.remove(ctx.message.content)
                                                using.remove(ctx.message.author.id)
                                                return
                                            else:
                                                new_dict[
                                                    ctx.message.content
                                                ] = msg.content
                                                new_dict[
                                                    "id" + ctx.message.content
                                                ] = msg.author.id
                                                new_dict[
                                                    "editable" + ctx.message.content
                                                ] = True
                                                await mymsg.edit(
                                                    content="ㅇㅋ `💰-500`",
                                                    allowed_mentions=discord.AllowedMentions.all(),
                                                )
                                                setpoint(
                                                    ctx.message.author.id,
                                                    getpoint(
                                                        ctx.message.author.id,
                                                        guild=ctx.guild,
                                                    )
                                                    - 500,
                                                    guild=ctx.guild,
                                                )
                                                log(
                                                    "Taking 500 Points from "
                                                    + str(ctx.message.author),
                                                    guild=ctx.message.guild,
                                                )
                                                savefile(
                                                    "dict",
                                                    new_dict,
                                                    guild=ctx.message.guild,
                                                )
                                                pending.remove(ctx.message.content)
                                                using.remove(ctx.message.author.id)
                                                return
                                    elif msg.content == "아니":
                                        await mymsg.edit(content="ㅇㅋ 싫음말고")
                                        return
                            else:
                                await mymsg.edit(content="500포인트 벌고와")
                                return

            if isowner(ctx.message.author.id):
                mymsg = await ctx.message.channel.send(
                    "주인님 새 명령어가 필요하십니까", allowed_mentions=discord.AllowedMentions.all()
                )
            elif getpoint(ctx.message.author.id, guild=ctx.guild) >= 200:
                mymsg = await ctx.message.channel.send("200포인트를 사용해서 대답을 알려줄래?")
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
            else:
                if msg.content == "어":
                    if isowner(ctx.message.author.id):
                        if ctx.message.content in pending:
                            await mymsg.edit(content="누군가 수정중인것 같아요 ;)")
                            return
                        pending.append(ctx.message.content)
                        using.append(ctx.message.author.id)
                        await mymsg.edit(
                            content="주인님 무엇을 원하십니까.",
                            allowed_mentions=discord.AllowedMentions.all(),
                        )
                        try:
                            msg = await bot.wait_for("message", check=checkc)
                        except asyncio.TimeoutError:
                            await mymsg.edit(content="...")
                            pending.remove(ctx.message.content)
                            using.remove(ctx.message.author.id)
                            return
                        else:
                            if msg.content == "":
                                errlog(
                                    "Cannot store empty message",
                                    guild=ctx.message.guild,
                                )
                                await mymsg.edit(
                                    content="주인님 이건좀...",
                                    allowed_mentions=discord.AllowedMentions.all(),
                                )
                                pending.remove(ctx.message.content)
                                using.remove(ctx.message.author.id)
                            else:
                                new_dict[ctx.message.content] = msg.content
                                new_dict["id" + ctx.message.content] = msg.author.id
                                new_dict["editable" + ctx.message.content] = True
                                await mymsg.edit(
                                    content="주인님 등록하였읍니다.",
                                    allowed_mentions=discord.AllowedMentions.all(),
                                )
                                savefile("dict", new_dict, guild=ctx.message.guild)
                                pending.remove(ctx.message.content)
                                using.remove(ctx.message.author.id)
                    else:
                        if ctx.message.content in pending:
                            await mymsg.edit(content="누군가 수정중인것 같아요 ;)")
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
                        else:
                            if msg.content == "":
                                errlog(
                                    "Cannot store empty message",
                                    guild=ctx.message.guild,
                                )
                                await mymsg.edit(
                                    content="이걸 어케등록하란겨",
                                    allowed_mentions=discord.AllowedMentions.all(),
                                )
                                pending.remove(ctx.message.content)
                                using.remove(ctx.message.author.id)
                            else:
                                new_dict[ctx.message.content] = msg.content
                                new_dict["id" + ctx.message.content] = msg.author.id
                                new_dict["editable" + ctx.message.content] = True
                                await mymsg.edit(
                                    content="ㅇㅋ `💰-200`",
                                    allowed_mentions=discord.AllowedMentions.all(),
                                )
                                setpoint(
                                    ctx.message.author.id,
                                    getpoint(ctx.message.author.id, guild=ctx.guild)
                                    - 200,
                                    guild=ctx.guild,
                                )
                                log(
                                    "Taking 200 Points from " + str(ctx.message.author),
                                    guild=ctx.message.guild,
                                )
                                savefile("dict", new_dict, guild=ctx.message.guild)
                                pending.remove(ctx.message.content)
                                using.remove(ctx.message.author.id)
                elif msg.content == "아니":
                    if isowner(ctx.message.author.id):
                        await mymsg.edit(content="알겠습니다 주인님")
                    else:
                        await mymsg.edit(content="ㅇㅋ 싫음말고")
            return
