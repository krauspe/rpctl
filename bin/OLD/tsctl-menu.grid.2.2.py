#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox

import os

#root = Tk()

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

def InputRegistrationKey():
    dialog = GetRegistrationKeyDialog(root)
    dialog.build_dialog()
    print dialog.GetValue()

def on_key_enetered(dialog):
    print "key_enetered: ", dialog.GetValue()
    
  
def Quit():
        print "Quit"
        root.quit()

# settings

logo = PhotoImage(file="../images/dfs.gif")
explanation = """ 2StepControl Mega Advanced \n(unregistered) """
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


    
class MainApp(Frame):
    #def __init__(self,root):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)    
        
        Label(self, image=logo).grid(row=0,column=0)
        Label(self,  
               fg = "dark blue",
               bg = "dark grey",
               font = "Helvetica 16 bold italic", 
    #           justify=LEFT,
               padx = 10, 
               text=explanation).grid(row=0,column=1)
        frame = Frame(self)
        frame.grid(row=1,column=3)
        r1 = 1
        list_witdth = 25
        Label(self, text="resource nsc list",width=list_witdth, relief=RIDGE).grid(row=r1,column=0)
        Label(self, text="remote nsc list",width=list_witdth, relief=RIDGE).grid(row=r1,column=1)
        Label(self, text="status list",width=list_witdth, relief=RIDGE).grid(row=r1,column=2)
        r1 +=1
        
        for resfqdn,remfqdn,status in nsc_status_list:
            Label(self, text=resfqdn,width=list_witdth, relief=SUNKEN).grid(row=r1,column=0)
            Label(self, text=remfqdn,width=list_witdth, relief=SUNKEN).grid(row=r1,column=1)
            Label(self, text=status,width=list_witdth,  relief=SUNKEN).grid(row=r1,column=2)
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
        self.build_menu()
        
        def write_slogan(self):
            print "Alles geht !"
        
        def build_menu(self):
            self.menu = Menu(self.root)
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
            help_menu.add_command(label="Register", command=InputRegistrationKey)
            help_menu.add_command(label="About...", command=About)
              
    class GetRegistrationKeyDialog(object):
        def __init__(self,root):
            self.root = Frame(root)
            #frame = Frame(root)

            
        def build_dialog(self):
            #self.root.wm_title("Register")
            self.label = Label (self.root, text= "Type in your registration key")
            self.label.pack()
    ##        self.result = ""

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
    ##        print "Print: ", self.input
            on_key_entered(self)
            

        def button_click(self, e):
            pass

        def GetValue(self):
            return self.input



##app = App(root)
##mainloop()
##root.destroy()


if __name__ == "__main__":
    root = Tk()
    main = MainApp(root)
    #main.pack(side="top", fill="both", expand=True)
    root.mainloop()



