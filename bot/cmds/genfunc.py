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

import os
import traceback
import time
import discord
from datetime import datetime
from operator import truediv, mul, add, sub
from discord.ext import commands
from .config import owner, eventlogger, conn, db
from .locales import getlc

operators = {"+": add, "-": sub, "*": mul, "/": truediv, "^": pow}


def calculate(s):
    log("calculate " + s)
    if s.isdigit():
        return float(s)
    for c in operators.keys():
        left, operator, right = s.partition(c)
        if operator in operators:
            return operators[operator](calculate(left), calculate(right))


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        eventlogger.error("Error: Creating directory. " + directory)


def log(msg, *, guild=None):
    if guild is None:
        eventlogger.info(msg)
    else:
        eventlogger.info(str(guild.id) + " - " + msg)


def dbglog(msg, *, guild=None):
    if guild is None:
        eventlogger.debug(msg)
    else:
        eventlogger.debug(str(guild.id) + " - " + msg)


def errlog(msg, *, guild=None):
    if guild is None:
        eventlogger.warning(msg)
    else:
        eventlogger.warning(str(guild.id) + " - " + msg)


def dumpdb():
    with conn:
        ts = time.time()
        log("Generating DB Backup")
        try:
            if not os.path.exists("./bbdata/backup"):
                os.makedirs("./bbdata/backup")
        except Exception as e:
            return
        with open(
            "./bbdata/backup/dbbackup-"
            + datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            + ".txt",
            "w",
        ) as f:
            for line in conn.iterdump():
                f.write("%s\n" % line)
        log("DB Backup generated in {}sec".format(str(time.time() - ts)))


def tblog(e, *, guild=None):
    errlog(
        "".join(traceback.format_exception(type(e), e, e.__traceback__)), guild=guild
    )


def loadallsetting(kwd):
    db.execute("SELECT * FROM setting WHERE name=?", (kwd,))
    subres = db.fetchall()
    if subres is None:
        return False
    res = []
    for tmp in subres:
        res.append(tmp[2])
    return res


def loadsetting(kwd, guild):
    db.execute(
        "SELECT * FROM setting WHERE guildid=? AND name=?",
        (
            guild.id,
            kwd,
        ),
    )
    subres = db.fetchone()
    if subres is None:
        return None
    return subres[2]


def savesetting(kwd, guild, tosave):
    delsetting(kwd, guild)
    db.execute(
        "INSERT OR REPLACE INTO setting(guildid, name, data) \
        VALUES(?,?,?)",
        (guild.id, kwd, tosave),
    )
    conn.commit()


def delsetting(kwd, guild):
    db.execute(
        "DELETE FROM setting WHERE guildid=? AND name=?",
        (
            guild.id,
            kwd,
        ),
    )
    conn.commit()


def loaddict(kwd):
    db.execute("SELECT * FROM dict WHERE command=?", (kwd,))
    subres = db.fetchone()
    if subres is None:
        return False
    return (subres[1], subres[2], subres[3])


def savedict(kwd, tosave):
    db.execute(
        "INSERT OR REPLACE INTO dict(command, replystr, editable, author) \
        VALUES(?,?,?,?)",
        (
            kwd,
            tosave[0],
            tosave[1],
            tosave[2],
        ),
    )
    conn.commit()


def deldict(kwd):
    db.execute("DELETE FROM dict WHERE command=?", (kwd,))
    conn.commit()


def isadmin(uid, guild):
    db.execute(
        "SELECT * FROM setting WHERE guildid=? AND name=?",
        (
            guild.id,
            "admin",
        ),
    )
    subres = db.fetchall()
    if subres is None:
        db.execute(
            "INSERT INTO setting(guildid, name, data) \
            VALUES(?,?,?)",
            (
                guild.id,
                "admin",
                guild.owner_id,
            ),
        )
        conn.commit()
        subres.append([guild.owner_id, "admin", uid])
    if len(subres) == 0:
        db.execute(
            "INSERT INTO setting(guildid, name, data) \
            VALUES(?,?,?)",
            (
                guild.id,
                "admin",
                guild.owner_id,
            ),
        )
        conn.commit()
        subres.append([guild.owner_id, "admin", uid])
    res = []
    for tmp in subres:
        res.append(tmp[2])
    return uid in res


