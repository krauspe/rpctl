#!/usr/bin/env python

#DONE: solve basedir path problem
#TODO: file not found error handling for status_list and target_config list
#DONE: disable "start reconfiguration" button after it has been pressed
#DONE: change default entry in remote fqdn select boxes to "no_change" after end of reconfiguration
#TODO: chosse solution for long lists of resource psps as workaround until creation off different "views" see below..
#DONE      -> Using scrolled labels: problem: when header in canvas frame: header scrolls too. header in own frame: it isn't alligned !
#TODO: create views (resource, remote, status...): possible solutins: tabs, windows, ..
#TODO: improve simulation: admin_get_status_list.sh should create a simulated status with random errors
#TODO:                     admin_reconfigure_nscs.sh should use the above get status script

from Tkinter import *
from tkFileDialog import askopenfilename,askopenfile
import tkFont
import ScrolledText
import subprocess as sub
import os
import pprint
from MyPILTools import LabelAnimated

# settings

# Titles
main_window_title = """ 2Step Remote Pilot Control 1.6 (unregistered) """
#main_window_title = """ 2Step Remote Pilot Control Mega Advanced (unregistered) """
about = """
2Step Remote Pilot Control 1.6 (c) Peter Krauspe DFS 11/2015
The expert tool for
Remote Piloting
"""
# operation mode

#mode = "simulate"
mode = "productive"
mode_comment = "as configured"

# path settings

pydir =  os.path.dirname(os.path.abspath(__file__))

basedir = os.path.dirname(pydir)
ext_basedir = os.path.join(os.path.dirname(basedir),'tsctl2')


imagedir = os.path.join(basedir, "images")
animdir = os.path.join(imagedir, "animated_gifs")
logo_filename = 'dfs.gif'
animated_gif_filename = 'airplane13.gif'
duration = 1
# default NOT in animated_gif dir because this can change ...
logo_file = os.path.join(imagedir, logo_filename)
animated_gif_file = os.path.join(imagedir, animated_gif_filename)

int_bindir  = os.path.join(basedir,"scripts")
int_confdir = os.path.join(basedir,"config")
int_vardir  = os.path.join(basedir, "var")

ext_bindir  = os.path.join(ext_basedir,"bin")
ext_confdir = os.path.join(ext_basedir,"config")
ext_vardir  = os.path.join(ext_basedir, "var")

sim_bindir  = os.path.join(basedir,"binsim")

cfg = {
    "productive":
           {"bindir":ext_bindir,
            "confdir":ext_confdir,
            "vardir":ext_vardir,
            "descr": "Production Mode"},
    "internal":
           {"bindir":int_bindir,
            "confdir":int_confdir,
            "vardir":int_vardir,
            "descr": "Using internal scripts and lists"},
    "internal_bin":
           {"bindir":int_bindir,
            "confdir":ext_confdir,
            "vardir":ext_vardir,
            "descr": "Using internal scripts and productive lists"},
    "simulate":
           {"bindir":sim_bindir,
            "confdir":int_confdir,
            "vardir":int_vardir,
            "descr": "Creating and using simulated internal lists"},
    }

# Workaround until settings are read from a file

# SETTINGS

# background colours for resource fqdn labels
lbgcol = {
    "ak1.lgn.dfs.de":"lightgreen",
    "ak2.lgn.dfs.de":"paleturquoise2",
    "ak3.lgn.dfs.de":"lightyellow",
    "ak4.lgn.dfs.de":"khaki1",
    "lx1.lgn.dfs.de":"lightcyan",
    "lx3.lgn.dfs.de":"lightblue",
    "te1.lgn.dfs.de":"lightyellow",
}

# label width settings
lhwidth = 17                                           # label header width
lwidth = 21

# label font settings
lhFont = {
    "family":"Arial Black",  # alternaive "Helvetica"
    "size":11,
}

lFont = {
    "family":"Arial",  # alternaive "Helvetica"
    "size":10,
}

optFont = {
    "family":"Arial",
    "size":10,
}
opthFont = {
    "family":"Arial Black",
    "size":9,
}

#TODO: maybe create a function for switching modes...

