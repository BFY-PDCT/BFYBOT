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

import random
import time
import numpy as np
import matplotlib.pyplot as plt
from .locales import getlc
from .config import bot, muted, conn, db
from .genfunc import dbglog, log, dumpdb, loadsetting, getlocalebyuid, localeerr
from discord.errors import HTTPException
from discord.ext import tasks, commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_cog(autodumpdb(bot))
    bot.add_cog(updatestka(bot))
    bot.add_cog(updatestkb(bot))
    bot.add_cog(updatestkc(bot))
    bot.add_cog(updatemute(bot))


class autodumpdb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process.start()

    def cog_unload(self):
        self.process.cancel()

    @tasks.loop(seconds=60*60*24)
    async def process(self):
        dumpdb()


class updatestka(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log("load stocka data")
        ts = time.time()
        print("Loading StockA Data...", end="")
        db.execute("SELECT * FROM stockdata WHERE stype=?", ("a"))
        subres = db.fetchall()
        self.res = []
        for tmp in subres:
            self.res.append(tmp[1])
        if len(self.res) == 0:
            self.inc, self.pn = True, 10000
        else:
            self.inc, self.pn = True, self.res[len(self.res) - 1]
        self.delta = 0
        print("OK ({}s)".format(str(time.time() - ts)))
        self.process.start()

    def cog_unload(self):
        self.process.cancel()

    @tasks.loop(seconds=60.0)
    async def process(self):
        if self.delta > 5000:
            self.delta = 5000
        if self.delta < -5000:
            self.delta = -5000
        self.pn = self.pn + self.delta
        self.delta = 0
        cp, ra, rb, t, mn, mx, exp = (
            7,
            5,
            100,
            500000,
            5000,
            50000,
            3,
        )  # stock const numbers
        x = random.uniform(ra, rb)
        x = t / (x ** exp)
        x = x // 1
        if not random.randrange(0, cp):
            self.inc = not self.inc
        if self.inc:
            self.pn = self.pn + x
        else:
            self.pn = self.pn - x
        if self.pn > mx:
            self.pn = mx
            self.inc = not self.inc
        if self.pn < mn:
            self.pn = mn
            self.inc = not self.inc
        self.res.append(self.pn)

        if len(self.res) > 1000:
            self.res.pop(0)

        x = np.arange(len(self.res))
        resary = np.array(self.res)

        plt.plot(x, resary[x])
        plt.title("STOCK: BFY Ent")
        plt.xlabel("time")
        plt.ylabel("price")
        plt.tight_layout()
        plt.savefig("./bbdata/stock_a.png", dpi=200)
        plt.clf()

    def getprice(self):
        return int(self.pn)

    def buy(self, cnt: int):
        self.delta = self.delta - cnt // 10

    def sell(self, cnt: int):
        self.delta = self.delta + cnt // 10

    @process.after_loop
    async def on_process_cancel(self):
        if self.process.is_being_cancelled():
            log("save stocka data")
            ts = time.time()
            print("Saving StockA Data...", end="")
            resdata = []
            for data in self.res:
                resdata.append(("a", data))
            db.execute("DELETE FROM stockdata WHERE stype=?", ("a"))
            db.executemany(
                "INSERT INTO stockdata(stype, price) \
                VALUES(?,?)",
                resdata,
            )
            print("OK ({}s)".format(str(time.time() - ts)))


class updatestkb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log("load stockb data")
        ts = time.time()
        print("Loading StockB Data...", end="")
        db.execute("SELECT * FROM stockdata WHERE stype=?", ("b"))
        subres = db.fetchall()
        self.res = []
        for tmp in subres:
            self.res.append(tmp[1])
        if len(self.res) == 0:
            self.inc, self.pn = True, 100000
        else:
            self.inc, self.pn = True, self.res[len(self.res) - 1]
        self.delta = 0
        print("OK ({}s)".format(str(time.time() - ts)))
        self.process.start()

    def cog_unload(self):
        self.process.cancel()

    @tasks.loop(seconds=60.0 * 2)
    async def process(self):
        if self.delta > 20000:
            self.delta = 20000
        if self.delta < -20000:
            self.delta = -20000
        self.pn = self.pn + self.delta
        self.delta = 0
        cp, ra, rb, t, mn, mx, exp = (
            4,
            60,
            300,
            8000000000,
            50000,
            500000,
            3,
        )  # stock const numbers
        x = random.uniform(ra, rb)
        x = t / (x ** exp)
        x = x // 1
        if not random.randrange(0, cp):
            self.inc = not self.inc
        if self.inc:
            self.pn = self.pn + x
        else:
            self.pn = self.pn - x
        if self.pn > mx:
            self.pn = mx
            self.inc = not self.inc
        if self.pn < mn:
            self.pn = mn
            self.inc = not self.inc
        self.res.append(self.pn)

        if len(self.res) > 1000:
            self.res.pop(0)

        x = np.arange(len(self.res))
        resary = np.array(self.res)

        plt.plot(x, resary[x])
        plt.title("STOCK: BFY Corp")
        plt.xlabel("time")
        plt.ylabel("price")
        plt.tight_layout()
        plt.savefig("./bbdata/stock_b.png", dpi=200)
        plt.clf()

    def getprice(self):
        return int(self.pn)

    def buy(self, cnt: int):
        self.delta = self.delta - cnt * 10

    def sell(self, cnt: int):
        self.delta = self.delta + cnt * 10

    @process.after_loop
    async def on_process_cancel(self):
        if self.process.is_being_cancelled():
            log("save stockb data")
            ts = time.time()
            print("Saving StockB Data...", end="")
            resdata = []
            for data in self.res:
                resdata.append(("b", data))
            db.execute("DELETE FROM stockdata WHERE stype=?", ("b"))
            db.executemany(
                "INSERT INTO stockdata(stype, price) \
                VALUES(?,?)",
                resdata,
            )
            print("OK ({}s)".format(str(time.time() - ts)))


class updatestkc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log("load stockc data")
        ts = time.time()
        print("Loading StockC Data...", end="")
        db.execute("SELECT * FROM stockdata WHERE stype=?", ("c"))
        subres = db.fetchall()
        self.res = []
        for tmp in subres:
            self.res.append(tmp[1])
        if len(self.res) == 0:
            self.inc, self.pn = True, 1000
        else:
            self.inc, self.pn = True, self.res[len(self.res) - 1]
        self.delta = 0
        print("OK ({}s)".format(str(time.time() - ts)))
        self.process.start()

    def cog_unload(self):
        self.process.cancel()

    @tasks.loop(seconds=15.0)
    async def process(self):
        if self.delta > 20:
            self.delta = 20
        if self.delta < -20:
            self.delta = -20
        self.pn = self.pn + self.delta
        self.delta = 0
        cp, ra, rb, t, mn, mx, exp = (
            10,
            10,
            80,
            20000,
            500,
            5000,
            2,
        )  # stock const numbers
        x = random.uniform(ra, rb)
        x = t / (x ** exp)
        x = x // 1
        if not random.randrange(0, cp):
            self.inc = not self.inc
        if self.inc:
            self.pn = self.pn + x
        else:
            self.pn = self.pn - x
        if self.pn > mx:
            self.pn = mx
            self.inc = not self.inc
        if self.pn < mn:
            self.pn = mn
            self.inc = not self.inc
        self.res.append(self.pn)

        if len(self.res) > 1000:
            self.res.pop(0)

        x = np.arange(len(self.res))
        resary = np.array(self.res)

        plt.plot(x, resary[x])
        plt.title("STOCK: AT7 Group")
        plt.xlabel("time")
        plt.ylabel("price")
        plt.tight_layout()
        plt.savefig("./bbdata/stock_c.png", dpi=200)
        plt.clf()

    def getprice(self):
        return int(self.pn)

    def buy(self, cnt: int):
        self.delta = self.delta - cnt // 20

    def sell(self, cnt: int):
        self.delta = self.delta + cnt // 20

    @process.after_loop
    async def on_process_cancel(self):
        if self.process.is_being_cancelled():
            log("save stockc data")
            ts = time.time()
            print("Saving StockC Data...", end="")
            resdata = []
            for data in self.res:
                resdata.append(("c", data))
            db.execute("DELETE FROM stockdata WHERE stype=?", ("c"))
            db.executemany(
                "INSERT INTO stockdata(stype, price) \
                VALUES(?,?)",
                resdata,
            )
            print("OK ({}s)".format(str(time.time() - ts)))


class updatemute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process.start()

    def cog_unload(self):
        self.process.cancel()

    @tasks.loop(seconds=1.0)
    async def process(self):
        for mute in muted:
            if mute[2] == 0:
                try:
                    await self.unmute(mute)
                except Exception as e:
                    dbglog(
                        "unmute failed roleid: "
                        + str(mute[3])
                        + ", guildid: "
                        + str(mute[0])
                    )
                muted.remove(mute)
            if mute[2] <= -1:
                try:
                    await self.unmute(mute, param=1)
                except Exception as e:
                    dbglog(
                        "unmute failed roleid: "
                        + str(mute[3])
                        + ", guildid: "
                        + str(mute[0])
                    )
                muted.remove(mute)
            mute[2] = mute[2] - 1

    async def unmute(self, mute, param=0):
        guild = bot.get_guild(mute[1])
        if guild is None:
            log("Can't find guild")
            return
        member = await guild.fetch_member(mute[0])
        if member is None:
            log("Can't find member")
            return
        locale = getlocalebyuid(member.id)
        if locale is None:
            locale = getlc.getlocale("en")
        setting_loaded = loadsetting("chnl", guild)
        channel = guild.get_channel(mute[4])
        if param == 0:
            await member.edit(roles=mute[3], reason="MUTE Command Timeout")
            log("Unmuted " + member.name, guild=guild)
            if setting_loaded is not False:
                try:
                    await bot.get_channel(setting_loaded).send(
                        locale["update_1"].format(member.mention)
                    )
                except HTTPException:
                    await channel.send(locale["update_1"].format(member.mention))
                    await channel.send(locale["update_2"])
            else:
                await channel.send(locale["update_1"].format(member.mention))
        elif param == 1:
            await member.edit(roles=mute[3], reason="MUTE Command Cancel")
            log("Unmuted " + member.name, guild=guild)
            if setting_loaded is not False:
                try:
                    await bot.get_channel(setting_loaded).send(
                        locale["update_0"].format(member.mention, mute[5].mention)
                    )
                except HTTPException:
                    await channel.send(
                        locale["update_0"].format(member.mention, mute[5].mention)
                    )
                    await channel.send(locale["update_2"])
            else:
                await channel.send(
                    locale["update_0"].format(member.mention, mute[5].mention)
                )
        return

    async def unmutenow(self, ctx: Context):
        guild = ctx.guild
        member = ctx.message.mentions[0]
        mute = None
        for tmpmute in muted:
            if tmpmute[0] == member.id and tmpmute[1] == guild.id:
                mute = tmpmute
                break
        if mute is None:
            return False
        mute[2] = -1
        mute.append(ctx.author)
        return True

    @process.before_loop
    async def before_process(self):
        log("wait until bot ready")
        ts = time.time()
        print("Waiting Until Bot Ready...", end="")
        await self.bot.wait_until_ready()
        print("OK ({}s)".format(str(time.time() - ts)))
        log("load ongiong mute data")
        ts = time.time()
        print("Loading Ongiong Mute Data...", end="")
        db.execute("SELECT * FROM muted")
        res = db.fetchall()
        tmp = [0, 0, 0, 0, 0]
        for mute in res:
            if (
                tmp[0] == mute[1]
                and tmp[1] == mute[0]
                and tmp[2] == mute[2]
                and tmp[4] == mute[4]
            ):
                try:
                    tmp[3].append(bot.get_guild(mute[0]).get_role(mute[3]))
                except Exception as e:
                    dbglog(
                        "get role failed roleid: "
                        + str(mute[3])
                        + ", guildid: "
                        + str(mute[0])
                    )
            else:
                if tmp != [0, 0, 0, 0, 0]:
                    muted.append(tmp)
                try:
                    tmp = [
                        mute[1],
                        mute[0],
                        mute[2],
                        [bot.get_guild(mute[0]).get_role(mute[3])],
                        mute[4],
                    ]
                except Exception as e:
                    dbglog(
                        "get role failed roleid: "
                        + str(mute[3])
                        + ", guildid: "
                        + str(mute[0])
                    )
        muted.append(tmp)
        print("OK ({}s)".format(str(time.time() - ts)))

    @process.after_loop
    async def on_process_cancel(self):
        if self.process.is_being_cancelled():
            for mute in muted:
                if mute[2] == 0:
                    try:
                        await self.unmute(mute)
                    except Exception as e:
                        dbglog(
                            "unmute failed roleid: "
                            + str(mute[3])
                            + ", guildid: "
                            + str(mute[0])
                        )
                    muted.remove(mute)
                if mute[2] <= -1:
                    try:
                        await self.unmute(mute, param=1)
                    except Exception as e:
                        dbglog(
                            "unmute failed roleid: "
                            + str(mute[3])
                            + ", guildid: "
                            + str(mute[0])
                        )
                    muted.remove(mute)
                nrlist = []
                for role in mute[3]:
                    try:
                        nrlist.append(role.id)
                    except Exception as e:
                        dbglog(
                            "get role failed roleid: "
                            + str(mute[3])
                            + ", guildid: "
                            + str(mute[0])
                        )
                mute[3] = nrlist
            res = []
            for mute in muted:
                for role in mute[3]:
                    res.append([mute[1], mute[0], mute[2], role, mute[4]])
            log("save ongoing mute data")
            ts = time.time()
            print("Saving Ongoing Mute Data...", end="")
            db.execute("DELETE FROM muted")
            db.executemany(
                "INSERT INTO muted(guildid, uid, time, role, channel) \
                VALUES(?,?,?,?,?)",
                res,
            )
            conn.commit()
            print("OK ({}s)".format(str(time.time() - ts)))