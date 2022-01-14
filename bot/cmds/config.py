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
import sqlite3
import time
from datetime import datetime
from discord.ext import commands

# owner - owner IDs as list / 소유자(슈퍼오너)의 ID를 리스트로 모두 입력해주세요.
# token - bot token / 봇 토큰
# invlink - invite link / 초대 링크
# vernum - version info / 버전 정보
# prefix - prefix / 프리픽스
# botname - bot's name / 봇 이름
# hasmusic - whether there is a music function / 음악 기능을 추가로 제공하는지
# botcolor - bot color / 봇의 색상
# musicstr - notice about music function
# helpmusicstr - help command of music function
# For detailed guide, see https://github.com/BFY-PDCT/BFYBOT/wiki/Editing-config.py

# Owner Setting
owner = [0]
token = ""
invlink = ""
vernum = "v1.7.0"
prefix = [""]
botname = ""
hasmusic = False
report = False
botcolor = 0x008EFE
musicstr = "음악 기능은 외부 프로그램을 통해 제공됩니다."
helpmusicstr = "#help를 입력해주세요."
# End

timestart = time.time()

# Config Error Check
ts = time.time()
print("Config Error Check...", end="")
if not (isinstance(owner, list) and all(isinstance(x, int) for x in owner)):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if len(owner) == 0:
    print("Fail")
    print("EMERG - Error: Owner can't be None")
    sys.exit(0)
if not isinstance(token, str):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(invlink, str):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(vernum, str):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not (isinstance(prefix, list) and all(isinstance(x, str) for x in prefix)):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if len(prefix) == 0:
    print("Fail")
    print("EMERG - Error: Prefix can't be None")
    sys.exit(0)
if not isinstance(botname, str):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(hasmusic, bool):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(report, bool):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(botcolor, int):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(musicstr, str):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
if not isinstance(helpmusicstr, str):
    print("Fail")
    print("EMERG - Error: TypeError")
    sys.exit(0)
print("OK ({}s)".format(str(time.time() - ts)))

# Check BfyBot DATA Directory (BBDATA)
ts = time.time()
print("Checking Data Directory...", end="")
try:
    if not os.path.exists("./bbdata"):
        os.makedirs("./bbdata")
except OSError:
    print("Fail")
    print("EMERG - Error: Failed to create directory ./bbdata")
    sys.exit(0)
print("OK ({}s)".format(str(time.time() - ts)))

# Initialize DB
ts = time.time()
print("Initializing DB...", end="")
try:
    conn = sqlite3.connect("./bbdata/bbdata.db")
    db = conn.cursor()
    db.execute(
        "CREATE TABLE IF NOT EXISTS dict \
        (command text PRIMARY KEY, replystr text, editable blob, author integer)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS point \
        (guildid integer, uid integer, point integer, \
        PRIMARY KEY(guildid, uid))"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS stock \
        (guildid integer, uid integer, stype text, \
        count integer, PRIMARY KEY(guildid, uid, stype))"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS stocklog \
        (guildid integer, uid integer, stype text, \
        count integer, price integer)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS stockdata \
        (stype text, price integer)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS setting \
        (guildid integer, name text, data blob)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS gsetting \
        (name text, data integer)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS muted \
        (guildid int, uid int, time int, role int, channel int)"
    )
    conn.commit()
except Exception as e:
    print("FAIL")
    print("EMERG - Error: " + str(e))
print("OK ({}s)".format(str(time.time() - ts)))

tmppfx = []
for x in prefix:
    tmppfx.append(x + " ")

pending, noticed, using, muted = [], [], [], []

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(
    command_prefix=tmppfx,
    intents=intents,
    help_command=None,
)

# Initialize Logger
ts = time.time()
print("Initializing Logger...", end="")
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s")
eventlogger = logging.getLogger("event")
eventlogger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(formatter)
filehandler = logging.FileHandler(
    filename="./bbdata/log-" + datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".txt",
    encoding="utf-8",
)
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
eventlogger.addHandler(console)
eventlogger.addHandler(filehandler)
print("OK ({}s)".format(str(time.time() - ts)))
