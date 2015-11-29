#!/usr/bin/env python

from Tkinter import *

root = Tk()

options = ["one", "two", "three", "four"]
var = {}
option = {}

for i in range(5):
    var[i] = StringVar(root)
    option[i] = OptionMenu(root, var[i], *options)
    option[i].pack()
    print i
#
# test stuff

def ok():
    for i in range(5):
        print "value is", var[i].get()

Button(root, text="OK", command=ok).pack()
Button(root, text="QUIT", command=root.quit).pack()


mainloop()

