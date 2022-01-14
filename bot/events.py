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
import time
from cmds.locales import getlocale
from private import on_admin_message, on_message_pre
from cmds import (
    prefix,
    botcolor,
    using,
    bot,
    timestart,
    vernum,
    isowner,
    loadsetting,
    log,
    dbglog,
    getlocalebyuid,
)
from discord.errors import Forbidden, HTTPException


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("열심히 일"))
    log("We have logged in as {.user}".format(bot))
    loadtime = time.time() - timestart
    log("---- Done Loading in {} sec! Running BFYBOT {} ----".format(loadtime, vernum))
    print("Done Loading, logged in as {.user}! (total {}sec)".format(bot, loadtime))


@bot.event
async def on_member_join(member):
    locale = getlocalebyuid(member.id)
    if locale is None:
        locale = getlocale("en")
    setting_loaded = loadsetting("chnl", guild=member.guild)
    msgj = loadsetting("msgj", guild=member.guild)
    joinrole = loadsetting("joinrole", guild=member.guild)
    chnl = False
    if setting_loaded is not None and msgj is not None:
        try:
            msgje = discord.Embed(title=msgj, color=botcolor)
            await bot.get_channel(setting_loaded).send(
                locale["events_0"].format(member.mention), embed=msgje
            )
            chnl = True
        except HTTPException:
            log("Error Sending Notice to " + str(setting_loaded["chnl"]))
        except Forbidden:
            log("Error Sending Notice to " + str(setting_loaded["chnl"]))
    if joinrole is not None:
        try:
            xrole: discord.Role = None
            find = False
            for rl in member.guild.roles:
                if rl.id == joinrole:
                    xrole = rl
                    find = True
                    break
            if not find:
                log("role not found", guild=member.guild)
                if chnl:
                    await bot.get_channel(setting_loaded).send(
                        locale["events_1"],
                        allowed_mentions=discord.AllowedMentions.all(),
                    )
                return
            await member.edit(roles=[xrole], reason="WELCOME!")
        except Forbidden:
            log("NO PERMISSION", guild=member.guild)
            if chnl:
                await bot.get_channel(setting_loaded).send(
                    locale["events_2"],
                    allowed_mentions=discord.AllowedMentions.all(),
                )
            return


@bot.event
async def on_member_remove(member):
    locale = getlocalebyuid(member.id)
    if locale is None:
        locale = getlocale("en")
    setting_loaded = loadsetting("chnl", guild=member.guild)
    msgl = loadsetting("msgl", guild=member.guild)
    if setting_loaded is not None and msgl is not None:
        try:
            msgle = discord.Embed(title=msgl, color=botcolor)
            await bot.get_channel(setting_loaded).send(
                locale["events_3"].format(member.mention), embed=msgle
            )
        except HTTPException:
            log("Error Sending Notice to " + str(setting_loaded))
        except Forbidden:
            log("Error Sending Notice to " + str(setting_loaded))


@bot.event
async def on_guild_join(guild):
    dbglog(
        "guild joined NAME: " + str(guild.name) + ", ID:" + str(guild.id), guild=guild
    )


@bot.event
async def on_guild_remove(guild):
    dbglog(
        "guild removed NAME: " + str(guild.name) + ", ID:" + str(guild.id), guild=guild
    )


@bot.event
async def on_message(message):
    await bot.wait_until_ready()

    if message.author == bot.user:  # Ignore My Message
        return

    if await on_message_pre(message):  # Custom Pre-processing
        return

    if message.content.startswith(tuple(prefix)):  # Block User Already Using
        if message.author.id in using:
            log("User Already Using: " + str(message.author.id))
            return

    if isowner(message.author.id):
        using.append(message.author.id)
        await on_admin_message(message)  # Custom Admin Commands
        return

    await bot.process_commands(message)
    return