if not os.path.exists(ext_basedir):
    mode = "simulate"
    mode_comment = "because %s doesn't exist !\n" % ext_basedir

mode_comment = str(cfg[mode]["descr"]) + '\n' + mode_comment
bindir  = str(cfg[mode]["bindir"])
confdir = str(cfg[mode]["confdir"])
vardir  = str(cfg[mode]["vardir"])

print "basedir=", basedir
print "ext_basedir=", ext_basedir
print "bindir=", bindir
print "confdir=",confdir
print "vardir=",vardir

resource_nsc_list_file  = os.path.join(vardir,"resource_nsc.list")
target_config_list_file = os.path.join(vardir,"target_config.list")
remote_nsc_list_file    = os.path.join(vardir,"remote_nsc.list")
nsc_status_list_file    = os.path.join(vardir,"nsc_status.list")

#run_shell_opt = "fake"
run_shell_opt = ""

# todo: einlesen und auswerten
#source ${confdir}/remote_nsc.cfg # providing:  subtype, ResourceDomainServers, RemoteDomainServers
# app settings
subtype = "psp"

def newFile():
    name = askopenfilename()
    print "open: ", name

def About():
    print about

def getFileAsList(file):
    #return [tuple(line.rstrip('\n').split()) for line in open(file) if not line.startswith('#')]
    return [line.rstrip('\n').split() for line in open(file) if not line.startswith('#')]

def getFileAsListOfRow(file, row):
    return [line.rstrip('\n').split()[row] for line in open(file) if not line.startswith('#')]

def getTargetConfigList(file):
    '''https://docs.python.org/2/library/itertools.html
    itertools.izip_longest(*iterables[, fillvalue])
    Make an iterator that aggregates elements from each of the iterables.
    If the iterables are of uneven length, missing values are filled-in with fillvalue.
    Iteration continues until the longest iterable is exhausted. Equivalent to
    TODO:
    Einlesen von tuples ungleicher laenge mit itertools'''
    pass

def saveListAsFile(list,filepath):
    print "\nSaving %s\n" % filepath
    f = open(filepath, 'w')
    for tup in list:
        line = ''
        for element in tup:
            line += ' ' + element
        f.write(line + '\n')
    f.close()
    #print "type(line) = %s\n" % type(line)

