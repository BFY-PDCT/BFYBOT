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
from private import on_admin_message, on_message_pre
from cmds import (
    prefix,
    botcolor,
    using,
    bot,
    isowner,
    loadfile,
    log,
    msglog,
)
from discord.errors import Forbidden, HTTPException


@bot.event
async def on_ready():
    log("We have logged in as {0.user}".format(bot))
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_member_join(member):
    log(
        "member joined NAME: " + str(member) + ", ID:" + str(member.id),
        guild=member.guild,
    )
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
            log("Error Sending Notice to " + str(setting_loaded["chnl"]))
        except Forbidden:
            log("Error Sending Notice to " + str(setting_loaded["chnl"]))
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
                log("role not found", guild=member.guild)
                if chnl:
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "새 멤버 역할이 잘못 지정되어 있습니다.",
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                using.remove(member.id)
                return
            await member.edit(roles=[xrole], reason="WELCOME!")
        except Forbidden:
            log("NO PERMISSION", guild=member.guild)
            if chnl:
                await bot.get_channel(setting_loaded["chnl"]).send(
                    "새 멤버 역할 변경 권한이 부족합니다.",
                    allowed_mentions=discord.AllowedMentions.all(),
                )
            using.remove(member.id)
            return


@bot.event
async def on_member_remove(member):
    log(
        "member removed NAME: " + str(member) + ", ID:" + str(member.id),
        guild=member.guild,
    )
    setting_loaded = loadfile("setting", guild=member.guild)
    if "chnl" in setting_loaded and "msgl" in setting_loaded:
        try:
            msgl = discord.Embed(title=setting_loaded["msgl"], color=botcolor)
            await bot.get_channel(setting_loaded["chnl"]).send(
                "{.mention}님이 떠났어요".format(member), embed=msgl
            )
        except HTTPException:
            log("Error Sending Notice to " + str(setting_loaded["chnl"]))
        except Forbidden:
            log("Error Sending Notice to " + str(setting_loaded["chnl"]))


@bot.event
async def on_guild_join(guild):
    log("guild joined NAME: " + str(guild.name) + ", ID:" + str(guild.id), guild=guild)


@bot.event
async def on_guild_remove(guild):
    log("guild removed NAME: " + str(guild.name) + ", ID:" + str(guild.id), guild=guild)


@bot.event
async def on_message(message):
    await bot.wait_until_ready()
    msglog(message, guild=message.guild)

    if message.author == bot.user:  # Ignore My Message
        return

    if await on_message_pre(message):  # Custom Pre-processing
        return

    if message.content.startswith(prefix):  # Block User Already Using
        if message.author.id in using:
            log("User Already Using: " + str(message.author.id))
            return

    if isowner(message.author.id):
        using.append(message.author.id)
        await on_admin_message(message)  # Custom Admin Commands
        return
    else:
        await bot.process_commands(message)
        return
