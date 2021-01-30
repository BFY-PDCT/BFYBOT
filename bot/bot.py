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

# Main Code

from cmds import (
    economy,
    general,
    manage,
    dictcmd,
    game,
    update,
    privatecmd,
    bot,
    token,
)
from events import (
    on_guild_join,
    on_guild_remove,
    on_member_join,
    on_member_remove,
    on_message,
    on_ready,
)
from private import on_private_channel_create


def main():
    economy.initcmd()
    general.initcmd()
    manage.initcmd()
    dictcmd.initcmd()
    game.initcmd()
    update.initcmd()
    privatecmd.initcmd()
    try:
        bot.loop.run_until_complete(bot.start(token))
    except KeyboardInterrupt:
        bot.loop.run_until_complete(bot.logout())
    finally:
        bot.loop.close()


if __name__ == "__main__":
    main()
