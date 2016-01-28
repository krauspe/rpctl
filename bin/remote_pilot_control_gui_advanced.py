#!/usr/bin/env python

#DONE: create functions/widgets to get list of selected target domains which are showed in OptionMenu
#TODO: show message (text or picture) on start/end of external scripts
#DONE: recrate status area completely after reread resource nsc list
#DONE: file not found error handling for status_list and target_config list
#DONE: chosse solution for long lists of resource psps as workaround until creation off different "views" see below..
#TODO: create views (resource, remote, status...): possible solutins: tabs, windows, ..
#TODO: improve simulation: admin_get_status_list.sh should create a simulated status with random errors
#TODO:                     admin_reconfigure_nscs.sh should use the above get status script
#TODO: maybe create a function for switching modes(simulate <-> production)


from Tkinter import *
from tkFileDialog import askopenfilename,askopenfile
import tkFont
import ScrolledText
import subprocess as sub
import os
from collections import defaultdict
import pprint
from MyPILTools import LabelAnimated

# Titles
main_window_title = """ 2Step Remote Pilot Control 1.8 (branch) """
#main_window_title = """ 2Step Remote Pilot Control Mega Advanced (unregistered) """
about = """
2Step Remote Pilot Control 1.8 (branch) (c) Peter Krauspe DFS 11/2015
The expert tool for
Remote Piloting
"""
# operation mode

gui_mode = "simulate"
#gui_mode = "productive"
mode_comment = "as configured"

# dynamic settings

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
lhwidth = 17                                          # label header width
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

# label colours and text translations

label_status_text_trans =         {"ready" : "READY", "unreachable" : "UNREACHABLE !", "unknown" : "unknown", None: ""}
label_operation_mode_text_trans = {"available" : "LOCAL", "occupied" : "REMOTE", "unreachable" : "?", "unknown" : "unknown", None: ""}
label_status_textcol =            {"ready" : "dark green", "unreachable" : "red",  "unknown" : "black"}
label_operation_mode_textcol =    {"available" : "black", "occupied" : "blue", "unreachable" : "red", None: "lightgrey",  "unknown" : "black",}

# derived settings

if not os.path.exists(ext_basedir):
    gui_mode = "simulate"
    mode_comment = "because %s doesn't exist !\n" % ext_basedir

mode_comment = str(cfg[gui_mode]["descr"]) + '\n' + mode_comment
bindir  = str(cfg[gui_mode]["bindir"])
confdir = str(cfg[gui_mode]["confdir"])
vardir  = str(cfg[gui_mode]["vardir"])

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
    if os.path.exists(file):
        in_list = [line.rstrip('\n').split() for line in open(file) if not line.startswith('#')]
        if len(in_list) < 0:
            print "WARNING: %s is empty or has no valid lines !!" % file
        return in_list
    else:
        print "WARNING: %s doesn't exist !!" % file
        return []

def getFileAsListOfRow(file, row):
    #return [tuple(line.rstrip('\n').split()) for line in open(file) if not line.startswith('#')]
    if os.path.exists(file):
        in_list = [line.rstrip('\n').split()[row] for line in open(file) if not line.startswith('#')]
        if len(in_list) < 0:
            print "WARNING: %s is empty or has no valid lines !!" % file
        return in_list
    else:
        print "WARNING: %s doesn't exist !!" % file
        return []

