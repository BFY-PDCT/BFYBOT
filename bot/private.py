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
from cmds import (
    botname,
    botcolor,
    bot,
    using,
    log,
)


@bot.event
async def on_private_channel_create(channel):
    ver = discord.Embed(
        title="Hi! I am " + botname,
        color=botcolor,
    )
    await channel.send("Hello!", embed=ver)


async def on_message_pre(
    message,
):  # if this function return true, on_message will return

    # Custom Code Here

    return False


async def on_admin_message(message):
    log("WELCOME ADMIN")

    # Custom Code Here

    using.remove(message.author.id)
    await bot.process_commands(message)
    return
