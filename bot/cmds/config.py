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

import sys

if __name__ == "__main__":
    print("Please execute bot.py")
    sys.exit(0)

import discord
import logging
import os
from discord.ext import commands

# Owner Setting
owner = [0]  # owner IDs as list / 소유자(슈퍼오너)의 ID를 리스트로 모두 입력해주세요.
token = ""  # bot token / 봇 토큰
invlink = ""  # invite link / 초대 링크
vernum = "v1.4.0"  # version info / 버전 정보
prefix = ""  # prefix / 프리픽스
botname = ""  # bot's name / 봇 이름
hasmusic = False  # whether there is a music function / 음악 기능을 추가로 제공하는지
botcolor = 0x008EFE  # bot color / 봇의 색상
musicstr = "음악 기능은 외부 프로그램을 통해 제공됩니다."  # notice about music function
helpmusicstr = "#help를 입력해주세요."  # help command of music function
# End

# Config Error Check
if len(owner) == 0:
    print("EMERG - Error: Owner can't be None")
    sys.exit(0)
if not isinstance(owner, list[int]):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(token, str):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(invlink, str):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(vernum, str):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(prefix, str):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(botname, str):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(hasmusic, bool):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(botcolor, int):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(musicstr, str):
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(helpmusicstr, str):
    print("EMERG - Error: TypeError")
    sys.exit(0)

try:
    if not os.path.exists("./bbdata"):
        os.makedirs("./bbdata")
except OSError:
    print("EMERG - Error: Creating directory ./bbdata")
    sys.exit(0)

pending, noticed, using, muted = [], [], [], []

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix=prefix + " ", intents=intents, help_command=None)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s")
eventlogger = logging.getLogger("event")
eventlogger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(formatter)
filehandler = logging.FileHandler(filename="./bbdata/log.txt", encoding="utf-8")
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
eventlogger.addHandler(console)
eventlogger.addHandler(filehandler)