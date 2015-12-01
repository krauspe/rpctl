#!/usr/bin/env python


from Tkinter import *
from tkFileDialog import askopenfilename
import ScrolledText
import subprocess as sub
import os
import pprint
from MyPILTools import LabelAnimated

# settings

main_window_title = """ 2Step Remote Pilot Control Mega Advanced (unregistered) """
about = """
2Step Remote Pilot Control 1.0 (c) Peter Krauspe DFS 11/2015
The expert tool for
Remote Piloting
"""


#basedir = ".."
#ext_basedir = basedir

basedir = "/opt/dfs/rpctl"
ext_basedir = "/opt/dfs/tsctl2"
#ext_basedir = os.path.join(basedir, "..", "tsctl2")

bindir  = os.path.join(ext_basedir,"bin")
confdir = os.path.join(ext_basedir,"config")
vardir  = os.path.join(ext_basedir, "var")

imagedir = os.path.join(basedir, "images")
animdir = os.path.join(imagedir, "animated_gifs")


resource_nsc_list_file  = os.path.join(vardir,"resource_nsc.list")
target_config_list_file = os.path.join(vardir,"target_config.list")
remote_nsc_list_file    = os.path.join(vardir,"remote_nsc.list")
nsc_status_list_file    = os.path.join(vardir,"nsc_status.list")

# decoration

animated_gif_filename = 'Lear-jet-flying-in-turbulent-sky.gif'
animated_gif_filename = 'Animated-fighter-jet-firing-missles.gif'
animated_gif_filename = 'Moving-picture-red-skull-chewing-animation.gif'
animated_gif_filename = 'Moving-picture-skeleton-sneaking-around-animated-gif.gif'
animated_gif_filename = '15a.gif'
animated_gif_filename = 'Animated-Lear-jet-loosing-control-spinning-around-with-smoke.gif'
animated_gif_filename = 'rotating-jet-smoke.gif'
animated_gif_filename = 'airplane13.gif'


animated_gif_file = os.path.join(animdir, animated_gif_filename)
duration = 1

#run_shell_opt = "fake"
run_shell_opt = ""

# external commands

def deploy_configs(): runShell(os.path.join(bindir,"admin_deploy_configs.sh"), run_shell_opt)
#def update_status_list(): runShell(os.path.join(bindir,"admin_get_status_list.sh"), run_shell_opt)
def update_status_list(): runShell(os.path.join(bindir,"admin_get_status_list.sh"), run_shell_opt)
def update_resource_nsc_list(): runShell(os.path.join(bindir,"admin_get_resource_nsc_list.sh"), run_shell_opt)
def reconfigure_nscs(): runShell(os.path.join(bindir,"admin_reconfigure_nscs.sh"), run_shell_opt)



# todo: einlesen und auswerten
#source ${confdir}/remote_nsc.cfg # providing:  subtype, ResourceDomainServers, RemoteDomainServers
# app settings
subtype = "psp"


def newFile():
    name = askopenfilename()
    name = askopenfilename
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
    f.write("HALLO\n")
    for tup in list:
        line = ''
        for element in tup:
            line += ' ' + element
        f.write(line + '\n')
    f.close()
    print "type(line) = %s\n" % type(line)

def Quit():
        print "Quit"
        root.quit()