def addadmin(uid, guild):
    if isadmin(uid, guild):
        return False
    db.execute(
        "INSERT INTO setting(guildid, name, data) \
        VALUES(?,?,?)",
        (
            guild.id,
            "admin",
            uid,
        ),
    )
    conn.commit()
    return True


def deladmin(uid, guild):
    guildid = guild.id
    if uid in owner:
        return 3
    if uid == guild.owner_id:
        return 2
    if not isadmin(uid, guild):
        return 1
    db.execute(
        "DELETE FROM setting WHERE guildid=? AND name=?",
        (
            guildid,
            "admin",
        ),
    )
    conn.commit()
    return 0


def admincheck():
    async def adminchk(ctx):
        return isadmin(ctx.author.id, ctx.guild)

    return commands.check(adminchk)


def isban(uid):
    db.execute(
        "SELECT * FROM gsetting WHERE name=?",
        ("ban",),
    )
    subres = db.fetchall()
    res = []
    for tmp in subres:
        res.append(tmp[1])
    return uid in res


def addban(uid):
    if isban(uid):
        return False
    db.execute(
        "INSERT INTO gsetting(name, data) \
        VALUES(?,?)",
        (
            "ban",
            uid,
        ),
    )
    conn.commit()
    return True


def delban(uid):
    if not isban(uid):
        return 1
    db.execute(
        "DELETE FROM gsetting WHERE name=? AND data=?",
        (
            "ban",
            uid,
        ),
    )
    conn.commit()
    return 0


async def getlocale(ctx):
    uid = ctx.author.id
    db.execute("SELECT * FROM gsetting WHERE name=?", ("lang" + str(uid)))
    res = db.fetchone()
    if res is None:
        emb = discord.Embed(title="Please set locale before using bot")
        await ctx.send()
        return None
    lang = res[1]
    return getlc.getlocale(lang)


async def setlocale(ctx, lang):
    uid = ctx.author.id
    db.execute(
        "INSERT OR REPLACE INTO gsetting(name, data) \
        VALUES(?,?)",
        (
            ("lang" + str(uid)),
            lang,
        ),
    )
    conn.commit()


def isowner(uid):
    return uid in owner


def setpoint(uid, newpoint: int, guild):
    db.execute(
        "INSERT OR REPLACE INTO point(guildid, uid, point) \
        VALUES(?,?,?)",
        (
            guild.id,
            uid,
            newpoint,
        ),
    )
    conn.commit()


def getpoint(uid, guild):
    db.execute(
        "SELECT * FROM point WHERE guildid=? AND uid=?",
        (
            guild.id,
            uid,
        ),
    )
    res = db.fetchone()
    if res is None:
        setpoint(uid, 0, guild)
        return 0
    return res[2]


def setstk(stype, uid, newpoint: int, guild):
    db.execute(
        "INSERT OR REPLACE INTO stock(guildid, uid, stype, count) \
        VALUES(?,?,?,?)",
        (
            guild.id,
            uid,
            stype,
            newpoint,
        ),
    )
    conn.commit()


def getstk(stype, uid, guild):
    db.execute(
        "SELECT * FROM stock WHERE guildid=? AND uid=? AND stype=?",
        (
            guild.id,
            uid,
            stype,
        ),
    )
    res = db.fetchone()
    if res is None:
        setstk(stype, uid, 0, guild)
        return 0
    return res[3]


def recstk(stype, uid, guild, buy, cnt, price):
    if not buy:
        cnt *= -1
    db.execute(
        "INSERT INTO stocklog(guildid, uid, stype, count, price) \
        VALUES(?,?,?,?,?)",
        (
            guild.id,
            uid,
            stype,
            cnt,
            price,
        ),
    )
    conn.commit()


def getrecstk(stype, uid, guild):
    db.execute(
        "SELECT * FROM stocklog WHERE guildid=? AND uid=? AND stype=?",
        (
            guild.id,
            uid,
            stype,
        ),
    )
    subres = db.fetchall()
    res = []
    for tmp in subres:
        if tmp[3] < 0:
            a = False
            b = tmp[3] * -1
        else:
            a = True
            b = tmp[3]
        res.insert(0, [a, b, tmp[4]])
    return res


"""
NOT USED
async def download(url, file_name):
    with open(file_name, "wb") as file:
        dbglog("querying " + url)
        httpclient = http3.AsyncClient()
        resp = await httpclient.get(url, timeout=100.0)
        file.write(resp.content)
"""
