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
import os
import datetime
import http3
import traceback
from operator import pow, truediv, mul, add, sub
from discord.ext import commands
from .config import owner, eventlogger

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
    now = datetime.datetime.now()
    if guild is None:
        eventlogger.info(msg)
    else:
        eventlogger.info(str(guild.id) + " - " + msg)


def msglog(msg, *, guild=None):
    now = datetime.datetime.now()
    if guild is None:
        eventlogger.info(str(msg.author) + ": " + str(msg.content))
    else:
        eventlogger.info(
            str(guild.id) + " - " + str(msg.author) + ": " + str(msg.content)
        )


def errlog(msg, *, guild=None):
    now = datetime.datetime.now()
    if guild is None:
        eventlogger.warning(msg)
    else:
        eventlogger.warning(str(guild.id) + " - " + msg)


def tblog(msg, e, *, guild=None):
    traceback.print_exception(type(e), e, e.__traceback__)


def isadmin(id, guild):
    owner_list = loadfile("owner", guild=guild)
    return id in owner_list


def addadmin(id, guild):
    owner_list = loadfile("owner", guild=guild)
    if id in owner_list:
        return False
    owner_list.append(id)
    savefile("owner", owner_list, guild=guild)
    return True


def deladmin(id, guild):
    owner_list = loadfile("owner", guild=guild)
    if id in owner:
        return 3
    if id == guild.owner_id:
        return 2
    if not id in owner_list:
        return 1
    owner_list.remove(id)
    savefile("owner", owner_list, guild=guild)
    return 0


def admincheck():
    async def adminchk(ctx):
        return isadmin(ctx.author.id, ctx.guild)

    return commands.check(adminchk)


def isban(id):
    owner_list = loadfile("ban")
    return id in owner_list


def addban(id):
    owner_list = loadfile("ban")
    if id in owner_list:
        return False
    owner_list.append(id)
    savefile("ban", owner_list)
    return True


def delban(id):
    owner_list = loadfile("ban")
    if not id in owner_list:
        return 1
    owner_list.remove(id)
    savefile("ban", owner_list)
    return 0


def isowner(id):
    owner_list = loadfile("sowner")
    return id in owner_list


def addowner(id):
    owner_list = loadfile("sowner")
    if id in owner_list:
        return False
    owner_list.append(id)
    savefile("sowner", owner_list)
    return True


def delowner(id):
    owner_list = loadfile("sowner")
    if id in owner:
        return 3
    if not id in owner_list:
        return 1
    owner_list.remove(id)
    savefile("sowner", owner_list)
    return 0


def getpoint(id, guild):
    point_list = loadfile("point", guild=guild)
    if id not in point_list:
        return -1
    return point_list[id]


def setpoint(id, newpoint: int, guild):
    point_list = loadfile("point", guild=guild)
    point_list[id] = newpoint
    savefile("point", point_list, guild=guild)
    return


def getstk(type, id, guild):  # type in ['stka', 'stkb']
    point_list = loadfile(type, guild=guild)
    if id not in point_list:
        return -1
    return point_list[id]


def setstk(type, id, newpoint: int, guild):  # type in ['stka', 'stkb']
    point_list = loadfile(type, guild=guild)
    point_list[id] = newpoint
    savefile(type, point_list, guild=guild)
    return


