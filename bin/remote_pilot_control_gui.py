#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox

import os

def NewFile():
    name = askopenfilename()
    name = askopenfilename
    print "open: ", name
    
def OpenFile():
    name = askopenfilename()
    print "open: ", name

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

  
def Quit():
        print "Quit"
        root.quit()

# settings

explanation = """ 2Step Remote Pilot Control \n Mega Advanced (unregistered) """
about = """ 
2StepControl 0.7 (c) Peter Krauspe DFS 2015
The expert Tool for
Remote Piloting
"""

label_textcol = { "available" : "blue", "occupied" : "red"}

# app settings
subtype = "psp"

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
subtype = "psp"

##resource_nsc_list = ()
##resource_nsc_list_dict = {}
##remote_nsc_list = ()
##target_config_list = ()
##nsc_status_list = ()

    
class MainApp(Frame):
    def __init__(self, root, *args, **kwargs):

        Frame.__init__(self, *args, **kwargs)
        self.logo = PhotoImage(file="../images/dfs.gif")
        
        Label(self, image=self.logo).grid(row=0,column=0)
        Label(self,  
               fg = "dark blue",
               bg = "dark grey",
               font = "Helvetica 13 bold italic", 
               text=explanation).grid(row=0,column=1)
        frame = Frame(self)
        frame.grid(row=1,column=3)
        

        self.button = Button(frame,text="QUIT", fg="red",command=frame.quit).grid(row=0,column=5)
##        
##        self.slogan = Button(frame,
##                             text="MachDasEsGeht",
##                             command=self.write_slogan)
##        self.slogan.grid(row=0,column=2)

        Label(self, text="Resource %s " % subtype,width=25, relief=GROOVE, highlightthickness=2).grid(row=1,column=0)
        Label(self, text="Current %s "  % subtype,width=25, relief=GROOVE).grid(row=1,column=1)
        Label(self, text="Status",width=25, relief=GROOVE).grid(row=1,column=2)
        Label(self, text="Choose Remote  %s "  % subtype,width=25, relief=GROOVE).grid(row=1,column=3)

        Button(self,text="Get Remote Pilot Status", command=self.UpdateLists).grid(row=0,column=3)
        self.build_menu(root)
        

    def DisplayLists(self):
        print "Display Lists..."

        self.r1 = 2
        for resfqdn,curfqdn,status in self.nsc_status_list:
            print resfqdn,curfqdn,status
            Label(self, text=resfqdn,width=25, bd=2, relief=GROOVE).grid(row=self.r1,column=0)
            Label(self, text=curfqdn,width=25, relief=SUNKEN).grid(row=self.r1,column=1)
            Label(self, text=status,width=25, fg=label_textcol[status], relief=SUNKEN).grid(row=self.r1,column=2)
            self.r1 +=1
            
        self.r1 = 2
        var = StringVar(self)
        var.set('default')
        
        for fqdn in self.max_target_fqdn_list:
            option = OptionMenu(self, var, *self.max_target_fqdn_list)
            option.grid(row=self.r1,column=3)
            #Label(self, text=fqdn,width=25, relief=SUNKEN).grid(row=self.r1,column=3)
            self.r1 +=1

    def UpdateLists(self):
        self.r1 = 1
        self.LoadLists()
        self.DisplayLists()
        

    def LoadLists(self):
        print "Loading Lists ..." 
        self.nsc_status_list = GetFileAsTuple(nsc_status_list_file)
        self.resource_nsc_list = GetFileAsTuple(resource_nsc_list_file)
        self.resource_nsc_list_dict = dict(self.resource_nsc_list)
        self.remote_nsc_list = GetFileAsTuple(remote_nsc_list_file)
        self.max_target_fqdn_list = [fqdn for fqdn in self.remote_nsc_list] + ["default"]
        self.target_config_list = GetFileAsTuple(target_config_list_file)


        
    def write_slogan(self):
        print "Alles geht !"
    
    def build_menu(self, root):
        self.menu = Menu(self)
        root.config(menu=self.menu)

        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=NewFile)
        file_menu.add_command(label="Open...", command=OpenFile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=Quit)

        list_menu = Menu(self.menu)
        self.menu.add_cascade(label="List", menu=list_menu)
        list_menu.add_command(label="Target Config", command=ListTargetConfig)
        list_menu.add_command(label="Status", command=ListStatus)

        help_menu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Register", command=self.InputRegistrationKey)
        help_menu.add_command(label="About...", command=About)
          
            
            
    def InputRegistrationKey(self):
        t = Toplevel(self)
        t.wm_title("Register")
        l = Label(t, text="Type in your registration keys").pack()
     
    
        self.entrytext = StringVar()
        Entry(self.root, textvariable=self.entrytext).pack()

        self.buttontext = StringVar()
        self.buttontext.set("Check")
        Button(self.root, textvariable=self.buttontext, command=self.clicked1).pack()

        self.label = Label(self.root, text="")
        self.label.pack()


    def clicked1(self):
        self.input = self.entrytext.get()
        self.label.configure(text=self.input)
        print "Print: ", self.input



if __name__ == "__main__":
    root = Tk()
    main = MainApp(root)
    main.grid(row=0,column=0)
    root.mainloop()
    root.destroy()

