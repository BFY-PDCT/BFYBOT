#######################################################
#                                                     #
#      BFY Entertainment                              #
#      Written-by: J.H.Lee                            #
#      (jhlee@bfy.kr)                                 #
#                                                     #
#######################################################

# Main Code

from cmds import economy, general, manage, dictcmd, game, bot, token
from events import (
    on_guild_join,
    on_guild_remove,
    on_member_join,
    on_member_remove,
    on_message,
    on_ready,
)


def main():
    economy.initcmd()
    general.initcmd()
    manage.initcmd()
    dictcmd.initcmd()
    game.initcmd()
    bot.run(token)


if __name__ == "__main__":
    main()
