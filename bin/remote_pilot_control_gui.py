#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename
import ScrolledText
import subprocess as sub
import os

# settings

main_window_title = """ 2Step Remote Pilot Control Mega Advanced (unregistered) """
about = """
2Step Remote Pilot Control 0.8 (c) Peter Krauspe DFS 11/2015
The expert tool for
Remote Piloting
"""

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
# app settings
subtype = "psp"


resource_nsc_list = ()
resource_nsc_list_dict = {}
remote_nsc_list = ()
target_config_list = ()
nsc_status_list = ()

def newFile():
    name = askopenfilename()
    name = askopenfilename
    print "open: ", name

def openFile():
    name = askopenfilename()
    print "open: ", name

def About():
    print about


def getFileAsTuple(file):
    return [tuple(line.rstrip('\n').split()) for line in open(file) if not line.startswith('#')]


def Quit():
        print "Quit"
        root.quit()

def runShell(cmd):
    # http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
    # p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE)
    # output, errors = p.communicate()
    # return output, errors

    p = sub.Popen(cmd, shell=True, stderr=sub.PIPE)
    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            return out
            # sys.stdout.write(out)
            # sys.stdout.flush()


class redirectText(object):
    """http://stackoverflow.com/questions/24707308/get-command-window-output-to-display-in-widget-with-tkinter
    http://stackoverflow.com/questions/30669015/autoscroll-of-text-and-scrollbar-in-python-text-box"""

    def __init__(self, outtext):
        """Constructor"""
        self.output = outtext

    def write(self, string):
        """"""
        self.output.insert(END, string)
        self.output.see("end")


