#!/usr/bin/env python

from Tkinter import *
from tkFileDialog   import askopenfilename

root = Tk()

# settings

logo = PhotoImage(file="../images/dfs.png")
explanation = """ 2StepControl Mega Advanced """
about = """ 
2StepControl 0.7 (c) Peter Krauspe DFS 2015
The expert Tool for
Remote Piloting
"""
resource_nsc_list = """
psp1-s1.ak1.lgn.dfs.de
psp2-s1.ak1.lgn.dfs.de
psp3-s1.ak2.lgn.dfs.de
psp4-s1.ak2.lgn.dfs.de
"""
remote_nsc_list = """
psp101-s1.ka1.krl.dfs.de
psp102-s1.ka1.krl.dfs.de
psp103-s1.mu1.muc.dfs.de
psp104-s1.br1.bre.dfs.de
"""
target_config_list = """
psp1-s1.ak1.lgn.dfs.de psp101-s1.ka1.krl.dfs.de
psp2-s1.ak1.lgn.dfs.de psp102-s1.ka1.krl.dfs.de
psp3-s1.ak2.lgn.dfs.de psp103-s1.mu1.muc.dfs.de
psp4-s1.ak2.lgn.dfs.de 
"""
status_list = """
psp1-s1.ak1.lgn.dfs.de psp101-s1.ka1.krl.dfs.de occupied
psp2-s1.ak1.lgn.dfs.de psp102-s1.ka1.krl.dfs.de occupied
psp3-s1.ak2.lgn.dfs.de psp103-s1.mu1.muc.dfs.de occupied
psp4-s1.ak2.lgn.dfs.de psp4-s1.ak2.lgn.dfs.de   available
"""



w1 = Label(root, image=logo).pack(side="left")
w2 = Label(root,  
           fg = "dark blue",
           bg = "dark grey",
           font = "Helvetica 16 bold italic", 
           justify=LEFT,
           padx = 10, 
           text=explanation).pack(side="top")

# Menu

def NewFile():
    print "Target Config"
def OpenFile():
    name = askopenfilename()
    print name
def About():
    print about
def List(list=list):
    print list
    
menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=NewFile)
file_menu.add_command(label="Open...", command=OpenFile)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

list_menu = Menu(menu)
menu.add_cascade(label="List", menu=list_menu)
list_menu.add_command(label="Resouce NSCs", command=List(list=resource_nsc_list))
list_menu.add_command(label="Remote NSCs", command=List(list=remote_nsc_list))
list_menu.add_command(label="Target Config", command=List(list=target_config_list))
list_menu.add_command(label="Status", command=List(list=status_list))

help_menu = Menu(menu)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About...", command=About)

class App:

  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.pack(side="bottom")
    self.slogan = Button(frame,
                         text="MachDasEsGeht",
                         command=self.write_slogan)
    self.slogan.pack(side=LEFT)

  def write_slogan(self):
    print "Alles geht !"

app = App(root)


mainloop()

