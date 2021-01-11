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
from cmds import (
    owner,
    prefix,
    botname,
    botcolor,
    pending,
    noticed,
    using,
    bot,
    download,
    errlog,
    getpoint,
    loadfile,
    log,
    msglog,
    savefile,
    setpoint,
)
from discord.errors import Forbidden, HTTPException


def printstat(text):
    tmp = text + "\npending:"
    for i in pending:
        tmp += str(i) + ","
    tmp += "\nusing:"
    for i in using:
        tmp += str(i) + ","
    log(tmp)


@bot.event
async def on_ready():
    log("We have logged in as {0.user}".format(bot))


@bot.event
async def on_member_join(member):
    log("member joined NAME: " + str(member) + ", ID:" + str(member.id))
    setting_loaded = loadfile("setting", guild=member.guild)
    chnl = False
    if "chnl" in setting_loaded and "msgj" in setting_loaded:
        try:
            msgj = discord.Embed(title=setting_loaded["msgj"], color=botcolor)
            await bot.get_channel(setting_loaded["chnl"]).send(
                "{.mention}님이 참가했어요".format(member), embed=msgj
            )
            chnl = True
        except HTTPException:
            errlog("Error Sending Notice to " + str(setting_loaded["chnl"]))
        except Forbidden:
            errlog("Error Sending Notice to " + str(setting_loaded["chnl"]))
    if "joinrole" in setting_loaded:
        try:
            xrole: discord.Role = None
            find = False
            for rl in member.guild.roles:
                if rl.id == setting_loaded["joinrole"]:
                    xrole = rl
                    find = True
                    break
            if not find:
                errlog("role not found", guild=member.guild)
                if chnl:
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "새 멤버 역할이 잘못 지정되어 있습니다.",
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                using.remove(member.id)
                return
            await member.edit(roles=[xrole], reason="WELCOME!")
        except Forbidden:
            errlog("NO PERMISSION", guild=member.guild)
            if chnl:
                await bot.get_channel(setting_loaded["chnl"]).send(
                    "새 멤버 역할 변경 권한이 부족합니다.",
                    allowed_mentions=discord.AllowedMentions.all(),
                )
            using.remove(member.id)
            return


@bot.event
async def on_member_remove(member):
    log("member removed NAME: " + str(member) + ", ID:" + str(member.id))
    setting_loaded = loadfile("setting", guild=member.guild)
    if "chnl" in setting_loaded and "msgl" in setting_loaded:
        try:
            msgl = discord.Embed(title=setting_loaded["msgl"], color=botcolor)
            await bot.get_channel(setting_loaded["chnl"]).send(
                "{.mention}님이 떠났어요".format(member), embed=msgl
            )
        except HTTPException:
            errlog("Error Sending Notice to " + str(setting_loaded["chnl"]))
        except Forbidden:
            errlog("Error Sending Notice to " + str(setting_loaded["chnl"]))


@bot.event
async def on_message(message):
    await bot.wait_until_ready()
    msglog(message, guild=message.guild)

    if message.author == bot.user:  # Ignore My Message
        return

    if message.content.startswith(prefix):  # Block User Already Using
        if message.author.id in using:
            return

    log("PROCESS COMMAND")
    await bot.process_commands(message)
    return