# def getTargetConfigList(file):
#     '''https://docs.python.org/2/library/itertools.html
#     itertools.izip_longest(*iterables[, fillvalue])
#     Make an iterator that aggregates elements from each of the iterables.
#     If the iterables are of uneven length, missing values are filled-in with fillvalue.
#     Iteration continues until the longest iterable is exhausted. Equivalent to
#     TODO:
#     Einlesen von tuples ungleicher laenge mit itertools'''
#     pass

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

        # Font settings

        self.lhFont = tkFont.Font(family=lhFont["family"], size=lhFont["size"])         # label header font
        self.lFont = tkFont.Font(family=lFont["family"], size=lhFont["size"])           # label font
        self.optFont = tkFont.Font(family=optFont["family"], size=optFont["size"])      # option menu font
        self.opthFont = tkFont.Font(family=opthFont["family"], size=opthFont["size"])   # option menu header font

        #Frame.__init__(self, master=None,*args, **kwargs)
        Frame.__init__(self, root)


        self.frame = Frame(root)
        self.frame.grid(row=0,column=1)

        self.logo = PhotoImage(file=logo_file)
        Label(self.frame, image=self.logo).grid(row=0,column=1,sticky="E")


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


        # LIST HEADER FRAME

        self.header_frame = Frame(root, bg="grey")
        self.header_frame.grid(row=4, column=0)

        Label(self.header_frame, text="Resource %s " % subtype.upper(), font=self.lhFont, width=lhwidth, bg="deepskyblue2", relief=GROOVE).grid(row=0, column=0)
        Label(self.header_frame, text="Choose Remote FQDN ", font=self.opthFont, width=22, bg="lightyellow", relief=GROOVE).grid(row=0, column=1,sticky=W+E)
        Label(self.header_frame, text="Current FQDN ", font=self.lhFont, width=lhwidth, bg="deepskyblue2", relief=GROOVE).grid(row=0, column=2,sticky=W+E)
        Label(self.header_frame, text="Operation Mode", font=self.lhFont, width=lhwidth, bg="deepskyblue2", relief=GROOVE).grid(row=0, column=3,sticky=W+E)
        Label(self.header_frame, text="Status", font=self.lhFont, width=lhwidth, bg="deepskyblue2", relief=GROOVE).grid(row=0, column=4,sticky=W+E)


        self.buildMenu(root)

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

        self.selected_domains = {}
        self.selected_domains["resource"] = []
        self.selected_domains["target"] = []

        self.listbox = {}

        self.om = {}

        self.new_target_config_list   = []

        # LIST SCROLL AREA FRAME (IN CANVAS) -> moved to createStatusView
        self.loadLists()

        # CHECK BUTTON FRAME :checboxes to choose domains

        self.domain_selector_frame = Frame(root, bg="grey")
        self.domain_selector_frame.grid(row=5, column=1)

        self.domaintSelectBox()
        self.createStatusView()

    #     self.domainCheckBoxSelector(self.domain_selector_frame, "create", "all")

    def domaintSelectBox(self):
        listvar = {}
        listbox_head_label = {}
        select_button = {}


        listvar["resource"] = StringVar()
        listvar["target"] = StringVar()

        listvar["resource"].set(" ".join(self.dns_all["resource"]))
        listbox_head_label["resource"] = Label(self.domain_selector_frame, text="Select Resource Domains",font=self.lhFont,bg="lightyellow", relief=GROOVE )
        listbox_head_label["resource"].pack()
        self.listbox["resource"] = Listbox(self.domain_selector_frame,listvariable=listvar["resource"], selectmode=MULTIPLE, font=self.lFont)
        self.listbox["resource"].pack(side="top")
        select_button["resource"] = Button(self.domain_selector_frame, text="apply", command=self.applySelectedResourceDomains)
        select_button["resource"].pack()

        listvar["target"].set(" ".join(self.dns_all["target"]))
        listbox_head_label["target"] = Label(self.domain_selector_frame, text="Select Target Domains",font=self.lhFont,bg="lightyellow", relief=GROOVE )
        listbox_head_label["target"].pack()
        self.listbox["target"] = Listbox(self.domain_selector_frame,listvariable=listvar["target"], selectmode=MULTIPLE, font=self.lFont)
        self.listbox["target"].pack(side="top")
        select_button["target"] = Button(self.domain_selector_frame, text="apply", command=self.applySelectedTargetDommains)
        select_button["target"].pack()

    def applySelectedResourceDomains(self):
        dn_list = []
        selection = self.listbox["resource"].curselection()
        for i in selection:
            dn = self.listbox["resource"].get(i)
            dn_list.append(dn)
        self.selected_domains["resource"] =  dn_list
        self.createStatusView()

    def applySelectedTargetDommains(self):
        dn_list = []
        selection = self.listbox["target"].curselection()
        for i in selection:
            dn = self.listbox["target"].get(i)
            dn_list.append(dn)
        self.selected_domains["target"] =  dn_list
        self.createStatusView()


    def createStatusView(self):

        # LIST SCROLL AREA FRAME (IN CANVAS)

        # delete possibly previuosly created objects
        if hasattr(self,'vsb'): self.vsb.destroy()
        if hasattr(self,'list_frame'): self.list_frame.destroy()
        if hasattr(self,'canvas'): self.canvas.destroy()
        if hasattr(self,'canvas_frame'): self.canvas_frame.destroy()

        self.canvas_frame = Frame(root, bg="grey")
        self.canvas_frame.grid(row=5, column=0)
        self.canvas = Canvas(self.canvas_frame, borderwidth=0, background="#ffffff")
        self.vsb = Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.vsb.pack(side="right", fill="y")
        self.list_frame = Frame(self.canvas, bg="grey")
        self.list_frame.grid(row=0, column=0)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.create_window((0,0),window=self.list_frame, anchor="nw",tags="self.list_frame")
        self.canvas.pack(side="left",fill="both", expand=True)

        #self.loadLists()
        self.r1 = 0

        resfqdns_selected = self.getSelectedFqdnOptionList("resource")

        for resfqdn in resfqdns_selected:
            curfqdn = self.current_fqdn[resfqdn]
            opmode  = self.nsc_status[resfqdn]
            status = self.resource_status[resfqdn]

            # define tkinter vars
            self.lt_resfqdns[resfqdn] = StringVar()
            self.lt_curfqdns[resfqdn] = StringVar()
            self.lt_Status[resfqdn]   = StringVar()
            self.lt_operation_mode[resfqdn]   = StringVar()
            self.lt_newfqdn[resfqdn]  = StringVar()

            # set initial values

            self.lt_resfqdns[resfqdn].set(resfqdn)
            self.lt_curfqdns[resfqdn].set(curfqdn)
            self.lt_Status[resfqdn].set(label_status_text_trans[status])
            self.lt_operation_mode[resfqdn].set(label_operation_mode_text_trans[opmode])

            # mark labels depemding on domain of resfqdn

            self.dn = ".".join( (resfqdn.split("."))[1:])
            if lbgcol.has_key(self.dn):
                resfqdn_lbgcol = lbgcol[self.dn]
            else:
                resfqdn_lbgcol = "white"

            # delete old labels
            if self.label_resfqdn.has_key(resfqdn): self.label_resfqdn[resfqdn].destroy()
            if self.label_curfqdn.has_key(resfqdn): self.label_curfqdn[resfqdn].destroy()
            if self.label_operation_mode.has_key(resfqdn): self.label_operation_mode[resfqdn].destroy()
            if self.label_status.has_key(resfqdn): self.label_status[resfqdn].destroy()
            # create lables
            self.label_resfqdn[resfqdn] = Label(self.list_frame, textvariable=self.lt_resfqdns[resfqdn], font=self.lFont, width=lwidth,  relief=GROOVE, bg=resfqdn_lbgcol)
            self.label_resfqdn[resfqdn].grid(row=self.r1, column=0, sticky=N+S)

            self.label_curfqdn[resfqdn] = Label(self.list_frame, textvariable=self.lt_curfqdns[resfqdn], font=self.lFont, width=lwidth, relief=SUNKEN)
            self.label_curfqdn[resfqdn].grid(row=self.r1, column=2, sticky=N+S)

            self.label_operation_mode[resfqdn] = Label(self.list_frame, textvariable=self.lt_operation_mode[resfqdn], font=self.lFont, width=lwidth, fg=label_operation_mode_textcol[opmode], relief=SUNKEN)
            self.label_operation_mode[resfqdn].grid(row=self.r1, column=3, sticky=N+S)

            self.label_status[resfqdn] = Label(self.list_frame, textvariable=self.lt_Status[resfqdn], font=self.lFont, width=lwidth, fg=label_status_textcol[status], relief=SUNKEN)
            self.label_status[resfqdn].grid(row=self.r1, column=4, sticky=N+S)

            self.label_curfqdn[resfqdn].config(fg=label_operation_mode_textcol[opmode])
            self.label_status[resfqdn].config(fg=label_status_textcol[status])
            self.label_operation_mode[resfqdn].config(fg=label_operation_mode_textcol[opmode])

            self.r1 +=1

        self.frame.bind("<Configure>", self.onFrameConfigure)
        #self.createOptionMENUS(self.resource_fqdns_all)
        self.createOptionMENUS()


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
        self.createOptionMENUS()

    def updateStatus(self):
        print "updateStatus: "
        #print "CURRENTLY DISABLED run external script to update status at that state (force by pressing the button !!)"
        self.update_status_list()
        self.loadLists()
        self.createStatusView()

    def updateStatusView(self):
        self.createStatusView()

    def createOptionMENUS(self):
        self.r1 = 0
        # delete old option menus
        for resfqdn in self.om.keys(): self.om[resfqdn].destroy()

        resfqdns_selected = self.getSelectedFqdnOptionList("resource")
        for resfqdn in resfqdns_selected:

            if self.resource_status[resfqdn] == "ready":
                #print "status[%s]=%s  create" % (resfqdn, self.resource_status[resfqdn])
                self.target_fqdn_option_list = self.getSelectedFqdnOptionList("target")
                self.om[resfqdn] = OptionMenu(self.list_frame, self.lt_newfqdn[resfqdn], *self.target_fqdn_option_list)
                self.om[resfqdn].config(width=20, font=self.optFont)
                self.om[resfqdn].grid(row=self.r1, column=1, sticky=S)
            else:
                self.lt_newfqdn[resfqdn].set("no change")
                self.om[resfqdn] = OptionMenu(self.list_frame, self.lt_newfqdn[resfqdn],"no change")
                self.om[resfqdn].config(width=20, font=self.optFont, bg="grey", fg="grey")
                self.om[resfqdn].grid(row=self.r1, column=1, sticky=S)


            #if opt == "init":
            self.lt_newfqdn[resfqdn].set("no change")
            self.r1 +=1

    def createTargetConfigListFromOptionMENU(self):
        print "\nCreating NEW Target config list...\n"
        self.new_target_config_list = []
        self.target_change_requests = 0
        self.bt_Start_Reconfiguration.config(state=DISABLED)

        print 'resfqdn\tnewfqdn\tenable_option\n-----------------------------------'

        for resfqdn in self.resource_fqdns_all:
            if  self.lt_newfqdn.has_key(resfqdn):
                newfqdn = self.lt_newfqdn[resfqdn].get()
                if newfqdn == "no change" or self.resource_status[resfqdn] != "ready":
                    newfqdn = self.current_fqdn[resfqdn]
                    enable_option = ""
                else:
                    enable_option = "enable_reconfiguration"
                    self.target_change_requests += 1
            else:
                if self.current_fqdn.has_key(resfqdn):
                    newfqdn = self.current_fqdn[resfqdn]
                else:
                    newfqdn = "unknown"


            print '%s\t%s\t%s' % (resfqdn, newfqdn,enable_option )
            self.new_target_config_list.append((resfqdn,newfqdn,enable_option))

        # Save NEW TARGET CONFIG LIST
        saveListAsFile(self.new_target_config_list,target_config_list_file)
        # ACTIVATE START RECONFIGURATION BUTTON IF CAHNGES ARE REQUESTED
        if self.target_change_requests > 0:
            self.bt_Start_Reconfiguration.config(state=ACTIVE)

        # print "------------------------\n"
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.new_target_config_list)

    # LOAD AND GENERATE LIST FUNCTIONS

    def loadLists(self):
        print "Loading Lists ..."
        self.nsc_status_list = getFileAsList(nsc_status_list_file)
        self.resource_nsc_list = getFileAsList(resource_nsc_list_file)
        self.resource_nsc_list_dict = dict(self.resource_nsc_list)
        self.remote_fqdns_all = getFileAsListOfRow(remote_nsc_list_file, 0)
        self.target_config_list = getFileAsList(target_config_list_file)

        self.nsc_status = defaultdict(lambda:'unknown')       # status as reead from script generated nsc_status_list
        self.current_fqdn = defaultdict(lambda:'unknown')     # current fqdns as reead from script generated nsc_status_list

        self.resource_status = {}  # dict for interpreted nsc_status for use in all GUI functions !!
        self.resource_mac = {}
        self.resource_fqdns_from_dn = {} # all resource fqdns from given domain
        self.remote_fqdns_from_dn = {}   # all remote fqdns from given domain
        self.resource_fqdns_from_nsc_status_list = [] # all resource fqdns contained in nsc_status_list
        self.resource_fqdns_all = []                  # all available resource fqdns read from script generated list

        # read originall nsc_status from shell script and translate to resource_status

        for resfqdn,curfqdn,status in self.nsc_status_list:
            self.nsc_status[resfqdn] = status
            self.current_fqdn[resfqdn] = curfqdn
            if self.nsc_status[resfqdn] == "available" or self.nsc_status[resfqdn] == "occupied":
                self.resource_status[resfqdn] = "ready"
            else:
                self.resource_status[resfqdn] = self.nsc_status[resfqdn]
            self.resource_fqdns_from_nsc_status_list.append(resfqdn)

        # read resource fqdn list with macs

        for resfqdn,mac in self.resource_nsc_list:  # list of lists from file (ALL resource NSC"s !)
            self.resource_mac = mac                 # store MAC addresses for later use .....
            if not self.nsc_status.has_key(resfqdn):
                self.resource_status[resfqdn] = 'unknown'
            if not self.current_fqdn.has_key(resfqdn):
                self.current_fqdn[resfqdn] = 'unknown'
            self.resource_fqdns_all.append(resfqdn)

        #print "loadlists: should be UPTODATE:", self.resource_fqdns_all

        self.fqdns_from_dn= {}
        self.dns_all = {}

        self.fqdns_from_dn["target"] = defaultdict(list)
        self.fqdns_from_dn["target"] = self.getListOfFqdnsPerDomain(self.remote_fqdns_all)
        self.dns_all["target"] = [dn for dn in self.fqdns_from_dn["target"].keys()]

        self.fqdns_from_dn["resource"] = defaultdict(list)
        self.fqdns_from_dn["resource"] = self.getListOfFqdnsPerDomain(self.resource_fqdns_all)
        self.dns_all["resource"] = [dn for dn in self.fqdns_from_dn["resource"].keys()]

    def getSelectedFqdnOptionList(self, type):
        fqdn_list = []
        selected_dns = self.selected_domains[type]
        if len(selected_dns) > 0:
            dn_list = selected_dns
        else:
            dn_list = self.dns_all[type]

        for dn in dn_list:
            fqdn_list += self.fqdns_from_dn[type][dn]
        if type == "target":
            fqdn_list += ["default", "no change"]

        return fqdn_list


    def getListOfFqdnsPerDomain(self,fqdn_list):
        fqdns_from_dn = defaultdict(list)
        for fqdn in fqdn_list:
            dn = '.'.join(fqdn.rsplit(".")[1:])
            fqdns_from_dn[dn].append(fqdn)
        return fqdns_from_dn

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
        for line in self.remote_fqdns_all:
            print line

    def printNscStatusList(self):
        print "\nStatus list:\n"
        for line in self.nsc_status_list:
            print line

    def startReconfiguration(self):
        print "\nStarting reconfiguration of PSPs ....\n"
        self.reconfigure_nscs()
        self.bt_Start_Reconfiguration.config(state=DISABLED)
        self.createOptionMENUS()
        #self.output = runShell("dir")
        #print self.output

    def writeSlogan(self):
        print "Alles geht !"

    def buildMenu(self, root):
        self.menu = Menu(self)
        root.config(menu=self.menu)

        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=newFile)
        file_menu.add_command(label="Open...", command=self.askOpenAnimatedGifFileM1)
        file_menu.add_command(label="Open...(method 2)", command=self.askOpenAnimatedGifFileM2)
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

    # animation functions

    def stopAnimation(self):
        self.anim.after_cancel(self.anim.cancel)
        self.anim.destroy()

    def askOpenAnimatedGifFileM1(self):
        self.openAnimatedGifFile(1, 1, 1)

    def askOpenAnimatedGifFileM2(self):
        self.openAnimatedGifFile(1, 1, 2)

    def openAnimatedGifFile(self,duration, mode, method):
        self.stopAnimation()  # stop previously or initially opened gif
        options = {}
        options['defaultextension'] = '.gif'
        #options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['filetypes'] = [('gif files', '.gif')]
        options['initialdir'] = animdir
        options['parent'] = self
        options['title'] = "Open a gif file"
        with askopenfile(mode='rb', **options) as file:
            self.showAnimatedGif(file,duration,"forever",duration, mode, method)

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