def Quit():
        print "Quit"
        root.quit()

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
        self.init_output =  "\nConsole output initialized.\n\n" + mode_comment
        self.r1 = 0
        self.label_status_text_trans =         {"available" : "READY", "occupied" : "READY", "unreachable" : "UNREACHABLE !", None: ""}
        self.label_operation_mode_text_trans = {"available" : "LOCAL", "occupied" : "REMOTE", "unreachable" : "?", None: ""}
        self.label_status_textcol =            {"available" : "dark green", "occupied" : "dark green", "unreachable" : "red", None: "lightgrey"}
        self.label_operation_mode_textcol =    {"available" : "black", "occupied" : "blue", "unreachable" : "red", None: "lightgrey"}

        # Font settings

        self.lhFont = tkFont.Font(family=lhFont["family"], size=lhFont["size"])         # label header font
        self.lFont = tkFont.Font(family=lFont["family"], size=lhFont["size"])           # label font
        self.optFont = tkFont.Font(family=optFont["family"], size=optFont["size"])      # option menu font
        self.opthFont = tkFont.Font(family=opthFont["family"], size=opthFont["size"])   # option menu header font

        #Frame.__init__(self, master=None,*args, **kwargs)
        Frame.__init__(self, root)


        self.frame = Frame(root)
        self.frame.grid(row=0,column=1)

        # tried to move buttons in logo frame (kack !)
        #Button(self.frame, text="Print Remote PSP list", command=self.printRemoteNscList).grid(row=0, column=0, sticky="W")
        #Button(self.frame, text="Print Status list", command=self.printNscStatusList).grid(row=0, column=1,sticky="W")
        #Button(self.frame, text="Print Resource PSP list", command=self.printResourceNscList).grid(row=0, column=2, sticky="W")
        #Label(self.frame,  text="", width=90).grid(row=0, column=3,sticky=W+E)
        # LOGO
        #self.frame.grid(row=0,column=6)
        self.logo = PhotoImage(file=logo_file)
        Label(self.frame, image=self.logo).grid(row=0,column=1,sticky="E")
        # Label(self, fg="dark blue", bg="dark grey", font="Helvetica 13 bold italic", text=explanation).grid(row=0,column=1);
        # self.slogan = Button(frame, text="MachDasEsGeht", command=self.writeSlogan).grid(row=0,column=2)


        # CONSOLE
        self.con_frame = Frame(root, bg="white")
        self.con_frame.grid(row=1, column=0)
        self.console = ScrolledText.ScrolledText(self.con_frame, bg="white")
        self.console.grid(row=1, column=0)

        # show initial animated gif
        # changed function in LabelAnimated plays gif only once when duration is nagative
        self.anim = self.showAnimatedGif(animated_gif_file,1,"forever",2,1,1)


        # redirect stdout
        self.stdoutOrig = sys.stdout
        self.redir = redirectText(self.console)
        sys.stdout = self.redir
        #self.console.insert(END, self.output)

        # print initial message

        print self.init_output

        # BUTTONS
        n=0
        self.con_and_button_frame = Frame(root, bg="lightgrey")
        self.con_and_button_frame.grid(row=1, column=1, sticky=W+E+N+S)

        Button(self.con_and_button_frame, text="Deploy Configs", command=self.deploy_configs).grid(row=1, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Update Resource PSP List", command=self.update_resource_nsc_list, state=DISABLED).grid(row=2, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Update Remote Pilot Status", command=self.updateStatus).grid(row=3, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Simulate External Command", command=self.simulateExternalCommand).grid(row=4, column=1, sticky=W+E)
        ##Label(self.con_and_button_frame,  text="").grid(row=4, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Print Remote PSP list", command=self.printRemoteNscList).grid(row=5, column=1, sticky=W+E)

        Button(self.con_and_button_frame, text="Print Status list", command=self.printNscStatusList).grid(row=6, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Print Resource PSP list", command=self.printResourceNscList).grid(row=7, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Stop Animation", command=self.stopAnimation).grid(row=8, column=1, sticky=W+E)
        Label(self.con_and_button_frame,  text="").grid(row=9, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Confirm Remote PSP Choices", command=self.confirmRemotePSPChoices).grid(row=10, column=1, sticky=W+E)
        #Label(self.con_and_button_frame,  text="").grid(row=10, column=1, sticky=W+E)

        self.bt_Start_Reconfiguration = Button(self.con_and_button_frame, text="Start Reconfiguration", command=self.startReconfiguration, state=DISABLED, activebackground="red")
        self.bt_Start_Reconfiguration.grid(row=11, column=1, sticky=W+E)

        Label(self.con_and_button_frame,  text="").grid(row=12, column=1, sticky=W+E)
        Button(self.con_and_button_frame,text="QUIT", fg="red",command=self.frame.quit).grid(row=13,column=1, sticky=W+E)


        # LIST HEADER

        #################

        self.canvas_frame = Frame(root, bg="grey")
        self.canvas_frame.grid(row=4, column=0)

        self.canvas = Canvas(self.canvas_frame, borderwidth=0, background="#ffffff")

        self.list_frame = Frame(self.canvas, bg="grey")
        self.list_frame.grid(row=4, column=0)

        # Label(self.list_frame, text="Resource %s " % subtype.upper(), font="-weight bold", width=lwidth, bg="lightblue", relief=GROOVE).grid(row=2, column=0)
        # Label(self.list_frame, text="Current FQDN ", font="-weight bold", width=lwidth, bg="lightblue", relief=GROOVE).grid(row=2, column=1)
        # Label(self.list_frame, text="Operation Mode", font="-weight bold", width=lwidth, bg="lightblue", relief=GROOVE).grid(row=2, column=2)
        # Label(self.list_frame, text="Status", font="-weight bold", width=lwidth, bg="lightblue", relief=GROOVE).grid(row=2, column=3)
        # Label(self.list_frame, text="Choose Remote FQDN ", width=23, bg="lightblue", relief=GROOVE).grid(row=2, column=4)


        Label(self.list_frame, text="Resource %s " % subtype.upper(), font=self.lhFont, width=lhwidth, bg="deepskyblue2", relief=GROOVE).grid(row=2, column=0)
        Label(self.list_frame, text="Choose Remote FQDN ", font=self.opthFont, width=20, bg="lightyellow", relief=GROOVE).grid(row=2, column=1)
        Label(self.list_frame, text="Current FQDN ", font=self.lhFont, width=lhwidth, bg="deepskyblue2", relief=GROOVE).grid(row=2, column=2)
        Label(self.list_frame, text="Operation Mode", font=self.lhFont, width=lhwidth, bg="deepskyblue2", relief=GROOVE).grid(row=2, column=3)
        Label(self.list_frame, text="Status", font=self.lhFont, width=lhwidth, bg="deepskyblue2", relief=GROOVE).grid(row=2, column=4)


        self.vsb = Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.canvas.create_window((0,0),window=self.list_frame, anchor="nw",tags="self.list_frame")
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left",fill="both", expand=True)

        self.buildMenu(root)

        self.ResourceStatus = {}   # define explicit dict for resource fqdn status

        # LIST | OptionMenu

        self.lt_resfqdns = {}
        self.lt_curfqdns = {}
        self.lt_Status   = {}
        self.lt_operation_mode = {}

        self.lt_newfqdn   = {}
        self.label_resfqdn = {}
        self.label_curfqdn = {}
        self.label_status = {}
        self.label_operation_mode = {}
        self.om = {}

        self.new_target_config_list   = []

        self.createStatusView()


    def createStatusView(self):
        self.loadLists()
        self.r1 = 3
        #self.testoptions = ("aaa","bbb","ccc","ddd")
        for resfqdn,curfqdn,status in self.nsc_status_list:

            self.ResourceStatus[resfqdn] = status

            # wenn sich die Anzahl der resfqdns erhoeht fehlen hierfuer labels, daher Neustart noetig !
            # Loesung: weitere Lables fuer neue Eintrage erzeugen (nicht in init)

            # define tkinter vars
            self.lt_resfqdns[resfqdn] = StringVar()
            self.lt_curfqdns[resfqdn] = StringVar()
            self.lt_Status[resfqdn]   = StringVar()
            self.lt_operation_mode[resfqdn]   = StringVar()

            self.lt_newfqdn[resfqdn]  = StringVar()

            # set initial values
            self.lt_resfqdns[resfqdn].set(resfqdn)
            self.lt_curfqdns[resfqdn].set(curfqdn)
            self.lt_Status[resfqdn].set(self.label_status_text_trans[status]) # translate: available -> LOCAL , occupied -> REMOTE
            self.lt_operation_mode[resfqdn].set("")

            # mark labels depemding on domain of resfqdn

            self.dn = ".".join( (resfqdn.split("."))[1:])
            if lbgcol.has_key(self.dn):
                resfqdn_lbgcol = lbgcol[self.dn]
            else:
                resfqdn_lbgcol = "white"


            self.label_resfqdn[resfqdn] = Label(self.list_frame, textvariable=self.lt_resfqdns[resfqdn], font=self.lFont, width=lwidth,  relief=GROOVE, bg=resfqdn_lbgcol)
            self.label_resfqdn[resfqdn].grid(row=self.r1, column=0, sticky=N+S)

            self.label_curfqdn[resfqdn] = Label(self.list_frame, textvariable=self.lt_curfqdns[resfqdn], font=self.lFont, width=lwidth, relief=SUNKEN)
            self.label_curfqdn[resfqdn].grid(row=self.r1, column=2, sticky=N+S)

            self.label_operation_mode[resfqdn] = Label(self.list_frame, textvariable=self.lt_operation_mode[resfqdn], font=self.lFont, width=lwidth, fg=self.label_status_textcol[status], relief=SUNKEN)
            self.label_operation_mode[resfqdn].grid(row=self.r1, column=3, sticky=N+S)

            self.label_status[resfqdn] = Label(self.list_frame, textvariable=self.lt_Status[resfqdn], font=self.lFont, width=lwidth, fg=self.label_status_textcol[status], relief=SUNKEN)
            self.label_status[resfqdn].grid(row=self.r1, column=4, sticky=N+S)

            self.r1 +=1

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.updateStatusView()
        self.createOptionMENUS("init")


    # function for scrolled labels
    def onFrameConfigure(self, event):
       '''Reset the scroll region to encompass the inner frame'''
       self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=880,height=650)


    def runShell(self,cmd,opt):
        # http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
        #cmd = "cat /etc/HOSTNAME"
        #cmd = "/opt/dfs/tsctl2/bin/admin_get_status_list.sh"
        #print "Running on:\n"
        cmd  += "; echo ; echo Done."
        #cmd = "ls -la"

        self.text = ""
        self.err_text = ""

        if opt == "fake":
            print "  running shell command:(FAKE !)"
            print "\n  %s\n" % cmd
        else:
            print "  running shell command:"
            print "\n  %s\n" % cmd

            # p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE)
            # output, errors = p.communicate()
            # return output, errors

            #p = sub.Popen(cmd, shell=True, stderr=sub.PIPE)
            self.update_idletasks()

            p = sub.Popen(cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
            while True:
                out = p.stdout.read(1)
                if out == '' and p.poll() != None:
                    break
                if out != '':
                    # self.text += out
                    self.redir.write(out)
                    self.stdoutOrig.write(out)
            while True:
                err = p.stderr.read(1)
                if err == '' and p.poll() != None:
                    break
                if err != '':
                    # self.err_text += err
                    self.redir.write(err)
                    self.stdoutOrig.write(err)


            # print self.text
            # # print "ERRORS : "
            # print self.err_text

                    #print out
                    # return out
                    # sys.stdout.write(out)
                    # sys.stdout.flush()


    # define functions for external shell scripts

    def deploy_configs(self):
        self.runShell(os.path.join(bindir,"admin_deploy_configs.sh"), run_shell_opt)
    def update_status_list(self):
        self.runShell(os.path.join(bindir,"admin_get_status_list.sh"), run_shell_opt)
    def update_resource_nsc_list(self):
        self.runShell(os.path.join(bindir,"admin_get_resource_nsc_list.sh"), run_shell_opt)
    def reconfigure_nscs(self):
        self.runShell(os.path.join(bindir,"admin_reconfigure_nscs.sh"), run_shell_opt)
    def simulateExternalCommand(self):
        self.runShell(os.path.join(sim_bindir,"admin_simulate.sh"), run_shell_opt)


    # define other functions

    def confirmRemotePSPChoices(self):
        self.createTargetConfigListFromOptionMENU()
        self.createOptionMENUS("update")

    def updateStatus(self):
        print "updateStatus: "
        #print "CURRENTLY DISABLED run external script to update status at that state (force by pressing the button !!)"
        self.update_status_list()
        self.updateStatusView()

    def updateStatusView(self):
        # TODO: HIER sollte noch eine aktualisierbare python status abfrage mit differenzierten Status-Meldungen rein,
        # TODO: solange wird der status aus der nsc_status_list genommen

        #self.stopAnimation()
        self.nsc_status_list = getFileAsList(nsc_status_list_file)
        for resfqdn,curfqdn,status in self.nsc_status_list:
            self.ResourceStatus[resfqdn] = status
            self.lt_resfqdns[resfqdn].set(resfqdn)
            #self.lt_curfqdns[resfqdn].set(curfqdn.upper())
            # upper sieht kacke aus je nach schriftart !
            self.lt_curfqdns[resfqdn].set(curfqdn)
            self.lt_Status[resfqdn].set(self.label_status_text_trans[status])
            self.lt_operation_mode[resfqdn].set(self.label_operation_mode_text_trans[status])
            self.label_operation_mode[resfqdn].config(fg=self.label_operation_mode_textcol[status])
            self.label_curfqdn[resfqdn].config(fg=self.label_status_textcol[status])
            self.label_status[resfqdn].config(fg=self.label_status_textcol[status])


    def createOptionMENUS(self,opt):
        self.r1 = 3

        for resfqdn,curfqdn,status in self.nsc_status_list:
            if opt == "update":
                self.om[resfqdn].destroy()
            self.om[resfqdn] = OptionMenu(self.list_frame, self.lt_newfqdn[resfqdn], *self.max_target_fqdn_list)
            self.om[resfqdn].config(width=20, font=self.optFont)
            self.om[resfqdn].grid(row=self.r1, column=1, sticky=S)
            if opt == "init":
                self.lt_newfqdn[resfqdn].set("no change")
                #self.lt_newfqdn[resfqdn].set(curfqdn)
            self.r1 +=1

    def createTargetConfigListFromOptionMENU(self):
        print "\nCreating NEW Target config list...\n"
        self.new_target_config_list = []
        self.target_change_requests = 0
        self.bt_Start_Reconfiguration.config(state=DISABLED)

        for resfqdn,curfqdn,status in self.nsc_status_list:
            newfqdn = self.lt_newfqdn[resfqdn].get()
            if newfqdn == "no change":
                newfqdn = curfqdn
                enable_option = ""
            else:
                enable_option = "enable_reconfiguration"
                self.target_change_requests += 1

            print '%s %s %s' % (resfqdn, newfqdn,enable_option )
            self.new_target_config_list.append((resfqdn,newfqdn,enable_option))

        # Save NEW TARGET CONFIG LIST

        saveListAsFile(self.new_target_config_list,target_config_list_file)

        # ACTIVATE START RECONFIGURATION BUTTON IF CAHNGES ARE REQUESTED

        if self.target_change_requests > 0:
            self.bt_Start_Reconfiguration.config(state=ACTIVE)

        # print "------------------------\n"
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.new_target_config_list)

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
        print "\nStarting reconfiguration of PSPs ....\n"
        self.reconfigure_nscs()
        self.bt_Start_Reconfiguration.config(state=DISABLED)
        self.createOptionMENUS("init")
        #self.output = runShell("dir")
        #print self.output

    # soll durch einzelne functions ersetzt werden
    def loadLists(self):
        print "Loading Lists ..."
        self.nsc_status_list = getFileAsList(nsc_status_list_file)
        self.resource_nsc_list = getFileAsList(resource_nsc_list_file)
        self.resource_nsc_list_dict = dict(self.resource_nsc_list)
        self.remote_nsc_list = getFileAsListOfRow(remote_nsc_list_file, 0)
        self.max_target_fqdn_list = [fqdn for fqdn in self.remote_nsc_list] + ["default","no change"]
        self.target_config_list = getFileAsList(target_config_list_file)
        #print "self.remote_nsc_list : "
        #print self.remote_nsc_list

    # def getResourceNscList(self):
    #     pass
    # def getRemoteNscList(self):
    #     pass
    # def getRemoteStatusList(self):
    #     pass
    # def getResourceNscList(self):
    #     pass




    def writeSlogan(self):
        print "Alles geht !"

    def buildMenu(self, root):
        self.menu = Menu(self)
        root.config(menu=self.menu)

        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=newFile)
        file_menu.add_command(label="Open...", command=self.openAnimatedGifFile)
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

    # fun stuff

    def stopAnimation(self):
        self.anim.after_cancel(self.anim.cancel)
        self.anim.destroy()

    def openAnimatedGifFile(self):
        self.stopAnimation()  # stop previously or initially opened gif
        options = {}
        options['defaultextension'] = '.gif'
        #options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['filetypes'] = [('gif files', '.gif')]
        options['initialdir'] = animdir
        options['parent'] = self
        options['title'] = "Open a gif file"
        with askopenfile(mode='rb', **options) as file:
            self.showAnimatedGif(file,duration,"forever",1,1,1)

    def showAnimatedGif(self,file,duration,mode,method,row,column):
        #if self.anim:
        #    self.stopAnimation()
        self.anim = LabelAnimated(self.con_frame, file, duration, mode, method)
        self.anim.grid(row=row,column=column)
        return self.anim


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
    #root.geometry("800x600")  # mal testen !!
    root.title(main_window_title)
    main = MainApp(root)
    #main.grid(row=0,column=0)
    main.grid()
    root.mainloop()
    root.destroy()

