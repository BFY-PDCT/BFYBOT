#######################################################
#                                                     #
#      BFY Entertainment                              #
#      Written-by: J.H.Lee                            #
#      (jhlee@bfy.kr)                                 #
#                                                     #
#######################################################

from cmds.genfunc import loadfile, savefile, is_non_zero_file, createFolder


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