def runShell(cmd,opt):
    # http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
    #cmd = "cat /etc/HOSTNAME"
    cmd = "/opt/dfs/tsctl2/bin/admin_get_status_list.sh"
    if opt == "fake":
        print "  running shell command:(FAKE !)"
        print "\n  %s\n" % cmd
    else:
        print "  running shell command:"
        print "\n  %s\n" % cmd

        # p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE)
        # output, errors = p.communicate()
        # return output, errors

        p = sub.Popen(cmd, shell=True, stderr=sub.PIPE)
        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                print out
                # return out
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
        self.label_txt_trans = {"available": "LOCAL", "occupied": "REMOTE", None:""}
        self.label_textcol = { "available" : "blue", "occupied" : "red", None:"lightgrey"}


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

        #self.anim = None
        self.anim = self.showAnimatedGif(animated_gif_file,duration,1,1)


        # redirect stdout
        redir = redirectText(self.console)
        sys.stdout = redir
        self.console.insert(END, self.output)

        # BUTTONS
        n=0
        self.con_and_button_frame = Frame(root, bg="lightgrey")
        self.con_and_button_frame.grid(row=1, column=3, sticky=W+E+N+S)


        Button(self.con_and_button_frame, text="Deploy configs", command=deploy_configs).grid(row=1, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Update resource PSP list", command=update_resource_nsc_list).grid(row=2, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Update Remote Pilot Status", command=self.updateStatus).grid(row=3, column=1, sticky=W+E)
        Label(self.con_and_button_frame,  text="").grid(row=4, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Print remote NSC list", command=self.printRemoteNscList).grid(row=5, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Print status list", command=self.printNscStatusList).grid(row=6, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Print resource NSC list", command=self.printResourceNscList).grid(row=7, column=1, sticky=W+E)
        Label(self.con_and_button_frame,  text="").grid(row=8, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Confirm Remote PSP Choices", command=self.confirmRemotePSPChoices).grid(row=9, column=1, sticky=W+E)
        #Label(self.con_and_button_frame,  text="").grid(row=10, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Stop animation", command=self.stopAnimation).grid(row=10, column=1, sticky=W+E)
        Button(self.con_and_button_frame, text="Start reconfiguration", bg="red", command=self.startReconfiguration).grid(row=11, column=1, sticky=W+E)
        Label(self.con_and_button_frame,  text="").grid(row=12, column=1, sticky=W+E)
        Button(self.con_and_button_frame,text="QUIT", fg="red",command=self.frame.quit).grid(row=13,column=1, sticky=W+E)


        # LIST HEADER
        self.list_frame = Frame(root, bg="grey")
        self.list_frame.grid(row=4, column=0)
        Label(self.list_frame, text="Resource %s " % subtype.upper(), width=25, relief=GROOVE, highlightthickness=2).grid(row=2, column=0)
        Label(self.list_frame, text="Current FQDN ", width=25, relief=GROOVE).grid(row=2, column=1)
        Label(self.list_frame, text="Status", width=25, relief=GROOVE).grid(row=2, column=2)
        Label(self.list_frame, text="Choose Remote FQDN ", width=25, relief=GROOVE).grid(row=2, column=3)

        self.buildMenu(root)
        self.loadLists()
        #self.updateStatus()

        # LIST | OptionMenu

        self.lt_resfqdns = {}
        self.lt_curfqdns = {}
        self.lt_Status   = {}
        self.lt_newfqdn   = {}
        self.label_resfqdn = {}
        self.label_curfqdn = {}
        self.label_status = {}
        self.om = {}

        self.new_target_config_list   = []


        self.r1 = 3
        #self.testoptions = ("aaa","bbb","ccc","ddd")
        for resfqdn,curfqdn,status in self.nsc_status_list:

            # wenn sich die Anzahl der resfqdns erhoeht fehlen hierfuer labels, daher Neustart noetig !
            # Loesung: weitere Lables fuer neue Eintrage erzeugen (nicht in init)

            # define tkinter vars
            self.lt_resfqdns[resfqdn] = StringVar()
            self.lt_curfqdns[resfqdn] = StringVar()
            self.lt_Status[resfqdn]   = StringVar()
            self.lt_newfqdn[resfqdn]  = StringVar()

            # set initial values
            self.lt_resfqdns[resfqdn].set(resfqdn)
            self.lt_curfqdns[resfqdn].set(curfqdn)
            self.lt_Status[resfqdn].set(self.label_txt_trans[status]) # translate: available -> LOCAL , occupied -> REMOTE

            self.label_resfqdn[resfqdn] = Label(self.list_frame, textvariable=self.lt_resfqdns[resfqdn], width=25, bd=2, relief=GROOVE)
            self.label_resfqdn[resfqdn].grid(row=self.r1, column=0)

            self.label_curfqdn[resfqdn] = Label(self.list_frame, textvariable=self.lt_curfqdns[resfqdn], width=25, relief=SUNKEN)
            self.label_curfqdn[resfqdn].grid(row=self.r1, column=1)

            self.label_status[resfqdn] = Label(self.list_frame, textvariable=self.lt_Status[resfqdn], width=25, fg=self.label_textcol[status], relief=SUNKEN)
            self.label_status[resfqdn].grid(row=self.r1, column=2)

            self.r1 +=1

        self.createOptionMENUS("init")


    def confirmRemotePSPChoices(self):
        self.createTargetConfigListFromOptionMENU()
        self.createOptionMENUS("update")


    def updateStatus(self):
        print "\nprint assignment...\n"
        update_status_list()
        #self.stopAnimation()
        self.nsc_status_list = getFileAsList(nsc_status_list_file)
        for resfqdn,curfqdn,status in self.nsc_status_list:
            self.lt_resfqdns[resfqdn].set(resfqdn) # eigentlich ueberfluessig
            self.lt_curfqdns[resfqdn].set(curfqdn)
            self.lt_Status[resfqdn].set(self.label_txt_trans[status])
            self.label_status[resfqdn].config(fg=self.label_textcol[status])

    def createOptionMENUS(self,opt):
        self.r1 = 3
        for resfqdn,curfqdn,status in self.nsc_status_list:
            if opt == "update":
                self.om[resfqdn].destroy()
            self.om[resfqdn] = OptionMenu(self.list_frame, self.lt_newfqdn[resfqdn], *self.max_target_fqdn_list)
            self.om[resfqdn].grid(row=self.r1, column=3)
            if opt == "init":
                self.lt_newfqdn[resfqdn].set(curfqdn)
            self.r1 +=1

    def createTargetConfigListFromOptionMENU(self):
        print "\nCreating NEW Target config list...\n"
        self.new_target_config_list = []
        for resfqdn,curfqdn,status in self.nsc_status_list:
            newfqdn = self.lt_newfqdn[resfqdn].get()
            if newfqdn != curfqdn:
                force_option = "force_reconfigure"
            else:
                force_option = ""
            print '%s %s %s' % (resfqdn, newfqdn,force_option )
            self.new_target_config_list.append((resfqdn,self.lt_newfqdn[resfqdn].get(),force_option))
        saveListAsFile(self.new_target_config_list,target_config_list_file)
        #saveListAsFile(self.new_target_config_list,target_config_list_file+".new")

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
        reconfigure_nscs()
        #self.output = runShell("dir")
        #print self.output


    def loadLists(self):
        print "Loading Lists ..."
        self.nsc_status_list = getFileAsList(nsc_status_list_file)
        self.resource_nsc_list = getFileAsList(resource_nsc_list_file)
        self.resource_nsc_list_dict = dict(self.resource_nsc_list)
        self.remote_nsc_list = getFileAsListOfRow(remote_nsc_list_file, 0)
        self.max_target_fqdn_list = [fqdn for fqdn in self.remote_nsc_list] + ["default"]
        self.target_config_list = getFileAsList(target_config_list_file)
        #print "self.remote_nsc_list : "
        #print self.remote_nsc_list


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

    def stopAnimation(self):
        self.anim.after_cancel(self.anim.cancel)
        self.anim.destroy()

    def openAnimatedGifFile(self):
        file = askopenfilename()
        self.showAnimatedGif(file,duration,1,1)

    def showAnimatedGif(self,file,duration,row,column):
        #if self.anim:
        #    self.stopAnimation()
        self.anim = LabelAnimated(self.con_frame, file, duration)
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
    root.title(main_window_title)
    main = MainApp(root)
    #main.grid(row=0,column=0)
    main.grid()
    root.mainloop()
    root.destroy()