def loadfile(type: str, *, guild=None):
    if type == "dict":
        a = is_non_zero_file("./bbdata/dict.custom")
        if not a:
            createFolder("./bbdata")
            new_dict = {}
            with open("./bbdata/dict.custom", "wb") as fw:
                pickle.dump(new_dict, fw)
            return {}
        else:
            with open("./bbdata/dict.custom", "rb") as fr:
                dict_loaded = pickle.load(fr)
            return dict_loaded
    elif type == "point":
        a = is_non_zero_file("./bbdata/" + str(guild.id) + "/point.custom")
        if not a:
            createFolder("./bbdata")
            createFolder("./bbdata/" + str(guild.id) + "/")
            new_dict = {}
            with open("./bbdata/" + str(guild.id) + "/point.custom", "wb") as fw:
                pickle.dump(new_dict, fw)
            return {}
        else:
            with open("./bbdata/" + str(guild.id) + "/point.custom", "rb") as fr:
                setting_loaded = pickle.load(fr)
            return setting_loaded
    elif type == "stka":
        a = is_non_zero_file("./bbdata/" + str(guild.id) + "/stka.custom")
        if not a:
            createFolder("./bbdata")
            createFolder("./bbdata/" + str(guild.id) + "/")
            new_dict = {}
            with open("./bbdata/" + str(guild.id) + "/stka.custom", "wb") as fw:
                pickle.dump(new_dict, fw)
            return {}
        else:
            with open("./bbdata/" + str(guild.id) + "/stka.custom", "rb") as fr:
                setting_loaded = pickle.load(fr)
            return setting_loaded
    elif type == "stkb":
        a = is_non_zero_file("./bbdata/" + str(guild.id) + "/stkb.custom")
        if not a:
            createFolder("./bbdata")
            createFolder("./bbdata/" + str(guild.id) + "/")
            new_dict = {}
            with open("./bbdata/" + str(guild.id) + "/stkb.custom", "wb") as fw:
                pickle.dump(new_dict, fw)
            return {}
        else:
            with open("./bbdata/" + str(guild.id) + "/stkb.custom", "rb") as fr:
                setting_loaded = pickle.load(fr)
            return setting_loaded
    elif type == "setting":
        a = is_non_zero_file("./bbdata/" + str(guild.id) + "/settings.custom")
        if not a:
            createFolder("./bbdata")
            createFolder("./bbdata/" + str(guild.id) + "/")
            new_dict = {}
            with open("./bbdata/" + str(guild.id) + "/settings.custom", "wb") as fw:
                pickle.dump(new_dict, fw)
            return {}
        else:
            with open("./bbdata/" + str(guild.id) + "/settings.custom", "rb") as fr:
                setting_loaded = pickle.load(fr)
            return setting_loaded
    elif type == "owner":
        a = is_non_zero_file("./bbdata/" + str(guild.id) + "/owner.custom")
        if not a:
            createFolder("./bbdata")
            createFolder("./bbdata/" + str(guild.id) + "/")
            new_array = [guild.owner_id] + owner
            with open("./bbdata/" + str(guild.id) + "/owner.custom", "wb") as fw:
                pickle.dump(new_array, fw)
            return new_array
        else:
            with open("./bbdata/" + str(guild.id) + "/owner.custom", "rb") as fr:
                owner_loaded = pickle.load(fr)
            return owner_loaded
    elif type == "sowner":
        a = is_non_zero_file("./bbdata/sowner.custom")
        if not a:
            createFolder("./bbdata")
            new_array = owner
            with open("./bbdata/sowner.custom", "wb") as fw:
                pickle.dump(new_array, fw)
            return new_array
        else:
            with open("./bbdata/sowner.custom", "rb") as fr:
                array_loaded = pickle.load(fr)
            return array_loaded
    elif type == "ban":
        a = is_non_zero_file("./bbdata/ban.custom")
        if not a:
            createFolder("./bbdata")
            new_array = []
            with open("./bbdata/ban.custom", "wb") as fw:
                pickle.dump(new_array, fw)
            return {}
        else:
            with open("./bbdata/ban.custom", "rb") as fr:
                array_loaded = pickle.load(fr)
            return array_loaded
    elif type == "settingall":
        setting_loaded = []
        files = os.listdir("./bbdata/")
        for item in files:
            if os.path.isdir("./bbdata/" + item):
                a = is_non_zero_file("./bbdata/" + item + "/settings.custom")
                if not a:
                    new_dict = {}
                    with open("./bbdata/" + item + "/settings.custom", "wb") as fw:
                        pickle.dump(new_dict, fw)
                else:
                    with open("./bbdata/" + item + "/settings.custom", "rb") as fr:
                        tmp = pickle.load(fr)
                    if "chnl" in tmp:
                        setting_loaded.append(tmp["chnl"])
        return setting_loaded


def savefile(type: str, data, *, guild=None):
    if type == "dict":
        with open("./bbdata/dict.custom", "wb") as fw:
            pickle.dump(data, fw)
        return
    elif type == "point":
        with open("./bbdata/" + str(guild.id) + "/point.custom", "wb") as fw:
            pickle.dump(data, fw)
        return
    elif type == "stka":
        with open("./bbdata/" + str(guild.id) + "/stka.custom", "wb") as fw:
            pickle.dump(data, fw)
        return
    elif type == "stkb":
        with open("./bbdata/" + str(guild.id) + "/stkb.custom", "wb") as fw:
            pickle.dump(data, fw)
        return
    elif type == "setting":
        with open("./bbdata/" + str(guild.id) + "/settings.custom", "wb") as fw:
            pickle.dump(data, fw)
        return
    elif type == "owner":
        with open("./bbdata/" + str(guild.id) + "/owner.custom", "wb") as fw:
            pickle.dump(data, fw)
        return
    elif type == "sowner":
        with open("./bbdata/sowner.custom", "wb") as fw:
            pickle.dump(data, fw)
        return
    elif type == "ban":
        with open("./bbdata/ban.custom", "wb") as fw:
            pickle.dump(data, fw)
        return


async def download(url, file_name):
    with open(file_name, "wb") as file:
        log("querying " + url)
        httpclient = http3.AsyncClient()
        resp = await httpclient.get(url, timeout=100.0)
        file.write(resp.content)
