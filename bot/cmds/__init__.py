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

from .config import (
    owner,
    token,
    invlink,
    vernum,
    prefix,
    botname,
    hasmusic,
    botcolor,
    pending,
    noticed,
    using,
    muted,
    bot,
)
from .genfunc import (
    addadmin,
    admincheck,
    calculate,
    createFolder,
    deladmin,
    download,
    errlog,
    getpoint,
    is_non_zero_file,
    isadmin,
    loadfile,
    log,
    msglog,
    savefile,
    setpoint,
)