class MainApp(Frame):

    #def __init__(self, root, *args, **kwargs):
    def __init__(self, root=None ):
        """http://stackoverflow.com/questions/6129899/python-multiple-frames-with-grid-manager"""
        self.choosen = {}
        self.var = {}
        self.output = "Console output initialized.\n\n"
        self.r1 = 0
        self.label_txt_trans = {"available": "LOCAL", "occupied": "REMOTE"}
        self.label_textcol = { "available" : "blue", "occupied" : "red"}

        #Frame.__init__(self, master=None,*args, **kwargs)
        Frame.__init__(self, root)

        # LOGO
        self.frame = Frame(root, bg="lightblue")
        #self.frame.grid(row=0,column=6)
        self.frame.grid(row=0,column=0)
        self.logo = PhotoImage(file="../images/dfs.gif")
        Label(self.frame, image=self.logo).grid(row=0,column=0)
        # Label(self, fg="dark blue", bg="dark grey", font="Helvetica 13 bold italic", text=explanation).grid(row=0,column=1);
        # self.slogan = Button(frame, text="MachDasEsGeht", command=self.writeSlogan).grid(row=0,column=2)

        # CONSOLE
        self.con_frame = Frame(root, bg="white")
        self.con_frame.grid(row=1, column=0)
        self.console = ScrolledText.ScrolledText(self.con_frame, bg="white")
        self.console.grid(row=1, column=0)
        # redirect stdout
        redir = redirectText(self.console)
        sys.stdout = redir
        self.console.insert(END, self.output)

        # BUTTONS
        n=0
        self.con_and_button_frame = Frame(root, bg="lightgrey")
        self.con_and_button_frame.grid(row=1, column=3, sticky=W+E+N+S)
        Button(self.con_and_button_frame, text="Update Remote Pilot Status", command=self.updateStatus).grid(row=1, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Start reconfiguration", bg="red", command=self.startReconfiguration).grid(row=2, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="print resource NSC list", command=self.printResourceNscList).grid(row=3, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="print remote NSC list", command=self.printRemoteNscList).grid(row=4, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="print status list", command=self.printNscStatusList).grid(row=5, column=1, sticky=W+E)
        Button(self.con_and_button_frame,text="QUIT", fg="red",command=self.frame.quit).grid(row=6,column=1, sticky=W+E)

        self.list_frame = Frame(root, bg="grey")
        self.list_frame.grid(row=4, column=0)
        Label(self.list_frame, text="Resource %s " % subtype, width=25, relief=GROOVE, highlightthickness=2).grid(row=2, column=0)
        Label(self.list_frame, text="Current %s " % subtype, width=25, relief=GROOVE).grid(row=2, column=1)
        Label(self.list_frame, text="Status", width=25, relief=GROOVE).grid(row=2, column=2)
        Label(self.list_frame, text="Choose Remote  %s " % subtype, width=25, relief=GROOVE).grid(row=2, column=3)

        self.buildMenu(root)
        self.updateStatus()


    def displayLists(self):
        print "Display lists...\n"

        self.r1 = 3
        for resfqdn,curfqdn,status in self.nsc_status_list:
            #print resfqdn,curfqdn,status
            Label(self.list_frame, text=resfqdn, width=25, bd=2, relief=GROOVE).grid(row=self.r1, column=0)
            Label(self.list_frame, text=curfqdn, width=25, relief=SUNKEN).grid(row=self.r1, column=1)
            Label(self.list_frame, text=self.label_txt_trans[status], width=25, fg=self.label_textcol[status], relief=SUNKEN).grid(row=self.r1, column=2)
            self.r1 +=1

        self.r1 = 3
        # var.set('default')

        for fqdn,mac in self.resource_nsc_list:
            self.var[fqdn] = StringVar()
            # self.choosen[fqdn] = self.var
            # http://effbot.org/tkinterbook/optionmenu.htm
            option = OptionMenu(self.list_frame, self.var[fqdn], *self.max_target_fqdn_list)
            option.grid(row=self.r1,column=3)
            self.r1 +=1

    def updateStatus(self):
        print "\nprint choosen fqdn assignment...\n"
        self.r1 = 1
        self.loadLists()
        self.displayLists()
        for fqdn,mac in self.resource_nsc_list:
            print fqdn, ": " , self.var[fqdn].get()
            #print fqdn, mac

    def printTargetConfigList(self):
        print "\nTarget config list:\n"
        for line in self.target_config_list:
            print line

    def printResourceNscList(self):
        print "\nResource nsc list:\n"
        for line in self.resource_nsc_list:
            print line
    def printRemoteNscList(self):
        print "\nRemote nsc list:\n"
        for line in self.remote_nsc_list:
            print line

    def printNscStatusList(self):
        print "\nStatus list:\n"
        for line in self.nsc_status_list:
            print line

    def startReconfiguration(self):
        print "\nStarting reconfiguraiton of NSCs ....\n"
        self.output = runShell("ls -la")


    def loadLists(self):
        print "Loading Lists ..."
        self.nsc_status_list = getFileAsTuple(nsc_status_list_file)
        self.resource_nsc_list = getFileAsTuple(resource_nsc_list_file)
        self.resource_nsc_list_dict = dict(self.resource_nsc_list)
        self.remote_nsc_list = getFileAsTuple(remote_nsc_list_file)
        self.max_target_fqdn_list = [fqdn for fqdn in self.remote_nsc_list] + ["default"]
        self.target_config_list = getFileAsTuple(target_config_list_file)


    def writeSlogan(self):
        print "Alles geht !"

    def buildMenu(self, root):
        self.menu = Menu(self)
        root.config(menu=self.menu)

        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=newFile)
        file_menu.add_command(label="Open...", command=openFile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=Quit)

        list_menu = Menu(self.menu)
        self.menu.add_cascade(label="List", menu=list_menu)
        list_menu.add_command(label="Target Config", command=self.printTargetConfigList)
        list_menu.add_command(label="Status", command=self.printNscStatusList)

        help_menu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Register", command=self.inputRegistrationKey)
        help_menu.add_command(label="About...", command=About)



    def inputRegistrationKey(self):
        '''inputRegistrationKey'''
        print("Open inputRegistrationKey Dialog")
        # t = Toplevel(self)
        # t.wm_title("Register")
        # l = Label(t, text="Type in your registration keys").pack()
        #
        #
        # self.entrytext = StringVar()
        # Entry(self.root, textvariable=self.entrytext).pack()
        #
        # self.buttontext = StringVar()
        # self.buttontext.set("Check")
        # Button(self.root, textvariable=self.buttontext, command=self.clicked1).pack()
        #
        # self.label = Label(self.root, text="")
        # self.label.pack()


    # def clicked1(self):
    #     self.input = self.entrytext.get()
    #     self.label.configure(text=self.input)
    #     print "Print: ", self.input



if __name__ == "__main__":
    root = Tk()
    root.title(main_window_title)
    main = MainApp(root)
    #main.grid(row=0,column=0)
    main.grid()
    root.mainloop()
    root.destroy()

