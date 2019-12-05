import config
from tkinter import *
import os
import LoDDict


def change(option):
    if getattr(config.options, option):
        setattr(config.options, option, False)
    else:
        config.options.drop_change = True


def mod(oc):
    config.options.mod = oc
    config.dictionary = LoDDict.LoDDict()


def start():
    main_window = Tk()
    monster_change = Button(main_window, text="Change Monster Stats", command=lambda: change("monster_change"))
    drop_change = Button(main_window, text="Change Monster Drops", command=lambda: change("drop_change"))
    oc = StringVar()
    oc.set("Base")
    mod_list = []
    for directories in os.listdir(config.cwd + "/Mods"):
        mod_list.append(directories)
    mods = OptionMenu(main_window, oc, *mod_list, command=mod)
    monster_change.grid(row=1, column=0)
    drop_change.grid(row=1, column=1)
    mods.grid(row=0, column=1)
    main_window.mainloop()

