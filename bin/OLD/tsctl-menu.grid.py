#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename
import os

root = Tk()

def NewFile():
    name = askopenfilename()
    name = askopenfilename
    print "open: ", name
    
def OpenFile():
    name = askopenfilename()
    print "open: ", name
    nsc_status_list_file
def About():
    print about

def ListTargetConfig():
    for line in target_config_list:
        print line
    
def ListStatus():
    for line in nsc_status_list:
        print line

def GetFileAsTuple(file):
    return [tuple(line.rstrip('\n').split()) for line in open(file) if not line.startswith('#')]


# settings

logo = PhotoImage(file="../images/dfs.gif")
explanation = """ 2StepControl Mega Advanced """
about = """ 
2StepControl 0.7 (c) Peter Krauspe DFS 2015
The expert Tool for
Remote Piloting
"""

# app settings

basedir = ".."
bindir  = os.path.join(basedir,"bin")
confdir = os.path.join(basedir,"config")
vardir  = os.path.join(basedir, "var")
resource_nsc_list_file  = os.path.join(vardir,"resource_nsc.list")
target_config_list_file = os.path.join(vardir,"target_config.list")
remote_nsc_list_file    = os.path.join(vardir,"remote_nsc.list")
nsc_status_list_file    = os.path.join(vardir,"nsc_status.list")

# todo: einlesen und auswerten
#source ${confdir}/remote_nsc.cfg # providing:  subtype, ResourceDomainServers, RemoteDomainServers


resource_nsc_list = GetFileAsTuple(resource_nsc_list_file)
resource_nsc_list_dict = dict(resource_nsc_list)

remote_nsc_list = GetFileAsTuple(remote_nsc_list_file)
target_config_list = GetFileAsTuple(target_config_list_file)
nsc_status_list = GetFileAsTuple(nsc_status_list_file)

w1 = Label(root, image=logo).grid(row=0,column=0)
w2 = Label(root,  
           fg = "dark blue",
           bg = "dark grey",
           font = "Helvetica 16 bold italic", 
#           justify=LEFT,
           padx = 10, 
           text=explanation).grid(row=0,column=1)

# Menu

    
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
list_menu.add_command(label="Target Config", command=ListTargetConfig)
list_menu.add_command(label="Status", command=ListStatus)

help_menu = Menu(menu)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About...", command=About)

class App:

  def __init__(self, master):
    frame = Frame(master)
    frame.grid(row=1,column=2)
    r1=1
    r2=1
    Label(text="resource nsc list", relief=RIDGE).grid(row=r1,column=0)
    Label(text="remote nsc list", relief=RIDGE).grid(row=r2,column=1)
    r1 +=1
    r2 +=1
    for fqdn,mac in resource_nsc_list:
        Label(text=fqdn, relief=RIDGE).grid(row=r1,column=0)
        r1 +=1
    for fqdn in remote_nsc_list:
        Label(text=fqdn, relief=RIDGE).grid(row=r2,column=1)
        r2 +=1

    r1=r2+1
    Label(text="status list", relief=RIDGE).grid(row=r1,column=0)
    r1 +=1
    
    for resfqdn,remfqdn,status in nsc_status_list:
        Label(text=resfqdn, relief=SUNKEN).grid(row=r1,column=0)
        Label(text=status, relief=SUNKEN).grid(row=r1,column=1)
        r1 +=1
    
    r3 = 1
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.grid(row=r3,column=3)
    self.slogan = Button(frame,
                         text="MachDasEsGeht",
                         command=self.write_slogan)
    self.slogan.grid(row=r3+1,column=3)

  def write_slogan(self):
    print "Alles geht !"

app = App(root)


mainloop()

