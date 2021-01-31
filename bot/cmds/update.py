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

import pickle
import random
import numpy as np
import matplotlib.pyplot as plt
from .config import bot, muted
from .genfunc import loadfile, log, is_non_zero_file, createFolder
from discord.errors import Forbidden, HTTPException
from discord.ext import tasks, commands
from discord.ext.commands import Context


def initcmd():
    # bot.add_command (함수 이름)
    bot.add_cog(updatestka(bot))
    bot.add_cog(updatestkb(bot))
    bot.add_cog(updatestkc(bot))
    bot.add_cog(updatemute(bot))


class updatestka(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log("load stocka data")
        print("load stocka data")
        a = is_non_zero_file("./bbdata/stocka.custom")
        if not a:
            createFolder("./bbdata")
            new_array = [19500, 20000]
            with open("./bbdata/stocka.custom", "wb") as fw:
                pickle.dump(new_array, fw)
            self.res = new_array
        else:
            with open("./bbdata/stocka.custom", "rb") as fr:
                array_loaded = pickle.load(fr)
            self.res = array_loaded
        self.inc, self.pn = True, self.res[len(self.res) - 1]
        self.delta = 0
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
        cp, ra, rb, t, mn, mx = 7, 5, 100, 500000, 500, 100000  # stock const numbers
        x = random.uniform(ra, rb)
        x = t / (x * x * x)
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
        return

    def sell(self, cnt: int):
        self.delta = self.delta + cnt // 10
        return

    @process.after_loop
    async def on_process_cancel(self):
        if self.process.is_being_cancelled():
            log("save stocka data")
            print("save stocka data")
            with open("./bbdata/stocka.custom", "wb") as fw:
                pickle.dump(self.res, fw)


class updatestkb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log("load stockb data")
        print("load stockb data")
        a = is_non_zero_file("./bbdata/stockb.custom")
        if not a:
            createFolder("./bbdata")
            new_array = [195000, 200000]
            with open("./bbdata/stockb.custom", "wb") as fw:
                pickle.dump(new_array, fw)
            self.res = new_array
        else:
            with open("./bbdata/stockb.custom", "rb") as fr:
                array_loaded = pickle.load(fr)
            self.res = array_loaded
        self.inc, self.pn = True, self.res[len(self.res) - 1]
        self.delta = 0
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
        cp, ra, rb, t, mn, mx = (
            4,
            60,
            300,
            8000000000,
            20000,
            1000000,
        )  # stock const numbers
        x = random.uniform(ra, rb)
        x = t / (x * x * x)
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
        return

    def sell(self, cnt: int):
        self.delta = self.delta + cnt * 10
        return

    @process.after_loop
    async def on_process_cancel(self):
        if self.process.is_being_cancelled():
            log("save stockb data")
            print("save stockb data")
            with open("./bbdata/stockb.custom", "wb") as fw:
                pickle.dump(self.res, fw)


class updatestkc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log("load stockc data")
        print("load stockc data")
        a = is_non_zero_file("./bbdata/stockc.custom")
        if not a:
            createFolder("./bbdata")
            new_array = [2000, 2000]
            with open("./bbdata/stockc.custom", "wb") as fw:
                pickle.dump(new_array, fw)
            self.res = new_array
        else:
            with open("./bbdata/stockc.custom", "rb") as fr:
                array_loaded = pickle.load(fr)
            self.res = array_loaded
        self.inc, self.pn = True, self.res[len(self.res) - 1]
        self.delta = 0
        self.process.start()

    def cog_unload(self):
        self.process.cancel()

    @tasks.loop(seconds=15.0)
    async def process(self):
        if self.delta > 50:
            self.delta = 50
        if self.delta < -50:
            self.delta = -50
        self.pn = self.pn + self.delta
        self.delta = 0
        cp, ra, rb, t, mn, mx = 10, 10, 80, 20000, 200, 5000  # stock const numbers
        x = random.uniform(ra, rb)
        x = t / (x * x)
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
        return

    def sell(self, cnt: int):
        self.delta = self.delta + cnt // 20
        return

    @process.after_loop
    async def on_process_cancel(self):
        if self.process.is_being_cancelled():
            log("save stockc data")
            print("save stockc data")
            with open("./bbdata/stockc.custom", "wb") as fw:
                pickle.dump(self.res, fw)


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
                except:
                    pass
                muted.remove(mute)
            if mute[2] <= -1:
                try:
                    await self.unmute(mute, param=1)
                except:
                    pass
                muted.remove(mute)
            mute[2] = mute[2] - 1

    async def unmute(self, mute, param=0):
        guild = bot.get_guild(mute[1])
        if guild == None:
            log("Can't find guild")
            return
        member = await guild.fetch_member(mute[0])
        if member == None:
            log("Can't find guild")
            return
        setting_loaded = loadfile("setting", guild=guild)
        channel = guild.get_channel(mute[4])
        if param == 0:
            await member.edit(roles=mute[3], reason="MUTE Command Timeout")
            log("Unmuted " + member.name, guild=guild)
            if "chnl" in setting_loaded:
                try:
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "처리 종료되었습니다 - 뮤트 {.mention}".format(member)
                    )
                except HTTPException:
                    await channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(member))
                    await channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
                except Forbidden:
                    await channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(member))
                    await channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            else:
                await channel.send("처리 종료되었습니다 - 뮤트 {.mention}".format(member))
        elif param == 1:
            await member.edit(roles=mute[3], reason="MUTE Command Cancel")
            log("Unmuted " + member.name, guild=guild)
            if "chnl" in setting_loaded:
                try:
                    await bot.get_channel(setting_loaded["chnl"]).send(
                        "처리 종료되었습니다 - 뮤트 {.mention} / 처리자: {.mention}".format(
                            member, mute[5]
                        )
                    )
                except HTTPException:
                    await channel.send(
                        "처리 종료되었습니다 - 뮤트 {.mention} / 처리자: {.mention}".format(
                            member, mute[5]
                        )
                    )
                    await channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
                except Forbidden:
                    await channel.send(
                        "처리 종료되었습니다 - 뮤트 {.mention} / 처리자: {.mention}".format(
                            member, mute[5]
                        )
                    )
                    await channel.send("구독 설정에 오류가 있습니다. 수정해주세요.")
            else:
                await channel.send(
                    "처리 종료되었습니다 - 뮤트 {.mention} / 처리자: {.mention}".format(
                        member, mute[5]
                    )
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
        await self.bot.wait_until_ready()

    @process.after_loop
    async def on_process_cancel(self):
        if self.process.is_being_cancelled():
            for mute in muted:
                if mute[2] == 0:
                    try:
                        await self.unmute(mute)
                    except:
                        pass
                    muted.remove(mute)
                if mute[2] <= -1:
                    try:
                        await self.unmute(mute, param=1)
                    except:
                        pass
                    muted.remove(mute)
                nrlist = []
                for role in mute[3]:
                    try:
                        nrlist.append(role.id)
                    except:
                        pass
                mute[3] = nrlist
            log("save ongoing mute data")
            print("save ongoing mute data")
            with open("./bbdata/muted.custom", "wb") as fw:
                pickle.dump(muted, fw)