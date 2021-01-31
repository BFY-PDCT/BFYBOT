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

from cmds import loadfile, is_non_zero_file, createFolder


def func():
    b = loadfile("dict")
    c = is_non_zero_file("./bbdata/dict.export.txt")
    if not c:
        createFolder("./bbdata")
    with open("./bbdata/dict.export.txt", "w", -1, "utf-8") as fw:
        for d, e in b.items():
            if d.startswith("id") or d.startswith("editable"):
                continue
            if "id" + d in b:
                fw.write("id: " + str(b["id" + d]) + " ")
            if "editable" + d in b:
                fw.write("ed: " + str(b["editable" + d]) + " ")
            fw.write("\n" + str(d) + "\n****\n" + str(e) + "\n--------\n")
    print("done")
    return


func()